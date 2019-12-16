---
layout: post
title: "Concurrency Models"
date: 2019-10-16 14:04
comments: true
categories: system design
abstract: "Five concurrency models you may want to know: Single-threaded; Multiprocessing and lock-based concurrency; Communicating Sequential Processes (CSP); Actor Model (AM); Software Transactional Memory (STM)."
language: en
---

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571262011/web-guiguio/Concurrency_Models_1.png)


* Single-threaded - Callbacks, Promises, Observables and async/await: vanilla JS
* threading/multiprocessing, lock-based concurrency
    * protecting critical section vs. performance
* Communicating Sequential Processes (CSP)
	* Golang or Clojure’s `core.async`. 
	* process/thread passes data through channels.
* Actor Model (AM): Elixir, Erlang, Scala
	* asynchronous by nature, and have location transparency that spans runtimes and machines - if you have a reference (Akka) or PID (Erlang) of an actor, you can message it via mailboxes.
	* powerful fault tolerance by organizing actors into a supervision hierarchy, and you can handle failures at its exact level of hierarchy.
* Software Transactional Memory (STM): Clojure, Haskell
	* like MVCC or pure functions: commit / abort / retry 
