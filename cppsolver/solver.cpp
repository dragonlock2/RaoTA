#include <iostream>
#include <vector>
#include <set>
#include "car.h"

using namespace std;

int main() {
	auto start = chrono::high_resolution_clock::now();

	set<int> a, b;
	a.insert(1); a.insert(2); a.insert(3);
	b.insert(4); b.insert(5); b.insert(6);

	Car c(5, a, b);
	Car d(10, a, b);

	// cout << (c == d) << endl;

	a.insert(9); b.insert(9);
	c.tas.insert(0); c.reached.insert(0);

	for (auto i = a.begin(); i != a.end(); i++) {
		cout << *i << " ";
	}
	cout << endl;
	for (auto i = b.begin(); i != b.end(); i++) {
		cout << *i << " ";
	}
	cout << endl;

	for (auto i = c.tas.begin(); i != c.tas.end(); i++) {
		cout << *i << " ";
	}
	cout << endl;
	for (auto i = c.reached.begin(); i != c.reached.end(); i++) {
		cout << *i << " ";
	}
	cout << endl;

	for (auto i = d.tas.begin(); i != d.tas.end(); i++) {
		cout << *i << " ";
	}
	cout << endl;
	for (auto i = d.reached.begin(); i != d.reached.end(); i++) {
		cout << *i << " ";
	}
	cout << endl;


	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

	cout << "Done! Time: " << duration.count() << "ms" << endl;
}