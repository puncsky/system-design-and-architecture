---
layout: post
title: "如何使用HTTP协议向移动设备传输视频? HTTP Live Streaming (HLS)"
date: 2019-01-14 18:58
comments: true
categories: interview, system design
language: zh-cn
abstract: 使用HTTP直播流的移动视频播放服务有以下两个问题：手机的内存和外存有限;受制于不稳定的网络连接以及不同的带宽，需要在传输过程中动态调整传输视频的质量。我们可以通过服务器层面和客户端两个层面解决。
references:
  - https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/StreamingMediaGuide/HTTPStreamingArchitecture/HTTPStreamingArchitecture.html#//apple_ref/doc/uid/TP40008332-CH101-SW2
---

## 为什么需要这样一个协议？

使用HTTP直播流的移动视频播放服务有以下问题：

1. ==手机的内存和外存有限==。
2. 受制于不稳定的网络连接以及不同的带宽，需要==在传输过程中动态调整传输视频的质量==。



## 解决方法

1. 服务器层面：在典型的设置中，编码硬件接受音视频输入，将其编码为H.264格式的视频和ACC格式的音频，然后将他们以MPEG-2格式流输出。
   1. 其后通过一个软件分流器将原始输出流分割为一系列短媒体文件（长度可能为10s的.ts文件）。
   2. 分流器同时也会维护一个包含所有媒体文件列表的索引文件（.m3u8格式）。
   3. 将以上步骤生成的媒体文件和索引文件发布在网络服务器上。
2. 客户端层面：客户端读取索引，然后向服务器顺序请求所需要的媒体文件，并且流畅地将各个短媒体文件的内容播放出来。



## 架构

![HLS Architecture](https://puncsky.com/img/hls-architecture.png)
