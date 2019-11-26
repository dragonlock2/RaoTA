CC=g++
FLAGS=-std=c++17 -Ofast

OBJECTS=car.o graph.o

solver: solver.o $(OBJECTS)
	$(CC) $(FLAGS) -o solver solver.o $(OBJECTS)

solver.o: solver.cpp
	$(CC) $(FLAGS) -c solver.cpp -o solver.o

$(OBJECTS): %.o: %.cpp %.h
	$(CC) $(FLAGS) -c $< -o $@

test: test.cpp
	$(CC) $(FLAGS) -o test test.cpp

clean:
	rm -rf *.o *.dSYM test solver