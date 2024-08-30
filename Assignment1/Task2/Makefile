all: perkalian.exe

perkalian.exe: perkalian.cpp
	 g++ -o perkalian.exe perkalian.cpp

dump: perkalian.exe
	 objdump -d perkalian.exe > perkalian.exe.asm

clean:
	 rm -f perkalian.exe perkalian.exe.asm

run: perkalian.exe
	 ./perkalian.exe
