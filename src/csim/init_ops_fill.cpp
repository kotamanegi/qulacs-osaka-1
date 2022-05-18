#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "init_ops.hpp"
#include "utility.hpp"
#ifdef _OPENMP
#include <omp.h>
#endif

// state initialization
void initialize_quantum_state_single(CTYPE* state, ITYPE dim);
void initialize_quantum_state_parallel(CTYPE* state, ITYPE dim);
void initialize_quantum_state(CTYPE* state, ITYPE dim) {
#ifdef _OPENMP
    UINT threshold = 15;
    if (dim < (((ITYPE)1) << threshold)) {
        initialize_quantum_state_single(state, dim);
    } else {
        initialize_quantum_state_parallel(state, dim);
    }
#else
    initialize_quantum_state_single(state, dim);
#endif
}
void initialize_quantum_state_single(CTYPE* state, ITYPE dim) {
    ITYPE index;
    for (index = 0; index < dim; ++index) {
        state[index] = 0;
    }
    state[0] = 1.0;
}
#ifdef _OPENMP
void initialize_quantum_state_parallel(CTYPE* state, ITYPE dim) {
    ITYPE index;
#pragma omp parallel for
    for (index = 0; index < dim; ++index) {
        state[index] = 0;
    }
    state[0] = 1.0;
}
#endif

void reinitialize_quantum_state_single(
    CTYPE* state, ITYPE old_dim, ITYPE new_dim);
void reinitialize_quantum_state_parallel(
    CTYPE* state, ITYPE old_dim, ITYPE new_dim);
void reinitialize_quantum_state(CTYPE* state, ITYPE old_dim, ITYPE new_dim) {
#ifdef _OPENMP
    UINT threshold = 15;
    if (new_dim < (((ITYPE)1) << threshold)) {
        reinitialize_quantum_state_single(state, old_dim, new_dim);
    } else {
        reinitialize_quantum_state_parallel(state, old_dim, new_dim);
    }
#else
    reinitialize_quantum_state_single(state, old_dim, new_dim);
#endif
}

void reinitialize_quantum_state_single(
    CTYPE* state, ITYPE old_dim, ITYPE new_dim) {
    ITYPE index;
    for (index = old_dim; index < new_dim; ++index) {
        state[index] = 0;
    }
}
#ifdef _OPENMP
void reinitialize_quantum_state_parallel(
    CTYPE* state, ITYPE old_dim, ITYPE new_dim) {
    ITYPE index;
#pragma omp parallel for
    for (index = old_dim; index < new_dim; ++index) {
        state[index] = 0;
    }
}
#endif
