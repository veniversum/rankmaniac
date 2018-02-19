CXX=g++
CXXFLAGS=-std=gnu++11 -Ofast -fno-signed-zeros -fno-trapping-math -funroll-loops

all: pagerank_map pagerank_reduce process_map process_reduce

clean:
	rm -f pagerank_map pagerank_reduce process_map process_reduce

pagerank_map: pagerank_map.cpp
	$(CXX) $(CXXFLAGS)  pagerank_map.cpp -o pagerank_map

pagerank_reduce: pagerank_reduce.cpp
	$(CXX) $(CXXFLAGS) pagerank_reduce.cpp -o pagerank_reduce

process_map: process_map.cpp
	$(CXX) $(CXXFLAGS) process_map.cpp -o process_map

process_reduce: process_reduce.cpp
	$(CXX) $(CXXFLAGS) process_reduce.cpp -o process_reduce

