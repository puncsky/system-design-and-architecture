<h1 align="center">System Design and Architecture</h1>

> ⚠️ The 2nd Edition is still a work in progress.

The book *System Design and Architecture* has helped millions of software engineers worldwide to succeed in the Internet industry since 2015. Here is why it works:

1. 🌎 Real-world engineering. It comes from real-world examples of FANNG and many other silicon valley companies. And it outlines how to build real-world Internet products and services.
2. 🍕 Easy to digest. System design at the right level of abstraction is like a map to route you to your destination with the shortest cut. There are charts, diagrams, and step-by-step guides - all for you to acquire the minimum actionable knowledge to excel system design interviews and get started building.
3. 🤲 Full-coverage. It strives to be "the book" for you to master most of the system design use-cases, from backend to frontend and from zero to hero.
4. 🚶‍♀️ 4-step framework. This book approaches and solve problems in a systematic and repeatable way: 1) Clarify requirements 2) Sketch out the high-level design 3) Discuss individual components and how they interact with each other 4) Wrap up with blind spots or bottlenecks.

What's different in the 2nd Edition? From 2015 to 2022, we saw mobile ate the world, cloud-native computing came across Kubernetes, and web3 went through ups and downs. There are always new companies at different stages of their lifecycles taking the lead in the Internet industry. I am interested in how they work, aren't you? So in the 2nd Edition, I will

* add more interesting content with new companies and products.
* rewrite existing content with new trends in the industry.
* add more charts and diagrams with step-by-step guides.
* add a PDF edition of the book.
* deduplicate repetitive content so that each design takes its unique abstraction.

What is out of this book's scope?

