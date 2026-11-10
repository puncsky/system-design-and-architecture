---
slug: 121-designing-facebook-photo-storage
id: 121-designing-facebook-photo-storage
title: "Designing Facebook photo storage"
date: 2019-01-04 12:11
comments: true
tags: [system design]
description: "Traditional NFS based design has metadata bottleneck: large metadata size limits the metadata hit ratio. Facebook photo storage eliminates the metadata by aggregating hundreds of thousands of images in a single haystack store file."
references:
  - https://www.usenix.org/conference/osdi10/finding-needle-haystack-facebooks-photo-storage
  - https://www.facebook.com/notes/facebook-engineering/needle-in-a-haystack-efficient-storage-of-billions-of-photos/76191543919
---

## Motivation & Assumptions

- PB-level Blob storage
- Traditional NFS based desgin (Each image stored as a file) has metadata bottleneck: large metadata size severely limits the metadata hit ratio.
  - Explain more about the metadata overhead

> For the Photos application most of this metadata, such as permissions, is unused and thereby wastes storage capacity. Yet the more significant cost is that the file’s metadata must be read from disk into memory in order to find the file itself. While insignificant on a small scale, multiplied over billions of photos and petabytes of data, accessing metadata is the throughput bottleneck.

## Solution

Eliminates the metadata overhead by aggregating hundreds of thousands of images in a single haystack store file.

## Architecture

![NFS-based Facebook photo storage architecture](../images/fb-photo-storage-architecture.svg)

## Data Layout

index file (for quick memory load) + haystack store file containing needles.

index file layout
![Haystack index file layout](../images/fb-photo-storage-index-file.svg)

![Haystack store file layout](../images/fb-photo-storage-store-file.svg)

haystack store file

![Haystack store file layout](../images/fb-photo-storage-store-file.svg)

### CRUD Operations

- Create: write to store file and then ==async== write index file, because index is not critical
- Read: read(offset, key, alternate_key, cookie, data_size)
- Update: Append only. If the app meets duplicate keys, then it can choose one with largest offset to update.
- Delete: soft delete by marking the deleted bit in the flag field. Hard delete is executed by the compact operation.

## Usecases

Upload

![Photo storage upload flow](../images/fb-photo-storage-upload.svg)

Download

![Photo storage download flow](../images/fb-photo-storage-download.svg)
