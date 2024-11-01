---
slug: 123-ios-architecture-patterns-revisited
id: 123-ios-architecture-patterns-revisited
layout: post
title: "iOS 架构模式再探"
date: 2019-01-10 02:26
comments: true
tags: [architecture, mobile, system design]
description: "架构可以直接影响每个功能的成本。让我们在三个维度上比较紧耦合 MVC、Cocoa MVC、MVP、MVVM 和 VIPER：功能参与者之间责任的平衡分配、可测试性以及易用性和可维护性。"
references:
  - https://medium.com/ios-os-x-development/ios-architecture-patterns-ecba4c38de52
---

## 为什么要关注架构？

答案：[为了降低每个功能的人力资源成本](https://puncsky.com/notes/10-thinking-software-architecture-as-physical-buildings#ultimate-goal-saving-human-resources-costs-per-feature)。

移动开发者从三个维度评估架构。

1. 功能参与者之间责任的平衡分配。
2. 可测试性
3. 易用性和可维护性


| | 责任分配 | 可测试性 |  易用性 |
| --- | ---    | ---    | --- |
| 紧耦合 MVC | ❌ | ❌ | ✅ |
| Cocoa MVC | ❌ VC 耦合 | ❌ | ✅⭐ |
| MVP | ✅ 分离的视图生命周期 | ✅ | 一般：代码较多 |
| MVVM | ✅ | 一般：由于视图依赖 UIKit | 一般 |
| VIPER | ✅⭐️ | ✅⭐️ | ❌ |



## 紧耦合 MVC

![传统 MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-0-mvc.png)

例如，在一个多页面的 web 应用中，一旦点击链接导航到其他地方，页面会完全重新加载。问题在于视图与控制器和模型紧密耦合。



## Cocoa MVC

苹果的 MVC 理论上通过控制器将视图与模型解耦。

![Cocoa MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-1-cocoa-mvc.png)


实际上，苹果的 MVC 鼓励 ==庞大的视图控制器==。而视图控制器最终负责所有事情。

![现实中的 Cocoa MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-2-realistic-cocoa-mvc.png)

测试耦合的庞大视图控制器是困难的。然而，Cocoa MVC 在开发速度方面是最佳的架构模式。



## MVP

在 MVP 中，呈现者与视图控制器的生命周期无关，视图可以轻松模拟。我们可以说 UIViewController 实际上就是视图。

![MVC 变体](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-3-mvc-variant.png)


还有另一种 MVP：带有数据绑定的 MVP。正如你所看到的，视图与其他两个之间存在紧密耦合。

![MVP](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-4-mvp.png)



## MVVM

它类似于 MVP，但绑定是在视图和视图模型之间。

![MVVM](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-5-mvvm.png)



## VIPER
与 MV(X) 相比，VIPER 有五个层次（VIPER 视图、交互器、呈现者、实体和路由）。这很好地分配了责任，但可维护性较差。

![VIPER](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-6-viper.png)


与 MV(X) 相比，VIPER

1. 模型逻辑转移到交互器，实体作为简单的数据结构保留。
2. ==与 UI 相关的业务逻辑放入呈现者，而数据修改能力放入交互器==。
3. 引入路由器负责导航。