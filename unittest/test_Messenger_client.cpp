//g++ test_Messenger_client.cpp ../Messenger/Messenger_Client.cpp ../Messenger/Messenger.cpp -o test_client -std=c++11 -lboost_system
#include "../Messenger/Messenger_Client.h"
#include <fstream>

int main(int argc, char *argv[]){
    Config *cct = new Config();
    Messenger_Client *messenger = new Messenger_Client(cct);
    //char image_off[] = "volume-1";
    uint64_t off = 128;
    char* image_off = argv[1];

/*    std::streampos fsize = 0;
    uint64_t size = 0;
    std::ifstream myReadFile(argv[2], std::ios::binary);
    myReadFile.seekg( 0 );
    fsize = myReadFile.tellg();
    myReadFile.seekg( 0, std::ios::end );
    fsize = myReadFile.tellg() - fsize;
    size = (uint64_t)fsize;

    std::cout << "size:"<< size << std::endl;
    char *data = (char*)malloc( size * sizeof(char) );
    memset(data, 0 ,size);
    myReadFile.seekg( 0 );
    myReadFile.read( data, size );

    myReadFile.close();
    */
    char* data = argv[2];
    uint64_t size = sizeof(data);
    Message message(image_off, off, data, size );
    messenger->send_msg(message._msg);
    messenger->read_msg(message._msg);

}

