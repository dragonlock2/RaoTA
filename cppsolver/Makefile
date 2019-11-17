CC=g++
FLAGS=-std=c++17 -O3

all:
	$(CC) $(FLAGS) -c -o solver.o solver.cpp
	$(CC) $(FLAGS) -c -o car.o car.cpp
	$(CC) $(FLAGS) -c -o pq.o pq.cpp
	$(CC) $(FLAGS) -o solver solver.o car.o pq.o
	rm *.o

clean:
	rm *.o