# Homework 5

## Installation

First, cd into the desired location to clone the repository.

Second, clone and update the repo with the address below onto the local ISP.
```gitexclude
git clone https://github.com/vulong2505/COE-332.git
```
Navigate to the homework5 folder for the relevant scripts.

## Part A

1. Include the yaml file used and the command issued to create the pod.
```
kubectl apply -f homework5_A.yml
```

2. Issue a command to get the pod using an appropriate selector. Copy and paste the command used and the output.
```
kubectl get pods --selector "greeting=personalized"
```

3. Check the logs of the pod. What is the output? Is that what you expected?
```
# Command
kubectl logs vulong25-hello-a

# Output
Hello,
```
* This is what I expected as I haven't given the environmental variable NAME a value.

4. Delete the pod. What command did you use?
```
kubectl delete pods vulong25-hello-a
```

## Part B

1. Include the yaml file used and the command issued to create the pod.
```
kubectl apply -f homework5_B.yml
```

2. Check the logs of the pod. What is the output? Copy and paste the command used and the output.
```
# Command
kubectl logs vulong25-hello-b

# Output 
Hello, Long
```

3. Delete the pod. What command did you use?
```
kubectl delete pods vulong25-hello-b
```

## Part C

1. Include the yaml file used to create a deployment with 3 replica pods, and include the command issued to create the deployment.
```
kubectl apply -f homework5_C.yml
```

2. First, use kubectl to get all the pods in the deployment and their IP address. Copy and paste the command used and the output.
```
# Command
kubectl get pods

# Output
NAME                                        READY   STATUS    RESTARTS   AGE
vulong25-hello-deployment-949c866ff-ppbkp   1/1     Running   0          4m49s
vulong25-hello-deployment-949c866ff-qj78v   1/1     Running   0          4m49s
vulong25-hello-deployment-949c866ff-rxz9g   1/1     Running   0          4m49s
```

3. Now, check the logs associated with each pod in the deployment. Does it match what you got in 2? Copy and paste the commands and the output.
```
# Pod 1
[...] $ kubectl logs vulong25-hello-deployment-949c866ff-ppbkp
Hello, Long from IP 10.244.4.153

# Pod 2
[...] $ kubectl logs vulong25-hello-deployment-949c866ff-qj78v
Hello, Long from IP 10.244.7.152

# Pod 3
[...] $ kubectl logs vulong25-hello-deployment-949c866ff-rxz9g
Hello, Long from IP 10.244.10.18
```
* The IPs differ between each pod. 