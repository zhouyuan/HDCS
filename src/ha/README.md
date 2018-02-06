*How to make
```
g++ test_HA_auto.c -o test -std=c++11 -I../ -lboost_thread -lboost_system -lboost_program_options -lpthread -lcrush -g

g++ HDCSAdmin.c -o hdcsadm -std=c++11 -I../ -lboost_thread -lboost_system -lboost_program_options -lpthread

```
*How to test
```
start HAManager:
./test -r server -n host01

CMDLINE
./hdcsadm get_status
```
