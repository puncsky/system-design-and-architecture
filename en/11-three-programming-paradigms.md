---
layout: post
title: "3 Programming Paradigms"
date: 2018-08-12 02:31
comments: true
categories: system design
language: en
references:
  - https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164
---

Structured programming vs. OO programming vs. Functional programming



1. Structured programming is discipline imposed upon direct transfer of control.
	1. Testability: software is like science: Science does not work by proving statements true, but rather by proving statements false. Structured programming forces us to recursively decompose a program into a set of small provable functions.



2. OO programming is discipline imposed upon indirect transfer of control.
	1. Capsulation, inheritance, polymorphism(pointers to functions) are not unique to OO.
	2. But OO makes polymorphism safe and convenient to use. And then enable the powerful ==plugin architecture== with dependency inversion
		1. Source code denpendencies and flow of control are typically the same. However, if we make them both depend on interfaces, dependency is inverted.
		2. Interfaces empower independent deployability. e.g. when deploying Solidity smart contracts, importing and using interfaces consume much less gases than doing so for the entire implementation.



3. Functional programming: Immutability. is discipline imposed upon variable assignment.
	1. Why important? All race conditions, deadlock conditions, and concurrent update problems are due to mutable variables.
	2. ==Event sourcing== is a strategy wherein we store the transactions, but not the state. When state is required, we simply apply all the transactions from the beginning of time.
