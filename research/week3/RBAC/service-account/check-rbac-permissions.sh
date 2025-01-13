echo "Checking if 'pod-reader-sa' has permission to get pods in the 'rbac-demo' namespace..."
kubectl auth can-i get pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo

echo "Checking if 'pod-reader-sa' has permission to create pods in the 'rbac-demo' namespace..."
kubectl auth can-i create pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo

