#!/bin/bash
# Run ASan experiment script
# Compile benchmarks with AddressSanitizer and run tests
# TODO: add compilation, execution, log collection

BENCHMARK_DIR="../benchmarks"
RESULT_DIR="../results"

echo "Starting ASan experiment..."
echo "Benchmark source: ${BENCHMARK_DIR}"
echo "Output results to: ${RESULT_DIR}"
