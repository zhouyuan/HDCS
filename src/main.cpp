#include "rbc/CacheService.h"
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

bool go = true;

void my_handler(int s){
    printf("Caught signal interrupt\n");
    go = false;
}

void usage(){
    printf("usage: hyperstash -c ${rbd_volume_name} -r ${master/replica}\n");
}

int main(int argc,char** argv)
{
    if(argc < 2){
        usage();
        return -1;
    }
    
    struct sigaction sigIntHandler;

    sigIntHandler.sa_handler = my_handler;
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_flags = 0;

    char* conf_name = NULL;
    bool if_master = false;

    for(int i=0; i<argc; i++){
        std::string arg(argv[i]);
        if( arg.compare("--config") == 0 || arg.compare("-c") == 0 ){
            conf_name = argv[i+1];
        }
        if( arg.compare("--role") == 0 || arg.compare("-r") == 0 ){
            if_master=argv[i+1][0]=='m'?true:false;
        }
    }

    if(conf_name){
        rbc::CacheService csd(conf_name, true, if_master);
        sigaction(SIGINT, &sigIntHandler, NULL);
        while( go ){sleep(1);}
        printf("exit while\n");
    }
            
    return 0;
}
