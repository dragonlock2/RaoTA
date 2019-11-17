#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>
#include "car.h"
#include "pq.h"

using namespace std;

int main(int argc, char** argv) {
	auto start = chrono::high_resolution_clock::now();

	for (int i = 0; i < argc; i++) {
		cout << argv[i] << endl;
	}

	set<int> a, b;
	a.insert(1); a.insert(2); a.insert(3);
	b.insert(1); b.insert(2); b.insert(3);

	Car c(5, a, b);
	Car d(5, a, b);
	Car e(5, a, b);
	c.reached.insert(4); c.tas.insert(4);
	d.reached.insert(5); d.tas.insert(5);
	e.reached.insert(69);

	FibPQ pq;
	pq.pushOrChangeKey(c, 0.5);
	pq.pushOrChangeKey(d, 10);
	pq.pushOrChangeKey(e, -1);
	pq.pushOrChangeKey(c, 15);

	while (!pq.empty()) {
		cout << pq.removeMin() << endl;
	}

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

	cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}