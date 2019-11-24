#ifndef GLOBALS_H
#define GLOBALS_H

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <deque>

using namespace std;

#define LOC_BITS 6
#define LOC_OFFSET 58 //=64-6

//Note a lot of these don't cout properly

typedef uint64_t carid_t; //max 58 locations, index 0-57
typedef uint64_t reach_t;

typedef uint8_t node_t; //can probs use a 32 bit int with no performance hit
typedef double weight_t;

const weight_t INF = numeric_limits<double>::infinity();//~(0);

#endif