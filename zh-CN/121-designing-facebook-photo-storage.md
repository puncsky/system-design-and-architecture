---
slug: 121-designing-facebook-photo-storage
id: 121-designing-facebook-photo-storage
layout: post
title: "设计 Facebook 照片存储"
date: 2019-01-04 12:11
comments: true
categories: 系统设计
language: cn
abstract: "传统的基于 NFS 的设计存在元数据瓶颈：大的元数据大小限制了元数据命中率。Facebook 照片存储通过将数十万张图像聚合在一个单一的 haystack 存储文件中，消除了元数据。"
references:
  - https://www.usenix.org/conference/osdi10/finding-needle-haystack-facebooks-photo-storage
  - https://www.facebook.com/notes/facebook-engineering/needle-in-a-haystack-efficient-storage-of-billions-of-photos/76191543919
---

## 动机与假设

* PB 级 Blob 存储
* 传统的基于 NFS 的设计（每张图像存储为一个文件）存在元数据瓶颈：大的元数据大小严重限制了元数据命中率。
	* 进一步解释元数据开销

> 对于照片应用，大部分元数据（如权限）未被使用，从而浪费了存储容量。然而，更重要的成本在于，文件的元数据必须从磁盘读取到内存中，以便找到文件本身。在小规模上这并不显著，但在数十亿张照片和 PB 级数据的情况下，访问元数据成为了吞吐量瓶颈。



## 解决方案

通过将数十万张图像聚合在一个单一的 haystack 存储文件中，消除了元数据开销。



## 架构

![Facebook 照片存储架构](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-architecture.png)



## 数据布局

索引文件（用于快速内存加载）+ 包含针的 haystack 存储文件。

索引文件布局
![索引文件布局 1](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-index-file-1.jpg)


![索引文件布局 2](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-storage-file.jpg)


haystack 存储文件

![haystack 存储文件](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-storage-file.jpg)



### CRUD 操作

* 创建：写入存储文件，然后 ==异步== 写入索引文件，因为索引不是关键的
* 读取：read(offset, key, alternate_key, cookie, data_size)
* 更新：仅追加。如果应用程序遇到重复键，则可以选择具有最大偏移量的一个进行更新。
* 删除：通过在标志字段中标记删除位进行软删除。硬删除通过压缩操作执行。



## 用例

上传

![照片存储上传](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-upload.png)


下载

![照片存储下载](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-download.png)