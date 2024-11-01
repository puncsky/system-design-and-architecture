---
slug: 162-designing-smart-notification-of-stock-price-changes
id: 162-designing-smart-notification-of-stock-price-changes
layout: post
title: "设计股票价格变动的智能通知"
date: 2019-08-13 12:21
comments: true
categories: system design
slides: false
---

## 需求

- 300 万用户
- 5000 支股票 + 250 支全球股票
- 用户在以下情况下会收到价格变动通知：
    1. 订阅该股票
    1. 股票价格变动达到 5% 或 10%
    1. 自 a) 上周或 b) 昨天以来
- 可扩展性。可能支持其他类型的通知，如突发新闻、财报电话会议等。

## 构建架构草图

上下文：
  * 什么是清算？清算是金融交易结算的程序——即资金及时准确地转移给卖方，证券转移给买方。通常，清算由一个称为清算所的专业组织作为中介。
  * 什么是证券交易所？一个股票经纪人和交易者可以买卖证券的场所。

<svg
xmlns="http://www.w3.org/2000/svg"
xmlnsXlink="http://www.w3.org/1999/xlink"
version="1.1"
width="100%"
height="100%"
viewBox="-0.5 -0.5 749 424"
content='<mxfile modified="2019-08-13T20:36:13.011Z" host="www.draw.io" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36" etag="pxUH_iOYvXXWOA2Ql9Aj" version="11.1.4" type="google"><diagram id="zNECO6JhliZ6oZAxU33_" name="Page-1">7Vxdc9o4FP01zOw+JGNLtoFHSEjabtPSpttunzrCCKPGWIwsB+ivX8nIgC2VmIKxmUkegn0t2+Kee+6XlLTgzWx5z9B8+kDHOGwBa7xswdsWALbd8cSHlKzWEs9TgoCRsRq0FTySX1gJLSVNyBjHuYGc0pCTeV7o0yjCPs/JEGN0kR82oWH+rXMUYE3w6KNQl34jYz5dSzuutZW/wSSYZm+2LXVlhrLBShBP0ZgudkRw0II3jFK+Ppotb3AolZfpZX3f3W+ubibGcMTL3BD/mHx9XgT/vPvgryadz2+f46fZFXDU5Pgq+8Z4LBSgTinjUxrQCIWDrbTPaBKNsXysJc62Y95TOhdCWwh/Ys5XCk2UcCpEUz4L1VW8JPy/nePv8lHXrjq7Xaonpyer7CTibLW5SZ7s3CVPt7elZ7n7hpiRGeaYKaGuO6XOmCbMx3sUltkgYgHme8YpK5fK3HmBQuYeUzEbthIDGA4RJ895a0PKaIPNuC2u4kBBewDM6rnPKEzUm3rzucASWMMknoqPD5STCfHFVGgk1YDZMxF6AF4ovmR/xMRRII/+6g0/xH9rNpO3iMWUcPw4R6kiF8Iv5NH/rfKfMeN4uVdd6qqXkUp5FehBYQipZLFlqZ2Nmu4w1LMq0jFwX6l0EJXARVIJaFS6pzRIuXRHGB6hWB7ehDQZi88HHMcoIFFgoNLdzUPzmOQ4DWCS98qkg5gEL5JJUGPSYIaIvO1xHX5inTS9b4/y+kD+Fi+NcTROE0lwh7nfODK5oAFksjW1NJ1M1mFk+nPeOCV5AxrFGwBeET0WUbtZiMJXRI9FFDYKUdiuE9Etit93rryE6BbEzV31IurWBSmxRvHH5PvTu+Wb+bsfV++jz+FHQw1dB8RnCHbtRjHJ0dQepb0KkTbXne453ULt5JrSPc+Q7TlVZXuunlMvRYUhLExIv4psmTJDVq1LHhB7ElYCrCFbJ+I1q1qrUi1Nzx1TVt2uSM/dC3cGXkln0GmUL/A0rX+mIxJNKZW9lt58roEgLYz4QqVohMMhjUna4IS3I8o5neW1mY3thSSQY7hEoY/UmS90LEv1fswZfcI3NKSycI9oJKGckDDMRC0ALas/uANy8BTN5VRmy0Cuj1yjXwnD1zMx6xD/iLMyF/bnlMjHD57FW+LT0QZ2ujneAKdj8FAQZMJd7rhV+ShoaTBdWG60zYZOnRu1LzNItzVi9oZvheAecbxAq9rDB/SszMSzCGKZYnXXEENgVTywX3nwUtx5kQfNokFHj09YGGm6IjBkdNkIIuRoAI0B4bw0qHUJ2mr9QfPjwG7/n9PALrvcXFupbJ52rQs4zfZspSG1m9V1tvUYP0Lcl5sHFky4LQ1x4ZF4HiCGY/ILjdIBVpb0pvN0+y331pRsF3PyGRmPU2sJZULfR/5TkNrNTu49SX+MGO01Vs2JbjYVqSm3dvftmJzrlXWtbiwNiXrWUGpiZwidTGJZfhcw27zyCBj1NtacGbd6CL0/NaDJYruFxM3YZGmfs8mSMXNHh1/IDF+Jeo7IXol1a+iokGgSJktxUdipUAmTc5niRG+tZCWjvwqJ0DR7WcujNSTvRxvBhhcfEy6egk8IBywscXbsskuc7crw0LteX4TxSt8pvpicvBhgzUikK1t3Ui+W90pU3lWZ0Muz6BS4WO1ihWPcyeEYgAGVrT3XU+GcOqbXEKoLcSHrgrqFNmjXyT9inX2ou7bg9RiTRfhmmAq8pd/jeoWtpYXxdnfveHGwnsFJI5ljiGTCAVMmSZjqGo0vNinJmHN8UmJdg24b5uDJ9jMca4150DcdluqTGHh5u5bPV190Szqt0y+vms0EOnk78WCnaCnruR7ttopvctrOXrelzQyAM7itjNmXunRU3sC6lRjYwcGsXQhOcH8wA1133/hqrCJT6stl2UIW3Q2oywBoXF0Ga2HSZbSdQNmVJdiwrXF62+nfWJq/9ShQIVFQ/94Ew+KSW3tXHerZsaaoZncaYKeoVtc2uRjX5GLcqtSqtxrOqVZGOVI7GK66J+ocOFYnr2VjR8ek5U5lxqsvpBX+QO1TgpMyLecL7ebotu+5pftslbVzoJ6k8KkwSR6mDtlHIjG5MCcDvGI7E5TLYapyME6tW8GbncM4oGQOYzcrh3HqaVc0GJ+TV4bH4QM0v+YzGv2kIw238+97LezXaJcLzdA7WFfidPvPCNZ17fZfOsDB/w==</diagram></mxfile>'
style={{ backgroundColor: "rgb(255, 255, 255)" }}
>
  <defs />
  <g>
    <path
      d="M 720 146 L 740 146 L 740 26 L 408.37 26"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 403.12 26 L 410.12 22.5 L 408.37 26 L 410.12 29.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={600}
      y="115.5"
      width={120}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(601.5,125.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={116}
          height={40}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 116,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              苹果推送通知服务
              <br />
              (APNs)
            </div>
          </div>
        </foreignObject>
        <text
          x={58}
          y={26}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          苹果推送通知服务&lt;br&gt;(APNs)
        </text>
      </switch>
    </g>
    <path
      d="M 720 226 L 740 226 L 740 26 L 408.37 26"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 403.12 26 L 410.12 22.5 L 408.37 26 L 410.12 29.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={600}
      y="195.5"
      width={120}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(601.5,205.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={116}
          height={40}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 116,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              Google Firebase 云消息传递
              <br />
              (FCM)
            </div>
          </div>
        </foreignObject>
        <text
          x={58}
          y={26}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Google Firebase 云消息传递&lt;br&gt;(FCM)
        </text>
      </switch>
    </g>
    <path
      d="M 720 306 L 740 306 L 740 26 L 408.37 26"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 403.12 26 L 410.12 22.5 L 408.37 26 L 410.12 29.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={600}
      y="275.5"
      width={120}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(601.5,285.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={116}
          height={40}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 116,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              电子邮件服务
              <br />
              AWS SES /sendgrid/etc
            </div>
          </div>
        </foreignObject>
        <text
          x={58}
          y={26}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          电子邮件服务&lt;br&gt;AWS SES /sendgrid/etc
        </text>
      </switch>
    </g>
    <path
      d="M 530 226 L 593.63 226"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 598.88 226 L 591.88 229.5 L 593.63 226 L 591.88 222.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 530 226 L 565 226 L 565 146 L 593.63 146"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 598.88 146 L 591.88 149.5 L 593.63 146 L 591.88 142.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 530 226 L 565 226 L 565 306 L 593.63 306"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 598.88 306 L 591.88 309.5 L 593.63 306 L 591.88 302.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 500 246 L 500 374 L 459.37 374"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 454.12 374 L 461.12 370.5 L 459.37 374 L 461.12 377.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 470 226 L 450 226 L 451 226 L 436.87 226"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 431.62 226 L 438.62 222.5 L 436.87 226 L 438.62 229.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={470}
      y="205.5"
      width={60}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(481.5,219.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={36}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 38,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              通知者
            </div>
          </div>
        </foreignObject>
        <text
          x={18}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          通知者
        </text>
      </switch>
    </g>
    <rect
      x={0}
      y={192}
      width={80}
      height={67}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(1.5,198.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={76}
          height={54}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 76,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              外部供应商
              <br />
              <br />
              市场价格
            </div>
          </div>
        </foreignObject>
        <text
          x={38}
          y={33}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          [不支持查看器]
        </text>
      </switch>
    </g>
    <path
      d="M 385 50.5 L 385 76 L 385 94.13"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 385 99.38 L 381.5 92.38 L 385 94.13 L 388.5 92.38 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 398.96 0.51 C 399.66 0.5 400.33 0.81 400.8 1.34 C 401.27 1.88 401.5 2.6 401.43 3.33 L 401.43 47.94 C 401.43 49.35 400.32 50.5 398.96 50.5 L 371.54 50.5 C 370.18 50.5 369.07 49.35 369.07 47.94 L 369.07 3.33 C 369 2.6 369.23 1.88 369.7 1.34 C 370.17 0.81 370.84 0.5 371.54 0.51 Z M 390.81 3.33 L 379.44 3.33 L 379.44 4.86 L 390.81 4.86 Z M 398.71 7.43 L 371.54 7.43 L 371.54 42.55 L 398.71 42.55 Z M 389.82 45.12 L 380.43 45.12 L 380.43 47.94 L 389.82 47.94 L 389.82 45.12 Z M 378.46 20.66 L 385.13 17.17 L 391.8 20.66 L 385.13 24.86 Z M 377.96 22.3 L 384.39 26.4 L 384.39 34.09 L 377.96 29.99 Z M 385.87 26.4 L 392.29 22.3 L 392.29 29.99 L 385.87 34.09 Z"
      fill="#00bef2"
      stroke="none"
      pointerEvents="none"
    />
    <g transform="translate(343.5,57.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={83}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              whiteSpace: "nowrap",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit"
              }}
            >
              Robinhood 应用
            </div>
          </div>
        </foreignObject>
        <text
          x={42}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Robinhood 应用
        </text>
      </switch>
    </g>
    <path
      d="M 386 186 L 386 204.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 386 209.88 L 382.5 202.88 L 386 204.63 L 389.5 202.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x="340.5"
      y="155.5"
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(350.5,164.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={70}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 72,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              API 网关
            </div>
          </div>
        </foreignObject>
        <text
          x={35}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          API 网关
        </text>
      </switch>
    </g>
    <path
      d="M 385 131 L 386 131 L 386 149.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 386 154.88 L 382.5 147.88 L 386 149.63 L 389.5 147.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={340}
      y="100.5"
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(345.5,109.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={78}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 80,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              反向代理
            </div>
          </div>
        </foreignObject>
        <text
          x={39}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          反向代理
        </text>
      </switch>
    </g>
    <path
      d="M 135 226 L 86.37 226"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 81.12 226 L 88.12 222.5 L 86.37 226 L 88.12 229.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 170 246 L 170 327.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 170 332.88 L 166.5 325.88 L 170 327.63 L 173.5 325.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(141.5,280.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={58}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              whiteSpace: "nowrap",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                backgroundColor: "#ffffff"
              }}
            >
              批量写入
            </div>
          </div>
        </foreignObject>
        <text
          x={29}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          批量写入
        </text>
      </switch>
    </g>
    <rect
      x={135}
      y="205.5"
      width={70}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(155.5,212.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={28}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 30,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              价格
              <br />
              监测器
            </div>
          </div>
        </foreignObject>
        <text
          x={14}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          [不支持查看器]
        </text>
      </switch>
    </g>
    <path
      d="M 110 347.5 C 110 328.83 230 328.83 230 347.5 L 230 389.5 C 230 408.17 110 408.17 110 389.5 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 110 347.5 C 110 361.5 230 361.5 230 347.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(115.5,365.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={108}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 110,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              时间序列数据库
              <br />
              influx 或 prometheus
            </div>
          </div>
        </foreignObject>
        <text
          x={54}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          时间序列数据库&lt;br&gt;influx 或 prometheus
        </text>
      </switch>
    </g>
    <g transform="translate(88.5,185.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={38}
          height={40}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 38,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              每 5 分钟一次
            </div>
          </div>
        </foreignObject>
        <text
          x={19}
          y={26}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          [不支持查看器]
        </text>
      </switch>
    </g>
    <path
      d="M 230 246 L 230 312 L 170 312 L 170 327.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 170 332.88 L 166.5 325.88 L 170 327.63 L 173.5 325.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(182.5,304.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={76}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              whiteSpace: "nowrap",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                backgroundColor: "#ffffff"
              }}
            >
              定期读取
            </div>
          </div>
        </foreignObject>
        <text
          x={38}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          定期读取
        </text>
      </switch>
    </g>
    <path
      d="M 275 226 L 320 226 L 320 374 L 366.63 374"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 371.88 374 L 364.88 377.5 L 366.63 374 L 364.88 370.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 250 245.5 L 250 282 L 275 282 L 275 327.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 275 332.88 L 271.5 325.88 L 275 327.63 L 278.5 325.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={205}
      y="205.5"
      width={70}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(218.5,212.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={42}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 44,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              价格
              <br />
              监测器
            </div>
          </div>
        </foreignObject>
        <text
          x={21}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          价格&lt;br&gt;监测器
        </text>
      </switch>
    </g>
    <path
      d="M 386 241 L 386 259.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 386 264.88 L 382.5 257.88 L 386 259.63 L 389.5 257.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x="340.5"
      y="210.5"
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(349.5,219.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={72}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 74,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              用户设置
            </div>
          </div>
        </foreignObject>
        <text
          x={36}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          用户设置
        </text>
      </switch>
    </g>
    <path
      d="M 360.5 274.5 C 360.5 262.5 410.5 262.5 410.5 274.5 L 410.5 301.5 C 410.5 313.5 360.5 313.5 360.5 301.5 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 360.5 274.5 C 360.5 283.5 410.5 283.5 410.5 274.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 388 349.5 C 388 328.17 438 328.17 438 349.5 L 438 397.5 C 438 418.83 388 418.83 388 397.5 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      transform="rotate(-90,413,373.5)"
      pointerEvents="none"
    />
    <path
      d="M 388 349.5 C 388 365.5 438 365.5 438 349.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      transform="rotate(-90,413,373.5)"
      pointerEvents="none"
    />
    <g transform="translate(371.5,407.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={98}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 100,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              通知队列
            </div>
          </div>
        </foreignObject>
        <text
          x={49}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          通知队列
        </text>
      </switch>
    </g>
    <path
      d="M 240 343 C 240 331 310 331 310 343 L 310 370 C 310 382 240 382 240 370 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 240 343 C 240 352 310 352 310 343"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(241.5,349.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={66}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 66,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              限流缓存
            </div>
          </div>
        </foreignObject>
        <text
          x={33}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          限流缓存
        </text>
      </switch>
    </g>
    <path
      d="M 205 163 L 205 184 L 170 184 L 170 199.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 170 204.88 L 166.5 197.88 L 170 199.63 L 173.5 197.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 205 163 L 205 184 L 240 184 L 240 199.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 240 204.88 L 236.5 197.88 L 240 199.63 L 243.5 197.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={180}
      y={127}
      width={50}
      height={36}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(184.5,138.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={40}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Helvetica",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 40,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "center"
            }}
          >
            <div
              xmlns="http://www.w3.org/1999/xhtml"
              style={{
                display: "inline-block",
                textAlign: "inherit",
                textDecoration: "inherit",
                whiteSpace: "normal"
              }}
            >
              cronjob
            </div>
          </div>
        </foreignObject>
        <text
          x={20}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          cronjob
        </text>
      </switch>
    </g>
  </g>
</svg>

## 这些组件是什么，它们如何相互作用？

* 价格监测器 
    * 数据获取策略
      * 选项 1 初步：每 5 分钟获取一次数据，并批量写入时间序列数据库。
      * 选项 2 高级：如今外部系统通常直接推送数据，因此我们不必一直拉取。
    * 每次请求或每次价格变动约 6000 个点。
    * 数据保留 1 周，因为这只是 lambda 架构的加速层。
* 价格观察者
    * 读取过去一周或过去 24 小时内每只股票的数据。
    * 计算波动是否超过 5% 或 10% 在这两个时间段内。我们得到的元组如 (股票, 上涨 5%, 1 周)。
        * 边缘情况：我们是否应该规范化价格数据？例如，某人错误地将 UBER 以 1 美元的价格出售。
    * **速率限制（因为 5% 或 10% 的变化可能在一天内发生多次）**，然后发出事件 `PRICE_CHANGE(STOCK_CODE, timeSpan, percentage)` 到通知队列。
* 定期触发器是 cron 作业，例如 Airflow、Cadence。
* 通知队列
    * 在用户和股票数量较少时，可能不一定会引入。
    * 可能接受通用消息事件，如 `PRICE_CHANGE`、`EARNINGS_CALL`、`BREAKING_NEWS` 等。
* 通知者
    * 订阅通知队列以获取事件
    * 然后从用户设置服务中获取通知对象
    * 最后根据用户设置，通过 APNs、FCM 或 AWS SES 发送消息。