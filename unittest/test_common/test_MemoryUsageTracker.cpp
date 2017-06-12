#include <iostream>
#include <string>
#include "../../src/include/rbc/common/MemoryUsageTracker.h"
#include "gtest/gtest.h"

using std::cout;
using std::endl;
using std::string;
using namespace rbc;

class TEST_MEMORY_USAGE_TRACKER{
public:
    int basic_add_test();
    int add_on_test();
    int basic_remove_test();
    int remove_over_test();
    int basic_update_test();

private:
    MemoryUsageTracker mem_tracker;
};

int TEST_MEMORY_USAGE_TRACKER::basic_add_test()
{
    string type_string = "one";
    ssize_t type_len = 100;
    ssize_t new_type_len = 0;
    mem_tracker.add(type_string, type_len);
    new_type_len = mem_tracker.get_value(type_string);
    if(new_type_len == type_len)
    {
        cout << "basic add key is right" << endl;
        return 0;
    }else
    {
        cout << "error: basic add failed" << endl;
        return -1;
    }
}

int TEST_MEMORY_USAGE_TRACKER::add_on_test()
{
    string type_string1 = "one";
    ssize_t type_len1 = 200;
    ssize_t add_len = 300;
    ssize_t new_type_len1 = 0;
    mem_tracker.add(type_string1, type_len1);
    new_type_len1 = mem_tracker.get_value(type_string1);
    if(new_type_len1 == add_len)
    {
        cout << "add some key is right" << endl;
        return 0;
    }else
    {
        cout << "error: add some key failed" << endl;
        return -1;
    }
}

int TEST_MEMORY_USAGE_TRACKER::basic_remove_test()
{
    string type_string = "one";
    ssize_t type_len = 200;
    ssize_t new_type_len = 0;
    mem_tracker.rm(type_string, type_len);
    new_type_len = mem_tracker.get_value(type_string);
    if(new_type_len == 100)
    {
        cout << "basic remove test is right" << endl;
        return 0;
    }else
    {
        cout << "error: basic remove failed" << endl;
        return -1;
    }
}

int TEST_MEMORY_USAGE_TRACKER::remove_over_test()
{
    string type_string = "one";
    ssize_t type_len = 200;
    ssize_t new_type_len = 0;
    mem_tracker.rm(type_string, type_len);
    new_type_len = mem_tracker.get_value(type_string);
    if(new_type_len == -100)
    {
        cout << "basic remove test is right" << endl;
        return 0;
    }else
    {
        cout << "error: basic remove failed" << endl;
        return -1;
    }
}

int TEST_MEMORY_USAGE_TRACKER::basic_update_test()
{
    string type_string = "two";
    ssize_t old_type_len = 200;
    ssize_t new_type_len = 300;
    ssize_t final_type_len = 0;
    mem_tracker.update(type_string, 0, old_type_len);
    mem_tracker.update(type_string, old_type_len, new_type_len);
    final_type_len = mem_tracker.get_value(type_string);
    if(final_type_len == 300)
    {
        cout << "basic update test is right" << endl;
        return 0;
    }else
    {
        cout << "error: basic update failed" << endl;
        return -1;
    }
}


TEST_MEMORY_USAGE_TRACKER memory_usage_tracker;

TEST (TEST_MEMORY_USAGE_TRACKER, basic_add_test)
{
    ASSERT_EQ(0, memory_usage_tracker.basic_add_test());
}

TEST (TEST_MEMORY_USAGE_TRACKER, add_on_test)
{
    ASSERT_EQ(0, memory_usage_tracker.add_on_test());
}

TEST (TEST_MEMORY_USAGE_TRACKER, basic_remove_test)
{
    ASSERT_EQ(0, memory_usage_tracker.basic_remove_test());
}

TEST (TEST_MEMORY_USAGE_TRACKER, remove_over_test)
{
    ASSERT_EQ(0, memory_usage_tracker.remove_over_test());
}

TEST (TEST_MEMORY_USAGE_TRACKER, basic_update_test)
{
    ASSERT_EQ(0, memory_usage_tracker.basic_update_test());
}
