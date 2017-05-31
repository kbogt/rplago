all:
	gcc -Wall -fPIC -c src/bmp180.c -o src/bmp180.o
	gcc -shared -Wl,-soname,libbmp180.so.1 -o src/libbmp180.so src/bmp180.o

clean:
	rm *.o > /dev/null 2>&1 &
