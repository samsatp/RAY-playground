# Objectives
- Hands-on practice with distributed ML pipelines.
- Learn how to use Ray


# Setup
- Use containers to mimic a distributed system: 1 master node + 2 workers + 1 client container


# Plan

### Setting up
- [x] master node can connect to worker nodes
- [x] client container can connect to master node and execute something in parallel

### Ray Data
- [ ] write a script to download data from [Kaggle](https://www.kaggle.com/datasets/gorororororo23/european-restaurant-reviews) and save to local.
- [ ] write a data processing script.
    -   We'll do sentiment classification of restaurant reviews
    -   For each worker, read the data (which is in .CSV) and return a list of (review, sentiment) tuples
- [ ] (POC) let workers perform data processing in parallel and measure that it's faster than doing it in one job.
- [ ] modify the script to download the data and save to MinIO.
- [ ] (POC) do the same POC, but this time access data from MinIO
- [ ] transform data and save back to MinIO 

### Ray Traing