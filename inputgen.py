import os, sys, argparse
from math import sqrt
import random as r
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import utils

class Point():
	MAX_X = 100
	MAX_Y = 100
	DEC_PLACES = 5

	def __init__(self, x, y):
		self.x = round(x, Point.DEC_PLACES)
		self.y = round(y, Point.DEC_PLACES)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __str__(self):
		return "({}, {})".format(self.x, self.y)

	def __repr__(self):
		return str(self)

	def tupler(self):
		return (self.x, self.y)

	def distance(p1, p2):
		return round(sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2), Point.DEC_PLACES)

	def genPoint():
		return Point(r.uniform(0, Point.MAX_X), r.uniform(0, Point.MAX_Y))

	def generatePoints(n):
		return [Point.genPoint() for _ in range(n)]

def plotGraph():
    pos = {i:pts[i].tupler() for i in pts}
    labels = nx.get_edge_attributes(G,'weight')
    cmap = []
    for node in G:
    	if node == home:
    		cmap.append('r')
    	elif node in tas:
    		cmap.append('g')
    	else:
    		cmap.append('c')
    nx.draw_networkx_nodes(G, pos, node_color=cmap)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.savefig("imgs/" + str(args.locations) + ".png")
    plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate some inputs")
	parser.add_argument("outputfile", type=str, help="File to write toa")
	parser.add_argument("locations", type=int, help="Number of locations to make")
	parser.add_argument("TAs", type=int, help="Number of TAs to make")
	parser.add_argument("extra_edges", type=int, help="Number of extra edges to add on top of making a tree")

	args = parser.parse_args()
	if (args.TAs > args.locations):
		print("Too many TAs!!!")
		sys.exit(1)

	r.seed() # TODO allow adding a seed in arg

	pts = Point.generatePoints(args.locations)
	pts = {i:pts[i] for i in range(len(pts))} # legit just gonna name these points by their number

	G = nx.Graph()
	G.add_nodes_from(pts)

	# Ensure graph is connected
	connect_pts, unconnect_pts = set(), set(pts.keys())
	connect_pts.add(unconnect_pts.pop())
	while unconnect_pts:
		p1 = r.sample(connect_pts, 1)[0]
		p2 = r.sample(unconnect_pts, 1)[0]
		G.add_edge(p1, p2, weight=Point.distance(pts[p1], pts[p2]))
		unconnect_pts.remove(p2)
		connect_pts.add(p2)

	# Now add a bunch of extra edges
	ps = set(pts.keys())
	i = 0
	while i < args.extra_edges:
		p1, p2 = r.sample(ps, 2)
		if not G.has_edge(p1, p2):
			G.add_edge(p1, p2, weight=Point.distance(pts[p1], pts[p2]))
			i += 1

	home = r.sample(ps, 1)[0]
	tas = r.sample(ps, args.TAs)

	adj = nx.to_numpy_array(G)

	# Start writing to file
	namemap = {i:"A" + str(i) for i in pts}
	string = ""
	string += str(len(pts)) + "\n" # Number of nodes
	string += str(len(tas)) + "\n" # Number of TAs

	for n in pts: # Add names of each node
		string += namemap[n] + " "
	string = string[:-1] + "\n" # Get rid of extra char space

	for t in tas: # Add TAs names
		string += namemap[t] + " "
	string = string[:-1] + "\n"

	string += namemap[home] + "\n" # Add home

	for row in adj: # Add adjacency matrix
		for elem in row:
			if elem == 0:
				string += 'x '
			else:
				string += str(elem) + " "
		string = string[:-1] + "\n"
	string = string[:-1]

	utils.write_to_file(args.outputfile, string)

	plotGraph() # TODO remove this if gonna run on some remote server




