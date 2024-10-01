# Week1: Apache Load Testing with Kubernetes and VM

## Overview

This project involves setting up an Apache web server on an Ubuntu Server running in a virtual machine (VM) and conducting load tests using Apache Benchmark (ab). We then extended our testing by deploying the server on Kubernetes using Minikube, enabling autoscaling features.

## Table of Contents

- [Prerequisites](#prerequisites)
- [System Configuration](#system-configuration)
- [Installation and Setup](#installation-and-setup)
  - [VM Setup](#vm-setup)
  - [Kubernetes Setup](#kubernetes-setup)
- [Conducting Tests](#conducting-tests)
- [Results and Analysis](#results-and-analysis)
- [Conclusion](#conclusion)

## Prerequisites

- Local machine with virtualization support
- Ubuntu Server LTS ISO image
- Minikube installed on your system
- Docker installed on your system
- Apache Benchmark (ab) tool
- Python installed on your system

## System Configuration

1. **Ensure virtualization is enabled** in your system's BIOS settings.
2. **Install necessary software**: Ensure you have Docker, Minikube, Apache Benchmark (ab), and Python installed on your system.

## Installation and Setup

### VM Setup

1. **Create a VM**:
   - Use your preferred virtualization software (e.g., UTM, VirtualBox) to create a new VM. We have used UTM for this project as 
        it is available on silicon macs.
   - Allocate sufficient resources (CPU, RAM) based on your load testing needs. We have used 4 CPUs and 4GB RAM for our VM.
   - It is better to use ssh to connect to the VM as it allows you to copy and paste material via scp. We have followed the guide [here](https://arteen.linux.ucla.edu/ssh-into-utm-vm.html) to connect to the VM using ssh. It is also possible to use port forwarding to connect to the deployed web server on the VM which is what we have done in this project.

2. **Install Ubuntu Server**:
   - Boot the VM with the Ubuntu Server ISO. We have used ARM alternative Ubuntu Server 24.04.1 LTS for our VM.
   
3. **Configure Web Server**:
   - Install Apache web server on the VM using the following commands:
     ```bash
     sudo apt update
     sudo apt install apache2
     ```
   - Start the Apache service:
     ```bash
     sudo systemctl start apache2
     ```
   - Verify the Apache service is running by visiting the VM's IP address in your browser. You can edit html files in the `/var/www/html` directory to customize the web page to ensure that the server serves the correct content.

### Kubernetes Setup

1. **Install Minikube**:
   - Follow the official Minikube [installation guide](https://minikube.sigs.k8s.io/docs/start/). We have used the Docker driver for Minikube in this project.

2. **Start Minikube**:
   ```bash
    minikube start --driver=docker
    ```
    You should also enable the metrics-server addon for the Horizontal Pod Autoscaler (HPA) to work properly:
    ```bash
    minikube addons enable metrics-server
    ```

    To allow minikube to see the docker images, you can use the following command:
    ```bash
    eval $(minikube docker-env)
    ```
    This will allow minikube to use the docker images that are built on the local machine.

    If you want to view the Kubernetes dashboard, you can enable it using the following command:
    ```bash
    minikube dashboard
    ```
    This will open the Kubernetes dashboard in your default browser.

3. **Create Dockerfile for Apache Server**:
    - We have created a file named `Dockerfile` with the following content. It will create an Apache server image using base image `httpd:2.4` and change the default content to our custom content. It also exposes port 8061. To be compatible with the service configuration it should remain 8061, otherwise you should also change the service configuration. Similarly, the docker image should be built with the same name as the one in the deployment configuration.Build the Docker image using the following command:
    ```bash
    docker build -t web-server-apache:latest .
    ```

4. ** Deploy to Kubernetes (No HPA)**:
    - Navigate to the directory containing the deployment and service configuration files under the `k8s-no-scale` directory
    ```bash
    cd k8s-no-scale
    ```
    - Apply the configurations using the following commands:
    ```bash
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```
    - You can check the status of the deployment and service using the following commands:
    ```bash
    kubectl get deployments
    kubectl get services
    ```
    - To get the IP address of the service, you can use the following command:
    ```bash
    minikube service apache-service --url
    ```
    - You can visit the IP address in your browser to verify that the Apache server is running.

5. **Set up Horizontal Pod Autoscaler (HPA)**:
    - Navigate to the directory containing the HPA configuration file under the `k8s-scale` directory
    ```bash
    cd k8s-scale
    ```
    - Apply the configuration using the following command:
    ```bash
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    kubectl apply -f hpa.yaml
    ```
    - You can check the status of the HPA using the following command:
    ```bash
    kubectl get hpa
    ```
    - You can also check the status of the deployment and service using the commands mentioned in the previous step.


## Conducting Tests

- We have conducted load tests using Apache Benchmark (ab) tool to measure the performance of the Apache server under varying loads. A typical load test command is as follows:
  ```bash
  ab -n 1000 -c 10 http://<HOST_IP>:<PORT>/
  ```
- We have used a bash script [ab_test.sh](ab_test.sh) to automate the testing process. The script takes the following parameters:
  - A list of Number of requests (n)
  - A list of Number of concurrent requests (c)
  - Host IP address
  - Port number
  - Output directory
- The script runs the load tests for all combinations of n and c values and saves the results in separate files in the output directory. Thus, you can edit the script for your specific needs and run it using the following command:
  ```bash
  ./ab_test.sh
  ```

## Results and Analysis

- We have conducted load tests on both the VM-based Apache server and the Kubernetes-deployed Apache server with HPA enabled. We have provided our test results at [here](#sample-plots-and-benchmark-results). The results include the output of the ab load tests. 
- We have also provided a Python script [analyze_results.py](analyze_results.py) to analyze the results and generate plots. The script reads the output files generated by the ab tests and generates plots for different metrics such as Requests per second, Time per request, and Failed requests. To run the script make sure you have the necessary Python libraries installed

  ```bash
  pip install numpy seaborn matplotlib
  ```
  Run the script using the following command:
  ```bash
  python plotter.py -i <RESULTS_DIRECTORY>
  ```
- The script will generate plots for each metric and save them in the same directory as the results under the `plots` directory.

### Sample Plots And Benchmark Results

- VM Apache Server Load Test Results:
  - Plots: [vm/plots](vm/plots)
  - Result Files: [vm/results](vm/results)
- Kubernetes Apache Server Load Test Results (No HPA):
    - Plots: [k8s-no-scale/plots](k8s-no-scale/plots)
    - Result Files: [k8s-no-scale/results](k8s-no-scale/results)
- Kubernetes Apache Server Load Test Results (With HPA):
    - Plots: [k8s-scale/plots](k8s-scale/plots)
    - Result Files: [k8s-scale/results](k8s-scale/results)

