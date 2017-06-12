//g++ test_Messenger_client_read.cpp ../Messenger/Messenger_Client.cpp ../Messenger/Messenger.cpp -o test_client_read -std=c++11 -lboost_system
#include "../Messenger/Messenger_Client.h"
#include <fstream>
#include <stdlib.h>

int main(int argc, char *argv[]){
    Config *cct = new Config();
    Messenger_Client *messenger = new Messenger_Client(cct);
    //char image_off[] = "volume-02150a4f-73c9-49ff-a313-93ccc96cc155:128";
    char* image_off = argv[1];
    uint64_t off = strtoul(argv[2], NULL, 0);
    uint64_t length = strtoul(argv[3], NULL, 0);
    char* data;

    Message message(image_off, off, data, length, 2 );
    messenger->send_msg(message._msg);
    messenger->read_msg(message._msg);

}

