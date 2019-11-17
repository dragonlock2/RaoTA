#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>
#include "car.h"

using namespace std;

template <>
struct std::hash<Car> {
    size_t operator()(const Car& c) const {
        return hash<int>()(c.loc);
    }
};

int main() {
	auto start = chrono::high_resolution_clock::now();

	set<int> a, b;
	a.insert(1); a.insert(2); a.insert(3);
	b.insert(1); b.insert(2); b.insert(3); b.insert(4); b.insert(5);

	Car c(5, a, a);
	Car d(5, b, b);

	cout << (c == d) << endl;

	cout << hash<Car>()(c) << endl;

	auto end = chrono::high_resolution_clock::now();
	auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

	cout << "Done! Time: " << duration.count() << "ms" << endl;
}