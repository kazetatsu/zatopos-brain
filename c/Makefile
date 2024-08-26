SRCS   = src/receiver.c
OBJS   = $(patsubst src/%.c, build/%.so, $(SRCS))
TARGET = build/libzatopos.so

all: $(TARGET)

$(TARGET): $(OBJS)
	gcc -shared -fPIC -o $@ $^ -lusb-1.0

$(OBJS): $(SRCS)
	mkdir -p build
	gcc -shared -fPIC -o $@ -c $< -I/usr/include/libusb-1.0 -I./include

clean:
	rm -r build
