---
layout: post
title: "How to stream video over HTTP for mobile devices? HTTP Live Streaming (HLS)"
date: 2018-09-07 21:32
comments: true
categories: system design
language: en
references:
  - https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/StreamingMediaGuide/HTTPStreamingArchitecture/HTTPStreamingArchitecture.html#//apple_ref/doc/uid/TP40008332-CH101-SW2
---

## Motivation

Video service over Http Live Streaming for mobile devices, which...

1. ==has limited memory/storage==
2. suffers from the unstable network connection and variable bandwidth, and needs ==midstream quality adjustments.==



## Solution

1. Server-side: In a typical configuration, a hardware encoder takes audio-video input, encodes it as H.264 video and AAC audio, and outputs it in an MPEG-2 Transport Stream

    1. the stream is then broken into a series of short media files (.ts possibly 10s) by a software stream segmenter.
    2. The segmenter also creates and maintains an index(.m3u8) file containing a list of the media files.
    3. Both the media fils and the index files are published on the web server.

2. Client-side: client reads the index, then requests the listed media files in order and displays them without any pauses or gaps between segments.



## Architecture

![HLS Architecture](/img/hls-architecture.png)
