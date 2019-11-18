#include <iostream>
#include <algorithm>
#include <vector>
#include <set>

#include "car.h"

Graph Car::G;
WeightMap Car::wm;
std::vector<std::vector<double>> Car::all_dists;
std::vector<std::vector<int>> Car::all_pcessors;
int Car::start_loc;
std::set<int> Car::start_tas;

Car::Car(int l, std::set<int> t, std::set<int> r) : loc(l), tas(t), reached(r) {} // It auto makes copies :)

std::vector<std::pair<Car, double>> Car::neighbors() {
	std::vector<std::pair<Car, double>> neighs;
	
	if (reached.count(loc)) { //If I've been here before, then can't drop anyone off
		for (auto ei = boost::out_edges(loc, G); ei.first != ei.second; ei.first++) {
			auto e = *ei.first;
			neighs.push_back(std::pair<Car, double>(Car(boost::target(e, G), tas, reached), wm[e] * 2/3));
		}
	} else {
		std::set<int> newreached = reached;
		newreached.insert(loc);

		std::set<int> poss_tas = tas; //possible tas left in car after dropoff
		poss_tas.erase(loc); //always dropoff ta that lives at current location

		for (auto& pd: powerSet(tas)) { //all possible ways have tas left in car
			double cost = 0; // cost of dropoff
			std::set<int> drops;
			std::set_difference(poss_tas.begin(), poss_tas.end(), pd.begin(), pd.end(), std::inserter(drops, drops.end()));
			for (auto& t: drops) {
				cost += all_dists[loc][t];
			}
			if (pd.size() == 0) { //if everyone dropped off, just head home
				neighs.push_back(std::pair<Car, double>(Car(start_loc, pd, newreached), cost + all_dists[loc][start_loc] * 2/3));
			} else {
				for (auto ei = boost::out_edges(loc, G); ei.first != ei.second; ei.first++) {
					auto e = *ei.first;
					neighs.push_back(std::pair<Car, double>(Car(boost::target(e, G), pd, newreached), cost + wm[e] * 2/3));
				}
			}
			
		}
	}

	return neighs;
}

std::vector<std::set<int>> Car::powerSet(std::set<int> s) {
	std::vector<std::set<int>> ps(intpow(2, s.size()));
	for (int i = 0; i < ps.size(); i++) {
		ps[i] = std::set<int>();
	}
	int i = 0;
	for (auto item = s.begin(); item != s.end(); item++) {
		for (int j = 0; j < ps.size(); j++) {
			if (j & (1 << i)) {
				ps[j].insert(*item);
			}
		}
		i++;
	}
	return ps;
}

int Car::intpow(int b, int n) {
	if (n == 0) {
		return 1;
	}
	if (n == 1) {
		return b;
	}
	if (n % 2 == 0) {
		return intpow(b*b, n/2);
	} else {
		return b * intpow(b*b, (n-1)/2);
	}
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