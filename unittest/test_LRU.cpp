/*please compile by
 g++ -o test test_LRU.cpp -std=c++11
 */

#include "../common/LRU.h"
#define LRU_LIST_LENGTH 5

uint64_t cal_value( const char &key ){
    uint64_t value = (uint64_t) &key;
    return value;
}

int main(){
    int lru_length = LRU_LIST_LENGTH;
    printf("initiate LRU list, length %d:\n", lru_length);
    LRU<char, uint64_t> myLRU_list( cal_value, lru_length );
    char key1[] = "hello";
    char key2[] = "lalae";
    uint64_t value = 0;
    char key_chain[LRU_LIST_LENGTH] = {0};

    char key = 'x';
    value = myLRU_list.get_value( key );
    printf("add new key:%c, value: %lx\n", key, value);
    myLRU_list.get_keys( key_chain );
    printf("current key list: %s\n", key_chain);

    for(int i=0; i < 5; i++){
        value = myLRU_list.get_value( key1[i] );
        printf("add new key:%c, value: %lx\n", key1[i], value);
        myLRU_list.get_keys( key_chain );
        printf("current key list: %s\n", key_chain);
    }

    for(int i=0; i < 5; i++){
        value = myLRU_list.get_value( key2[i] );
        printf("add new key:%c, value: %lx\n", key2[i], value);
        myLRU_list.get_keys( key_chain );
        printf("current key list: %s\n", key_chain);
    }

    return 0;
}
