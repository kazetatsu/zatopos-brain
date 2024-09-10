LOCATOR_TYPE = cpu
OBJS   = build/locator.o build/ear_agent.o
TARGET = build/libzatopos.so

all: $(TARGET)

$(TARGET): $(OBJS)
	gcc -shared -fPIC -o $@ $^ -lusb-1.0 -lm

build/locator.o: build/locator_$(LOCATOR_TYPE).o
	ln -fs $(subst build/,,$<) $@

build/locator_cpu.o: src/locator_cpu.c
	@mkdir -p build
	gcc -o $@ -c $< -I./include

build/ear_agent.o: src/ear_agent.c
	@mkdir -p build
	gcc -o $@ -c $< -I/usr/include/libusb-1.0 -I./include

clean:
	rm -r build
