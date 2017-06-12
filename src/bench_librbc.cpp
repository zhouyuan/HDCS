//g++ -o test_librbc  test_librbc.cpp ../utils/librbc.cpp  ../CacheService/CacheService.cpp ../DataStore/BlockCacher/SimpleBlockCacher.cpp ../common/BufferList.cpp ../BackendStore/BackendStore.cpp ../CacheService/AgentService.cpp ../MetaStore/MetaStore.cpp ../Messenger/Messenger.cpp ../CacheService/CacheEntry.cpp -std=c++11 -lrados -lrbd -lboost_thread -lboost_system -lpthread -lmemcached -lrocksdb
#include "rbc/librbc.h"
#include "stdlib.h"
#include "stdio.h"
#include <time.h>
#include <thread>

time_t start;
bool go = true;
struct cb_param{
   uint8_t inflight_ops;
   uint64_t io_complete_count;
   cb_param(){
       inflight_ops = 0;
       io_complete_count = 0;
   }
};

cb_param arg;

struct io_u{
    cb_param *history;
    char* data;
    io_u( cb_param* history, char* data ):history(history), data(data){}
    ~io_u(){
        free(data);
    }
};

static void _finish_aiocb(int r, void *data){
    io_u* _io_u = (io_u*)data;
    cb_param* tmp = _io_u->history;
    tmp->inflight_ops--;
    tmp->io_complete_count++;
    //printf("%lu completed\n", offset);
    //inflight_ops--;
    delete _io_u;
    return;
}

void monitor(){
    time_t now;
    while(1){
        sleep(1);
        time(&now);
        uint64_t elapsed = difftime(now, start);

        printf("%d secs: iops %d, inflight_ops:%u, total completed:%lu\n", elapsed, arg.io_complete_count/elapsed, arg.inflight_ops, arg.io_complete_count);
        if(elapsed > 30)
            go = false;
    }

}

int rbc_aio_write( rbc::librbc* rbc, const char* image_name, uint64_t off, uint64_t length){
    char* data = (char*)malloc(sizeof(char)*4096);
    memset(data, 'a', 4096);
    io_u* _io_u = new io_u( &arg, data );
    rbc::rbc_completion_t comp;
    rbc::rbc_aio_create_completion( (void*)_io_u, _finish_aiocb, &comp );
    rbc->rbc_aio_write(image_name, off, length, data, comp);
    arg.inflight_ops++;
    return 0;
}

int rbc_aio_read( rbc::librbc* rbc, const char* image_name, uint64_t off, uint64_t length ){
    char* data = (char*)malloc(sizeof(char)*4096);
    memset(data, 'a', 4096);
    io_u* _io_u = new io_u( &arg, data );
    rbc::rbc_completion_t comp;
    rbc::rbc_aio_create_completion( (void*)_io_u, _finish_aiocb, &comp );
    rbc->rbc_aio_read(image_name, off, length, data, comp);
    arg.inflight_ops++;

    return 0;
}


int main(int argc, char *argv[]){
    arg.inflight_ops = 0;
    arg.io_complete_count = 0;

    const char* op_type = argv[1];
    const char* image_name = argv[2];

    rbc::librbc *rbc = new rbc::librbc(image_name);
    rbc::ThreadPool *threadpool = new rbc::ThreadPool(2);

    time(&start);
    threadpool->schedule( &monitor );
    bool is_write = true;

    if(op_type[0] == 'r'){
        is_write = false;
    }

    srand(time(NULL));

    while(go){
        uint64_t off = rand()%10737418240/4096*4096;
        uint64_t length = 4096;
        if( arg.inflight_ops < 128 )
            if( is_write )
                threadpool->schedule(boost::bind( rbc_aio_write, rbc, image_name, off, length) );
            if( !is_write )
                threadpool->schedule(boost::bind( rbc_aio_read, rbc, image_name, off, length ) );
        else{

            //printf("inflight_ops:%lu, do no op\n",inflight_ops);
            std::this_thread::yield();
        }
    }

    delete rbc;
    return 0;
}
