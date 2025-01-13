## Overview

Containerized environments are the backbone of modern cloud-native applications. However, traditional container runtimes like ‘runc‘ prioritize performance over security, leaving room for improvement in isolation and resilience against exploits. This project investigates and benchmarks alternative secure runtimes: ‘runsc‘ (gVisor) and ‘Kata Containers‘, against the widely used ‘runc‘ in a Kubernetes setting.

The project consisted a research phase, where we studied the security features of the runtimes, and a benchmarking phase, where we compared the performance of the runtimes in a Kubernetes cluster. The research phase involved reading academic papers, official documentation, and blog posts to understand the security features of the runtimes. The benchmarking phase involved setting up a Kubernetes cluster, deploying a sample application, and running performance tests to compare the runtimes.

The testing setup and related configuration files etc can be found in the repository. The results of the benchmarking tests are summarized in the report. 

## Project Structure

The project is structured as follows:
- 'research' directory contains the research phase of the project.
- 'test-setup' directory contains the testing setup and configuration files.
- 'report.pdf' contains the report summarizing the project.
- 'poster.pdf' contains the poster for the project.


