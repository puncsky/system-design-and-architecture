---
slug: 169-how-to-write-solid-code
id: 169-how-to-write-solid-code
title: "如何编写稳健的代码？"
date: 2019-09-25 02:29
comments: true
tags: [系统设计]
description: 同理心在编写稳健代码中扮演着最重要的角色。此外，您需要选择一个可持续的架构，以减少项目扩展时的人力资源成本。然后，采用模式和最佳实践；避免反模式。最后，必要时进行重构。
---

![他喜欢它](https://res.cloudinary.com/dohtidfqh/image/upload/v1557957637/web-guiguio/he-likes-it.jpg)

1. 同理心 / 视角转换是最重要的。
    1. 意识到代码首先是为人类阅读而编写的，然后才是为机器执行。
    2. 软件是如此“柔软”，有很多方法可以实现同一目标。关键在于做出适当的权衡，以满足需求。
    3. 发明与简化：Apple Pay RFID 与 微信扫码二维码。

2. 选择可持续的架构，以减少每个功能的人力资源成本。

<script src="https://tianpan.co/notes/11-three-programming-paradigms/js"></script>
<script src="https://tianpan.co/notes/12-solid-design-principles/js"></script>

3. 采用模式和最佳实践。

4. 避免反模式
    * 缺少错误处理
    * 回调地狱 = 意大利面条代码 + 不可预测的错误处理
    * 过长的继承链
    * 循环依赖
    * 过于复杂的代码
        * 嵌套的三元操作
        * 注释掉未使用的代码
    * 缺少国际化，特别是 RTL 问题
    * 不要重复自己
      * 简单的复制粘贴
      * 不合理的注释

5. 有效的重构
    * 语义版本
    * 永远不要对非主要版本引入破坏性更改
        * 两腿变更