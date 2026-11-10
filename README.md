<h1 align="center">System Design and Architecture</h1>

<p align="center">
  <b>Learn how Uber, Netflix, Stripe, and modern AI agents are built, one system at a time.</b><br />
  A practical, diagram-first guide for engineers who build real systems and ace system design interviews.
</p>

<p align="center">
  <a href="https://github.com/puncsky/system-design-and-architecture/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/puncsky/system-design-and-architecture?style=flat&logo=github" /></a>
  <a href="https://github.com/puncsky/system-design-and-architecture/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/puncsky/system-design-and-architecture/ci.yml?branch=main&label=CI" /></a>
  <a href="./README.md#license"><img alt="License: GPL v3" src="https://img.shields.io/badge/license-GPL%20v3-blue" /></a>
  <a href="https://t.me/system_design_and_architecture"><img alt="Telegram" src="https://img.shields.io/badge/chat-Telegram-26A5E4?logo=telegram&logoColor=white" /></a>
  <a href="https://discord.gg/Pb5YbK3ykN"><img alt="Discord" src="https://img.shields.io/badge/chat-Discord-5865F2?logo=discord&logoColor=white" /></a>
</p>

<p align="center">
  <a href="#start-here">Start here</a> ·
  <a href="#whats-new">What's new</a> ·
  <a href="#system-design-in-practice">Case studies</a> ·
  <a href="#system-design-theories">Theories</a> ·
  <a href="#prepare-for-an-interview-effectively">Interview prep</a> ·
  <a href="./zh-CN/README.md">简体中文</a> ·
  <a href="https://tianpan.co">Website</a>
</p>

<p align="center"><b>⭐ Star this repo to follow new chapters as they land.</b></p>

> The 2nd Edition is a work in progress. New chapters are published regularly, so watch the repo for updates.

## Why this book

Since 2015, _System Design and Architecture_ has helped software engineers around the world land roles and design better systems. It works because it is:

1. 🌎 **Grounded in real systems.** Every design starts from how companies such as Uber, Facebook, Netflix, Stripe, and Dropbox actually build their products.
2. 🍕 **Easy to digest.** System design at the right level of abstraction is a map that gets you to the destination by the shortest route. Charts, diagrams, and step-by-step guides give you the minimum actionable knowledge to excel in interviews and start building.
3. 🤲 **Broad.** It covers backend to frontend, and classic distributed systems to LLM inference and AI agents.
4. 🚶‍♀️ **Repeatable.** Every design follows the same 4-step framework:
   1. Clarify requirements
   2. Sketch the high-level design
   3. Deep dive into components and how they interact
   4. Wrap up with blind spots and bottlenecks

## Start here

