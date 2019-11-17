CC=g++
FLAGS=-std=c++17

all:
	$(CC) -O3 -c -o solver.o solver.cpp $(FLAGS)
	$(CC) -O3 -c -o car.o car.cpp $(FLAGS)
	$(CC) -O3 -o solver solver.o car.o $(FLAGS)
	rm *.o

clean:
	rm *.o