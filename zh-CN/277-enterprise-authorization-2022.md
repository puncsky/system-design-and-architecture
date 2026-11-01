---
slug: 277-enterprise-authorization-2022
id: 277-enterprise-authorization-2022
title: "企业授权服务 2022"
date: "2022-12-12 23:41"
comments: true
published: true
tags: [system design]
description: 授权决定个人或系统是否有权访问特定资源。这个过程是一个典型的场景，可以通过软件进行自动化。我们将回顾谷歌的 Zanzibar、受 Zanzibar 启发的解决方案以及市场上的其他 AuthZ 服务。
references:
  - https://research.google/pubs/pub48190/
---

授权决定个人或系统是否可以访问特定资源。这个过程是一个典型的场景，可以通过软件进行自动化。我们将回顾谷歌的 Zanzibar、受 Zanzibar 启发的解决方案以及市场上的其他 AuthZ 服务。

## Zanzibar：谷歌的一致性全球授权系统

- 谷歌的 = 经受住了谷歌产品的考验，每秒检查 2000 万个权限，p95 < 10 毫秒，99.999% 的可用性
- 一致性 = 确保授权检查基于不超过客户端指定更改的 ACL 数据
- 全球 = 地理分布的数据中心，并在全球数千台服务器上分配负载。
- 授权 = 通用授权

在 Zanzibar 的背景下，我们可以这样表达 AuthZ 问题：

```
isAuthorized(user, relation, object) = 用户与对象之间是否存在关系？
```

这被称为基于关系的访问控制（==ReBAC==）。客户端可以在 ReBAC 的基础上构建 ABAC 和 RBAC。不幸的是，Zanzibar 不是开源的，也不能作为现成的服务购买。

Zanzibar 架构

