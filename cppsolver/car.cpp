#include <iostream>
#include <vector>
#include <set>
#include "car.h"

Car::Car(int l, std::set<int> t, std::set<int> r) : loc(l), tas(t), reached(r) {} // It auto makes copies :)

bool Car::operator==(Car other) const {
	return loc == other.loc;
}

std::ostream& operator<<(std::ostream &strm, const Car &c) {
	strm << "Car(" << c.loc << ", {";
	for (auto i = c.tas.begin(); i != c.tas.end(); i++) {
		strm << *i << " ";
	}
	if (!c.tas.empty()) {
		strm << "\b";
	}
	strm << "}, {";
	for (auto i = c.reached.begin(); i != c.reached.end(); i++) {
		strm << *i << " ";
	}
	if (!c.reached.empty()) {
		strm << "\b";
	}
	strm << "})";
	return strm;
}