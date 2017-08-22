//g++ -o test_librbc  test_librbc.cpp ../utils/librbc.cpp  ../CacheService/CacheService.cpp ../DataStore/BlockCacher/SimpleBlockCacher.cpp ../common/BufferList.cpp ../BackendStore/BackendStore.cpp ../CacheService/AgentService.cpp ../MetaStore/MetaStore.cpp ../Messenger/Messenger.cpp ../CacheService/CacheEntry.cpp -std=c++11 -lrados -lrbd -lboost_thread -lboost_system -lpthread -lmemcached -lrocksdb
#include <rbc/librbc.h>
#include "stdlib.h"
#include "stdio.h"

struct cb_param{
   uint8_t inflight_ops;
   uint64_t io_complete_count;
};

cb_param arg;
static void _finish_aiocb(int r, void *data){
    if( r< 0 ){
	printf("io operation fail\n");
    }
    cb_param* tmp = (cb_param*) data;
    tmp->inflight_ops--;
    tmp->io_complete_count++;
    //printf("%lu completed\n", offset);
    //inflight_ops--;
    return;
}

static void _finish_aio_read(int r, void *data){
    std::cout << "rbc_read: " << (char*)data  << ", size:" << r << std::endl;
}

int main(int argc, char *argv[]){
    rbc::librbc rbc("volume_3");
    char* op_type = argv[1];
    if(op_type[0] == 'w'){
        char* image_name = argv[2];
        uint64_t off = strtoul(argv[3], NULL, 0);
        char* data = argv[4];
        uint64_t length = strlen(data);
        rbc::rbc_completion_t comp;
        rbc.rbc_aio_create_completion( (void*)&off, _finish_aiocb, &comp );
        rbc.rbc_aio_write(image_name, off, length, data, comp);

    }else if(op_type[0] == 'r'){
        char* image_name = argv[2];
        uint64_t off = strtoul(argv[3], NULL, 0);
        uint64_t length = strtoul(argv[4], NULL, 0);
        char* data = new char[length+1]();
        rbc::rbc_completion_t comp;
        rbc.rbc_aio_create_completion( (void*)data, _finish_aio_read, &comp );
        rbc.rbc_aio_read(image_name, off, length, data, comp);

    }else{
        printf("Unrecognised type: ./test_librbc read/write volume_name offset data/length\n");
    }
    sleep(10);
    return 0;
}
