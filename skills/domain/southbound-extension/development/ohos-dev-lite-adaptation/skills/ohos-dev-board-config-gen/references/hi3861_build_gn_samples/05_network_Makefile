CC := gcc
CFLAGS := -Wall

COMMON_SRCS := demo_entry_posix.c

TCP_CLIENT_SRCS := tcp_client_test.c
TCP_SERVER_SRCS := tcp_server_test.c
UDP_CLIENT_SRCS := udp_client_test.c
UDP_SERVER_SRCS := udp_server_test.c

TCP_CLIENT_TARGET := tcp_client_test
TCP_SERVER_TARGET := tcp_server_test
UDP_CLIENT_TARGET := udp_client_test
UDP_SERVER_TARGET := udp_server_test

###########################################################################################################

COMMON_OBJS := $(addsuffix .o, $(notdir $(basename $(COMMON_SRCS))))
TCP_CLIENT_OBJS := $(addsuffix .o, $(notdir $(basename $(TCP_CLIENT_SRCS))))
TCP_SERVER_OBJS := $(addsuffix .o, $(notdir $(basename $(TCP_SERVER_SRCS))))
UDP_CLIENT_OBJS := $(addsuffix .o, $(notdir $(basename $(UDP_CLIENT_SRCS))))
UDP_SERVER_OBJS := $(addsuffix .o, $(notdir $(basename $(UDP_SERVER_SRCS))))

SRCS := $(COMMON_SRCS) $(TCP_CLIENT_SRCS) $(TCP_SERVER_SRCS) $(UDP_CLIENT_SRCS) $(UDP_SERVER_SRCS)
OBJS := $(addsuffix .o, $(notdir $(basename $(SRCS))))

TARGETS := $(TCP_CLIENT_TARGET) $(TCP_SERVER_TARGET) $(UDP_CLIENT_TARGET) $(UDP_SERVER_TARGET)

###########################################################################################################

all: $(TARGETS)

$(TCP_CLIENT_TARGET): $(TCP_CLIENT_OBJS) $(COMMON_OBJS)
	$(CC) $(CCFLAGS) -o $@ $^

$(TCP_SERVER_TARGET): $(TCP_SERVER_OBJS) $(COMMON_OBJS)
	$(CC) $(CCFLAGS) -o $@ $^

$(UDP_CLIENT_TARGET): $(UDP_CLIENT_OBJS) $(COMMON_OBJS)
	$(CC) $(CCFLAGS) -o $@ $^

$(UDP_SERVER_TARGET): $(UDP_SERVER_OBJS) $(COMMON_OBJS)
	$(CC) $(CCFLAGS) -o $@ $^

clean:
	rm $(OBJS) $(TARGETS) || echo

.PHONY: clean all
