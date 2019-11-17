#ifndef CAR_H
#define CAR_H

#include <vector>
#include <set>

// Intended for use inside an unordered_map (hash map)

class Car {
	public:
		int loc;
		std::set<int> tas;
		std::set<int> reached;

		Car(int l, std::set<int> t, std::set<int> r);

		//TODO still need to make neighbors()

		bool operator==(Car other) const;
		friend std::ostream& operator<<(std::ostream &strm, const Car &c);
};

namespace std {
	template <>
	struct hash<set<int>> {
		size_t operator()(const set<int>& s) const {
			size_t h = 0;
			for (auto i: s) {
				h += hash<int>()(i);
			}
			return h;
		}
	};
	template <>
	struct hash<Car> {
	    size_t operator()(const Car& c) const {
	        return hash<int>()(c.loc) + hash<set<int>>()(c.tas);
	    }
	};
}

#endif