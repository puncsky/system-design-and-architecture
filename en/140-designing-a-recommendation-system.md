---
layout: post
title: "Toutiao Recommendation System: P1 Overview"
date: 2019-02-19 01:33
comments: true
categories: system design
language: en
references:
  - https://medium.com/@impxia/newsfeed-system-behind-toutiao-2c2454a6d23d
  - https://36kr.com/p/5114077
---

## What are we optimizing for? User Satisfaction
We are finding the best  `function` below to maximize `user satisfaction` .

```txt
user satisfaction = function(content, user profile, context)
```

1. Content: features of articles, videos, UGC short videos, Q&As, etc.
2. User profile: interests, occupation, age, gender and behavior patterns, etc.
3. Context: Mobile users in contexts of workspace, commuting, traveling, etc.



## How to evaluate the satisfaction?

1. Measurable Goals, e.g.
	* click through rate
	* Session duration
	* upvotes
	* comments
	* reposts


2. Hard-to-measurable Goals: 
	* Frequency control of ads and special-typed contents (Q&A)
	* Frequency control of vulgar content
	* Reducing clickbait, low quality, disgusting content
	* Enforcing / pining / highly-weighting important news
	* Lowly-weighting contents from low-level accounts



## How to optimize for those goals? Machine Learning Models
It is a typical supervised machine learning problem to find the best `function`  above. To implement the system, we have these algorithms:

1. Collaborative Filtering
2. Logistic Regression
3. DNN
4. Factorization Machine
5. GBDT


A world-class recommendation system is supposed to have the **flexibility** to A/B-test and combine multiple algorithms above. It is now popular to combine LR and DNN. Facebook used both LR and GBDT years ago.



## How do models observe and measure the reality? Feature engineering

1. *Correlation, between content’s characteristic and user’s interest.* Explicit correlations include keywords, categories, sources, genres. Implicit correlations can be extract from user’s vector or item’s vector from models like FM.
2. *Environmental features such as geo location, time.* It’s can be used as bias or building correlation on top of it.


3. *Hot trend.* There are global hot trend, categorical hot trend, topic hot trend and keyword hot trend. Hot trend is very useful to solve cold-start issue when we have little information about user.
4. *Collaborative features, which helps avoid situation where recommended content get more and more concentrated.* Collaborative filtering is not analysing each user’s history separately, but finding users’ similarity based on their behaviour by clicks, interests, topics, keywords or event implicit vectors. By finding similar users, it can expand the diversity of recommended content.



## Large-scale Training in Realtime

* Users like to see news feed updated in realtime according to what we track from their actions.
* Use Apache storm to train data (clicks, impressions, faves, shares) in realtime.
* Collect data to a threshold and then update to the recommendation model
* Store  model parameters , like tens of billions of raw features and billions of  vector features, in high performance computing clusters.


They are implemented in the following steps:

1. Online services record features in realtime.
2. Write data into Kafka
3. Ingest data from Kafka to Storm
4. Populate full user profiles and  prepare samples
5. Update model parameters according to the latest samples
6. Online modeling gains new knowledge




## How to further reducing the latency? Recall Strategy

It is impossible to predict all the things with the model, considering the super-large scale of all the contents. Therefore, we need recall strategies to focus on a representative subset of the data. Performance is critical here and timeout is 50ms.

![recall strategy](https://res.cloudinary.com/dohtidfqh/image/upload/v1554489731/web-guiguio/recall-strategy_1.png)


Among all the recall strategies, we take the `InvertedIndex<Key, List<Article>> `.

The `Key` can be topic, entity, source, etc.

| Tags of Interests | Relevance | List of Documents |
|---   |---   |---   |
| E-commerce | 0.3| … |
| Fun | 0.2| … |
| History | 0.2|  … |
| Military | 0.1| … |



## Data Dependencies

* Features depends on tags of user-side and content-side.
* recall strategy depends on tags of user-side and content-side.
* content analysis and data mining of user tags are cornerstone of the recommendation system.




## What is the content analysis? 

content analysis = derive intermediate data from raw articles and user behaviors. 

Take articles for example. To model user interests, we need to tag contents and articles. To associate a user with the interests of the “Internet” tag, we need to know whether a user reads an article with the “Internet” tag.



## Why are we analyzing those raw data?

We do it for the reason of …

1. Tagging users (user profile)
    * Tagging users who liked articles with “Internet” tag. Tagging users who liked articles with “xiaomi” tag.
2. Recommending contents to users by tags
    * Pushing “meizu” contents to users with “meizu” tag. Pushing “dota” contents to users with “dota” tag.
3. Preparing contents by topics
    * Put “Bundesliga”  articles to  “Bundesliga topic”. Put “diet” articles to “diet topic”.



## Case Study: Analysis Result of an Article

Here is an example of “article features” page. There are article features like categorizations, keywords, topics, entities.

![Analysis Result of an Article](https://res.cloudinary.com/dohtidfqh/image/upload/v1555019221/web-guiguio/toutiao-article-analysis-features.jpg)


![Analysis Result of an Article: Details](https://res.cloudinary.com/dohtidfqh/image/upload/v1555020387/web-guiguio/toutiao-article-analysis-features-detailed.jpg)

What are the article features? 

1. Semantic Tags: Human predefine those tags with explicit meanings.
2. Implicit Semantics, including topics and keywords. Topic features are describing the statistics of words. Certain rules generate keywords.


4. Similarity. Duplicate recommendation once to be the most severe feedbacks we get from our customers. 
5. Time and location. 
6. Quality. Abusing, porn, ads, or “chicken soup for the soul”?



## Article features are important

* It is not true that a recommendation system cannot work at all without article features. Amazon, Walmart, Netflix can recommend by collaborative filtering. 
* **However, in news product, users consume contents of the same day. Bootstrapping without article features is hard. Collaborative filtering cannot help with bootstrapping.**
    * The finer of the granularity of the article feature, the better the ability to bootstrap.



## More on Semantic Tags

We divide features of semantic tags into three levels:

1. Categorizations: used in the user profile, filtering contents in topics, recommend recall, recommend features
2. Concepts: used in filtering contents in topics, searching tags, recommend recall(like)
3. Entities: used in filtering contents in topics, searching tags, recommend recall(like)


Why dividing into different levels? We do this so that they can capture articles in different granularities. 

1. Categorizations: full in coverage, low in accuracy.
2. Concepts: medium in coverage, medium in accuracy.
3. Entities: low in coverage, high in accuracy. It only covers hot people, organizations, products in each area.


Categorizations and concepts are sharing the same technical infrastructure.


Why do we need semantic tags? 

* Implicit semantics 
    * have been functioning well.
    * cost much less than semantic tags.
* But, topics and interests need a clear-defined tagging system.
* Semantic tags also evaluate the capability in NPL technology of a company.



## Document classification 

Classification hierarchy

1. Root
2. Science, sports, finance, entertainment
3. Football, tennis, table tennis, track and field, swimming
4. International, domestic
5. Team A, team B


Classifiers:

* SVM
* SVM + CNN
* SVM + CNN + RNN



## Calculating relevance 
1. Lexical analysis for articles
2. Filtering keywords
3. Disambiguation
4. Calculating relevance
