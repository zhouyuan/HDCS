#include <iostream>

#include "../src/common/WorkQueue.h"
#include "gtest/gtest.h"

using std::cout;
using std::endl;
using namespace hdcs;

class TEST_WORK_QUEUE{
public:

    int basic_push_pop();
    int pop_empty();

private:
    WorkQueue<void*> request_queue;
};

int TEST_WORK_QUEUE::basic_push_pop()
{
    int* push_pointer;
    request_queue.enqueue(push_pointer);
    void* pop_pointer;
    pop_pointer = request_queue.dequeue();
    if(pop_pointer == push_pointer)
    {
        cout << "pop front pointer is right" << endl;
        return 0;
    }else
    {
        cout << "error: pop front pointer failed" << endl;
        return -1;
    }
}

int TEST_WORK_QUEUE::pop_empty()
{
    int* push_pointer1;
    request_queue.enqueue(push_pointer1);
    void* pop_pointer1;
    pop_pointer1 = request_queue.dequeue();
    if(pop_pointer1 == push_pointer1)
    {
        pop_pointer1 = request_queue.dequeue();
        if(pop_pointer1 == NULL)
        {
            cout << "pop empty is right" << endl;
            return 0;
        }else
        {
            cout << "pop empty failed" << endl;
            return -1;
        }
    }else
    {
        cout << "pop empty first test failed" << endl;
        return -1;
    }
}

TEST_WORK_QUEUE work_queue;

TEST (WORK_QUEUE, basic_push_pop)
{
    ASSERT_EQ(0, work_queue.basic_push_pop());
}

TEST (WORK_QUEUE, pop_empty)
{
    ASSERT_EQ(0, work_queue.pop_empty());
}
