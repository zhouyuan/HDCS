LIBRBC_VERSION = 1.5.0

CC=cc
CXX=g++
PLATFORM=OS_LINUX
OPTIMIZATION?=-O2
OPT=$(OPTIMIZATION)
CXXFLAGS=-std=c++11 ${OPT} -fPIC -g -D__STDC_FORMAT_MACROS -DLIBRBC_VERSION='"${LIBRBC_VERSION}"'
CCFLAGS=${OPT} -fPIC -g -D__STDC_FORMAT_MACROS -DLIBRBC_VERSION='"${LIBRBC_VERSION}"'
PLATFORM_LDFLAGS=-lboost_thread -lboost_system -lpthread -lrbd -lrados
INCS=-I./

DIST_LIB = libhdcs.so
BENCH = bench

.PHONY : all
all: $(DIST_LIB)

%.o : %.cpp
	${CXX} -c ${CXXFLAGS} ${INCS} $< -o $@

%.o : %.c
	${CC} -c ${CCFLAGS} ${INCS} $< -o $@

COMMON_OBJECTS:= store/SimpleStore/SimpleBlockStore.o core/policy/CachePolicy.o core/HDCSCore.o 
RBD_OBJECTS:= store/RBD/RBDImageStore.o 

$(BENCH): $(COMMON_OBJECTS) $(RBD_OBJECTS)
	${CXX} ${CXXFLAGS} ${INCS} bench_libhdcs.cpp -o $@ $^ ${PLATFORM_LDFLAGS}

$(DIST_LIB): $(COMMON_OBJECTS) $(RBD_OBJECTS)
	${CXX} ${CXXFLAGS} ${INCS} libhdcs.c -shared -o $@ $^ ${PLATFORM_LDFLAGS}

clean:
	rm -rf common/*.o core/*.o store/SimpleStore/*.o store/RBD/*.o core/policy/*.o libhdcs.so
	rm -rf /usr/local/include/hdcs
	rm -rf /usr/local/lib/libhdcs.so

install:
	cp -r include/ /usr/local/include/hdcs
	cp libhdcs.so /usr/local/lib/
