#include <iostream>
#include <vector>
#include <set>

#include "car.h"

int Car::G = 0;
int Car::all_paths = 0;
int Car::start_loc = 0;

Car::Car(int l, std::set<int> t, std::set<int> r) : loc(l), tas(t), reached(r) {} // It auto makes copies :)

std::vector<std::pair<Car, double>> Car::neighbors() {
	std::vector<std::pair<Car, double>> v;
	Car c(5, std::set<int>(), std::set<int>());
	v.push_back(std::pair<Car, double>(c, G));
	v.push_back(std::pair<Car, double>(c, start_loc));
	return v;
}

bool Car::operator==(Car other) const {
	return loc == other.loc && tas == other.tas;
}

std::ostream& operator<<(std::ostream &strm, const Car &c) {
	strm << "Car(" << c.loc << ", {";
	for (auto i = c.tas.begin(); i != c.tas.end(); i++) {
		strm << *i << ", ";
	}
	if (!c.tas.empty()) {
		strm << "\b\b";
	}
	strm << "}, {";
	for (auto i = c.reached.begin(); i != c.reached.end(); i++) {
		strm << *i << ", ";
	}
	if (!c.reached.empty()) {
		strm << "\b\b";
	}
	strm << "})";
	return strm;
}