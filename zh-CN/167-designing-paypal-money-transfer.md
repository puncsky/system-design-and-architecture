---
slug: 167-designing-paypal-money-transfer
id: 167-designing-paypal-money-transfer
layout: post
title: 设计 Square Cash 或 PayPal 转账系统
date: 2019-08-23 17:02
comments: true
categories: 系统设计
language: cn
slides: false
abstract: 设计一个可以接收、发送和支付的转账后端系统。它应涵盖扩展性、国际化、去重、单点故障、强一致性等问题。
references:
  - https://medium.com/airbnb-engineering/scaling-airbnbs-payment-platform-43ebfc99b324
  - https://beancount.io
---

## 澄清需求

设计一个类似于 Square Cash（以下称为 Cash App）或 PayPal 的转账后端系统，以实现：

1. 从银行存款和支付
2. 账户之间转账
3. 高扩展性和可用性
4. 国际化：语言、时区、货币兑换
5. 非幂等 API 和至少一次交付的去重
6. 跨多个数据源的一致性


## 架构

<svg
xmlns="http://www.w3.org/2000/svg"
xmlnsXlink="http://www.w3.org/1999/xlink"
version="1.1"
width="944px"
viewBox="-0.5 -0.5 944 300"
content='<mxfile modified="2019-08-23T22:19:44.443Z" host="www.draw.io" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36" etag="D6R8hmRlifbxjgfwLXy7" pages="1" version="11.2.2" type="google"><diagram id="q0F2OQlhvJY46wws1bqZ" name="Page-1">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</diagram></mxfile>'
onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&&src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&&!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&&evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://www.draw.io/?client=1&lightbox=1&edit=_blank');}}})(this);"
style={{ cursor: "pointer", maxWidth: "100%", maxHeight: 300 }}
>
  <defs />
  <g>
    <rect
      x={610}
      y={269}
      width={100}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(612.5,276.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={94}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 95,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              AWS CloudHSM
            </div>
          </div>
        </foreignObject>
        <text
          x={47}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          AWS CloudHSM
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={0}
      width={160}
      height={282}
      fill="#ffffff"
      stroke="#000000"
      strokeDasharray="3 3"
      pointerEvents="none"
    />
    <g transform="translate(67.5,7.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={113}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 114,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              演示层
            </div>
          </div>
        </foreignObject>
        <text
          x={57}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          演示层
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={26}
      width={160}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,34.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={60}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 61,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              SDK/文档
            </div>
          </div>
        </foreignObject>
        <text
          x={30}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          SDK/文档
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={56}
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,57.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={86}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 86,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              移动仪表板
            </div>
          </div>
        </foreignObject>
        <text
          x={43}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          移动仪表板
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={86}
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,87.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={86}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 86,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              网页仪表板
            </div>
          </div>
        </foreignObject>
        <text
          x={43}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          网页仪表板
        </text>
      </switch>
    </g>
    <path
      d="M 225 86 L 255 86 L 255 132 L 277.63 132"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 282.88 132 L 275.88 135.5 L 277.63 132 L 275.88 128.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={155}
      y={56}
      width={70}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(157.5,72.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={70}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 70,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              仪表板客户端
            </div>
          </div>
        </foreignObject>
        <text
          x={35}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          仪表板客户端
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={139}
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,147.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={81}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 82,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              移动钱包
            </div>
          </div>
        </foreignObject>
        <text
          x={41}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          移动钱包
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={169}
      width={90}
      height={31}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,178.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={65}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 66,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              网页钱包
            </div>
          </div>
        </foreignObject>
        <text
          x={33}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          网页钱包
        </text>
      </switch>
    </g>
    <path
      d="M 225 185 L 255 185 L 255 132 L 277.63 132"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 282.88 132 L 275.88 135.5 L 277.63 132 L 275.88 128.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={155}
      y={139}
      width={70}
      height={91}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(157.5,171.5)">
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
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 66,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              钱包客户端
            </div>
          </div>
        </foreignObject>
        <text
          x={33}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          钱包客户端
        </text>
      </switch>
    </g>
    <ellipse
      cx={30}
      cy={42}
      rx="7.5"
      ry="7.5"
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <path
      d="M 30 49.5 L 30 74.5 M 30 54.5 L 15 54.5 M 30 54.5 L 45 54.5 M 30 74.5 L 15 94.5 M 30 74.5 L 45 94.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(-0.5,102.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={60}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
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
              商户&nbsp;
              <br />
              用户
            </div>
          </div>
        </foreignObject>
        <text
          x={30}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          商户&nbsp;&lt;br&gt;用户
        </text>
      </switch>
    </g>
    <ellipse
      cx={30}
      cy={167}
      rx="7.5"
      ry="7.5"
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <path
      d="M 30 174.5 L 30 199.5 M 30 179.5 L 15 179.5 M 30 179.5 L 45 179.5 M 30 199.5 L 15 219.5 M 30 199.5 L 45 219.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(2.5,227.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={54}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
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
              最终用户
            </div>
          </div>
        </foreignObject>
        <text
          x={27}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          最终用户
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={200}
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,201.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={86}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 86,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              网页 Chrome 扩展
            </div>
          </div>
        </foreignObject>
        <text
          x={43}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          网页 Chrome 扩展
        </text>
      </switch>
    </g>
    <path
      d="M 898.5 133.5 L 843.87 133.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 838.62 133.5 L 845.62 130 L 843.87 133.5 L 845.62 137 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <ellipse
      cx="913.5"
      cy={111}
      rx="7.5"
      ry="7.5"
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <path
      d="M 913.5 118.5 L 913.5 143.5 M 913.5 123.5 L 898.5 123.5 M 913.5 123.5 L 928.5 123.5 M 913.5 143.5 L 898.5 163.5 M 913.5 143.5 L 928.5 163.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(883.5,171.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={60}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
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
              操作员
            </div>
          </div>
        </foreignObject>
        <text
          x={30}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          操作员
        </text>
      </switch>
    </g>
    <path
      d="M 684.87 133.5 L 742.5 133.5"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 679.62 133.5 L 686.62 130 L 684.87 133.5 L 686.62 137 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 639 93.63 L 639 63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 639 98.88 L 635.5 91.88 L 639 93.63 L 642.5 91.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 607 108 C 607 86.67 671 86.67 671 108 L 671 156 C 671 177.33 607 177.33 607 156 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      transform="rotate(-90,639,132)"
      pointerEvents="none"
    />
    <path
      d="M 607 108 C 607 124 671 124 671 108"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      transform="rotate(-90,639,132)"
      pointerEvents="none"
    />
    <path
      d="M 539 132 L 569 132 L 592.63 132"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 597.88 132 L 590.88 135.5 L 592.63 132 L 590.88 128.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 487 152 L 487 245 L 562.63 245"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 567.88 245 L 560.88 248.5 L 562.63 245 L 560.88 241.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 460 152 L 460 178 L 407 178 L 407 198.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 407 203.88 L 403.5 196.88 L 407 198.63 L 410.5 196.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={434}
      y="111.5"
      width={105}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(436.5,125.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={53}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 54,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              支付
            </div>
          </div>
        </foreignObject>
        <text
          x={27}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          支付
        </text>
      </switch>
    </g>
    <path
      d="M 790 84 L 790 104 L 790 94 L 790 107.13"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 790 112.38 L 786.5 105.38 L 790 107.13 L 793.5 105.38 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x="742.5"
      y={44}
      width={95}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(745.5,57.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={68}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 69,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              任务队列
            </div>
          </div>
        </foreignObject>
        <text
          x={34}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          任务队列
        </text>
      </switch>
    </g>
    <rect
      x="742.5"
      y="113.5"
      width={95}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(745.5,120.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={91}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 91,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              财务报告
            </div>
          </div>
        </foreignObject>
        <text
          x={46}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          财务报告
        </text>
      </switch>
    </g>
    <path
      d="M 639 220 L 639 170.37"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 639 165.12 L 642.5 172.12 L 639 170.37 L 635.5 172.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 709 245 L 788.63 245"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 793.88 245 L 786.88 248.5 L 788.63 245 L 786.88 241.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 569 258 L 569 261 L 443.37 261"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 438.12 261 L 445.12 257.5 L 443.37 261 L 445.12 264.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={569}
      y={220}
      width={140}
      height={50}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(571.5,238.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={109}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 110,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              支付网关
            </div>
          </div>
        </foreignObject>
        <text
          x={55}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          支付网关
        </text>
      </switch>
    </g>
    <path
      d="M 873.45 270 C 880.2 269.15 885.01 262.69 884.2 255.57 C 883.39 248.45 877.26 243.38 870.52 244.23 C 870.44 233.6 863.38 224.46 853.52 222.23 C 843.67 220 833.67 225.29 829.48 234.96 C 826.36 231.2 821.42 229.79 816.94 231.36 C 812.46 232.94 809.31 237.2 808.95 242.17 C 801.67 241.89 795.54 247.89 795.27 255.57 C 795 263.25 800.69 269.72 807.98 270 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeWidth="1.95"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(817.5,231.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={43}
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
              银行 /&nbsp;
              <br />
              供应商
            </div>
          </div>
        </foreignObject>
        <text
          x={22}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          [不支持的查看器]
        </text>
      </switch>
    </g>
    <rect
      x={591}
      y="22.5"
      width={95}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(593.5,29.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={91}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 91,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              副作用制造者
            </div>
          </div>
        </foreignObject>
        <text
          x={46}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          副作用制造者
        </text>
      </switch>
    </g>
    <rect
      x={65}
      y={252}
      width={160}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(67.5,260.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={111}
          height={12}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 112,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              帮助服务门户
            </div>
          </div>
        </foreignObject>
        <text
          x={56}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          帮助服务门户
        </text>
      </switch>
    </g>
    <path
      d="M 299 221 C 299 199.67 359 199.67 359 221 L 359 269 C 359 290.33 299 290.33 299 269 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 299 221 C 299 237 359 237 359 221"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(301.5,236.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={46}
          height={40}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 47,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              用户
              <br />
              配置文件
              <br />
              AuthDB
              <br />
            </div>
          </div>
        </foreignObject>
        <text
          x={23}
          y={26}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          [不支持的查看器]
        </text>
      </switch>
    </g>
    <path
      d="M 374 132 L 427.63 132"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 432.88 132 L 425.88 135.5 L 427.63 132 L 425.88 128.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 329 160 L 329 198.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 329 203.88 L 325.5 196.88 L 329 198.63 L 332.5 196.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={284}
      y={103}
      width={90}
      height={57}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(286.5,118.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={74}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 75,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              <br />
              单体
              <br />
            </div>
          </div>
        </foreignObject>
        <text
          x={37}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          API 网关&lt;br&gt;单体&lt;br&gt;
        </text>
      </switch>
    </g>
    <path
      d="M 377 221 C 377 199.67 437 199.67 437 221 L 437 269 C 437 290.33 377 290.33 377 269 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 377 221 C 377 237 437 237 437 221"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(379.5,243.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={53}
          height={26}
          requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              display: "inline-block",
              fontSize: 12,
              fontFamily: "Verdana",
              color: "rgb(0, 0, 0)",
              lineHeight: "1.2",
              verticalAlign: "top",
              width: 54,
              whiteSpace: "nowrap",
              overflowWrap: "normal",
              textAlign: "left"
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
              支付
              <br />
              数据库
              <br />
            </div>
          </div>
        </foreignObject>
        <text
          x={27}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Verdana"
        >
          支付&lt;br&gt;数据库&lt;br&gt;
        </text>
      </switch>
    </g>
    <g transform="translate(378.5,213.5)">
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
              Aurora
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
          Aurora
        </text>
      </switch>
    </g>
    <rect
      x={435}
      y="78.5"
      width={42}
      height={33}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(436.5,81.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={38}
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
              风险控制
            </div>
          </div>
        </foreignObject>
        <text
          x={19}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          风险控制
        </text>
      </switch>
    </g>
    <rect
      x={569}
      y={270}
      width={45}
      height={29}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(570.5,271.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={41}
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
              width: 41,
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
              风险控制
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
          风险控制
        </text>
      </switch>
    </g>
    <g transform="translate(630.5,121.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={36}
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
              whiteSpace: "nowrap",
              textAlign: "left"
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
              事件 <br />
              队列
            </div>
          </div>
        </foreignObject>
        <text
          x={18}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          [不支持的查看器]
        </text>
      </switch>
    </g>
  </g>
</svg>

## 功能和组件

### 支付服务

支付数据模型本质上是“[复式记账](https://en.wikipedia.org/wiki/Double-entry_bookkeeping_system)”。每个账户的每一笔入账都需要在另一个账户中有相应的对立入账。所有借方和贷方的总和等于零。

#### 存款和支付

交易：新用户 Jane Doe 从银行向 Cash App 存入 100 美元。这一笔交易涉及以下数据库条目：

记账表（用于历史记录）

```txt
+ 借方, 美元, 100, CashAppAccountNumber, txId
- 贷方, 美元, 100, RoutingNumber:AccountNumber, txId
```

交易表

```txt
txId, 时间戳, 状态（待处理/已确认）, [记账条目], 叙述
```

一旦银行确认交易，更新上述待处理状态和以下资产负债表，均在一笔交易中完成。

资产负债表

```txt
CashAppAccountNumber, 美元, 100
```

#### 在 Cash App 内部账户之间转账

与上述情况类似，但没有待处理状态，因为我们不需要慢速外部系统来更改其状态。所有记账表、交易表和资产负债表的更改都在一笔交易中完成。

### 国际化

我们在三个维度上解决国际化问题。

1. 语言：所有文本，如文案、推送通知、电子邮件，均根据 `accept-language` 头部进行选择。
2. 时区：所有服务器时区均为 UTC。我们在客户端将时间戳转换为本地时区。
3. 货币：所有用户转账交易必须使用相同货币。如果他们想要跨货币转移，必须先以对 Cash App 有利的汇率兑换货币。

例如，Jane Doe 想以 0.2 的汇率将 1 美元兑换为 6.8 人民币。

记账表

```txt
- 贷方, 美元, 1, CashAppAccountNumber, txId
+ 借方, 人民币, 6.8, CashAppAccountNumber, txId, @7.55 人民币/美元
+ 借方, 美元, 0.1, ExpensesOfExchangeAccountNumber, txId
```

交易表、资产负债表等与存款和支付中讨论的交易类似。主要区别在于银行或供应商提供兑换服务。

### 如何在交易表和外部银行及供应商之间同步？

* [使用幂等性重试以提高外部调用的成功率并确保没有重复订单](https://tianpan.co/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency)。
* 检查待处理订单是否已完成或失败的两种方法。
    1. `轮询`：定时作业（SWF、Airflow、Cadence 等）轮询待处理订单的状态。
    2. `回调`：为外部供应商提供回调 API。
* 优雅关闭。银行网关调用可能需要数十秒才能完成，重启服务器可能会从数据库恢复未完成的交易。该过程可能会创建过多连接。为减少连接，在关闭之前停止接受新请求，并等待现有的外发请求完成。

### 去重

为什么去重是一个问题？

1. 不是所有端点都是幂等的
2. 事件队列可能是至少一次的。

#### 不是所有端点都是幂等的：如果外部系统不是幂等的怎么办？

对于上述 `轮询` 情况，如果外部网关不支持幂等 API，为了不淹没重复条目，我们必须记录外部系统给我们的订单 ID 或参考 ID，并通过订单 ID 查询 `GET`，而不是一直使用 `POST`。

对于 `回调` 情况，我们可以确保实现幂等 API，并且无论如何我们将 `待处理` 更改为 `已确认`。

#### 事件队列可能是至少一次的

* 对于事件队列，我们可以使用一个完全一次的 Kafka，生产者吞吐量仅下降 3%。
* 在数据库层，我们可以使用 [幂等性密钥或去重密钥](https://tianpan.co/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency)。
* 在服务层，我们可以使用 Redis 键值存储。

### 可用性和扩展性

* 整体故障转移策略：[通过故障转移提高可用性](https://tianpan.co/notes/85-improving-availability-with-failover)：冷备份、热备份、温备份、主动-主动。
* 服务层扩展：[AKF 扩展立方体](https://tianpan.co/notes/41-how-to-scale-a-web-service)
* 数据层扩展：CQRS 模式
* 需要速度层吗？[Lambda 架构](https://tianpan.co/notes/83-lambda-architecture)