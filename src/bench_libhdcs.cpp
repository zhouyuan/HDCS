#include "include/libhdcs.h"
#include "stdlib.h"
#include "stdio.h"
#include <time.h>
#include <thread>
#include "common/ThreadPool.h"

time_t start;
bool go = true;
struct cb_param{
   uint64_t inflight_ops;
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

static void _finish_aiocb(int r, void *ret){
    io_u* _io_u = (io_u*)ret;
    cb_param* tmp = _io_u->history;
    tmp->inflight_ops--;
    tmp->io_complete_count++;
    delete _io_u;
    return;
}

void monitor(){
    time_t now;
    while(1){
        sleep(1);
        time(&now);
        uint64_t elapsed = difftime(now, start);

        printf("%lu secs: iops %lu, inflight_ops:%lu, total completed:%lu\n", elapsed, arg.io_complete_count/elapsed, arg.inflight_ops, arg.io_complete_count);
        if(elapsed > 30)
            go = false;
    }

}

int aio_write( hdcs::libhdcs* hdcs, uint64_t off, uint64_t length){
    //char* data = (char*)malloc(sizeof(char)*4096);
    char* data;
    posix_memalign((void**)&data, 4096, 4096);
    memset(data, 'a', 4096);
    io_u* _io_u = new io_u( &arg, data );
    hdcs::hdcs_completion_t comp;
    hdcs::hdcs_aio_create_completion( (void*)_io_u, _finish_aiocb, &comp );
    hdcs->hdcs_aio_write(data, off, length, comp);
    return 0;
}

int aio_read( hdcs::libhdcs* hdcs, uint64_t off, uint64_t length ){
    //char* data = (char*)malloc(sizeof(char)*4096);
    char* data;
    posix_memalign((void**)&data, 4096, 4096);
    memset(data, 'a', 4096);
    io_u* _io_u = new io_u( &arg, data );
    hdcs::hdcs_completion_t comp;
    hdcs::hdcs_aio_create_completion( (void*)_io_u, _finish_aiocb, &comp );
    hdcs->hdcs_aio_read(data, off, length, comp);

    return 0;
}


int main(int argc, char *argv[]){
    arg.inflight_ops = 0;
    arg.io_complete_count = 0;

    const char* op_type = argv[1];

    hdcs::libhdcs *hdcs = new hdcs::libhdcs();
    hdcs::ThreadPool *threadpool = new hdcs::ThreadPool(2);

    time(&start);
    threadpool->schedule( &monitor );
    bool is_write = true;

    if(op_type[0] == 'r'){
        is_write = false;
    }

    srand(time(NULL));

    while(go){
        uint64_t off = rand()%1073741824/4096*4096;
        uint64_t length = 4096;
        if( arg.inflight_ops < 128 )
            arg.inflight_ops++;
            if( is_write )
                threadpool->schedule(std::bind(aio_write, hdcs, off, length) );
            if( !is_write )
                threadpool->schedule(std::bind(aio_read, hdcs, off, length ) );
        else{

            //printf("inflight_ops:%lu, do no op\n",inflight_ops);
            std::this_thread::yield();
        }
    }

    delete hdcs;
    return 0;
}
