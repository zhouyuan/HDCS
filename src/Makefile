LIBRBC_VERSION = 1.3.0

CC=cc
CXX=g++
PLATFORM=OS_LINUX
OPTIMIZATION?=-O2
OPT=$(OPTIMIZATION)
CXXFLAGS=-std=c++11 ${OPT} -fPIC -g -D__STDC_FORMAT_MACROS -DLIBRBC_VERSION='"${LIBRBC_VERSION}"'
CCFLAGS=${OPT} -fPIC -g -D__STDC_FORMAT_MACROS -DLIBRBC_VERSION='"${LIBRBC_VERSION}"'
#PLATFORM_LDFLAGS=-lboost_thread -lboost_system -lpthread -lrbd -lrados
PLATFORM_LDFLAGS=-lboost_thread -lboost_system -lpthread
INCS=-I./
CONTROLLER = HDCS
DIST_LIB = lib/libhdcs.so
TEST_TOOL = hdcs_test_tool
POLICY = ALL
.PHONY : all
all: $(DIST_LIB) $(CONTROLLER) $(TEST_TOOL)

%.o : %.cpp
	${CXX} -c ${CXXFLAGS} ${INCS} $< -o $@

%.o : %.c
	${CC} -c ${CCFLAGS} ${INCS} $< -o $@

COMMON_OBJECTS:= store/SimpleStore/SimpleBlockStore.o core/policy/CachePolicy.o core/policy/TierPolicy.o core/HDCSCore.o HDCSController.o

RBD_OBJECTS:= store/RBD/RBDImageStore.o 

$(CONTROLLER): $(COMMON_OBJECTS) $(RBD_OBJECTS)
	${CXX} ${CXXFLAGS} ${INCS} -DCACHE_POLICY -DTIER_POLICY HDCS.cpp -o $@ $^ ${PLATFORM_LDFLAGS}

$(DIST_LIB):
	mkdir -p lib
	${CXX} ${CXXFLAGS} ${INCS} libhdcs.c -shared -o $@ $^ ${PLATFORM_LDFLAGS}

$(TEST_TOOL): $(DIST_LIB)
	${CXX} ${CXXFLAGS} ${INCS} test.c -o $@ $^ -Llib -lhdcs

test:
	${CXX} ${CXXFLAGS} ${INCS} ../unittest/test_common/testrun.cpp -o $@ $^ ../unittest/lib/libgmock.a -pthread
	echo "./test" | bash


clean:
	rm -f test $(CONTROLLER) $(DIST_LIB) $(TEST_TOOL) && find . -name "*.o" | xargs rm -f

uninstall:
	rm -rf /usr/local/include/hdcs
	rm -rf /usr/local/lib/libhdcs.so

clean_test:
	rm hdcs_test_tool

install:
	cp -r include/ /usr/local/include/hdcs
	cp lib/libhdcs.so /usr/local/lib/
	cp HDCS /usr/local/bin/
