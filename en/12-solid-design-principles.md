---
layout: post
title: "SOLID Design Principles"
date: 2018-08-13 18:07
comments: true
categories: system design
language: en
references:
  - https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164
---

SOLID is an acronym of design principles that help software engineers write solid code within a project.

1. S - **Single Responsibility Principle**. A module should be responsible to one, and only one, actor. a module is just a cohesive set of functions and data structures.


2. O - **Open/Closed Principle**. A software artifact should be open for extension but closed for modification.


3. L - **Liskov’s Substitution Principle**. Simplify code with interface and implementation, generics, sub-classing, and duck-typing for inheritance.


4. I - **Interface Segregation Principle**. Segregate the monolithic interface into smaller ones to decouple modules.


5. D - **Dependency Inversion Principle**. The source code dependencies are inverted against the flow of control. most visible organizing principle in our architecture diagrams.
      1. Things should be stable concrete, Or stale abstract, not ==concrete and volatile.==
      2. So use ==abstract factory== to create volatile concrete objects (manage undesirable dependency.) 产生 interface 的 interface
      3. DIP violations cannot be entirely removed. Most systems will contain at least one such concrete component — this component is often called main.