| If you are...                             | Read this path                                                                                                              |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 🧑‍💼 **Senior (Google L5+)**                | Go straight to [System Design in Practice](#system-design-in-practice).                                                     |
| 🧑‍💻 **Junior or mid-level (Google L3/L4)** | Read [System Design Theories](#system-design-theories) first, then [System Design in Practice](#system-design-in-practice). |
| 🌱 **Just starting out**                  | Begin with [Prepare for an Interview effectively](#prepare-for-an-interview-effectively), then Theories, then Practice.     |

## What's new

The 2nd Edition covers what changed between 2015 and today: mobile ate the world, cloud-native computing arrived with Kubernetes, web3 rose and fell, and AI agents became a new class of system. Recent additions:

- 🆕 [Designing an Always-on Agent](./en/2026-10-21-designing-always-on-agent.md)
- 🆕 [Agent System Layers and Logical Components](./en/2026-10-22-agent-system-layers-and-logical-components.md)
- 🆕 [LLM Inference Stack](./en/2026-10-24-llm-inference-stack.md)
- 🆕 [Designing an LLM Architecture](./en/2026-11-01-designing-an-llm-architecture.md)

Also coming in the 2nd Edition: more companies and products, existing chapters rewritten for current trends, more diagrams with step-by-step guides, a PDF edition, and less repetition so that each design teaches its own abstraction.

**Out of scope:** API design for specific domains (see [Google's API design guide](https://cloud.google.com/apis/design)) and deep object-oriented design.

## System Design in Practice

### 🤖 AI and Agents

| Product                                                                                                                          | Question                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1595029150/web-guiguio/favicon-32x32.png" alt="Agent" width="40" /> | [Designing an Always-on Agent](./en/2026-10-21-designing-always-on-agent.md)                               |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710354/web-guiguio/tiktok.webp" alt="TikTok" width="40" />      | [Designing a recommendation system](./en/140-designing-a-recommendation-system.md)                         |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708917/web-guiguio/uber.png" alt="Uber" width="40" />           | [Fraud Detection with Semi-supervised Learning](./en/136-fraud-detection-with-semi-supervised-learning.md) |

### 📱 Social, Media, and Marketplaces

| Product                                                                                                                                 | Question                                                                                                                |
| --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708936/web-guiguio/instagram.png" alt="Instagram" width="40" />        | [Designing Instagram or Pinterest](./en/2016-02-13-crack-the-system-design-interview.md)                                |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708917/web-guiguio/uber.png" alt="Uber" width="40" />                  | [Designing Uber](./en/120-designing-uber.md)                                                                            |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710222/web-guiguio/airbnb.png" alt="Airbnb" width="40" />              | [Designing Airbnb or a hotel booking system](./en/177-designing-Airbnb-or-a-hotel-booking-system.md)                    |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709369/web-guiguio/facebook.png" alt="Facebook" width="40" />          | [How Facebook Scale its Social Graph Store? TAO](./en/49-facebook-tao.md)                                               |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709414/web-guiguio/netflix.png" alt="Netflix" width="40" />            | [How Netflix Serves Viewing Data?](./en/45-how-to-design-netflix-view-state-service.md)                                 |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709414/web-guiguio/netflix.png" alt="Netflix" width="40" />            | [How to stream video over HTTP for mobile devices? HTTP Live Streaming (HLS)](./en/38-how-to-stream-video-over-http.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710390/web-guiguio/lyft.png" alt="Lyft" width="40" />                  | [Lyft's Marketing Automation Platform -- Symphony](./en/178-lyft-marketing-automation-symphony.md)                      |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709990/web-guiguio/linkedin.png" alt="LinkedIn" width="40" />          | [Designing typeahead search or autocomplete](./en/179-designing-typeahead-search-or-autocomplete.md)                    |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1595029150/web-guiguio/favicon-32x32.png" alt="Online judge" width="40" /> | [Designing Online Judge or Leetcode](https://tianpan.co/notes/243-designing-online-judge-or-leetcode)                   |

### 💳 Payments and Fintech

| Product                                                                                                                          | Question                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709444/web-guiguio/stripe.png" alt="Stripe" width="40" />       | [How to design robust and predictable APIs with idempotency?](./en/43-how-to-design-robust-and-predictable-apis-with-idempotency.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709444/web-guiguio/stripe.png" alt="Stripe" width="40" />       | [Designing payment webhook](./en/166-designing-payment-webhook.md)                                                                   |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710085/web-guiguio/square.png" alt="Square" width="40" />       | [Designing Square Cash or PayPal Money Transfer System](./en/167-designing-paypal-money-transfer.md)                                 |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710037/web-guiguio/robinhood.png" alt="Robinhood" width="40" /> | [Designing Stock Exchange](./en/161-designing-stock-exchange.md)                                                                     |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710037/web-guiguio/robinhood.png" alt="Robinhood" width="40" /> | [Designing Smart Notification of Stock Price Changes](./en/162-designing-smart-notification-of-stock-price-changes.md)               |

### 🏗️ Storage and Infrastructure

| Product                                                                                                                          | Question                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709618/web-guiguio/confluent.png" alt="Confluent" width="40" /> | [Designing a distributed logging system](./en/61-what-is-apache-kafka.md)                           |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709677/web-guiguio/twitter.png" alt="Twitter" width="40" />     | [Designing a URL shortener](./en/84-designing-a-url-shortener.md)                                   |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709990/web-guiguio/linkedin.png" alt="LinkedIn" width="40" />   | [Designing a KV store with external storage](./en/97-designing-a-kv-store-with-external-storage.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709823/web-guiguio/memcached.png" alt="Memcached" width="40" /> | [Designing a distributed in-memory KV store or Memcached](./en/174-designing-memcached.md)          |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709369/web-guiguio/facebook.png" alt="Facebook" width="40" />   | [Designing Facebook photo storage](./en/121-designing-facebook-photo-storage.md)                    |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710137/web-guiguio/grafana.jpg" alt="Grafana" width="40" />     | [Designing a metric system](./en/168-designing-a-metric-system.md)                                  |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710529/web-guiguio/nginx.jpg" alt="Nginx" width="40" />         | [Designing a Load Balancer or Dropbox Bandaid](./en/182-designing-l7-load-balancer.md)              |

## System Design Theories

**Foundations**

- [Introduction to Architecture](./en/145-introduction-to-architecture.md)
- [How to scale a web service?](./en/41-how-to-scale-a-web-service.md)
- [Concurrency Model](./en/181-concurrency-models.md)
- [Cloud Design Patterns](./en/2018-07-10-cloud-design-patterns.md)
- [Public API Choices](./en/66-public-api-choices.md)
- [Load Balancer Types](./en/2018-07-23-load-balancer-types.md)
- How to do capacity planning? _(coming soon)_

**Data and consistency**

- [ACID vs BASE](./en/2018-07-26-acid-vs-base.md)
- [Data Partition and Routing](./en/2018-07-21-data-partition-and-routing.md)
- [Replica, Consistency, and CAP theorem](./en/2018-07-24-replica-and-consistency.md)
- [Improving availability with failover](./en/85-improving-availability-with-failover.md)
- [Intro to Relational Database](./en/80-relational-database.md)
- [4 Kinds of No-SQL](./en/78-four-kinds-of-no-sql.md)
- [Key value cache](./en/122-key-value-cache.md)
- [Stream and Batch Processing Frameworks](./en/137-stream-and-batch-processing.md)
- [Lambda Architecture](./en/83-lambda-architecture.md)

**Data structures**

- [Bloom Filter](./en/68-bloom-filter.md)
- [Skiplist](./en/69-skiplist.md)
- [B tree vs. B+ tree](./en/2018-07-22-b-tree-vs-b-plus-tree.md)

**AI systems**

- [Agent System Layers and Logical Components](./en/2026-10-22-agent-system-layers-and-logical-components.md)
- [LLM Inference Stack](./en/2026-10-24-llm-inference-stack.md)
- [Designing an LLM Architecture](./en/2026-11-01-designing-an-llm-architecture.md)

**Engineering craft**

- [3 Programming Paradigms](./en/11-three-programming-paradigms.md)
- [SOLID Design Principles](./en/12-solid-design-principles.md)
- [iOS Architecture Patterns Revisited](./en/123-ios-architecture-patterns-revisited.md)

## Prepare for an Interview effectively

- [Crack the system design interview](./en/2016-02-13-crack-the-system-design-interview.md)
- [What can we communicate in soft skills interview?](./en/63-soft-skills-interview.md)
- [Experience Deep Dive](./en/2018-07-20-experience-deep-dive.md)
- Introduction to software engineer interview _(coming soon)_
- How to crack the coding interview, for real? _(coming soon)_
- Culture fit _(coming soon)_
- Be a software engineer - a hero's journey _(coming soon)_

## Read in your language

- 🇺🇸 English: you are here
- 🇨🇳 [简体中文](./zh-CN/README.md)

## About the author

Tian Pan is a software engineer and engineering manager who has worked in the San Francisco Bay Area for 10+ years, at Uber, Oracle, IoTeX, and Microsoft. More notes live at [tianpan.co](https://tianpan.co).

## Community and contributing

- 💬 Join the discussion on [Telegram](https://t.me/system_design_and_architecture) or [Discord](https://discord.gg/Pb5YbK3ykN).
- 🐛 Found a typo, a broken diagram, or a gap in a design? Open an issue or send a PR.
- 🌐 Translations are welcome. Chapters in `en/` and `zh-CN/` use identical filenames.

## License

GPL v3

Found this useful? ⭐ Star the repo. Spotted a gap? Open a PR.
