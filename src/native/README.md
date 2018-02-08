# Algorithm

The algorithm implemented draws inspiration from Eager Pagerank approach outlined in [these](https://www.cs.purdue.edu/homes/suresh/papers/eagermap09.pdf) [papers](https://www.cs.purdue.edu/homes/suresh/papers/cluster10.pdf).
The approach relaxes the requirement of global synchronization in traditional iterative MapReduce implementation, noting that:
>The fundamental observation here is that it takes fewer iterations to converge for a graph having already converged sub-graphs. The trends are more pronounced when the graph follows the power-law distribution more closely. '

This observation allows to use the Gauss-Seidel iteration method for finding convergence, which required total ordering of update operations (and knowing the entire adjacency matrix) that are infeasible for distributed computation using MapReduce.
By relaxing the sychronization constraint, we only need to enforce a partial ordering of update operations on the nodes in the subgraph within a each reducer node, which is partitioned such that each MapReduce runner can easily handle the computation required.
Edge cases where cross subgraph boundaries are handled in the same manner as the traditional iteration method. While performance gain is most significant if using a min-cut partitioning (or natural partitioning from web crawler behavior), there is still a significant improvement in the number of iterations required till convergence when partitions are selected randomly.
The convergence behaviour is that of Gauss-Seidel when there is only 1 reducer, and degrades to Jacobian iteration as number of reducers approaches the number of nodes in the graph. Thus, our implementation should converge in strictly less iteration that naive Jacobian iteration approaches.

The details of the Gauss-Seidel method is described in [this paper](http://www.w3c.ethz.ch/CDstore/www2002/poster/173.pdf).


It is crucial that an appropriate number of nodes be chosen such that the graph fits on disk (hard requirement) and more preferably in memory (soft requirement).
The paper highlights the tradeoff between a reduced communication overhead, and the extra work in terms of CPU ops due to partial synchronization.

>The time to solution depends strongly on the number of iterations but is not completely determined by it. It is true that the global synchronization costs would decrease, but when we reduce the number of partitions significantly, the work done by each map task increases. This increase potentially results in increased cost of computation; more than the benefit from reduced communication/synchronizations. Consequently, there is an optimal number of partitions for every application on a given platform

Empirically, we determined that for our test cases (largest digraph tested with >2mil nodes and >5mil edges), the optimal number of partitions is very small. It would seem that the overhead in the MapReduce approach only justifies it's use for __LARGE__ graphs. The tradeoff might make sense if you're Google back in the days and the MapReduce job lasts a week, but for small (<100mil) cases the overhead dominates the actual computation of the problem. 


# Build

Makefile provided.
Use gcc/g++ version 4.8.4 targeting 64-bit little endian Linux 2.6 for both cython and cpp builds.
Ensure for cython builds that cython is not compiled with the `--with-fpectl` flag since cython on the 3.11.0 AMI on EMR isn't compiled with it.

# Optimizations

- Original python implementation using iteration -- 5 hours with 0 inaccuracy
- Add early stopping on some conditions -- 1.5 hours with ~0 inaccuracy
	- Top `k` rankings is stable for last `t` iterations, or
	- Total change in PageRank is less than `EPSILON * num nodes`
- Cythonize python code
	- Naive compilation of .py -> .c -> binary actually _increases_ runtime!
		- Overhead of typechecks, casting, etc in cython
		- Can generate annotated compiled output using `-a` flag.
	- Use annotated compilation output to optimize code
		- Compilation path .pyx -> .c -> binary
		- cdef classes
		- Add early type bindings
		- use native C libraries for IO, etc
	- ~20-30% performance increase over python implementation
		- horrible frankencode of half C / half python with syntax of both
- C++ rewrite
	- Only uses std libraries, no need for LD of boost.
	- Disable c++ stream synchronization for more speed
		- Can't read stdin from files anymore (need to disable for debugging)!
		- Significant speed boost
	- Use C printf instead of streams for output
		- iostream is __SLOW__
		- slightly messier code
		- tried using unsafe gets/puts which is faster but even messier, so reverted.
	- Optimization of IO / serialization
		- 10 significant figures necessary & sufficient to preserve exact value of 64-bit floating point.
		- coalese emits in map ('local' reduce to aggregate emits with same key)
		- process_map is no-op, just reemits whatever the input is
			- read from stdin -> write to stdout is slow
			- use syscalls `sendfile` and `splice` instead which are zero-copy depending on kernel implementations.
				- memory pages are just remapped
				- still slower than /bin/cat
	- Partial sort for process reduce
		- ~O(N log k) runtime, k is constant tunable variable.
		- Might be faster to use introselect (possible optimization)?
	- Compilation flags
		- `-Ofast` is used which enables some non standard optimizations.
		- `-fno-signed-zeros -fno-trapping-math` even more non standard conforming stuff.
		- `-funroll-loops` increases speed at the expense of larger file size.
			- implicitly enables `frename-registers`
		- `-march=native` compile using CPU architecture specific instructions
			- __UNSAFE__! Spin up own EMR cluster with just single master instance running 3.11.0 AMI to compile using this flag
			- Costs $0.10 per compilation since m1.medium is cheapest supported instance type

# Tunable parameters

- pagerank_map
	- `EPSILON`: Convergence criteria for local MR
	- `MAX_LOCAL_ITERS`: Secondary convergence criteria for local MR
- process_reduce
	- `STRICTNESS`: Top number of ranks to check stability for
	- `PATIENCE`: Early stop after stability of top ranks achieved for this number of rounds
	- `EPSILON`: Secondary convergence criteria for global MR
- config
	- `num_mappers`: Number of mappers. Mapper step should take much longer than setup time for mapper.
	- `num_reducers`: Number of reducers. At most 0.9 * 2 * number of nodes. Ideally ~0.75x `num_mappers`