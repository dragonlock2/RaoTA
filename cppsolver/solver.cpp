#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>

#include "car.h"
#include "pq.h"

using namespace std;

// If necessary, can probs use uint8_t for indices

int main(int argc, char** argv) {
	auto start = chrono::high_resolution_clock::now();

	// Process args and build graph
	Car::start_loc = atoi(argv[1]); // Home
	int num_tas = atoi(argv[2]); // Number TAs
	set<int> tas; // Set to hold all initial TAs
	for (int i = 0; i < num_tas; i++) {
		tas.insert(atoi(argv[3+i]));
	}
	int num_locs = atoi(argv[3+num_tas]);

	cout << endl;
	int adjstart = 4 + num_tas;
	for (int i = 0; i < num_locs; i++) {
		for (int j = 0; j < num_locs; j++) {
			char *str = argv[adjstart + i*num_locs + j];
			if (str[0] != 'x') {
				double weight = atof(str);
				cout <<  "Edge: from-" << i << " to-" << j << " w-" << weight << endl;
			}
		}
	}

	

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

	cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}