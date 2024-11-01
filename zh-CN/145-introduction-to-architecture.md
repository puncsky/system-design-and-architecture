---
slug: 145-introduction-to-architecture
id: 145-introduction-to-architecture
layout: post
title: "建筑导论"
date: 2019-05-11 15:52
comments: true
categories: 系统设计
description: 建筑为软件系统的整个生命周期提供服务，使其易于理解、开发、测试、部署和操作。O’Reilly的书《软件架构模式》对五种基本架构进行了简单而有效的介绍。
references:
  - https://puncsky.com/notes/10-thinking-software-architecture-as-physical-buildings
  - https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html
  - http://www.ruanyifeng.com/blog/2016/09/software-architecture.html
---

## 什么是架构？

架构是软件系统的形状。将其视为物理建筑的全景。

* 范式是砖块。
* 设计原则是房间。
* 组件是建筑。

它们共同服务于特定的目的，例如医院是为治愈病人而设，学校是为教育学生而设。

## 我们为什么需要架构？

### 行为与结构

每个软件系统为利益相关者提供两种不同的价值：行为和结构。软件开发人员负责确保这两种价值都保持高水平。

==软件架构师由于其工作描述，更加关注系统的结构，而不是其特性和功能。==

### 终极目标 - ==每个功能节省人力资源成本==

架构为软件系统的整个生命周期提供服务，使其易于理解、开发、测试、部署和操作。目标是最小化每个业务用例的人力资源成本。

O’Reilly的书《软件架构模式》由Mark Richards撰写，是对这五种基本架构的简单而有效的介绍。

## 1. 分层架构

分层架构是最常见的架构，开发人员广泛熟知，因此是应用程序的事实标准。如果您不知道使用什么架构，请使用它。

[comment]: \<\> (https://www.draw.io/#G1ldM5O9Y62Upqg_t5rcTNHIRseP-7fqQT)

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/Software_Architecture_101.png)

示例

* TCP / IP模型：应用层 > 传输层 > 网络层 > 网络接入层
* [Facebook TAO](https://puncsky.com/notes/49-facebook-tao)：网页层 > 缓存层（跟随者 + 领导者） > 数据库层

优缺点

* 优点
    * 易于使用
    * 职责分离
    * 可测试性
* 缺点
    * 单体
        * 难以调整、扩展或更新。您必须对所有层进行更改。

## 2. 事件驱动架构

状态变化将向系统发出事件。所有组件通过事件相互通信。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-event-driven.png)

一个简单的项目可以结合中介、事件队列和通道。然后我们得到一个简化的架构：

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-event-driven-simplified.png)

示例

* QT：信号和插槽
* 支付基础设施：银行网关通常具有非常高的延迟，因此在其架构设计中采用异步技术。

## 3. 微内核架构（即插件架构）

软件的职责被划分为一个“核心”和多个“插件”。核心包含最基本的功能。插件彼此独立，并实现共享接口以实现不同的目标。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-micro-kernel.png)

示例

* Visual Studio Code，Eclipse
* MINIX操作系统

## 4. 微服务架构

一个庞大的系统被解耦为多个微服务，每个微服务都是一个单独部署的单元，它们通过[RPCs](/blog/2016-02-13-crack-the-system-design-interview#21-communication)相互通信。

![uber architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546574738/web-guiguio/uber-architecture_2.jpg)

示例

* Uber：见[设计Uber](https://puncsky.com/notes/120-designing-uber)
* Smartly

## 5. 基于空间的架构

该模式得名于“元组空间”，意为“分布式共享内存”。没有数据库或同步数据库访问，因此没有数据库瓶颈。所有处理单元在内存中共享复制的应用数据。这些处理单元可以弹性启动和关闭。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-space-based.png)

示例：见[维基百科](https://en.wikipedia.org/wiki/Tuple_space#Example_usage)

- 主要在Java用户中采用：例如，JavaSpaces