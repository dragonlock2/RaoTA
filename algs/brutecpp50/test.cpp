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
	//Init stuff to be tested
	vector<uint64_t> ind;
	vector<uint64_t> arr;

	priority_queue<uint64_t> pq;
	boost::heap::binomial_heap<uint64_t> bpq;

	std::random_device rd;
	std::mt19937_64 eng(rd());
	std::uniform_int_distribution<uint64_t> distr(0, (uint64_t) 1 << 33);

	for (int i = 0; i < ARR_SIZE; i++) {
		uint64_t r = distr(eng);
		ind.push_back(i);
		arr.push_back(r);

		pq.push(r);
		bpq.push(r);
	}

	shuffle(ind.begin(), ind.end(), eng);


	//Begin Benchmark
	auto start = chrono::high_resolution_clock::now();

	for (auto i = ind.begin(); i != ind.end(); i++) {
		// pq.push(arr[*i]);
		pq.pop();
	}

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	cout << "Done! Time: " << duration.count() << "ms" << endl;

	start = chrono::high_resolution_clock::now();

	for (auto i = ind.begin(); i != ind.end(); i++) {
		// bpq.push(arr[*i]);
		bpq.pop();
	}

	end = chrono::high_resolution_clock::now();
	duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}