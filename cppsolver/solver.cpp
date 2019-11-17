#include <iostream>
#include <vector>
#include "car.h"

int main() {
	auto start = std::chrono::high_resolution_clock::now();

	Car c(10);

	std::cout << c.getX() << std::endl;

	auto end = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

	std::cout << "Done! Time: " << duration.count() << "ms" << std::endl;
}