#include <iostream>

#include "rbc/common/WorkQueue.h"
#include "gtest/gtest.h"

using std::cout;
using std::endl;
using namespace rbc;

class TEST_WORK_QUEUE{
public:

    int basic_push_pop();
    int pop_empty();
    int push_pop_complex();

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

int TEST_WORK_QUEUE::push_pop_complex()
{
    int* push_pointer2;
    for (int i=0; i<3; i++)
    {
        request_queue.enqueue(push_pointer2);
        push_pointer2++;
    }
    void* pop_pointer2;
    for (int j=0; j<3; j++)
    {
        pop_pointer2 =  request_queue.dequeue();
        if (pop_pointer2 == (push_pointer2-(3-j)))
        {
            cout << "pop queue pointer is right" << endl;
        }else
        {
            cout << "pop pointer failed" << endl;
            return -1;
            break;
        }
    }
    return 0;
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

TEST (WORK_QUEUE, push_pop_complex)
{
    ASSERT_EQ(0, work_queue.push_pop_complex());
}
