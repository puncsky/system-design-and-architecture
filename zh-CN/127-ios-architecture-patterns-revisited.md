---
layout: post
title: "再窥iOS架构模式"
date: 2019-01-17 03:07
comments: true
categories: architecture, mobile, system design
language: zh-cn
references:
  - https://medium.com/ios-os-x-development/ios-architecture-patterns-ecba4c38de52
---

## 我们为什么要在架构上费心思？

答案是：[为了减少在每做一个功能的时候所耗费的人力资源](https://puncsky.com/notes/10-thinking-software-architecture-as-physical-buildings#ultimate-goal-saving-human-resources-costs-per-feature)。

移动开发人员会在以下三个层面上评估一个架构的好坏：

1. 各个功能分区的职责分配是否均衡
2. 是否具有易测试性
3. 是否易于使用和维护


| | 职责分配的均衡性 | 易测试性 | 易用性 |
| --- | --- | --- | --- |
| 紧耦合MVC | ❌ | ❌ | ✅ |
| Cocoa MVC | ❌ V和C是耦合的 | ❌ | ✅⭐ |
| MVP | ✅ 独立的视图生命周期 | ✅ | 一般：代码较多 |
| MVVM | ✅ | 一般：视图（View）存在对UIKit的依赖 | 一般 |
| VIPER | ✅⭐️ | ✅⭐️ | ❌ |



## 紧耦合MVC

![传统 MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-0-mvc.png)

举一个例子，在一个多页面的网页Web应用程序中，当你点击一个链接导航至其他页面的时候，该页面就会被全部重新加载。该架构的问题在于视图（View）与控制器（Controller）和模型（Model）是紧密耦合的。



## Cocoa MVC

Cocoa MVC 是苹果公司建议iOS开发者使用的架构。理论上来说，该架构可以通过控制器（Controller）将模型（Model）与视图（View）剥离开。

![Cocoa MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-1-cocoa-mvc.png)


然而，在实际操作过程中，Cocoa MVC 鼓励大规模视图控制器的使用，最终使得视图控制器完成所有操作。

![实际的 Cocoa MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-2-realistic-cocoa-mvc.png)

尽管测试这样的耦合大规模视图控制器是十分困难的，然而在开发速度方面，Cocoa MVC是现有的这些选择里面表现最好的。



## MVP

在MVP中，Presenter与视图控制器（view controller）的生命周期没有任何关系，视图可以很轻易地被取代。我们可以认为UIViewController实际上就是视图（View）。

![MVC 的变体](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-3-mvc-variant.png)


还有另外一种类型的MVP：带有数据绑定的MVP。如下图所示，视图（View）与模型（Model）和控制器（Controller）是紧密耦合的。

![MVP](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-4-mvp.png)



## MVVM

MVVM与MVP相似不过MVVM绑定的是视图（View）与视图模型（View Model）。

![MVVM](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-5-mvvm.png)



## VIPER

不同于MV(X)的三层结构，VIPER具有五层结构（VIPER View, Interactor, Presenter, Entity, 和 Routing）。这样的结构可以很好地进行职责分配但是其维护性较差。

![VIPER](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-6-viper.png)


相较于MV(X)，VIPER有下列不同点：

1. Model 的逻辑处理转移到了 Interactor 上，这样一来，Entities 没有逻辑，只是纯粹的保存数据的结构。
2. ==UI相关的业务逻辑分在Presenter中，数据修改功能分在Interactor中==。
3. VIPER为实现模块间的跳转功能引入了路由模块 Router 。
