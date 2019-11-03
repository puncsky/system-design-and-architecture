---
layout: post
title: "Lyft 的营销自动化平台 Symphony"
date: 2019-10-02 20:53
comments: true
categories: marketing, architecture, system design
language: zh-CN
slides: false
abstract: 广告投放如何花更少的钱用更少的人得到更高回报？Lyft 的答案是自动化，包括LTV 预测模块 、预算分配模块、投放模块。当人从繁琐的投放任务解放出来，专注于理解用户、理解渠道、理解自身要传达给受众的信息之后，就能够获得更好的投放效果
references:
  - https://eng.lyft.com/lyft-marketing-automation-b43b7b7537cc
---

## 获客效率问题：广告投放如何花更少的钱用更少的人得到更高回报？

具体来讲，Lyft 的广告投放要服务如下特点

1. 管理基于地域的 campaign
2. 数据驱动的增长：增长必须是规模化的、可测量的、可预测的
3. 支撑起 Lyft 独特的增长模型，如图：

![lyft growth model](https://res.cloudinary.com/dohtidfqh/image/upload/v1570050291/web-guiguio/1_JBgJKb6DFrG7X2Fc7dtAaQ.png)

主要的挑战是：难以规模化管理跨地域营销中的各个环节，广告竞标、预算、素材、激励、选择受众、测试等等。下图是营销者的一天：

![营销者的一天](https://res.cloudinary.com/dohtidfqh/image/upload/v1570050798/web-guiguio/0_FXK0RW9qx3e9f_kv.png)

我们可以发现“执行”占去了大部分的时间，而更少的时间花在了更重要的“分析和决策”上。规模化意味着减少繁复的操作，让营销人员专注于分析与决策。

## 解决方案：自动化

为了降低成本，提高做实验的效率，需要

1. 预测新用户是否对产品感兴趣
2. 多渠道优化，有效评估和分配预算
3. 方便地管理上千个 campaigns

数据由 Lyft 的 [Amundsen](https://guigu.io/blog/2018-12-03-making-progress-30-kilometers-per-day) 系统做增强学习。

自动化的部分包括：

1. 更新 bid 的关键词
2. 关掉效果不好的素材
3. 根据市场改变 referrals values
4. 找到高价值的用户 segment
5. 在多个 campaign 中共享策略

## 构架

![Lyft Symphony Architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1570052539/web-guiguio/0_k_I3YVF9XEAu9OLl.png)

技术栈：Apache Hive, Presto, ML platform, Airflow, 3rd-party APIs, UI.

## 具体的组成模块

### LTV 预测模块

用户的终身价值是衡量渠道的重要标准，预算由 LTV 和我们愿意为该地区的获客付出的价格共同决定。

我们对新用户的认知有限，随着交互的增多，所提供的历史记录会更准确地预测。

一开始的特征值：

![特征值](https://res.cloudinary.com/dohtidfqh/image/upload/v1570072545/web-guiguio/0_YHwm9D9a-Fvm7cq8.png)


随着历史上的交互记录的积累，做出的判断就会越准确：

![根据历史记录判断 LTV](https://res.cloudinary.com/dohtidfqh/image/upload/v1570072568/web-guiguio/0_SwHgIjhJAQf35t_C.png)


### 预算分配模块

搞定了 LTV，接下来是根据价格定预算。拟合出 `LTV = a * (spend)^b` 形式的曲线以及周围的区间里类似参数的曲线。为了找到全局最优，需要付出一些随机性的代价。

![预算计算](https://res.cloudinary.com/dohtidfqh/image/upload/v1570073827/web-guiguio/0_bLNhBPW6UFA227JB.png)


### 投放模块

分为两部分，一部分是调参者，一部分是执行者。调参者根据定价，设定基于渠道的具体的参数；执行者把这些参数执行到具体的渠道上。

有很多流行的投放策略，在各色的渠道中，是共通的：

![投放策略](https://res.cloudinary.com/dohtidfqh/image/upload/v1570074354/web-guiguio/0_bPtZels9tqGXoFCW.png)

### 总结

要注意人的经验在系统中的重要性，否则会 garbage in, garbage out. 当人从繁琐的投放任务解放出来，专注于理解用户、理解渠道、理解自身要传达给受众的信息之后，就能够获得更好的投放效果——花更少的时间达到更高的 ROI。


