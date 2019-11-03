---
layout: post
title: "构架入门"
date: 2019-06-11 22:06
comments: true
categories: architecture, system design
language: zh-CN
abstract: 架构服务于软件系统的整个生命周期，使软件系统易于理解，开发，测试，部署和操作，其目标是最小化每个业务用例的人力资源成本。O’Reilly出版的《软件架构》介绍了五种基本架构：分层架构；事件驱动架构；微核架构；微服务架构；基于空间的架构。
references:
  - https://puncsky.com/notes/10-thinking-software-architecture-as-physical-buildings
  - https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html
  - http://www.ruanyifeng.com/blog/2016/09/software-architecture.html
---

## 什么是构架

构架是软件系统的形状。拿建筑物来举例子：

* 范式 paradigm 是砖块
* 设计原则是房间
* 组件是建筑

他们共同服务于一个特定的目的，就像医院治疗病人，学校教育学生一样。

## 我们为什么需要架构？

### 行为 vs. 结构

每一个软件系统提供两个不同的价值给利益相关者：行为与结构。软件开发者必须确保这两项价值都要高

==由于其工作的需要，软件架构师更多地聚焦于系统的结构而不是特性和功能。==

### 终极目标——==减少每加一个新特性所需要耗费的人力成本==

架构服务于软件系统的整个生命周期，使其易于理解，开发，测试，部署和操作。
其目标是最小化每个业务用例的人力资源成本。



O’Reilly 出版的《软件架构》一书很好地介绍了这样五种基本的构架。



## 1.分层架构



分层架构是被广泛采用，也是被开发者所熟知的一种架构。因此，它也是应用层面上事实上的标准。如果你不知道应该使用什么架构，用分层架构就是不错的选择。
![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/Software_Architecture_101.png)


示例

* TCP/IP模式：应用层 > 运输层 >  网际层 > 网络接口层
* [Facebook TAO](https://puncsky.com/notes/49-facebook-tao)网络层 > 缓存层(follower + leader) > 数据库层

优缺点：

* 优点
  * 易于使用
  * 职责划分
  * 可测试性
* 缺点
  * 庞大而僵化
    * 想要对架构进行调整、扩展或者更新就必须要改变所有层，十分棘手



## 2.事件驱动架构



任何一个状态的改变都会向系统发出一个事件。系统组件之间的通信都是经由事件完成的。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-event-driven.png)

一个简化的架构包含中介(mdiator)，事件队列(event queue)和通道(channel)。下图所示即为简化的事件驱动架构：

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-event-driven-simplified.png)

示例

* QT：信号(signals)和槽(slots)
* 支付基础设施：由于银行网关通常有较高的延迟，因此银行的架构中采用了异步技术



## 3.微核架构(aka Plug-in Architecture)



软件的功能被分散到一个核心和多个插件中。核心仅仅含有最基本的功能。各个插件之间互相独立并实现共享借口以实现不同的目标。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-micro-kernel.png)


示例

* Visual Studio Code 和 Eclipse
* MINIX 操作系统



## 4.微服务架构



大型系统被解离成众多微服务，每一个都是单独部署的单位，他们之间通过[RPCs](/blog/2016-02-13-crack-the-system-design-interview#21-communication)进行通信。

![uber architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546574738/web-guiguio/uber-architecture_2.jpg)



示例

* Uber: 详情查看 [designing Uber](https://puncsky.com/notes/120-designing-uber)
* Smartly



## 5.基于空间的架构



“基于空间的架构”这一名称来源于“元组空间”，“元组空间“有”分布式共享空间“的含义。基于空间的架构中没有数据库或同步数据库访问，因此该架构没有数据库的瓶颈问题。所有处理单元共享内存中应用数据副本。这些处理单元都可以很弹性地启动和关闭。

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-space-based.png)


示例：详见 [Wikipedia](https://en.wikipedia.org/wiki/Tuple_space#Example_usage)

- 主要被使用Java的架构所采用：例如：JavaSpaces
