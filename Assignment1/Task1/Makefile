all: add_numbers.exe

add_numbers.exe: add_numbers.cpp
	 g++ -o add_numbers.exe add_numbers.cpp

dump: add_numbers.exe
	 objdump -d add_numbers.exe > add_numbers.exe.asm

clean:
	 rm -f add_numbers.exe add_numbers.exe.asm

run: add_numbers.exe
	 ./add_numbers.exe
