#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>
#include <queue>
#include "car.h"
#include "pair.h"

using namespace std;

int main(int argc, char** argv) {
	auto start = chrono::high_resolution_clock::now();

	for (int i = 0; i < argc; i++) {
		cout << argv[i] << endl;
	}

	set<int> a, b;
	a.insert(1); a.insert(2); a.insert(3);
	b.insert(1); b.insert(2); b.insert(3); b.insert(4); b.insert(5);

	Car c(5, a, b);
	Car d(5, a, b);
	c.tas.insert(54);

	Pair p1(c, 1.234456756);
	Pair p2(d, 1.23);
	Pair p3(c, 0.69);
	Pair p4(d, 69.0);

	priority_queue<Pair> pq;
	pq.push(p1); pq.push(p2); pq.push(p3); pq.push(p4);

	while (!pq.empty()) {
		cout << pq.top() << endl;
		pq.pop();
	}

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

	cout << "Done! Time: " << duration.count() << "ms" << endl;

	return 0;
}