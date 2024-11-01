---
slug: 179-designing-typeahead-search-or-autocomplete
id: 179-designing-typeahead-search-or-autocomplete
layout: post
title: "设计实时联想搜索或自动完成功能"
date: 2019-10-10 18:33
comments: true
categories: 系统设计
language: cn
slides: false
abstract: 如何设计一个实时的联想自动完成服务？Linkedin 的 Cleo 库通过多层架构（浏览器缓存 / 网络层 / 结果聚合器 / 各种联想后端）和 4 个元素（倒排索引 / 正向索引，布隆过滤器，评分器）来回答这个问题。
references:
  - https://engineering.linkedin.com/open-source/cleo-open-source-technology-behind-linkedins-typeahead-search
  - http://sna-projects.com/cleo/
---

## 需求

* 为社交网络（如 Linkedin 或 Facebook）提供实时 / 低延迟的联想和自动完成功能
* 使用前缀搜索社交资料
* 新添加的账户在搜索范围内即时出现
* 不是用于“查询自动完成”（如 Google 搜索框下拉），而是用于显示实际的搜索结果，包括
    * 通用联想：来自全球排名方案（如人气）的网络无关结果。
    * 网络联想：来自用户的第一和第二度网络连接的结果，以及“你可能认识的人”评分。

![Linkedin 搜索](https://res.cloudinary.com/dohtidfqh/image/upload/v1570758247/web-guiguio/linkedin-typeahead.jpg)

## 架构

多层架构

* 浏览器缓存
* 网络层
* 结果聚合器
* 各种联想后端

![Cleo 架构](https://res.cloudinary.com/dohtidfqh/image/upload/v1570321528/web-guiguio/cleo.png)

## 结果聚合器
这个问题的抽象是通过前缀和术语在大量元素中查找文档。解决方案利用这四种主要数据结构：

1. `InvertedIndex<前缀或术语, 文档>`：给定任何前缀，找到所有包含该前缀的文档 ID。
2. `为每个文档准备一个 BloomFilter<前缀或术语>`：随着用户输入的增加，我们可以通过检查它们的布隆过滤器快速过滤掉不包含最新前缀或术语的文档。
3. `ForwardIndex<文档, 前缀或术语>`：之前的布隆过滤器可能会返回假阳性，现在我们查询实际文档以拒绝它们。
4. `scorer(文档):相关性`：每个分区返回所有真实命中及其评分。然后我们进行聚合和排名。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1570758116/web-guiguio/cleo-search-flow_0.jpg)

## 性能

* 通用联想：延迟 \< \= 1 毫秒在一个集群内
* 网络联想（第一和第二度网络的超大数据集）：延迟 \< \= 15 毫秒 
* 聚合器：延迟 \< \= 25 毫秒