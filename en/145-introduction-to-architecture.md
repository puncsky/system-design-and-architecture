---
layout: post
title: "Introduction to Architecture"
date: 2019-05-11 15:52
comments: true
categories: system design
language: en
references:
  - https://puncsky.com/notes/10-thinking-software-architecture-as-physical-buildings
  - https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html
  - http://www.ruanyifeng.com/blog/2016/09/software-architecture.html
---

## What is architecture?

Architecture is the shape of the software system. Thinking it as a big picture of physical buildings.

* paradigms are bricks.
* design principles are rooms.
* components are buildings.

Together they serve a specific purpose like a hospital is for curing patients and a school is for educating students.


## Why do we need architecture?

### Behavior vs. Structure

Every software system provides two different values to the stakeholders: behavior and structure. Software developers are responsible for ensuring that both those values remain high.

==Software architects are, by virtue of their job description, more focused on the structure of the system than on its features and functions.==


### Ultimate Goal - ==saving human resources costs per feature==

Architecture serves the full lifecycle of the software system to make it easy to understand, develop, test, deploy, and operate.
The goal is to minimize the human resources costs per business use-case.



The O’Reilly book Software Architecture Patterns by Mark Richards is a simple but effective introduction to these five fundamental architectures.



## 1. Layered Architecture



The layered architecture is the most common in adoption, well-known among developers, and hence the de facto standard for applications. If you do not know what architecture to use, use it.

[comment]: <> (https://www.draw.io/#G1ldM5O9Y62Upqg_t5rcTNHIRseP-7fqQT)

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/Software_Architecture_101.png)


Examples

* TCP / IP Model: Application layer > transport layer > internet layer > network access layer
* [Facebook TAO](https://puncsky.com/notes/49-facebook-tao): web layer > cache layer (follower + leader) > database layer

Pros and Cons

* Pros
    * ease of use
    * separation of responsibility
    * testability
* Cons
    * monolithic
        * hard to adjust, extend or update. You have to make changes to all the layers.



## 2. Event-Driven Architecture



A state change will emit an event to the system. All the components communicate with each other through events.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-event-driven.png)


A simple project can combine the mediator, event queue, and channel. Then we get a simplified architecture: 

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-event-driven-simplified.png)


Examples

* QT: Signals and Slots
* Payment Infrastructure: Bank gateways usually have very high latencies, so they adopt async technologies in their architecture design.



## 3. Micro-kernel Architecture (aka Plug-in Architecture)



The software's responsibilities are divided into one "core" and multiple "plugins". The core contains the bare minimum functionality. Plugins are independent of each other and implement shared interfaces to achieve different goals. 

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-micro-kernel.png)


Examples

* Visual Studio Code, Eclipse
* MINIX operating system



## 4. Microservices Architecture



A massive system is decoupled to multiple micro-services, each of which is a separately deployed unit, and they communicate with each other via [RPCs](/blog/2016-02-13-crack-the-system-design-interview#21-communication).


![uber architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546574738/web-guiguio/uber-architecture_2.jpg)



Examples

* Uber: See [designing Uber](https://puncsky.com/notes/120-designing-uber)
* Smartly




## 5. Space-based Architecture



This pattern gets its name from "tuple space", which means “distributed shared memory". There is no database or synchronous database access, and thus no database bottleneck. All the processing units share the replicated application data in memory. These processing units can be started up and shut down elastically.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1557614663/web-guiguio/software-architecture-101-space-based.png)



Examples: See [Wikipedia](https://en.wikipedia.org/wiki/Tuple_space#Example_usage)

- Mostly adopted among Java users: e.g., JavaSpaces
