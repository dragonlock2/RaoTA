#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <map>
#include <random>

#include <boost/heap/binomial_heap.hpp>

using namespace std;

#define ARR_SIZE 50000000

int main() {
	uint64_t x = 0;
	if (x == 0) {
		cout << "Hi!" << endl;
	}

	//Begin Benchmark
	auto start = chrono::high_resolution_clock::now();

	

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	cout << "Done! Time: " << duration.count() << "ms" << endl;

	start = chrono::high_resolution_clock::now();

	

	end = chrono::high_resolution_clock::now();
	duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}