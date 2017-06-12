#include <iostream>
#include <string.h>

#include "rbc/common/Log.h"
#include "rbc/common/AllocateMap.h"
#include "gtest/gtest.h"

using std::cout;
using std::endl;
using namespace rbc;

class TEST_ALLOCATE_MAP{
public:

    TEST_ALLOCATE_MAP():test_allocate_map(mpool){};
    bool compare_maps( DATAMAP_T dst, std::map<uint64_t, uint64_t> src);
    int test_lookup_boundaries();
    int test_update_non_overlap();
    int test_update_overlap_1();
    int test_update_overlap_2();
    int test_update_overlap_3();
    int test_update_overlap_4();
    int test_update_overlap_5();

private:

    Mempool* mpool = new Mempool(false);
    AllocateMap test_allocate_map;
};
bool TEST_ALLOCATE_MAP::compare_maps( DATAMAP_T data_map_return, std::map<uint64_t, uint64_t> desired_map){
    bool fail = false;
    std::map<uint64_t, uint64_t>::const_iterator it = desired_map.begin();
    DATAMAP_T::iterator it_check = data_map_return.begin();
    for( ; it_check != data_map_return.end(); it_check++ ){
        if( it_check->first != it->first || it_check->second != it->second ){
            fail = true;
            cout << "error: after update, data_map does not match the desire, desired= <" <<
                it->first << "," << it->second << ">, but returned= <" <<
                it_check->first << "," << it_check->second << "> ." << endl;
        }
        it++;
    }
    return !fail;
}

int TEST_ALLOCATE_MAP::test_lookup_boundaries(){
    bool exist = false;
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 1024, 512 );
    exist = test_allocate_map.lookup( 1024, 512 );
    if( !exist ){
        cout << "error: lookup for a exactly match block failed." << endl;
        return 1;
    }

    exist = test_allocate_map.lookup( 1024, 256 );
    if( !exist ){
        cout << "error: lookup for a block that left = start, right < end failed." << endl;
        return 1;
    }

    exist = test_allocate_map.lookup( 1280, 256 );
    if( !exist ){
        cout << "error: lookup for a block that left > start, right = end failed." << endl;
        return 1;
    }

    exist = test_allocate_map.lookup( 1024, 1024 );
    if( exist ){
        cout << "error: lookup for a block that left = start, right > end succeed, which is not right." << endl;
        return 1;
    }

    exist = test_allocate_map.lookup( 512, 1024 );
    if( exist ){
        cout << "error: lookup for a block that left < start, start < right < end succeed, which is not right." << endl;
        return 1;
    }

    exist = test_allocate_map.lookup( 512, 512 );
    if( exist ){
        cout << "error: lookup for a block that left < start, start = right < end succeed, which is not right." << endl;
        return 1;
    }

    exist = test_allocate_map.lookup( 1536 , 512 );
    if( exist ){
        cout << "error: lookup for a block that left > start, end < right suceed, which is not right." << endl;
        return 1;
    }

    return 0;
}

int TEST_ALLOCATE_MAP::test_update_non_overlap(){
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 3072, 512 );
    test_allocate_map.update( 2048, 512 );

    std::map<uint64_t, uint64_t> desired_map = {{1024, 512}, {2048,512}, {3072, 512}};
    DATAMAP_T data_map_return = test_allocate_map.get();

    if( compare_maps( data_map_return, desired_map ) )
        return 0;
    else
        return -1;
}

int TEST_ALLOCATE_MAP::test_update_overlap_1(){
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 768, 512 );

    std::map<uint64_t, uint64_t> desired_map = {{768, 768}, {2048,512}, {3072, 512}};
    DATAMAP_T data_map_return = test_allocate_map.get();

    if( compare_maps( data_map_return, desired_map ) )
        return 0;
    else
        return -1;
}

int TEST_ALLOCATE_MAP::test_update_overlap_2(){
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 1024, 768 );

    std::map<uint64_t, uint64_t> desired_map = {{768,1024}, {2048,512}, {3072, 512}};
    DATAMAP_T data_map_return = test_allocate_map.get();

    if( compare_maps( data_map_return, desired_map ) )
        return 0;
    else
        return -1;
}

int TEST_ALLOCATE_MAP::test_update_overlap_3(){
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 1536, 768 );

    std::map<uint64_t, uint64_t> desired_map = {{768,1792}, {3072, 512}};
    DATAMAP_T data_map_return = test_allocate_map.get();

    if( compare_maps( data_map_return, desired_map ) )
        return 0;
    else
        return -1;
}

int TEST_ALLOCATE_MAP::test_update_overlap_4(){
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 0, 512 );

    std::map<uint64_t, uint64_t> desired_map = {{0,512}, {768,1792}, {3072, 512}};
    DATAMAP_T data_map_return = test_allocate_map.get();

    if( compare_maps( data_map_return, desired_map ) )
        return 0;
    else
        return -1;
}

int TEST_ALLOCATE_MAP::test_update_overlap_5(){
    LOG_DEBUG_ENABLE = true;
    test_allocate_map.update( 256, 3584 );

    std::map<uint64_t, uint64_t> desired_map = {{0,3840}};
    DATAMAP_T data_map_return = test_allocate_map.get();

    if( compare_maps( data_map_return, desired_map ) )
        return 0;
    else
        return -1;
}

TEST_ALLOCATE_MAP allocate_map;

TEST (ALLOCATE_MAP, test_lookup_boundaries){
    ASSERT_EQ(0,allocate_map.test_lookup_boundaries());
}

TEST (ALLOCATE_MAP, test_update_non_overlap){
    ASSERT_EQ(0,allocate_map.test_update_non_overlap());
}

TEST (ALLOCATE_MAP, test_update_overlap_1){
    ASSERT_EQ(0,allocate_map.test_update_overlap_1());
}

TEST (ALLOCATE_MAP, test_update_overlap_2){
    ASSERT_EQ(0,allocate_map.test_update_overlap_2());
}

TEST (ALLOCATE_MAP, test_update_overlap_3){
    ASSERT_EQ(0,allocate_map.test_update_overlap_3());
}

TEST (ALLOCATE_MAP, test_update_overlap_4){
    ASSERT_EQ(0,allocate_map.test_update_overlap_4());
}

TEST (ALLOCATE_MAP, test_update_overlap_5){
    ASSERT_EQ(0,allocate_map.test_update_overlap_5());
}

