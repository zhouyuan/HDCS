#ifndef CONTENTSEGMENT
#define CONTENTSEGMENT
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <cassert>
#include <inttypes.h>

#define SHM_SIZE 2147483648
//#define SHM_SIZE 20971520
#define SHM_TRUNK_LENGTH 512
#define SHM_TRUNK_SIZE 2097152

namespace rbc{
class ContentSegment{
public:
    struct trunk{
        uint64_t index;
        uint16_t end;
        uint16_t count;
        trunk* prev;
        trunk* next;
        trunk(){
            end = 0;
            count = 0;
            next = NULL;
            prev = NULL;
        }
        void set_index( uint64_t i ){
            index = i;
        }
        void clean_trunk(){
            end = 0;
            count = 0;
        }
        void pop(){
            if(prev) prev->next = next;
            if(next) next->prev = prev;
            prev = NULL;
            next = NULL;
        }
        bool insert( trunk* next_trunk ){
            trunk* prev_trunk = next_trunk?next_trunk->prev:NULL;
            this->prev = prev_trunk;
            this->next = next_trunk;
            if(prev_trunk) prev_trunk->next = this;
            if(next_trunk) next_trunk->prev = this;
            return true;
        }
        bool check_if_free_after_pop(){
            if( count == 1 ){
                return true;
            }
            return false;
        }
    };

    struct trunk_link{
        trunk* head;
        trunk_link(){
            head = NULL;
        }
        trunk* pop(){
            if(head == NULL)
                return NULL;
            trunk* tmp = head;
            head = head->next;
            tmp->pop();
            return tmp;
        }
        void push( trunk* new_item ){
            if( new_item->insert( head ) )
                head = new_item;
        }
    };


    ContentSegment( uint32_t port, bool init = false ):key(port),init(init){
        /* create a shared memory segment */
        key = key%999 + 5000; 
        if ((shmid = shmget(key, SHM_SIZE, IPC_CREAT | 0666)) < 0) {
            printf("unable to do shmget by create, key: %u \n", key);
            failover_handler(SH_GET,NULL);
        }
    
        uint64_t trunk_count = SHM_SIZE/(SHM_TRUNK_SIZE);
        trunk_list_mutex.lock();
        trunk_list = new trunk[trunk_count]();
        for(uint64_t i = 0; i<trunk_count; i++){
            trunk_list[i].set_index(i);
        }
      
        free_link =  new trunk_link();
        recent_used_link =  new trunk_link();
        for(int64_t i = trunk_count-1; i>=0; i--){
            free_link->push(&trunk_list[i]);
        }
        trunk_list_mutex.unlock();
        if ((shared_memory_ptr = (char*)shmat(shmid, NULL, 0)) == (char *) -1) {
            perror("unable to do shmat");
	    failover_handler(SH_AT,NULL);
            assert(0);
        }
    }

    ~ContentSegment(){
        /* Detach the shared memory segment.  */
        if(0!=shmdt(shared_memory_ptr)){
	     failover_handler(SHM_DT,NULL);
	}
        if( init ){
            /* Deallocate the shared memory segment.  */
            if(0!=shmctl(shmid, IPC_RMID, 0)){
		failover_handler(SHM_CTL,NULL);
	    }
        }
    }
    
    char* get_free_trunk( uint64_t size ){
        uint64_t offset = get_free_trunk_offset( size );
        char* trunk_ptr;
        if( offset != -1 ){
            trunk_ptr = &shared_memory_ptr[offset];
        }else{
            trunk_ptr = NULL;
        }
        return trunk_ptr;
    }

    uint64_t get_free_trunk_offset( uint64_t size ){
        std::lock_guard<std::mutex> lock(trunk_list_mutex);        
        uint64_t offset = 0;
        trunk* ptr = free_link->pop();
        if( !ptr ){
            perror("No free shared memory\n");
            return -1;
        /* no free 2M trunk, need to use space inside trunk*/
            for(trunk* s = recent_used_link->head; s != NULL; s = s->next){
                if( size <= (SHM_TRUNK_LENGTH - s->end)*4096 ){
                     offset = s->end;
                     s->count++;
                     s->end += size/4096;
                     std::cout << "free index:" << s->index << ", offset:" << offset << std::endl;
                     return (offset*4096 + s->index*(SHM_TRUNK_SIZE));
                }
            }
            perror("No free shared memory\n");
            return -1;
        }
        recent_used_link->push( ptr );
        //ptr->end += size/4096;
        //ptr->count++;
        //std::cout << "free index:" << ptr->index << ", offset:0" << std::endl;
        return (ptr->index*(SHM_TRUNK_SIZE));
    }

    void release_trunk( uint64_t offset, uint64_t size ){
        std::lock_guard<std::mutex> lock(trunk_list_mutex);        
        uint64_t index = offset/(SHM_TRUNK_SIZE);
        //std::cout << "release index:" << index << std::endl;
        trunk* tmp = &trunk_list[index];
        if( recent_used_link->head == tmp ) recent_used_link->head = recent_used_link->head->next;
            tmp->pop();
            tmp->clean_trunk();
            free_link->push( tmp );
        return;
        if( tmp->check_if_free_after_pop() ){
            tmp->pop();
            tmp->clean_trunk();
            free_link->push( tmp );
        }else{
            tmp->count--;
        }
    }
    
    char* get_shm_ptr(){
        return shared_memory_ptr;
    }
private:
    trunk* trunk_list;
    trunk_link* free_link;
    trunk_link* recent_used_link;
    std::mutex trunk_list_mutex;
    int shmid;
    key_t key;
    char *shared_memory_ptr;
    bool init;
};
}
#endif
