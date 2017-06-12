//g++ test_Messenger.cpp ../Messenger/Messenger.cpp -o test -std=c++
#include "../Messenger/Messenger.h"

int main(){
    Config *cct = new Config();
    Messenger *messenger_d = new Messenger(cct);
    messenger_d->start_listen();
    return 0;
}
