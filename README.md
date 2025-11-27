# Flask + MongoDB on Kubernetes

A beginner-friendly project demonstrating:

* Python Flask API
* MongoDB with authentication
* Docker containerization
* Kubernetes Deployments, StatefulSets, PV/PVC
* Horizontal Pod Autoscaler (HPA)
* DNS-based service discovery
* Resource requests & limits
* Local cluster using Minikube

---

## Project Overview

This project deploys a **Flask REST API** connected to **MongoDB** inside a **Kubernetes cluster**.

### API Endpoints:

* **GET /** → Return greeting + server time
* **GET /data** → Return all MongoDB documents
* **POST /data** → Insert JSON into MongoDB

### Deployment Features:

* Flask API deployed as a **Deployment** with autoscaling
* MongoDB deployed as a **StatefulSet** with persistent storage
* Secret-based authentication
* Services for internal/external access
* Autoscaling based on CPU metrics

This setup mirrors what you would use in a real microservices environment.

---

## 📂 Folder Structure

```
flask-mongodb-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
├── k8s/
│   ├── namespace.yaml
│   ├── mongodb-secret.yaml
│   ├── mongodb-storage.yaml
│   ├── mongodb-service.yaml
│   ├── mongodb-statefulset.yaml
│   ├── flask-deployment-service.yaml
│   └── flask-hpa.yaml
```

---

## 1. Prerequisites

Install:

* Docker
  [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
* kubectl
  [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)
* Minikube
  [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)

Check versions:

```bash
docker --version
kubectl version --client
minikube version
```

---

## 2. Run the Application Locally

### Create & activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Start MongoDB using Docker:

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Run Flask:

```bash
export FLASK_APP=app.py
flask run
```

### Test Endpoints:

```bash
curl http://localhost:5000/
curl http://localhost:5000/data
```

POST sample:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"hello": "world"}' \
     http://localhost:5000/data
```

---

## 3. Build & Push Docker Image

Replace `<your-docker-username>` below.

### Build:

```bash
docker build -t flask-mongodb-app:latest .
```

### Tag:

```bash
docker tag flask-mongodb-app:latest <your-docker-username>/flask-mongodb-app:latest
```

### Push:

```bash
docker push <your-docker-username>/flask-mongodb-app:latest
```

---

## 4. Start Minikube

```bash
minikube start
minikube addons enable metrics-server
```

---

## 5. Deploy Kubernetes Resources

### Apply everything:

```bash
kubectl apply -f k8s/
```

### Or apply step-by-step:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/mongodb-secret.yaml
kubectl apply -f k8s/mongodb-storage.yaml
kubectl apply -f k8s/mongodb-service.yaml
kubectl apply -f k8s/mongodb-statefulset.yaml
kubectl apply -f k8s/flask-deployment-service.yaml
kubectl apply -f k8s/flask-hpa.yaml
```

---

## 6. Access the Flask App

Use Minikube to open the service:

```bash
minikube service flask-app-service -n flask-mongo-namespace
```

You will get a URL like:

```
http://127.0.0.1:31234
```

Test:

```bash
curl http://127.0.0.1:31234/
curl http://127.0.0.1:31234/data
```

---

## 7. Kubernetes Concepts Used

* ### Deployment (Flask)

Manages stateless Pods with scaling.

* ### StatefulSet (MongoDB)

Stable network IDs + persistent storage.

* ### Service

Provides DNS names for Pods:

* `flask-app-service` → NodePort (external access)
* `mongodb-service` → ClusterIP (internal only)

### PersistentVolume + PVC

MongoDB data survives restarts.

* ### Secrets

Stores database credentials securely.

* ### Horizontal Pod Autoscaler (HPA)

Scales Flask replicas between **2–5** based on CPU usage.

---

## 8. DNS Resolution Explained

Inside Kubernetes, services are accessible via DNS:

```
mongodb-service.flask-mongo-namespace.svc.cluster.local
```

Flask connects with:

```
MONGO_HOST=mongodb-service
```

Pods in the same namespace can simply use the **service name**.

---

## 9. Resource Requests & Limits

```yaml
resources:
  requests:
    cpu: "0.2"
    memory: "250Mi"
  limits:
    cpu: "0.5"
    memory: "500Mi"
```

### Why?

* **Requests** guarantee minimum resources
* **Limits** prevent runaway usage
* HPA measures CPU relative to requests

---

## 10. Test Autoscaling

Generate load:

```bash
for i in {1..10000}; do curl -s http://127.0.0.1:<NODEPORT>/ > /dev/null & done
```

Watch HPA:

```bash
kubectl get hpa -w -n flask-mongo-namespace
```

Watch replicas:

```bash
kubectl get deploy -w -n flask-mongo-namespace
```

### Expected Behavior:

* CPU ↑ → replicas increase (max 5)
* CPU ↓ → replicas decrease (min 2)

---

## 11. Design Choices (Interview-Ready)

* **StatefulSet** for MongoDB → stable hostnames & storage
* **Secrets** for credentials → no hardcoding
* **ClusterIP** for MongoDB → internal-only access
* **NodePort** for Flask → reachable via Minikube
* **Separate YAML files** → clean & maintainable
* **HPA on CPU** → simple and metrics-server supported

---

## 12. Cleanup

Stop & delete Minikube:

```bash
minikube stop
minikube delete
```

Remove local MongoDB container:

```bash
docker stop mongodb
docker rm mongodb
```

---

## Done!

You now have a fully working **Flask + MongoDB + Kubernetes** project with:

* Docker image
* Secret-based MongoDB authentication
* Autoscaling
* Persistent storage
* Clean YAML structure
* Fully functional local Kubernetes cluster
