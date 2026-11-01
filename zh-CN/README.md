<h1 align="center">系统设计与架构</h1>

<p align="center">
  <b>一次一个系统，学会 Uber、Netflix、Stripe 以及现代 AI Agent 是怎么搭起来的。</b><br />
  面向一线工程师和系统设计面试的实战指南，以图为主。
</p>

<p align="center">
  <a href="https://github.com/puncsky/system-design-and-architecture/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/puncsky/system-design-and-architecture?style=flat&logo=github" /></a>
  <a href="https://t.me/system_design_and_architecture"><img alt="Telegram" src="https://img.shields.io/badge/chat-Telegram-26A5E4?logo=telegram&logoColor=white" /></a>
  <a href="https://discord.gg/Pb5YbK3ykN"><img alt="Discord" src="https://img.shields.io/badge/chat-Discord-5865F2?logo=discord&logoColor=white" /></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · 简体中文 · <a href="https://tianpan.co">网站</a>
</p>

<p align="center"><b>⭐ 点 Star 关注新章节。</b></p>

## 从哪里开始

- **资深工程师（Google L5+）**：直接看[实战案例](#实战案例-system-design-in-practice)。
- **初中级工程师（Google L3/L4）**：先看[理论基础](#理论基础-system-design-theories)，再看实战案例。
- **入门**：先看[面试准备](#面试准备)，再看理论基础，最后看实战案例。

每个案例都遵循同一个四步框架：1）明确需求 2）高层设计 3）深入各组件及其交互 4）总结盲点与瓶颈。

## 最近更新

- 🆕 [Designing an Always-on Agent](2026-10-21-designing-always-on-agent.md)
- 🆕 [Agent System Layers and Logical Components](2026-10-22-agent-system-layers-and-logical-components.md)
- 🆕 [LLM Inference Stack](2026-10-24-llm-inference-stack.md)

## 实战案例 System Design in Practice

### 🤖 AI 与 Agent

| Product                                                                                                                          | Question                                                                                              |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1595029150/web-guiguio/favicon-32x32.png" alt="Agent" width="40" /> | [Designing an Always-on Agent](2026-10-21-designing-always-on-agent.md)                               |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710354/web-guiguio/tiktok.webp" alt="TikTok" width="40" />      | [Designing a recommendation system](140-designing-a-recommendation-system.md)                         |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708917/web-guiguio/uber.png" alt="Uber" width="40" />           | [Fraud Detection with Semi-supervised Learning](136-fraud-detection-with-semi-supervised-learning.md) |

### 📱 社交、媒体与平台

| Product                                                                                                                                 | Question                                                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708936/web-guiguio/instagram.png" alt="Instagram" width="40" />        | [Designing Instagram or Pinterest](2016-02-13-crack-the-system-design-interview.md)                                |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708917/web-guiguio/uber.png" alt="Uber" width="40" />                  | [Designing Uber](120-designing-uber.md)                                                                            |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710222/web-guiguio/airbnb.png" alt="Airbnb" width="40" />              | [Designing Airbnb or a hotel booking system](177-designing-Airbnb-or-a-hotel-booking-system.md)                    |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709369/web-guiguio/facebook.png" alt="Facebook" width="40" />          | [How Facebook Scale its Social Graph Store? TAO](49-facebook-tao.md)                                               |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709414/web-guiguio/netflix.png" alt="Netflix" width="40" />            | [How Netflix Serves Viewing Data?](45-how-to-design-netflix-view-state-service.md)                                 |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709414/web-guiguio/netflix.png" alt="Netflix" width="40" />            | [How to stream video over HTTP for mobile devices? HTTP Live Streaming (HLS)](38-how-to-stream-video-over-http.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710390/web-guiguio/lyft.png" alt="Lyft" width="40" />                  | [Lyft's Marketing Automation Platform -- Symphony](178-lyft-marketing-automation-symphony.md)                      |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709990/web-guiguio/linkedin.png" alt="LinkedIn" width="40" />          | [Designing typeahead search or autocomplete](179-designing-typeahead-search-or-autocomplete.md)                    |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1595029150/web-guiguio/favicon-32x32.png" alt="Online judge" width="40" /> | [Designing Online Judge or Leetcode](https://tianpan.co/notes/243-designing-online-judge-or-leetcode)              |

### 💳 支付与金融科技

| Product                                                                                                                          | Question                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709444/web-guiguio/stripe.png" alt="Stripe" width="40" />       | [How to design robust and predictable APIs with idempotency?](43-how-to-design-robust-and-predictable-apis-with-idempotency.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709444/web-guiguio/stripe.png" alt="Stripe" width="40" />       | [Designing payment webhook](166-designing-payment-webhook.md)                                                                   |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710085/web-guiguio/square.png" alt="Square" width="40" />       | [Designing Square Cash or PayPal Money Transfer System](167-designing-paypal-money-transfer.md)                                 |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710037/web-guiguio/robinhood.png" alt="Robinhood" width="40" /> | [Designing Stock Exchange](161-designing-stock-exchange.md)                                                                     |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710037/web-guiguio/robinhood.png" alt="Robinhood" width="40" /> | [Designing Smart Notification of Stock Price Changes](162-designing-smart-notification-of-stock-price-changes.md)               |

### 🏗️ 存储与基础设施

| Product                                                                                                                          | Question                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709618/web-guiguio/confluent.png" alt="Confluent" width="40" /> | [Designing a distributed logging system](61-what-is-apache-kafka.md)                           |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709677/web-guiguio/twitter.png" alt="Twitter" width="40" />     | [Designing a URL shortener](84-designing-a-url-shortener.md)                                   |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709990/web-guiguio/linkedin.png" alt="LinkedIn" width="40" />   | [Designing a KV store with external storage](97-designing-a-kv-store-with-external-storage.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709823/web-guiguio/memcached.png" alt="Memcached" width="40" /> | [Designing a distributed in-memory KV store or Memcached](174-designing-memcached.md)          |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709369/web-guiguio/facebook.png" alt="Facebook" width="40" />   | [Designing Facebook photo storage](121-designing-facebook-photo-storage.md)                    |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710137/web-guiguio/grafana.jpg" alt="Grafana" width="40" />     | [Designing a metric system](168-designing-a-metric-system.md)                                  |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710529/web-guiguio/nginx.jpg" alt="Nginx" width="40" />         | [Designing a Load Balancer or Dropbox Bandaid](182-designing-l7-load-balancer.md)              |

## 理论基础 System Design Theories

**基础**

- [Introduction to Architecture](145-introduction-to-architecture.md)
- [How to scale a web service?](41-how-to-scale-a-web-service.md)
- [Concurrency Model](181-concurrency-models.md)
- [Cloud Design Patterns](2018-07-10-cloud-design-patterns.md)
- [Public API Choices](66-public-api-choices.md)
- [Load Balancer Types](2018-07-23-load-balancer-types.md)
- How to do capacity planning? _(coming soon)_

**数据与一致性**

- [ACID vs BASE](2018-07-26-acid-vs-base.md)
- [Data Partition and Routing](2018-07-21-data-partition-and-routing.md)
- [Replica, Consistency, and CAP theorem](2018-07-24-replica-and-consistency.md)
- [Improving availability with failover](85-improving-availability-with-failover.md)
- [Intro to Relational Database](80-relational-database.md)
- [4 Kinds of No-SQL](78-four-kinds-of-no-sql.md)
- [Key value cache](122-key-value-cache.md)
- [Stream and Batch Processing Frameworks](137-stream-and-batch-processing.md)
- [Lambda Architecture](83-lambda-architecture.md)

**数据结构**

- [Bloom Filter](68-bloom-filter.md)
- [Skiplist](69-skiplist.md)
- [B tree vs. B+ tree](2018-07-22-b-tree-vs-b-plus-tree.md)

**AI 系统**

- [Agent System Layers and Logical Components](2026-10-22-agent-system-layers-and-logical-components.md)
- [LLM Inference Stack](2026-10-24-llm-inference-stack.md)

**工程实践**

- [3 Programming Paradigms](11-three-programming-paradigms.md)
- [SOLID Design Principles](12-solid-design-principles.md)
- [iOS Architecture Patterns Revisited](123-ios-architecture-patterns-revisited.md)

## 面试准备

- [Crack the system design interview](2016-02-13-crack-the-system-design-interview.md)
- [What can we communicate in soft skills interview?](63-soft-skills-interview.md)
- [Experience Deep Dive](2018-07-20-experience-deep-dive.md)

## 社区

加入讨论：[Telegram](https://t.me/system_design_and_architecture) · [Discord](https://discord.gg/Pb5YbK3ykN)。发现错别字或设计漏洞，欢迎提 Issue 或 PR。

⭐ 觉得有用就点个 Star。
