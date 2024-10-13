# Week2: Kubernetes Networking and Multi-Container Application Deployment with VM and CSP

## Overview

This guide outlines the steps to set up a multi-node Kubernetes cluster using two VMs, configure networking, and deploy multi-container applications. We will also cover deploying the application to a cloud service provider (CSP) and running load tests using Locust.

## Table of Contents

- [Prerequisites](#prerequisites)
- [System Setup](#system-setup)
  - [VM Configuration](#vm-configuration)
  - [CSP Configuration](#csp-configuration)
  - [Kubernetes Setup with CRI-O](#kubernetes-setup-with-cri-o)
- [Ingress and Networking](#ingress-and-networking)
- [Horizontal Pod Autoscaler (HPA)](#horizontal-pod-autoscaler-hpa)
- [Load Testing with Locust](#load-testing-with-locust)
- [Results and Analysis](#results-and-analysis)

## Prerequisites

- Two virtual machines (VMs) with Ubuntu Server LTS.
  - **Master node**: 2 GB RAM, 2 cores.
  - **Worker node**: 4 GB RAM, 2 cores.
- A cloud service provider (CSP) account, such as DigitalOcean.
- Locust for load testing.

## VM Configuration

We have used UTM as our virtual machine manager. We have created two virtual machines, one for the master node and the other for the worker node. The master node has 2 GB of RAM and 2 cores, while the worker node has 4 GB of RAM and 2 cores. We have installed Ubuntu Server LTS on both VMs. It is important to ensure that VMs to be able to communicate with each other over the network. We have set networking type of both VMs to "Bridged" in UTM so that they can communicate with each other and with the host machine.

## CSP Configuration
We have used Digital Ocean as our cloud service provider.Digital Ocean offers a managed Kubernetes service that allows you to create a Kubernetes cluster with ease. In this section, we will be setting up a Kubernetes cluster manually. To do this we have created two droplets just like our local setup. One droplet is for the master node and the other is for the worker node. 

## Kubernetes Setup with CRI-O

### Overview
This repository provides instructions and guidelines for setting up a Kubernetes cluster using CRI-O as the container runtime. This section will guide you through the installation process on a Debian-based operating system.
The process will be same for both local and cloud setup. We will be using the same Kubernetes version for both setups. 

## Installation Guide

### Prerequisites
- A Debian-based operating system (e.g., Ubuntu)
- Sudo or root access to the machine

### Step 1: Install Dependencies
Update your system and install the necessary tools:

```bash
apt-get update
apt-get install -y software-properties-common curl
```

### Step 2: Add Kubernetes Repository
Add the Kubernetes repository and key:

```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" | tee /etc/apt/sources.list.d/kubernetes.list

```

### Step 3: Add CRI-O Repository
Add the CRI-O repository and key:

```bash
curl -fsSL https://pkgs.k8s.io/addons:/cri-o:/stable:/v1.31/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/cri-o-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/cri-o-apt-keyring.gpg] https://pkgs.k8s.io/addons:/cri-o:/stable:/v1.31/deb/ /" | tee /etc/apt/sources.list.d/cri-o.list

```

### Step 4: Install CRI-O and Kubernetes Tools
Install CRI-O, kubelet, kubeadm, and kubectl:

```bash
apt-get update
apt-get install -y cri-o kubelet kubeadm kubectl
```

### Step 5: Start CRI-O
Start the CRI-O service:

```bash
systemctl start crio.service
```

### Step 6: Bootstrap Kubernetes Cluster
Prepare your system and initialize the cluster:

1. Swap off all swap partitions:
   ```bash
   swapoff -a
   ```
2. Load the br_netfilter module:
   ```
   modprobe br_netfilter
   ```
3. Set `net.ipv4.ip_forward` to 1:
   ```bash
   sysctl -w net.ipv4.ip_forward=1
   ```

These steps should be done on both master and worker nodes.

Initialize the cluster on the master node:

```bash
kubeadm init
```

Follow the instructions to set up the cluster. Once done, you will see a message with the `kubeadm join` command to add worker nodes to the cluster.

### Step 7: Join Worker Nodes

Run the `kubeadm join` command on the worker node to join the cluster:

```bash
kubeadm join <master-node-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

Verify that the worker node has joined the cluster:

```bash
kubectl get nodes
```

### Step 8: Deploy CNI Plugin

We used Calico as the CNI plugin. Deploy Calico using the following command:

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

### Step 9: Verify Cluster Setup

Check the status of the nodes and pods:

```bash
kubectl get nodes
kubectl get pods --all-namespaces
```

### Set Up Simple Backend and Frontend Applications

We have created two simple applications, a backend and a frontend, to demonstrate multi-container deployment on Kubernetes. Both backend and frontend applications are written in Python using Flask. The backend application serves as an API that returns a JSON response, while the frontend application is a simple web page that consumes the API. Backend application has a simple HTTP GET endpoint that returns a JSON response with a random number. And frontend application has a simple web page that displays the random number returned by the backend API on each click of a button on the web page. Both applications are containerized using Docker and deployed on Kubernetes. See project files for more details.

- [backend](backend/)
- [frontend](frontend/)

#### Sending Requests to the Backend API
To send requests to the backend API, frontend application somehow get the backend API URL. We have used environment variables to pass the backend API URL to the frontend application. The frontend application reads the backend API URL from the environment variable and sends requests to the backend API. Those environment variables are set in the Kubernetes deployment configuration file. Kuberneted DNS service called CoreDNS resolves the backend API URL to the backend service IP address.

### Push Docker Images to Docker Hub
In kuberneted deployment configuration files, we have used the Docker images for the backend and frontend applications. Before deploying the applications on Kubernetes, we need to push the Docker images to a Docker registry. We have used Docker Hub as the Docker registry. Follow the steps below to push the Docker images to Docker Hub.

1. Ensure the Docker images are available for both the local Kubernetes cluster and the cloud environment.
```bash
docker tag my-image:latest <your-docker-hub-username>/my-image:latest
docker push <your-docker-hub-username>/my-image:latest
```

Alternatively, you can use the pre built images available at Docker Hub. Our docker images are available at [Docker Hub](https://hub.docker.com/repository/docker/2024cmpe492). We have listed our backend and frontend images on Docker Hub. You can pull these images from Docker Hub and deploy them on your Kubernetes cluster.


### Ingress and Networking

#### Ingress Configuration

1. **Use NodePort ingress**: Instead of using a load balancer, we will use the `NodePort` type for ingress routing. Used nginx-ingress-controller. Reconfigured its service to use NodePort.

2. **Modify /etc/hosts**:
   To route different host names to different services, modify the `/etc/hosts` file on each node in the cluster. This project uses the following entries:
   ```
   api.cmpe492.com <remote worker node ip>
   cmpe492.com <remote worker node ip>
   api.local.cmpe492.com <local worker node ip>
   local.cmpe492.com <local worker node ip>
   ```

   To connect to the services remember to use the hostname with the node port number for ingress routing. To see the node port number, use the following command:
   ```bash
   kubectl get svc -n ingress-nginx
   ```
   The output will show the node port number for the ingress controller service.

3. **Apply Ingress Configuration**:
   Apply the ingress configuration using the `kubectl apply` command. An example ingress configuration is provided in the `ingress.yaml` file under the backend and frontend directories. Apply the ingress configuration using the following command:
   ```bash
   kubectl apply -f ingress.yaml
   ```
   For the local deployment scenario, use the `ingress.local.yaml` file.


4. **Test the Ingress Configuration**:
   Use `curl` or a web browser to test the ingress configuration by accessing the services using the hostnames defined in the `/etc/hosts` file.

#### Horizontal Pod Autoscaler (HPA)

1. **Set up Metrics Server**: Enable insecure connections for the metrics server to collect resource usage data.
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/metrics-server/master/deploy/1.8+/metrics-server-deployment.yaml --enable-retries=true
      ```
2. **Deploy HPA**:
   Use `kubectl apply` to configure HPA for autoscaling based on CPU/memory metrics. An example HPA configuration is provided in the `hpa.yaml` file  under backend and frontend directories. Apply the HPA configuration using the following command:
   ```bash
   kubectl apply -f hpa.yaml
   ```


### Load Testing with Locust

#### Install Locust

Install Locust using pip:

```bash
pip install locust
```

#### Run Locust Tests

We have provided a simple locust test script in the `locustfile.py` file. Run the Locust tests using the following command:

```bash
locust -f locustfile.py --headless -u 10000 -r 10 --run-time 15m --host <host_url> --html <report_name>.html --csv <report_name>
```

Replace `<host_url>` with the URL of the application you want to test. The `-u` flag specifies the number of users, `-r` specifies the hatch rate, and `--run-time` specifies the duration of the test. The `--html` flag generates an HTML report, and the `--csv` flag generates a CSV report.

## Results and Analysis

This section will provide the results of the Locust load tests for each deployment scenario, along with HTML reports for performance metrics.

You can visit the [results](results/) directory to view the Locust HTML reports for each scenario.

