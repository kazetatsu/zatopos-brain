# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

MUSICAL_TYPE = cpu
OBJS   = build/musical.o build/ear_driver.o
TARGET = build/libzatopos.so

all: $(TARGET)

$(TARGET): $(OBJS)
	gcc -shared -fPIC -o $@ $^ -lusb-1.0 -lm

build/musical.o: build/musical_$(MUSICAL_TYPE).o
	ln -fs $(subst build/,,$<) $@

build/musical_cpu.o: src/musical_cpu.c
	@mkdir -p build
	gcc -o $@ -c $< -I./include

build/ear_driver.o: src/ear_driver.c
	@mkdir -p build
	gcc -o $@ -c $< -I/usr/include/libusb-1.0 -I./include

clean:
	rm -r build
