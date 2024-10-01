#!/bin/bash

PORT=60199              # Define the port number
HOST="127.0.0.1"        # Define the host IP address
OUTPUT_DIR="."          # Define the output directory

# Define the ranges for C and N
C_values=(1 2 4 8 16 32 64 128)
N_values=(2048 4096 8192 16384 32768 65536 131072)

# Loop through each combination of C and N
for C in "${C_values[@]}"; do
  for N in "${N_values[@]}"; do
    # Define the output filename using the current C and N values
    output_file="result_n${N}_c${C}.txt"

    # Run the Apache Benchmark command and redirect the output to the file
    echo "Running test with n=${N} and c=${C} on port ${PORT}..."
    ab -k -n "${N}" -c "${C}" -r "http://${HOST}:${PORT}/" > "${OUTPUT_DIR}/${output_file}"

    echo "Results saved in ${output_file}"

    # Sleep for a specified duration (e.g., 1 seconds) between tests
    # This is to ensure that the server has time to recover between testss
    sleep 1
  done
done

echo "All tests completed!"
