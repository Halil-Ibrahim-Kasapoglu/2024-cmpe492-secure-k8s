#!/bin/bash

# Check if user has permission to get pods in the rbac-demo namespace
echo "Checking if user '492user-reader' has read-only access to pods in the 'rbac-demo' namespace..."
kubectl auth can-i get pods --as=492user-reader -n rbac-demo

# Check if user has permission to create pods in the rbac-demo namespace
echo "Checking if user '492user-reader' has permission to create new pods in the 'rbac-demo' namespace..."
kubectl auth can-i create pods --as=492user-reader -n rbac-demo

