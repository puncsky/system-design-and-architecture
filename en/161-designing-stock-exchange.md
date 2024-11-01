---
slug: 161-designing-stock-exchange
id: 161-designing-stock-exchange
layout: post
title: "Designing Stock Exchange"
date: 2019-08-12 09:50
comments: true
categories: system design
language: en
slides: false
---

## Requirements

* order-matching system for `buy` and `sell` orders. Types of orders:
    * Market Orders
    * Limit Orders
    * Stop-Loss Orders
    * Fill-or-Kill Orders
    * Duration of Orders
* high availability and low latency for millions of users
    * async design - use messaging queue extensively (btw. side-effect: engineers work on one service pub to a queue and does not even know where exactly is the downstream service and hence cannot do evil.)



## Architecture

<svg
xmlns="http://www.w3.org/2000/svg"
xmlnsXlink="http://www.w3.org/1999/xlink"
version="1.1"
width="100%"
height="100%"
viewBox="-0.5 -0.5 672 412"
content='<mxfile modified="2019-07-29T04:46:36.590Z" host="www.draw.io" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36" etag="fP7YkbHKARZ_0o3JLRy3" version="11.0.7" type="google"><diagram id="uO2wHRNSVC2y_v88RBhh" name="Page-1">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</diagram></mxfile>'
style={{ backgroundColor: "rgb(255, 255, 255)" }}
>
  <defs />
  <g>
    <path
      d="M 196.45 50.07 L 196.45 59.72 L 264.72 59.72 L 264.72 73.36"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 78.61 L 261.22 71.61 L 264.72 73.36 L 268.22 71.61 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 209.96 0.01 C 210.66 0 211.33 0.31 211.8 0.84 C 212.27 1.38 212.5 2.1 212.43 2.83 L 212.43 47.44 C 212.43 48.85 211.32 50 209.96 50 L 182.54 50 C 181.88 50 181.26 49.73 180.79 49.25 C 180.33 48.77 180.07 48.12 180.07 47.44 L 180.07 2.83 C 180 2.1 180.23 1.38 180.7 0.84 C 181.17 0.31 181.84 0 182.54 0.01 Z M 201.81 2.83 L 190.44 2.83 L 190.44 4.36 L 201.81 4.36 Z M 209.71 6.93 L 182.54 6.93 L 182.54 42.05 L 209.71 42.05 Z M 200.82 44.62 L 191.43 44.62 L 191.43 47.44 L 200.82 47.44 L 200.82 44.62 Z M 189.46 20.16 L 196.13 16.67 L 202.8 20.16 L 196.13 24.36 Z M 188.96 21.8 L 195.39 25.9 L 195.39 33.59 L 188.96 29.49 Z M 196.87 25.9 L 203.29 21.8 L 203.29 29.49 L 196.87 33.59 Z"
      fill="#00bef2"
      stroke="none"
      pointerEvents="none"
    />
    <path
      d="M 264.72 50.07 L 264.72 74.05"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 79.3 L 261.22 72.3 L 264.72 74.05 L 268.22 72.3 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <image
      x="239.5"
      y="-0.5"
      width={50}
      height={50}
      xlinkHref="https://www.draw.io/img/lib/active_directory/server_farm.svg"
      pointerEvents="none"
    />
    <path
      d="M 342.5 21.25 L 342.66 59.72 L 264.72 59.72 L 264.72 73.36"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 78.61 L 261.22 71.61 L 264.72 73.36 L 268.22 71.61 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <image
      x={317}
      y="-0.5"
      width={50}
      height="42.5"
      xlinkHref="https://www.draw.io/img/lib/mscae/Browser.svg"
      pointerEvents="none"
    />
    <path
      d="M 264.72 110.07 L 264.72 133.36"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 138.61 L 261.22 131.61 L 264.72 133.36 L 268.22 131.61 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={230}
      y={80}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(231.5,81.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={67}
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
              width: 67,
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
              Reverse Proxy
            </div>
          </div>
        </foreignObject>
        <text
          x={34}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Reverse Proxy
        </text>
      </switch>
    </g>
    <path
      d="M 264.72 170.07 L 264.72 185.24 L 617.83 185.24 L 617.83 198.87"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 617.83 204.12 L 614.33 197.12 L 617.83 198.87 L 621.33 197.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 170.07 L 264.72 185.24 L 370.24 185.24 L 370.24 198.87"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 370.24 204.12 L 366.74 197.12 L 370.24 198.87 L 373.74 197.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 170.07 L 264.72 185.24 L 144.72 185.24 L 144.72 198.87"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 144.72 204.12 L 141.22 197.12 L 144.72 198.87 L 148.22 197.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 170.07 L 264.72 190.07 L 264.72 198.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 203.88 L 261.22 196.88 L 264.72 198.63 L 268.22 196.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 299.9 154.9 L 328.7 154.9"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 333.95 154.9 L 326.95 158.4 L 328.7 154.9 L 326.95 151.4 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 170.07 L 264.72 185.24 L 475.07 185.24 L 475.07 198.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 475.07 203.88 L 471.57 196.88 L 475.07 198.63 L 478.57 196.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 170.07 L 264.72 185.24 L 559.9 185.24 L 559.9 198.87"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 559.9 204.12 L 556.4 197.12 L 559.9 198.87 L 563.4 197.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={230}
      y={140}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(231.5,141.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={67}
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
              width: 67,
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
              API Gateway
            </div>
          </div>
        </foreignObject>
        <text
          x={34}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          API Gateway
        </text>
      </switch>
    </g>
    <path
      d="M 264.72 234.9 L 264.72 250.07 L 233.69 250.07 L 233.69 270.07 L 228.7 270.07"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 233.95 270.07 L 226.95 273.57 L 228.7 270.07 L 226.95 266.57 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 264.72 234.9 L 264.72 250.07 L 304.03 250.07 L 304.03 263.7"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 304.03 268.95 L 300.53 261.95 L 304.03 263.7 L 307.53 261.95 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={230}
      y={205}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(231.5,206.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={67}
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
              width: 67,
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
              Order Matching
            </div>
          </div>
        </foreignObject>
        <text
          x={34}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Order Matching
        </text>
      </switch>
    </g>
    <path
      d="M 635.07 234.9 L 634.5 263.7"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 634.4 268.95 L 631.04 261.88 L 634.5 263.7 L 638.04 262.02 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={600}
      y={205}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(605.5,213.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={57}
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
              width: 59,
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
              User Store
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
          User Store
        </text>
      </switch>
    </g>
    <path
      d="M 370.24 234.9 L 370.24 263.7"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 370.24 268.95 L 366.74 261.95 L 370.24 263.7 L 373.74 261.95 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 328.7 219.72 L 306.26 219.72"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 333.95 219.72 L 326.95 223.22 L 328.7 219.72 L 326.95 216.22 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 301.01 219.72 L 308.01 216.22 L 306.26 219.72 L 308.01 223.22 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 404.72 219.72 L 423.87 219.72"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 429.12 219.72 L 422.12 223.22 L 423.87 219.72 L 422.12 216.22 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 352.31 234.9 L 352.31 317.66 L 76.61 317.66"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 71.36 317.66 L 78.36 314.16 L 76.61 317.66 L 78.36 321.16 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(81.5,310.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={29}
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
              settle
            </div>
          </div>
        </foreignObject>
        <text
          x={15}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          settle
        </text>
      </switch>
    </g>
    <rect
      x={335}
      y={205}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(351.5,213.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={37}
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
              width: 37,
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
              Orders
            </div>
          </div>
        </foreignObject>
        <text
          x={19}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Orders
        </text>
      </switch>
    </g>
    <path
      d="M 624.5 276 C 624.5 268 644.5 268 644.5 276 L 644.5 294 C 644.5 302 624.5 302 624.5 294 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 624.5 276 C 624.5 282 644.5 282 644.5 276"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 225 276 C 225 268 245 268 245 276 L 245 294 C 245 302 225 302 225 294 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 225 276 C 225 282 245 282 245 276"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 360.5 276 C 360.5 268 380.5 268 380.5 276 L 380.5 294 C 380.5 302 360.5 302 360.5 294 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 360.5 276 C 360.5 282 380.5 282 380.5 276"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 144.72 234.9 L 144.72 263.7"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 144.72 268.95 L 141.22 261.95 L 144.72 263.7 L 148.22 261.95 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 110.24 219.72 L 76.61 219.72"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 71.36 219.72 L 78.36 216.22 L 76.61 219.72 L 78.36 223.22 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={110}
      y={205}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(113.5,213.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={61}
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
              width: 61,
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
              Stock Meta
            </div>
          </div>
        </foreignObject>
        <text
          x={31}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Stock Meta
        </text>
      </switch>
    </g>
    <path
      d="M 135 276 C 135 268 155 268 155 276 L 155 294 C 155 302 135 302 135 294 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 135 276 C 135 282 155 282 155 276"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 415.07 154.9 L 635.07 154.9 L 635.07 198.87"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 635.07 204.12 L 631.57 197.12 L 635.07 198.87 L 638.57 197.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={335}
      y={140}
      width={80}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(363.5,148.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={23}
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
              width: 25,
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
              auth
            </div>
          </div>
        </foreignObject>
        <text
          x={12}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          auth
        </text>
      </switch>
    </g>
    <path
      d="M 281 276 C 281 268 326 268 326 276 L 326 294 C 326 302 281 302 281 294 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 281 276 C 281 282 326 282 326 276"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(286.5,282.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={34}
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
              width: 36,
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
              Cache
            </div>
          </div>
        </foreignObject>
        <text
          x={17}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Cache
        </text>
      </switch>
    </g>
    <path
      d="M 475.07 234.9 L 475.07 263.7"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 475.07 268.95 L 471.57 261.95 L 475.07 263.7 L 478.57 261.95 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={430}
      y={205}
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(431.5,206.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={87}
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
              width: 87,
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
              Balances &amp; Bookkeeping
            </div>
          </div>
        </foreignObject>
        <text
          x={44}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Balances &amp; Bookkeeping
        </text>
      </switch>
    </g>
    <path
      d="M 465 276 C 465 268 485 268 485 276 L 485 294 C 485 302 465 302 465 294 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 465 276 C 465 282 485 282 485 276"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={10}
      y="202.5"
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(10.5,206.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={57}
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
              width: 57,
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
              external pricing
            </div>
          </div>
        </foreignObject>
        <text
          x={29}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          external pricing
        </text>
      </switch>
    </g>
    <rect
      x={0}
      y={300}
      width={70}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(12.5,303.5)">
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
              width: 43,
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
              clearing
              <br />
              house
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
          clearing&lt;br&gt;house
        </text>
      </switch>
    </g>
    <path
      d="M 100 410 L 100 130"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      strokeDasharray="3 3"
      pointerEvents="none"
    />
    <rect
      x={0}
      y={360}
      width={70}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(0.5,363.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={67}
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
              width: 67,
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
              Bank, ACH, Visa, etc
            </div>
          </div>
        </foreignObject>
        <text
          x={34}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Bank, ACH, Visa, etc
        </text>
      </switch>
    </g>
    <path
      d="M 559.9 234.9 L 559.9 377.66 L 76.61 377.66"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 71.36 377.66 L 78.36 374.16 L 76.61 377.66 L 78.36 381.16 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={525}
      y={205}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(536.5,213.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={47}
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
              width: 49,
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
              Payment
            </div>
          </div>
        </foreignObject>
        <text
          x={24}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Payment
        </text>
      </switch>
    </g>
    <g transform="translate(435.5,304.5)">
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
              Audit &amp; Report
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
          Audit &amp; Report
        </text>
      </switch>
    </g>
  </g>
</svg>



## Components and How do they interact with each other.

### order matching system

* shard by stock code
* order's basic data model (other metadata are omitted): `Order(id, stock, side, time, qty, price)`
* the core abstraction of the order book is the matching algorithm. there are a bunch of matching algorithms([ref to stackoverflow](http://web.archive.org/web/20120626161034/http://www.cmegroup.com/confluence/display/EPICSANDBOX/Match+Algorithms), [ref to medium](https://medium.com/lgogroup/a-matching-engine-for-our-values-part-1-795a29b400fa))
* example 1: [price-time FIFO](https://stackoverflow.com/questions/13112062/which-are-the-order-matching-algorithms-most-commonly-used-by-electronic-financi) - a kind of 2D vector cast or flatten into 1D vector
    * x-axis is price
    * y-axis is orders. Price/time priority queue, FIFO.
        * Buy-side: ascending in price, descending in time.
        * Sell-side: ascending in price, ascending in time.
    * in other words
        * Buy-side: the higher the price and the earlier the order, the nearer we should put it to the center of the matching.
        * Sell-side: the lower the price and the earlier the order, the nearer we should put it to the center of the matching.

x-axis

![line of prices](https://res.cloudinary.com/dohtidfqh/image/upload/v1564355657/web-guiguio/singleMarket.png)

with y-axis cast into x-axis


```text
Id   Side    Time   Qty   Price   Qty    Time   Side  
---+------+-------+-----+-------+-----+-------+------
#3                        20.30   200   09:05   SELL  
#1                        20.30   100   09:01   SELL  
#2                        20.25   100   09:03   SELL  
#5   BUY    09:08   200   20.20                       
#4   BUY    09:06   100   20.15                       
#6   BUY    09:09   200   20.15                       
```

Order book from Coinbase Pro

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1564466496/web-guiguio/1_EiZZjOVe0mqXhxbOhe4_uw.png)


[The Single Stock-Exchange Simulator](http://homepages.gold.ac.uk/nikolaev/aalts.htm)

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1564466429/web-guiguio/SSESNIK.gif)


* example 2: pro-rata

![pure pro-rata](https://res.cloudinary.com/dohtidfqh/image/upload/v1564361620/web-guiguio/1_hahTecyPk0aKMJ1CCME4qw.png)


How to implement the price-time FIFO matching algorithm?

* shard by stock, CP over AP: one stock one partition
* stateful in-memory tree-map
    * periodically iterate the treemap to match orders
* data persistence with cassandra
* in/out requests of the order matching services are made through messaging queues
* failover
    * the in-memory tree-maps are snapshotting into database
    * in an error case, recover from the snapshot and de-duplicate with cache

How to transmit data of the order book to the client-side in realtime?

* websocket

How to support different kinds of orders?

* same `SELL or BUY: qty @ price` in the treemap with different creation setup and matching conditions
    * Market Orders: place the order at the last market price.
    * Limit Orders: place the order with at a specific price.
    * Stop-Loss Orders: place the order with at a specific price, and match it in certain conditions.
    * Fill-or-Kill Orders: place the order with at a specific price, but match it only once.
    * Duration of Orders: place the order with at a specific price, but match it only in the given time span.
    
### Orders Service

* Preserves all active orders and order history.
* Writes to order matching when receives a new order.
* Receives matched orders and settle with external clearing house (async external gateway call + cronjob to sync DB)


### References

* How Exchange Happen? [Simulating a financial exchange in Scala](http://falconair.github.io/2015/01/05/financial-exchange.html)
* Open Sources
  * [GitHub - objectcomputing/liquibook: Modern C++ order matching engine](https://github.com/objectcomputing/liquibook)
  * [GitHub - cyanly/gotrade: A proof of concept of an electronic trading system written in Golang](https://github.com/cyanly/gotrade)
* [The Financial Information eXchange ("FIX") Protocol](http://help.cqg.com/continuum/default.htm#!Documents/fixserver.htm)
* Types of orders: [Technical Analysis Course. Training,Coaching & Mentoring for Traders / Investors - Types of orders used when buying or selling a stock](http://www.tradersplace.in/TypesofOrders.html)
* [GitHub - fmstephe/matching_engine: A simple financial trading matching engine. Built to learn more about how they work.](https://github.com/fmstephe/matching_engine)
* [Automated Algorithmic Trading: Learning Agents for Limit Order Book Trading](http://homepages.gold.ac.uk/nikolaev/aalts.htm)
