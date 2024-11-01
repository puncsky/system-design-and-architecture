---
slug: 38-how-to-stream-video-over-http
id: 38-how-to-stream-video-over-http
layout: post
title: "如何通过 HTTP 为移动设备流式传输视频？HTTP 实时流媒体 (HLS)"
date: 2018-09-07 21:32
comments: true
categories: 系统设计
description: "移动设备上的 HTTP 视频服务面临两个问题：有限的内存或存储和不稳定的网络连接以及可变的带宽。HTTP 实时流媒体通过关注点分离、文件分段和索引来解决这些问题。"
references:
  - https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/StreamingMediaGuide/HTTPStreamingArchitecture/HTTPStreamingArchitecture.html#//apple_ref/doc/uid/TP40008332-CH101-SW2
---

## 动机

移动设备上的 HTTP 实时流媒体视频服务，...

1. ==内存/存储有限==
2. 遭受不稳定的网络连接和可变带宽的影响，并需要 ==中途质量调整。==



## 解决方案

1. 服务器端：在典型配置中，硬件编码器接收音视频输入，将其编码为 H.264 视频和 AAC 音频，并以 MPEG-2 传输流的形式输出。

    1. 然后，流被软件流分段器分解为一系列短媒体文件（.ts 可能为 10 秒）。
    2. 分段器还创建并维护一个索引（.m3u8）文件，其中包含媒体文件的列表。
    3. 媒体文件和索引文件都发布在网络服务器上。

2. 客户端：客户端读取索引，然后按顺序请求列出的媒体文件，并在段之间无任何暂停或间隙地显示它们。



## 架构

![HLS 架构](/img/hls-architecture.png)