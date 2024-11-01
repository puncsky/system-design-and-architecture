---
slug: 167-designing-paypal-money-transfer
id: 167-designing-paypal-money-transfer
layout: post
title: Designing Square Cash or PayPal Money Transfer System
date: 2019-08-23 17:02
comments: true
categories: system design
language: en
slides: false
description: Design a money-transfer backend system that can receive, send, and payout. It should cover issues like scaling, internationalization, Deduplication, single-point failure, strong consistency.
references:
  - https://medium.com/airbnb-engineering/scaling-airbnbs-payment-platform-43ebfc99b324
  - https://beancount.io
---

## Clarifying Requirements

Designing a service money transfer backend system like Square Cash (we will call this system Cash App below) or PayPal to

1. Deposit from and payout to bank
2. Transfer between accounts
3. High scalability and availability
4. i18n: language, timezone, currency exchange
5. Deduplication for non-idempotent APIs and for at-least-once delivery.
6. Consistency across multiple data sources.


## Architecture

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
              Presentation Layer
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
          Presentation Layer
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
              SDK/Docs
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
          SDK/Docs
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
              mobile-dashboard
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
          mobile-dashboard
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
              web-dashboard
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
          web-dashboard
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
              dashboard-client
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
          dashboard-client
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
              mobile-wallet
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
          mobile-wallet
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
              web-wallet
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
          web-wallet
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
              wallet-client
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
          wallet-client
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
              Merchant&nbsp;
              <br />
              User
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
          Merchant&nbsp;&lt;br&gt;User
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
              End User
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
          End User
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
              web-chrome-extension
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
          web-chrome-extension
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
              Operators
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
          Operators
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
              payment
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
          payment
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
              task-queue
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
          task-queue
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
              financial-reporter
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
          financial-reporter
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
              payment-gateway
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
          payment-gateway
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
              banks /&nbsp;
              <br />
              vendors
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
          [Not supported by viewer]
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
              side-effect maker
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
          side-effect maker
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
              help service portal
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
          help service portal
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
              User
              <br />
              Profiles
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
          [Not supported by viewer]
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
              api-gateway
              <br />
              monolithic
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
          api-gateway&lt;br&gt;monolithic&lt;br&gt;
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
              Payment
              <br />
              DB
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
          Payment&lt;br&gt;DB&lt;br&gt;
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
              risk control
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
          risk control
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
              risk control
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
          risk control
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
              Event <br />
              Queue
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
          [Not supported by viewer]
        </text>
      </switch>
    </g>
  </g>
</svg>

## Features and Components

### Payment Service

The payment data model is essentially “[double-entry bookkeeping](https://en.wikipedia.org/wiki/Double-entry_bookkeeping_system)”. Every entry to an account requires a corresponding and opposite entry to a different account. Sum of all debit and credit equals to zero.

#### Deposit and Payout

Transaction: new user Jane Doe deposits $100 from bank to Cash App. This one transaction involves those DB entries:

bookkeeping table (for history)

```txt
+ debit, USD, 100, CashAppAccountNumber, txId
- credit, USD, 100, RoutingNumber:AccountNumber, txId
```

transaction table

```txt
txId, timestamp, status(pending/confirmed), [bookkeeping entries], narration
```


Once the bank confirmed the transaction, update the pending status above and the following balance sheet in one transaction.

balance sheet

```txt
CashAppAccountNumber, USD, 100
```

#### Transfer between accounts within Cash App

Similar to the case above, but there is no pending state because we do not need the slow external system to change their state. All changes in bookkeeping table, transaction table, and balance sheet table happen in one transaction.

### i18n

We solve the i18n problems in 3 dimensions.

1. Language: All texts like copywriting, push notifications, emails are picked up according to the `accept-language` header.
2. Timezones: All server timezones are in UTC. We transform timestamps to the local timezone in the client-side.
3. Currency: All user transferring transactions must be in the same currency. If they want to move across currencies, they have to exchange the currency first, in a rate that is favorable to the Cash App.

For example, Jane Doe wants to exchange 1 USD with 6.8 CNY with 0.2

bookkeeping table

```txt
- credit, USD, 1, CashAppAccountNumber, txId
+ debit, CNY, 6.8, CashAppAccountNumber, txId, @7.55 CNY/USD
+ debit, USD, 0.1, ExpensesOfExchangeAccountNumber, txId
```

Transaction table, balance sheet, etc. are similar to the transaction discussed in Deposit and Payout. The major difference is that the bank or the vendor provides the exchange service.

### How to sync across the transaction table and external banks and vendors?

* [retry with idempotency to improve the success rate of the external calls and ensure no duplicate orders](43-how-to-design-robust-and-predictable-apis-with-idempotency).
* two ways to check if the PENDING orders are filled or failed.
    1. `poll`: cronjobs (SWF, Airflow, Cadence, etc.) to poll the status for PENDING orders.
    2. `callback`: provide a callback API for the external vendors.
* Graceful shutdown. The bank gateway calls may take tens of seconds to finish, and restarting the servers may resume unfinished transactions from the database. The process may create too many connections. To reduce connections, before the shutdown, stop accepting new requests and wait for the existing outgoing ones to wrap up.

### Deduplication

Why is Deduplication a concern?

1. not all endpoints are idempotent
2. Event queue may be at-least-once.

#### not all endpoints are idempotent: what if the external system is not idempotent?

For the `poll` case above, if the external gateway does not support idempotent APIs, in order not to flood with duplicate entries, we must keep record of the order ID or the reference ID the external system gives us with 200, and query `GET` by the order ID instead of `POST` all the time.

For the `callback` case, we can ensure we implement with idempotent APIs, and we mutate `pending` to `confirmed` anyway.

#### Event queue may be at-least-once

* For the even queue, we can use an exactly-once Kafka with the producer throughput declines only by 3%.
* In the database layer, we can use [idempotency key or deduplication key](43-how-to-design-robust-and-predictable-apis-with-idempotency).
* In the service layer, we can use Redis key-value store.

### Availability and Scalability

* Overall failover strategies: [Improving availability with failover](85-improving-availability-with-failover): Cold Standby, Hot Standby, Warm Standby, Active-active.
* Service layer scaling: [AKF Scale Cube](41-how-to-scale-a-web-service)
* Data layer scaling: CQRS Pattern
* Needing a speed layer? [Lambda Architecture](83-lambda-architecture)
