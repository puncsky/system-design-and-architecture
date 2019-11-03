---
layout: post
title: "How to write solid code?"
date: 2019-09-25 02:29
comments: true
categories: system design
language: en
---

![he likes it](https://res.cloudinary.com/dohtidfqh/image/upload/v1557957637/web-guiguio/he-likes-it.jpg)

1. empathy / perspective-taking is the most important.
    1. realize that code is written for human to read first and then for machines to execute.
    2. software is so "soft" and there are many ways to achieve one thing. It's all about making the proper trade-offs to fulfill the requirements.
    3. Invent and Simplify: Apple Pay RFID vs. Wechat Scan QR Code.

2. choose a sustainable architecture to reduce human resources costs per feature.

<script src="/notes/11-three-programming-paradigms/js"></script>
<script src="/notes/12-solid-design-principles/js"></script>

3. adopt patterns and best practices.

4. avoid anti-patterns
    * missing error-handling
    * callback hell = spaghetti code + unpredictable error handling
    * over-long inheritance chain
    * circular dependency
    * over-complicated code
        * nested tertiary operation
        * comment out unused code
    * missing i18n, especially RTL issues
    * don't repeat yourself
      * simple copy-and-paste
      * unreasonable comments

5. effective refactoring
    * semantic version
    * never introduce breaking change to non major versions
        * two legged change
