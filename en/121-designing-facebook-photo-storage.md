---
layout: post
title: "Designing Facebook photo storage"
date: 2019-01-04 12:11
comments: true
categories: system design
language: en
references:
  - https://www.usenix.org/conference/osdi10/finding-needle-haystack-facebooks-photo-storage
  - https://www.facebook.com/notes/facebook-engineering/needle-in-a-haystack-efficient-storage-of-billions-of-photos/76191543919
---

## Motivation & Assumptions

* PB-level Blob storage
* Traditional NFS based desgin (Each image stored as a file) has metadata bottleneck: large metadata size severely limits the metadata hit ratio.
	* Explain more about the metadata overhead

> For the Photos application most of this metadata, such as permissions, is unused and thereby wastes storage capacity. Yet the more significant cost is that the file’s metadata must be read from disk into memory in order to find the file itself. While insignificant on a small scale, multiplied over billions of photos and petabytes of data, accessing metadata is the throughput bottleneck.



## Solution

Eliminates the metadata overhead by aggregating hundreds of thousands of images in a single haystack store file.



## Architecture

![Facebook Photo Storage Architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-architecture.png)



## Data Layout

index file (for quick memory load) + haystack store file containing needles.

index file layout
![index file layout 1](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-index-file-1.jpg)


![index file layout 2](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-storage-file.jpg)


haystack store file

![haystack store file](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-storage-file.jpg)



### CRUD Operations

* Create: write to store file and then ==async== write index file, because index is not critical
* Read: read(offset, key, alternate_key, cookie, data_size)
* Update: Append only. If the app meets duplicate keys, then it can choose one with largest offset to update.
* Delete: soft delete by marking the deleted bit in the flag field. Hard delete is executed by the compact operation.



## Usecases

Upload

![Photo Storage Upload](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-upload.png)


Download

![Photo Storage Download](https://res.cloudinary.com/dohtidfqh/image/upload/v1546633724/web-guiguio/facebook-photo-storage-download.png)
