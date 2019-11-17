#ifndef CAR_H
#define CAR_H

#include <vector>
#include <set>

class Car {
	public:
		int loc;
		std::set<int> tas;
		std::set<int> reached;

		Car(int l, std::set<int> t, std::set<int> r);

		bool operator==(Car other) const;
		friend std::ostream& operator<<(std::ostream &strm, const Car &c);
};

#endif