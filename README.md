# On the Relation of Software Configurations and Workloads: An Empirical Study of Performance

## Interactive Dashboard
We provide an interactive dashboard using `streamlit` that allows exploring in detail our analysis for each configuration option and workload. We have deployed a version on [Heroku](https://workload-performance.herokuapp.com) and provide a Docker-ized version to run the dashboard locally.

### Build & Run Docker image
```bash
cd ./dashboard
sudo docker build -t streamlitapp:latest .
docker run -p 8501:8501 streamlitapp:latest
```
You can now explore the dashboard **running locally** at [https://127.0.0.1:8501](https://127.0.0.1:8501).

### Usage
some words on how to use the dashboard


## Experiment Data
### Subject Systems 
### Configurations
### Workloads