* API design for specific domains. Please go to [Google's API design guide](https://cloud.google.com/apis/design).
* Object-oriented design. Its importance is quite overestimated by mediocre engineers.

## How to use this book?

* For professionals (Google L5 or above), go directly to *System Design in Practice*.
* For junior and intermediate programmers (Google L3/L4), go to *System Design Theories* and then read *System Design in Practice*.
* For beginners, go to *Prepare for an Interview effectively*, then read *System Design Theories*, and finally go to *System Design in Practice*.

### System Design in Practice

| Product | Question |
| ---      | ---      | 
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708936/web-guiguio/instagram.png" width="52" />  | [Designing Instagram or Pinterest](./en/2016-02-13-crack-the-system-design-interview.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708917/web-guiguio/uber.png" width="52" />| [Designing Uber](./en/120-designing-uber.md) | |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709369/web-guiguio/facebook.png" width="52" />| [How Facebook Scale its Social Graph Store? TAO](./en/49-facebook-tao.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709414/web-guiguio/netflix.png" width="52" />| [How Netflix Serves Viewing Data?](./en/45-how-to-design-netflix-view-state-service.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709444/web-guiguio/stripe.png" width="52" />| [How to design robust and predictable APIs with idempotency?](./en/43-how-to-design-robust-and-predictable-apis-with-idempotency.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709414/web-guiguio/netflix.png" width="52" />| [How to stream video over HTTP for mobile devices? HTTP Live Streaming (HLS)](./en/38-how-to-stream-video-over-http.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709618/web-guiguio/confluent.png" width="52" />| [Designing a distributed logging system](./en/61-what-is-apache-kafka.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709677/web-guiguio/twitter.png" width="52" />| [Designing a URL shortener](./en/84-designing-a-url-shortener.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709990/web-guiguio/linkedin.png" width="52" />| [Designing a KV store with external storage](./en/97-designing-a-kv-store-with-external-storage.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709823/web-guiguio/memcached.png" width="52" />| [Designing a distributed in-memory KV store or Memcached](./en/174-designing-memcached.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709369/web-guiguio/facebook.png" width="52" />| [Designing Facebook photo storage](./en/121-designing-facebook-photo-storage.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710037/web-guiguio/robinhood.png" width="52" />| [Designing Stock Exchange](./en/161-designing-stock-exchange.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710037/web-guiguio/robinhood.png" width="52" />| [Designing Smart Notification of Stock Price Changes](./en/162-designing-smart-notification-of-stock-price-changes.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710085/web-guiguio/square.png" width="52" />| [Designing Square Cash or PayPal Money Transfer System](./en/167-designing-paypal-money-transfer.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709444/web-guiguio/stripe.png" width="52" />| [Designing payment webhook](./en/166-designing-payment-webhook.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710137/web-guiguio/grafana.jpg" width="52" />| [Designing a metric system](./en/168-designing-a-metric-system.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710354/web-guiguio/tiktok.webp" width="52" />| [Designing a recommendation system](./en/140-designing-a-recommendation-system.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710222/web-guiguio/airbnb.png" width="52" />| [Designing Airbnb or a hotel booking system](./en/177-designing-Airbnb-or-a-hotel-booking-system.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710390/web-guiguio/lyft.png" width="52" />| [Lyft's Marketing Automation Platform -- Symphony](./en/178-lyft-marketing-automation-symphony.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580709990/web-guiguio/linkedin.png" width="52" />| [Designing typeahead search or autocomplete](./en/179-designing-typeahead-search-or-autocomplete.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580710529/web-guiguio/nginx.jpg" width="52" />| [Designing a Load Balancer or Dropbox Bandaid](./en/182-designing-l7-load-balancer.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1580708917/web-guiguio/uber.png" width="52" />| [Fraud Detection with Semi-supervised Learning](./en/136-fraud-detection-with-semi-supervised-learning.md) |
| <img src="https://res.cloudinary.com/dohtidfqh/image/upload/v1595029150/web-guiguio/favicon-32x32.png" width="52" />| [Designing Online Judge or Leetcode](https://tianpan.co/notes/243-designing-online-judge-or-leetcode) |

### System Design Theories

* [Introduction to Architecture](./en/145-introduction-to-architecture.md)
* [How to scale a web service?](./en/41-how-to-scale-a-web-service.md)
* [ACID vs BASE](./en/2018-07-26-acid-vs-base.md)
* [Data Partition and Routing](./en/2018-07-21-data-partition-and-routing.md)
* [Replica, Consistency, and CAP theorem](./en/2018-07-24-replica-and-consistency.md)
* [Load Balancer Types](./en/2018-07-23-load-balancer-types.md)
* [Concurrency Model](./en/181-concurrency-models.md)
* [Improving availability with failover](./en/85-improving-availability-with-failover.md)
* [Bloom Filter](./en/68-bloom-filter.md)
* [Skiplist](./en/69-skiplist.md)
* [B tree vs. B+ tree](./en/2018-07-22-b-tree-vs-b-plus-tree.md)
* [Intro to Relational Database](./en/80-relational-database.md)
* [4 Kinds of No-SQL](./en/78-four-kinds-of-no-sql.md)
* [Key value cache](./en/122-key-value-cache.md)
* [Stream and Batch Processing Frameworks](./en/137-stream-and-batch-processing.md)
* [Cloud Design Patterns](./en/2018-07-10-cloud-design-patterns.md)
* [Public API Choices](./en/66-public-api-choices.md)
* [Lambda Architecture](./en/83-lambda-architecture.md)
* [iOS Architecture Patterns Revisited](./en/123-ios-architecture-patterns-revisited.md)
* [What can we communicate in soft skills interview?](./en/63-soft-skills-interview.md)
* [Experience Deep Dive](./en/2018-07-20-experience-deep-dive.md)
* [3 Programming Paradigms](./en/11-three-programming-paradigms.md)
* [SOLID Design Principles](./en/12-solid-design-principles.md)
* How to do capacity planning?

### Prepare for an Interview effectively

* Introduction to software engineer interview
* How to crack the coding interview, for real?
* How to communicate in the interview?
* Experience deep dive
* Culture fit
* Be a software engineer - a hero's journey

[[Chinese Edition](./zh-CN/README.md)]



## Who's Tian Pan?

Tian Pan has been a high-performing software engineer and engineering manager working in the San Francisco Bay Area for 10 years, previously worked at Uber, Oracle, IoTeX, and Microsoft.

## Join us for further discussion!

* [Telegram](https://t.me/system_design_and_architecture)
* [Discord](https://discord.gg/Pb5YbK3ykN)

---
## License

GPL v3

If you found this resource helpful, give it a 🌟 otherwise contribute to it and give it a ⭐️.