![Zanzibar 架构](https://tp-misc.b-cdn.net/zanzibar-architecture.png "Zanzibar 架构")

为什么 Zanzibar 可扩展？

- 使用 Spanner 作为数据库
- Leopard 索引系统
  - 将组到组的路径展平，类似于图中的可达性问题
  - 将索引元组存储为整数的有序列表，使用如跳表等结构，以实现集合之间的高效并集和交集。
  - 异步数据流客户端 > aclserver > changelog > Leopard 索引系统
- 如何维护外部一致性？Zookie 协议 - 客户端使用基于时间戳的令牌检查权限。

## Auth0 细粒度授权 (FGA)

[Auth0 FGA](https://github.com/openfga/openfga) 是谷歌 Zanzibar 的 [开源实现](https://github.com/openfga)。请查看互动教程 https://zanzibar.academy/。

对于微服务背景下的企业开发者，如何使用 FGA 的托管解决方案？

![如何使用 FGA？](https://tp-misc.b-cdn.net/FGA@2x.png "如何使用 FGA？")

1. 访问 FGA 仪表板，以 DSL 和关系元组定义授权模型，最后添加像自动化测试一样的授权断言（这太棒了！）。
2. 开发者返回他们的服务并调用 FGA 包装器的检查端点。

不幸的是，我没有看到变更日志审计和版本控制，以便在开发者在 FGA 仪表板中出错时进行回滚，可能是因为 FGA 仍在进行中。

## OSO

使用 Oso，你可以：

- **建模**：使用 Oso 的内置原语设置常见的权限模式，如基于角色的访问控制（RBAC）和关系。根据需要使用 Oso 的声明式策略语言 Polar（DSL）进行扩展。
- **过滤**：超越是/否的授权问题。也对集合实施授权 - 例如，“只显示 Juno 可以看到的记录。”
- **测试**：在你拥有单一接口的情况下，现在可以编写单位测试来验证你的授权逻辑。使用 Oso 调试器或 REPL 来追踪意外行为。

<img
style={{ maxHeight: 500 }}
src="https://tp-misc.b-cdn.net/osohq-architecture.png"
/>

## Ory Keto

[Keto](https://github.com/ory/keto) 是 Zanzibar 的开源（Go）实现。提供 gRPC、REST API、新 SQL 和易于使用的细粒度权限语言（DSL）。支持 ACL、RBAC 和其他访问模型。

## Authzed SpiceDB

[SpiceDB](https://github.com/authzed/spicedb) 是一个开源数据库系统，用于管理受安全保护的应用程序权限，灵感来自谷歌的 Zanzibar 论文。

![](https://tp-misc.b-cdn.net/spicedb-architecture.png)

## Aserto Topaz

[Topaz](https://github.com/aserto-dev/topaz) 是一个开源授权服务，为应用程序和 API 提供细粒度、实时、基于策略的访问控制。

它使用 [Open Policy Agent](https://www.openpolicyagent.org/)（OPA）作为决策引擎，并提供一个受谷歌 [Zanzibar](https://research.google/pubs/pub48190/) 数据模型启发的内置目录。

授权策略可以利用用户属性、组成员资格、应用程序资源及其之间的关系。所有用于授权的数据都在嵌入式数据库中建模和存储，因此可以快速高效地评估授权决策。

![](https://tp-misc.b-cdn.net/topaz-architecture.png)

## Cloudentity

这似乎是一个集成的 CIAM 解决方案，没有独立的企业授权功能。文档令人困惑...

## Open Policy Agent

[Open Policy Agent (OPA)](https://www.openpolicyagent.org/) 是一个开源的通用政策引擎，统一了整个堆栈的政策执行。OPA 提供了一种高级声明性语言，让你可以将政策指定为代码，并提供简单的 API，将政策决策从你的软件中卸载。你可以在微服务、Kubernetes、CI/CD 管道、API 网关等中使用 OPA 来执行政策。

OPA 最初由 [Styra](https://www.styra.com/) 创建，并且是 [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/) 的一个毕业项目。

## Permit.IO

Permit.IO 是一个基于 OPA 和 OPAL 的低代码 AuthZ 平台。

<img
style={{ maxHeight: 500 }}
src="https://tp-misc.b-cdn.net/permit-io-architecture.svg"
/>

## Scaled Access

[Scaled Access](https://www.scaledaccess.com/) 是一家欧洲公司，已被 onewelcome 收购。它提供丰富的上下文感知访问控制、实时政策执行、细粒度授权和基于关系的访问控制。文档中有 API，但没有 SDK。

## Casbin

[Casbin](https://casbin.org/) 是一个授权库，支持 Golang 中的 ACL、RBAC、ABAC 等访问控制模型。它在多种编程语言中提供 SDK。然而，它的配置在 CSV 文件中相对静态，更适合企业内部使用，而不适合面向客户的授权。

## SGNL

这个服务看起来相当简陋 - 美丽的网站却没有任何开发者内容。没有文档，没有视频或自助演示。我怀疑它的定位是面向非技术企业。不推荐。

## 总结

这是我初步检查后的排名。理想情况下，我希望有一个类似 LaunchDarkly 的 AuthZ 平台 - 易于集成和操作，配备完整的审计日志、版本控制和面向开发者的网页门户。

<br/>

<div style={{ fontSize: 16 }}>

|                                                     | Github Stars | Models     | DevEx                              | Perf | Score (out of 5) |
| --------------------------------------------------- | ------------ | ---------- | ---------------------------------- | ---- | ---------------- |
| [Oso](https://github.com/osohq/oso)                 | 2.8k         | ReBAC      | DSL, API, SDK, web portal          | ?    | 3                |
| [Spicedb](https://github.com/authzed/spicedb)       | 3k           | ReBAC      | DSL, API, SDK, web portal          | ?    | 3                |
| [permit.io](https://permit.io/)                     | 840          | ReBAC      | DSL, API, SDK, low-code web portal | ?    | 3                |
| [Aserto Topas](https://github.com/aserto-dev/topaz) | 534          | ReBAC      | DSL, API, SDK, web portal          | ?    | 3                |
| [FGA](https://github.com/openfga/openfga)           | 657          | ReBAC      | DSL, API, SDK, web portal          | ?    | 3                |
| [Keto](https://github.com/ory/keto)                 | 3.8k         | ReBAC      | DSL, API, SDK                      | ?    | 2                |
| [Casbin](https://casbin.org/)                       | 13.4k        | ABAC, RBAC | Library, static file for policies  | ?    | 1                |

</div>
