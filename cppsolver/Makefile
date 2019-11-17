CC=g++
FLAGS=-std=c++17 -O3

all:
	$(CC) -c -o solver.o solver.cpp $(FLAGS)
	$(CC) -c -o car.o car.cpp $(FLAGS)
	$(CC) -c -o pair.o pair.cpp $(FLAGS)
	$(CC) -o solver solver.o car.o pair.o $(FLAGS)
	rm *.o

clean:
	rm *.o