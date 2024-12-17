---
slug: 136-fraud-detection-with-semi-supervised-learning
id: 136-fraud-detection-with-semi-supervised-learning
title: "Fraud Detection with Semi-supervised Learning"
date: 2019-02-13 23:57
comments: true
tags: [architecture, system design]
description: Fraud Detection fights against account takeovers and Botnet attacks during login. Semi-supervised learning has better learning accuracy than unsupervised learning and less time and costs than supervised learning.
references:
  - https://www.slideshare.net/Hadoop_Summit/semisupervised-learning-in-an-adversarial-environment
image: https://web-dash-v2.onrender.com/api/og-tianpan-co?title=Fraud%20Detection%20with%20Semi-supervised%20Learning

---

![](https://web-dash-v2.onrender.com/api/og-tianpan-co?title=Fraud%20Detection%20with%20Semi-supervised%20Learning)

## Clarify Requirements

Calculate risk probability scores in realtime and make decisions along with a rule engine to prevent ATO (account takeovers) and Botnet attacks.

Train clustering fatures with online and offline pipelines

1. Source from website logs, auth logs, user actions, transactions, high-risk accounts in watch list
2. track event data in kakfa topics
3. Process events and prepare clustering features

Realtime scoring and rule-based decision

4. assess a risk score comprehensively for online services

5. Maintain flexibility with manually configuration in a rule engine
6. share, or use the insights in online services

ATOs ranking from easy to hard to detect

1. from single IP
2. from IPs on the same device 
3. from IPs across the world
4. from 100k IPs
5. attacks on specific accounts
6. phishing and malware

Challenges

* Manual feature selection
* Feature evolution in adversarial environment
* Scalability
* No online DBSCAN

## **High-level Architecture**

![](https://tp-misc.b-cdn.net/SDA/136-fraud-detection-with-semi-supervised-learning-1.png)

## Core Components and Workflows

Semi-supervised learning = unlabeled data + small amount of labeled data 

Why? better learning accuracy than unsupervised learning + less time and costs than supervised learning

### Training: To prepare clustering features in database

- **Streaming Pipeline on Spark:**
  - Runs continuously in real-time.
  - Performs feature normalization and categorical transformation on the fly.
    - **Feature Normalization**: Scale your numeric features (e.g., age, income) so that they are between 0 and 1.
    - **Categorical Feature Transformation**: Apply one-hot encoding or another transformation to convert categorical features into a numeric format suitable for the machine learning model.
  - Uses **Spark MLlib’s K-means** to cluster streaming data into groups.
    - After running k-means and forming clusters, you might find that certain clusters have more instances of fraud.
    - Once you’ve labeled a cluster as fraudulent based on historical data or expert knowledge, you can use that cluster assignment during inference. Any new data point assigned to that fraudulent cluster can be flagged as suspicious.
- **Hourly Cronjob Pipeline:**
  - Runs periodically every hour (batch processing).
  - Applies **thresholding** to identify anomalies based on results from the clustering model.
  - **Tunes parameters** of the **DBSCAN algorithm** to improve clustering and anomaly detection.
  - Uses **DBSCAN** from **scikit-learn** to find clusters and detect outliers in batch data.
    - DBSCAN, which can detect outliers, might identify clusters of regular transactions and separate them from **noise**, which could be unusual, potentially fraudulent transactions.
    - Transactions in the noisy or outlier regions (points that don’t belong to any dense cluster) can be flagged as suspicious.
    - After identifying a cluster as fraudulent, DBSCAN helps detect patterns of fraud even in irregularly shaped transaction distributions.

## Serving

The serving layer is where the rubber meets the road - where we turn our machine learning models and business rules into actual fraud prevention decisions. Here's how it works:

- Fraud Detection Scoring Service:
  - Takes real-time features extracted from incoming requests
  - Applies both clustering models (K-means from streaming and DBSCAN from batch)
  - Combines scores with streaming counters (like login attempts per IP)
  - Outputs a unified risk score between 0 and 1
- Rule Engine:
  - Acts as the "brain" of the system
  - Combines ML scores with configurable business rules
  - Examples of rules:
    - If risk score > 0.8 AND user is accessing from new IP → require 2FA
    - If risk score > 0.9 AND account is high-value → block transaction
  - Rules are stored in a database and can be updated without code changes
  - Provides an admin portal for security teams to adjust rules
- Integration with Other Services:
  - Exposes REST APIs for real-time scoring
  - Publishes results to streaming counters for monitoring
  - Feeds decisions back to the training pipeline to improve model accuracy
- Observability:
  - Tracks key metrics like false positive/negative rates
  - Monitors model drift and feature distribution changes
  - Provides dashboards for security analysts to investigate patterns
  - Logs detailed information for post-incident analysis

