#include <iostream>
#include "car.h"

using namespace std;

int main(int argc, char** argv) {
	auto start = chrono::high_resolution_clock::now();

	Car::startloc = 63;
	Car::doneid = (carid_t) Car::startloc << LOC_OFFSET;

	//diy graph with vector and dijkstras
	//allpaths with vector
	//pcessor with vector
	//maps to carid and costs
	//std pq
	//smart ptrs?

	//generation of neighbors is highly parallelizable
	// 1 << x == 2^x

	

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
	cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}