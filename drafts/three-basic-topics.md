## Appendix: Three Basic Topics

> Here are three basic topics that could be discussed during the interview.

### Communication

How do different microservices interact with each other? -- communication protocols.

Here is a simple comparison of those protocols.

- UDP and TCP are both transport layer protocols. TCP is reliable and connection-based. UDP is connectionless and unreliable.
- HTTP is in the application layer and is TCP-based since HTTP assumes a reliable transport.
- RPC, a session layer (or application layer in TCP/IP layer model) protocol, is an inter-process communication that allows a computer program to cause a subroutine or procedure to execute in another machine, like a function call.

##### Further discussions

Since RPC is super useful, some interviewers may ask how RPC works. The following picture is a brief answer.


<p align="middle"><img src="https://puncsky.github.io/images/crack-the-system-design-interview/rpc.png" alt="RPC"></p>

* Stub procedure: a local procedure that marshals the procedure identifier and the arguments into a request message, and then to send via its communication module to the server. When the reply message arrives, it unmarshals the results.

We do not have to implement our own RPC protocols. There are off-the-shelf frameworks, like gRPC, Apache Thrift, and Apache Avro.

- gRPC: a cross-platform open source high performance RPC framework developed by Google.
- Apache Thrift: supports more languages, richer data structures: list, set, map, etc. that Protobuf does not support) Incomplete documentation and hard to find good examples.
    - User case: Hbase/Cassandra/Hypertable/Scrib/..
- Apache Avro: Avro is heavily used in the hadoop ecosystem and based on dynamic schemas in Json. It features dynamic typing, untagged data, and no manually-assigned field IDs.

Generally speaking, RPC is internally used by many tech companies for its great performance; however, it is rather hard to debug or may have compatibility issues in different environments. So for public APIs, we tend to use HTTP APIs, and are usually following the RESTful style.

- REST (Representational state transfer of resources)
    - Best practice of HTTP API to interact with resources.
    - URL only decides the location. Headers (Accept and Content-Type, etc.) decide the representation. HTTP methods(GET/POST/PUT/DELETE) decide the state transfer.
    - minimize the coupling between client and server (a huge number of HTTP infras on various clients, data-marshalling).
    - stateless and scaling out.
    - service partitioning feasible.
    - used for public API.

Learn more in [public API choices](66-public-api-choices.md).

### Storage

#### Relational Database

The relational database is the default choice for most use cases because of ACID (atomicity, consistency, isolation, and durability). One tricky thing is **consistency -- it means that any transaction will bring the database from one valid state to another, (different from the consistency in CAP** in the distributed system.

##### Schema Design and 3rd Normal Form (3NF)

To reduce redundancy and improve consistency, people follow 3NF when designing database schemas:

- 1NF: tabular, each row-column intersection contains only one value
- 2NF: only the primary key determines all the attributes
- 3NF: only the candidate keys determine all the attributes (and non-prime attributes do not depend on each other)

##### Db Proxy

What if we want to eliminate single point of failure? What if the dataset is too large for one single machine to hold? For MySQL, the answer is to use a DB proxy to distribute data, [either by clustering or by sharding](http://dba.stackexchange.com/questions/8889/mysql-sharding-vs-mysql-cluster ).

Clustering is a decentralized solution. Everything is automatic. Data is distributed, moved, rebalanced automatically. Nodes gossip with each other, (though it may cause group isolation).

Sharding is a centralized solution. If we get rid of properties of clustering that we don't like, sharding is what we get. Data is distributed manually and does not move. Nodes are not aware of each other.

#### NoSQL

In a regular Internet service, the read write ratio is about 100:1 to 1000:1. However, when reading from a hard disk, a database join operation is time consuming, and 99% of the time is spent on disk seek. Not to mention a distributed join operation across networks.

To optimize the read performance, **denormalization** is introduced by adding redundant data or by grouping data. These four categories of NoSQL are here to help.

##### Key-value Store

The abstraction of a KV store is a giant hashtable/hashmap/dictionary.

The main reason we want to use a key-value cache is to reduce latency for accessing active data. Achieve an O(1) read/write performance on a fast and expensive media (like memory or SSD), instead of a traditional O(logn) read/write on a slow and cheap media (typically hard drive).

There are three major factors to consider when we design the cache.

1. Pattern: How to cache? is it read-through/write-through/write-around/write-back/cache-aside?
2. Placement: Where to place the cache? client side/distinct layer/server side?
3. Replacement: When to expire/replace the data? LRU/LFU/ARC?

Out-of-box choices: Redis/Memcache? Redis supports data persistence while memcache does not. Riak, Berkeley DB, HamsterDB, Amazon Dynamo, Project Voldemort, etc.

##### Document Store

The abstraction of a document store is like a KV store, but documents, like XML, JSON, BSON, and so on, are stored in the value part of the pair.

The main reason we want to use a document store is for flexibility and performance. Flexibility is obtained by schemaless document, and performance is improved by breaking 3NF. Startup's business requirements are changing from time to time. Flexible schema empowers them to move fast.

Out-of-box choices: MongoDB, CouchDB, Terrastore, OrientDB, RavenDB, etc.

##### Column-oriented Store

The abstraction of a column-oriented store is like a giant nested map: ColumnFamily<RowKey, Columns<Name, Value, Timestamp>>.

The main reason we want to use a column-oriented store is that it is distributed, highly-available, and optimized for write.

Out-of-box choices: Cassandra, HBase, Hypertable, Amazon SimpleDB, etc.

##### Graph Database

As the name indicates, this database's abstraction is a graph. It allows us to store entities and the relationships between them.

If we use a relational database to store the graph, adding/removing relationships may involve schema changes and data movement, which is not the case when using a graph database. On the other hand, when we create tables in a relational database for the graph, we model based on the traversal we want; if the traversal changes, the data will have to change.

Out-of-box choices: Neo4J, Infinitegraph, OrientDB, FlockDB, etc.

### CAP Theorem

When we design a distributed system, **trading off among CAP (consistency, availability, and partition tolerance)** is almost the first thing we want to consider.

- Consistency: all nodes see the same data at the same time
- Availability: a guarantee that every request receives a response about whether it succeeded or failed
- Partition tolerance: system continues to operate despite arbitrary message loss or failure of part of the system

In a distributed context, the choice is between CP and AP. Unfortunately, CA is just a joke because a single point of failure is never a choice in the real distributed systems world.

To ensure consistency, there are some popular protocols to consider: 2PC, eventual consistency (vector clock + RWN), Paxos, [In-Sync Replica](http://www.confluent.io/blog/hands-free-kafka-replication-a-lesson-in-operational-simplicity/), etc.

To ensure availability, we can add replicas for the data. As to components of the whole system, people usually do [cold standby, warm standby, hot standby, and active-active](https://www.ibm.com/developerworks/community/blogs/RohitShetty/entry/high_availability_cold_warm_hot?lang=en) to handle the failover.
