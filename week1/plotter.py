import os
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse Apache benchmark results.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Directory containing the result files')
    return parser.parse_args()

# Parse command-line arguments
args = parse_arguments()
RESULT_DIR = args.input

# Create a directory for plots
PLOT_DIR = os.path.join(RESULT_DIR, 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

# Initialize a dictionary to store the parsed results
data = {
    'requests_per_second': {},
    'failed_requests': {},
    'time_per_request': {},
    'longest_request': {},
    'longest_95_request': {}
}

# Regex pattern to extract n and c values from the filename
filename_pattern = re.compile(r"result_n(\d+)_c(\d+)\.txt")

# Regex patterns to extract metrics from the file content
requests_per_second_pattern = re.compile(r"Requests per second:\s+([\d\.]+)")
failed_requests_pattern = re.compile(r"Failed requests:\s+(\d+)")
time_per_request_pattern = re.compile(r"Time per request:\s+([\d\.]+) \[ms\]")
longest_request_pattern = re.compile(r"100%\s+(\d+)")
longest_95_request_pattern = re.compile(r"95%\s+(\d+)")

# Loop through each result file
for filename in os.listdir(RESULT_DIR):
    # Match the filename to extract n and c values
    match = filename_pattern.match(filename)
    if match:
        n_val = int(match.group(1))
        c_val = int(match.group(2))
        
        # Open the file and read the content
        with open(os.path.join(RESULT_DIR, filename), 'r') as file:
            content = file.read()
            
            # Extract each metric using regex
            rps_match = requests_per_second_pattern.search(content)
            failed_requests_match = failed_requests_pattern.search(content)
            time_per_request_match = time_per_request_pattern.search(content)
            longest_request_match = longest_request_pattern.search(content)
            longest_95_request_match = longest_95_request_pattern.search(content)
            
            # Store the values in nested dictionaries
            if rps_match:
                requests_per_second = float(rps_match.group(1))
                if n_val not in data['requests_per_second']:
                    data['requests_per_second'][n_val] = {}
                data['requests_per_second'][n_val][c_val] = requests_per_second
            
            if failed_requests_match:
                failed_requests = int(failed_requests_match.group(1))
                if n_val not in data['failed_requests']:
                    data['failed_requests'][n_val] = {}
                data['failed_requests'][n_val][c_val] = failed_requests
            
            if time_per_request_match:
                time_per_request = float(time_per_request_match.group(1))
                if n_val not in data['time_per_request']:
                    data['time_per_request'][n_val] = {}
                data['time_per_request'][n_val][c_val] = time_per_request
            
            if longest_request_match:
                longest_request = int(longest_request_match.group(1))
                if n_val not in data['longest_request']:
                    data['longest_request'][n_val] = {}
                data['longest_request'][n_val][c_val] = longest_request

            if longest_95_request_match:
                longest_95_request = int(longest_95_request_match.group(1))
                if n_val not in data['longest_95_request']:
                    data['longest_95_request'][n_val] = {}
                data['longest_95_request'][n_val][c_val] = longest_95_request

# Create a sorted list of unique n and c values
n_values = sorted(data['requests_per_second'].keys())
c_values = sorted({c for n in data['requests_per_second'] for c in data['requests_per_second'][n].keys()})

# Function to plot heatmap
def plot_heatmap(metric_data, metric_name, x_labels, y_labels):
    # Create an empty matrix to store the heatmap data
    heatmap_matrix = np.zeros((len(y_labels), len(x_labels)))

    # Fill the matrix with the parsed data
    for i, n in enumerate(y_labels):
        for j, c in enumerate(x_labels):
            heatmap_matrix[i, j] = metric_data.get(n, {}).get(c, 0)  # Get the value or 0 if not found

    # Plot the heatmap using seaborn
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_matrix, annot=True, fmt=".1f", cmap="coolwarm", 
                xticklabels=x_labels, yticklabels=y_labels, linewidths=.5)
    plt.title(f"{metric_name} Heatmap")
    plt.xlabel("Concurrency Level (c)")
    plt.ylabel("Number of Requests (n)")

    # Save the figure
    plt.savefig(os.path.join(PLOT_DIR, f"{metric_name.replace(' ', '_').lower()}.png"))
    plt.close()  # Close the figure to free up memory

# Plot heatmaps for each metric
plot_heatmap(data['requests_per_second'], "Requests per Second", c_values, n_values)
plot_heatmap(data['failed_requests'], "Failed Requests", c_values, n_values)
plot_heatmap(data['time_per_request'], "Time per Request (ms)", c_values, n_values)
plot_heatmap(data['longest_request'], "100% Longest Request (ms)", c_values, n_values)
plot_heatmap(data['longest_95_request'], "95% Longest Request (ms)", c_values, n_values)

print("All plots saved in the 'plots' directory.")
