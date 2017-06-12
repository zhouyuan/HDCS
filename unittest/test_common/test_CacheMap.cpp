#include <iostream>
#include <string.h>

#include "rbc/common/CacheMap.h"
#include "gtest/gtest.h"

using std::cout;
using std::endl;
using namespace rbc;

class TEST_CACHE_MAP{
public:

    TEST_CACHE_MAP():test_cache_map(mpool){};
    int test_p_case1();
    int test_p_case2();
    int test_p_case3();
    int test_p_case4();

private:

    Mempool* mpool = new Mempool(false);
    CacheMap test_cache_map;
};

int TEST_CACHE_MAP::test_p_case1(){
    std::string key("a");
    int value = 1;
    char* value_ref = (char*)&value;
    int value_return;
    char* value_return_ref;
    test_cache_map.insert(key, value_ref);
    value_return_ref = test_cache_map.find_key(key);
    value_return = *((int*)value_return_ref);
    if(1 == value_return){
        cout << "get key value: " << value_return << endl;
        return 0;
    }else{
        cout << "error: positive test case 1 failed" << endl;
        return 1;
    }
}

int TEST_CACHE_MAP::test_p_case2(){
    std::string keys[5] = {"b","c","d","e","f"};
    int values[5] = {2,3,4,5,6};
    char* value_ref;
    int value_return;
    char* value_return_ref;
    for(int i = 0; i < 5; i++){
        value_ref = (char*)&values[i];
        test_cache_map.insert(keys[i],value_ref);
    }
    value_return_ref = test_cache_map.find_key(keys[2]);
    value_return = *((int*)value_return_ref);
    if(4 == value_return){
        cout << "get key value: " << value_return << endl;
        return 0;
    }else{
        cout << "error: positive test case 2 failed" << endl;
        return 1;
    }
}

int TEST_CACHE_MAP::test_p_case3(){
    std::string key = "d";
    char* value;
    test_cache_map.evict(key);
    value = test_cache_map.find_key(key);
    if(value == NULL){
        cout << "evict value successfully" << endl;
        return 0;
    }else{
        cout << "error: positive test case 3 failed" << endl;
        return 1;
    }
}

int TEST_CACHE_MAP::test_p_case4(){
    std::string key = "g";
    char* value;
    value = test_cache_map.find_key(key);
    if(NULL == value){
        cout << "found a non-exist key failed, which is the correct move" << endl;
        return 0;
    }else{
        cout << "error: positive test case 4 failed" << endl;
        return 1;
    }
}

TEST_CACHE_MAP cache_map;

TEST (CACHE_MAP, test_p_case1){
    ASSERT_EQ(0,cache_map.test_p_case1());
}

TEST (CACHE_MAP, test_p_case2){
    ASSERT_EQ(0,cache_map.test_p_case2());
}

TEST (CACHE_MAP, test_p_case3){
    ASSERT_EQ(0,cache_map.test_p_case3());
}

TEST (CACHE_MAP, test_p_case4){
    ASSERT_EQ(0,cache_map.test_p_case4());
}

