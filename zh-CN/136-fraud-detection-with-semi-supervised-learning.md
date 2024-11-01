---
slug: 136-fraud-detection-with-semi-supervised-learning
id: 136-fraud-detection-with-semi-supervised-learning
title: "使用半监督学习进行欺诈检测"
date: 2019-02-13 23:57
comments: true
tags: [architecture, system design]
description: 欺诈检测旨在防止登录时的账户接管和僵尸网络攻击。半监督学习的学习准确性优于无监督学习，并且所需时间和成本低于监督学习。
references:
  - https://www.slideshare.net/Hadoop_Summit/semisupervised-learning-in-an-adversarial-environment
---

## 动机

在用户登录时利用用户和设备数据进行斗争

1. ATO（账户接管）
2. 僵尸网络攻击

ATO的检测难度从易到难

1. 单个IP
2. 同一设备上的IP
3. 全球范围内的IP
4. 10万个IP
5. 针对特定账户的攻击
6. 网络钓鱼和恶意软件

## 解决方案

半监督学习 = 无标签数据 + 少量有标签数据

为什么？学习准确性优于无监督学习 + 所需时间和成本低于监督学习

* K均值：效果不佳
* DBSCAN：效果更好。使用标签来
	1. 调整超参数
	2. 约束

挑战

* 手动特征选择
* 对抗环境中的特征演变
* 可扩展性
* 无在线DBSCAN

架构

![反欺诈查询]( https://res.cloudinary.com/dohtidfqh/image/upload/v1550134196/web-guiguio/anti-fraud-query.png )

![反欺诈特征]( https://res.cloudinary.com/dohtidfqh/image/upload/v1550134196/web-guiguio/anti-fraud-feature.png )

# 生产设置
* 批处理：7天的数据，每小时运行一次DBSCAN
* 流处理：60分钟的移动窗口，运行流式K均值
* 使用反馈信号成功率将聚类标记为好、坏或未知
* 坏聚类：始终丢弃
* 好聚类：小比例的尝试
* 未知聚类：X%的尝试