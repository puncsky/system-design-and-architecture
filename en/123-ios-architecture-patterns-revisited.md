---
layout: post
title: "iOS Architecture Patterns Revisited"
date: 2019-01-10 02:26
comments: true
categories: architecture, mobile, system design
language: en
references:
  - https://medium.com/ios-os-x-development/ios-architecture-patterns-ecba4c38de52
---

## Why bother with architecture?

Answer: [for reducing human resources costs per feature](https://puncsky.com/notes/10-thinking-software-architecture-as-physical-buildings#ultimate-goal-saving-human-resources-costs-per-feature).

Mobile developers evaluate the architecture in three dimensions.

1. Balanced distribution of responsibilities among feature actors.
2. Testability
3. Ease of use and maintainability


| | Distribution of Responsibility | Testability |  Ease of Use |
| --- | ---    | ---    | --- |
| Tight-coupling MVC | ❌ | ❌ | ✅ |
| Cocoa MVC | ❌ VC are coupled | ❌ | ✅⭐ |
| MVP | ✅ Separated View Lifecycle | ✅ | Fair: more code |
| MVVM | ✅ | Fair: because of View's UIKit dependant | Fair |
| VIPER | ✅⭐️ | ✅⭐️ | ❌ |



## Tight-coupling MVC

![Traditional MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-0-mvc.png)

For example, in a multi-page web application, page completely reloaded once you press on the link to navigate somewhere else.  The problem is that the View is tightly coupled with both Controller and Model.



## Cocoa MVC

Apple’s MVC, in theory, decouples View from Model via Controller.

![Cocoa MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-1-cocoa-mvc.png)


Apple’s MVC in reality encourages ==massive view controllers==. And the view controller ends up doing everything.

![Realistic Cocoa MVC](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-2-realistic-cocoa-mvc.png)

It is hard to test coupled massive view controllers. However, Cocoa MVC is the best architectural pattern regarding the speed of the development.



## MVP

In an MVP, Presenter has nothing to do with the life cycle of the view controller, and the View can be mocked easily. We can say the UIViewController is actually the View.

![MVC Variant](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-3-mvc-variant.png)


There is another kind of MVP: the one with data bindings. And as you can see, there is tight coupling between View and the other two.

![MVP](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-4-mvp.png)



## MVVM

It is similar to MVP but binding is between View and View Model.

![MVVM](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-5-mvvm.png)



## VIPER
There are five layers (VIPER View, Interactor, Presenter, Entity, and Routing) instead of three when compared to MV(X).  This distributes responsibilities well but the maintainability is bad.

![VIPER](https://res.cloudinary.com/dohtidfqh/image/upload/v1547002648/web-guiguio/ios-architecture-6-viper.png)


When compared to MV(X), VIPER

1. Model logic is shifted to Interactor and Entities are left as dumb data structures.
2. ==UI related business logic is placed into Presenter, while the data altering capabilities are placed into Interactor==.
3. It introduces Router for the navigation responsibility.
