---
layout: post
title: "Fraud Detection with Semi-supervised Learning"
date: 2019-02-13 23:57
comments: true
categories: architecture
language: en
abstract: Fraud Detection fights against account takeovers and Botnet attacks during login. Semi-supervised learning has better learning accuracy than unsupervised learning and less time and costs than supervised learning.
references:
  - https://www.slideshare.net/Hadoop_Summit/semisupervised-learning-in-an-adversarial-environment
---

## Motivation

Leveraging user and device data during user login to fight against

1. ATO (account takeovers)
2. Botnet attacks



ATOs ranking from easy to hard to detect

1. from single IP
2. from IPs on the same device 
3. from IPs across the world
4. from 100k IPs
5. attacks on specific accounts
6. phishing and malware



## Solutions

Semi-supervised learning = unlabeled data + small amount of labeled data 

Why? better learning accuracy than unsupervised learning + less time and costs than supervised learning

* K-means: not good
* DBSCAN: better. Use labels to
	1. Tune hyperparameter
	2. Constrain


Challenges

* Manual feature selection
* Feature evolution in adversarial environment
* Scalability
* No online DBSCAN


Architecture

![Anti-fraud Query]( https://res.cloudinary.com/dohtidfqh/image/upload/v1550134196/web-guiguio/anti-fraud-query.png )


![Anti-fraud Featuring]( https://res.cloudinary.com/dohtidfqh/image/upload/v1550134196/web-guiguio/anti-fraud-feature.png )



# Production Setup
* Batch: 7 days worth of data, run DBSCAN hourly 
* Streaming: 60 minutes moving window, run streaming k-means 
* Used feedback signal success ratios to mark clusters as good, bad or unknown 
* Bad clusters: Always throw 
* Good clusters: Small % of attempts 
* Unknown clusters: X% of attempts 

