---
slug: 243-designing-online-judge-or-leetcode
id: 243-designing-online-judge-or-leetcode
title: "Designing Online Judge or Leetcode"
date: 2020-07-14 23:50
comments: true
slides: false
tags: [system design, architecture]
description: An online judge is primarily a place where you can execute code remotely for educational or recruitment purposes. In this design, we focus on designing an OJ for interview preparation like Leetcode.
audio: https://anchor.fm/tian-pan/embed/episodes/Designing-Online-Judge-or-Leetcode-egninc
references:
  - https://minio.judge0.com/public/paper-in-review.pdf
---

## Requirements

An online judge is primarily a place where you can execute code remotely for educational or recruitment purposes. In this design, we focus on designing an OJ for interview preparation like Leetcode, with the following requirements:

- It should have core OJ functionalities like fetching a problem, submitting the solution, compiling if needed, and executing it.
- It should be highly available with an **async** design, since running code may take time.
- It should be horizontal scalable or, saying, easy to scale-out.
- It should be robust and secure to execute untrusted source code.

## Architecture

The architecture below is featured on queueing for async execution and sandboxing for secure execution. And each component is separately deployable and scalable.

![designing online judge system](https://res.cloudinary.com/dohtidfqh/image/upload/v1594706130/web-guiguio/designing-online-judge.png)

## Components

### Presentation Layer

The user agent is usually a web or mobile app like coderoma.com. It displays the problem description and provides the user with a code editor to write and submit code.

When the user submits the code, the client will get a token since it is an async call. Then the client polls the server for the submission status.

### API

Please see [Public API Choices](https://tianpan.co/notes/66-public-api-choices) for the protocols we can choose from. And let’s design the interface itself here and GraphQL for example:

```gql
type Query {
  problems(id: String): [Problem]
  languageSetup(id: String!, languageId: LanguageId!): LanguageSetup
  submission(token: String!) Submission
}

type Mutation {
  createSubmission(
    problemId: String!
    code: String!
    languageId: LanguageId!
  ): CreatedSubmission!
}

enum LanguageId {
  JAVA
  JS
  ELIXIR
  # ...
}


type Problem {
  id: String!
  title: String!
  description: String!
  supportedLanguages: [Float!]!
}

type LanguageSetup {
  languageId: LanguageId!
  template: String!
  solutions: [String!]!
}

type Status {
  id: Float!
  description: String!
}

type Submission {
  compileOutput: String
  memory: Float
  message: String
  status: Status
  stderr: String
  stdout: String
  time: String
  token: String
}

type CreatedSubmission {
  token: String!
}

```

The API layer records the submission in the database, publishes it into the queue, and returns a token for the client's future reference.

### Code Execution Engine

Code execution engine (CEE) polls the queue for the code, uses a sandbox to compile and run the code and parses the metadata from the compilation and execution.

The sandbox could be LXC containers, Docker, virtual machines, etc. We can choose Docker for its ease of deployment.

## Coderoma.com

I am recently learning [Elixir](https://elixir-lang.org/) and creating an online judge [coderoma.com](https://coderoma.com) for my daily practice. It now supports Elixir and JavaScript. And I am adding more languages (like Java) and problems to it.

We may host future events to improve your coding skills. Join us at https://t.me/coderoma for the English community or use your WeChat to scan the following QR `onetptp` and reply `刷题` for the Chinese community.

<img
alt="onetptp"
style={{ height: 250 }}
src="https://res.cloudinary.com/dohtidfqh/image/upload/v1594718876/web-guiguio/onetptp.jpg"
/>
