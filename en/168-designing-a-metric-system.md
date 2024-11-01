---
slug: 168-designing-a-metric-system
id: 168-designing-a-metric-system
layout: post
title: "Designing a metric system"
date: 2019-08-26 11:58
comments: true
tags: [system design]
slides: false
references:
  - https://github.com/prometheus/prometheus/blob/master/README.md
---

## Requirements

Log v.s Metric: A log is an event that happened, and a metric is a measurement of the health of a system.

We are assuming that this system’s purpose is to serve metrics - namely, counters, conversion rate, timers, etc. for monitoring the system performance and health. If the conversion rate drops drastically, the system should alert the on-call.

1. Monitoring business metrics like signup funnel’s conversion rate
2. Supporting various queries, like on different platforms (IE/Chrome/Safari, iOS/Android/Desktop, etc.)
3. data visualization
4. Scalability and Availability


## Architecture

Two ways to build the system:

1. Push Model: Influx/Telegraf/Grafana
2. Pull Model: Prometheus/Grafana

The pull model is more scalable because it decreases the number of requests going into the metrics databases - there is no hot path and concurrency issue.

<svg
xmlns="http://www.w3.org/2000/svg"
xmlnsXlink="http://www.w3.org/1999/xlink"
version="1.1"
width="100%"
viewBox="-0.5 -0.5 361 556"
content='<mxfile modified="2019-08-26T19:32:27.492Z" host="www.draw.io" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36" etag="slGGjoSwGesaS89Ibu59" pages="1" version="11.2.3" type="google"><diagram id="rrGVAOw1E3pQ3IQIfVm4" name="Page-1">7Vttd6I4FP41fpweIIL6sb7Udrc7225nz3T2y54IETMTiSfGqv31k2BAIanSFoSe0/nQIZcQ4Lkvz72X2AKD+WbM4GL2Fw0QaTlWsGmBYctxOl1P/JWC7U7geUoQMhzsRPZe8ICfkRJaSrrCAVpmJnJKCceLrNCnUYR8npFBxug6O21KSfauCxgiTfDgQ6JLv+OAz3bSrmvt5dcIh7PkzralzsxhMlkJljMY0PWBCIxaYMAo5buj+WaAiMQuwWV33dULZ9MHYyjiRS6Y3Nzjn//DP8ZP4W14/zh+Dn+sv6hVniBZqRdWD8u3CQKMrqIAyUWsFuivZ5ijhwX05dm1ULmQzficiJEtDvWHSu6AGEebA5F6yDGic8TZVkxRZ3sKL2UwDlDj9R5+O8F0dgC9p2RQaTxMV96DIg4ULq/AyGkeRqmVJSC16wYJNBAkOweSWzdIbQ2kB8TECwnZFWRzDTHxojwLy5Iz+gsNKKFMSCIaiZn9KSYkJ4IEh5EY+gI+sT7oS9iwCGuX6sQcB4G8jVEPWU1VoArg6KroGTThVKWJroY1CkTcV0PK+IyGNIJktJfmUNnPuaV0odTzE3G+VSQGV5xmlYc2mD8eHP+QS124ajTcqJXjwTYZROJ1H+OJtpuMdxda6Xh/aTzKXHuHGBaYSSM4rs0lXTEfHcHMVfQLWYj4kXmK4CWgR22DIQI5fsoSbematvXwvWbC5As4G0NL/Awn8QQJ3YLiiMfP5/Zb7vBVbkbgBJE+9H+FsRkl7tpywDT+Z9TMMdPVnC/NgdQTZ9IMk1NKi2p7Gb9M8oHCqlGL30lkDqbQ6XQpbCSvu/QZ3q5OV9MmRwSFDE7r55tOjm86rhbkXFcPcqCqIOdpWN1EU7LaDPsaViI5XchDf0uwAI2dBmyyQ/d2kgpS4/57xcUqqDxk0/QmoQ9Ppw/PQB9uVcjatobgGfnDunDcAwqxjxLI2+N9r+w4ngsWiXK7wKzcZIkd4airyo8otp66/jN6+CYkl3c3H5Yl7Jec7NU08cW6AL0knU94ot10nuhpSh0LjoARrJ0mQL52c3Wa6BqCWbuy+tY6whPW3Wo5E/+pxk4Z3iDi2nIX4uwD5yBoyg2uwWVs7C+FQnAUfosDpTC+cvi6m1WE3TPUh6CiquTPr7Ph5VcIr4fuyhug/67H/pWhG3PH5NIztFrGqoiXaKYqDIFG086R1MnNqKJtSJ3s9jlVoVcNl4sFEXBwTKP3xZBCMJcAaq6R5howNdXcZXQ/jJB69eZMxVOmg5o7W3KfqLeN+dLJ3MuIlcpJDmtt4zz3nSnZuxSqJ06jzULoSDa0ynCQNF8q3xk8A+manKGM2syInd4K9AlGcXJE8IRBdYtGYZjv4nmWDmLnnCDqzQDAAkmUkHGxukdkfJ0Ia/RCeVR6BK/QQDsGbE0GWkZWaMS2V2u0fkuH1M62R091R0uM1t2C0bpdZ7S29exyESeUzaxwCxeuWZW9bMvHClzLUd7WiILWnJC2602fMi0nq5hH5vIn+3we2SnokS/1Ps7jkh3NIw/rvY9QY6Q+mKQEtl5DO6YaultZDd2p00/e9mmv8cRl18tc9eYiH6tyLKxSUKdKk4+YBz13sS5GQtC81DwNYEmQawMtyJk+PwG3KoewNJA+k/P3OkSt/mD4CCW3BmHxZo41xEufCgtuYEsg7xodA/+f1zU+4M6e2lzDbhcli1r7jLZh3xynTO7cbZxDACv7JaN2rnDAB0yevJ6TdQrL6Z1wiyOb3crxFcP2NzPgTq2+ovdEZU15f9tAV+k2LK1yPkvH4v6QFP6n/aFW7nA+84EqdOrVqlN9w8olEZFoDiORE7DmRbp8l8wt+ksEAKqC0NEg/I4mQvDvTUs+yJX4m26YUuN4O5w1iD9TltSeLJVOCpQiZpAr4xMDF0sDHa54A0u5PB27ht9onJeO9f3LoznEDWwQadB5+sfbkqATw/1PBnfflva/uwSj3w==</diagram></mxfile>'
onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&&src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&&!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&&evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://www.draw.io/?client=1&lightbox=1&edit=_blank');}}})(this);"
style={{ cursor: "pointer", maxWidth: "100%", maxHeight: 556 }}
>
  <defs />
  <g>
    <rect
      x={0}
      y={40}
      width={120}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <rect
      x={10}
      y={50}
      width={120}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <rect
      x={20}
      y={60}
      width={120}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(31.5,133.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={66}
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
              width: 68,
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
              Server Farm
            </div>
          </div>
        </foreignObject>
        <text
          x={33}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Server Farm
        </text>
      </switch>
    </g>
    <path
      d="M 135 100 L 159 100 L 159 166.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 159 171.88 L 155.5 164.88 L 159 166.63 L 162.5 164.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(145.5,126.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={25}
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
              write
            </div>
          </div>
        </foreignObject>
        <text
          x={13}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          write
        </text>
      </switch>
    </g>
    <rect
      x={80}
      y={85}
      width={55}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(86.5,93.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={41}
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
              telegraf
            </div>
          </div>
        </foreignObject>
        <text
          x={21}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          telegraf
        </text>
      </switch>
    </g>
    <path
      d="M 150 180 C 150 166.67 210 166.67 210 180 L 210 210 C 210 223.33 150 223.33 150 210 Z"
      fill="#ffffff"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 150 180 C 150 190 210 190 210 180"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(156.5,195.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={46}
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
              width: 46,
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
              InfluxDB
            </div>
          </div>
        </foreignObject>
        <text
          x={23}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          InfluxDB
        </text>
      </switch>
    </g>
    <path
      d="M 230 105 L 230 138 L 193 138 L 193 163.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 193 168.88 L 189.5 161.88 L 193 163.63 L 196.5 161.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(198.5,130.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={55}
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
              REST API
            </div>
          </div>
        </foreignObject>
        <text
          x={28}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          REST API
        </text>
      </switch>
    </g>
    <rect
      x={210}
      y={65}
      width={80}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(227.5,78.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={44}
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
              Grafana
            </div>
          </div>
        </foreignObject>
        <text
          x={22}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Grafana
        </text>
      </switch>
    </g>
    <g transform="translate(91.5,2.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={112}
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
              InfluxDB Push Model
            </div>
          </div>
        </foreignObject>
        <text
          x={56}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          InfluxDB Push Model
        </text>
      </switch>
    </g>
    <g transform="translate(86.5,287.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={124}
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
              Prometheus Pull Model
            </div>
          </div>
        </foreignObject>
        <text
          x={62}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Prometheus Pull Model
        </text>
      </switch>
    </g>
    <rect
      x={0}
      y={385}
      width={90}
      height={60}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(2.5,392.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={59}
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
              width: 60,
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
              Application
            </div>
          </div>
        </foreignObject>
        <text
          x={30}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Application
        </text>
      </switch>
    </g>
    <path
      d="M 45 495 L 45 508.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 45 513.88 L 41.5 506.88 L 45 508.63 L 48.5 506.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={0}
      y={465}
      width={90}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(21.5,473.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={46}
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
              width: 46,
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
              Exporter
            </div>
          </div>
        </foreignObject>
        <text
          x={23}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Exporter
        </text>
      </switch>
    </g>
    <rect
      x={20}
      y={415}
      width={70}
      height={30}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(22.5,423.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={64}
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
              client library
            </div>
          </div>
        </foreignObject>
        <text
          x={32}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          client library
        </text>
      </switch>
    </g>
    <rect
      x={0}
      y={515}
      width={90}
      height={40}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(15.5,521.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={58}
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
              width: 60,
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
              3rd Party
              <br />
              Application
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
          3rd Party&lt;br&gt;Application
        </text>
      </switch>
    </g>
    <path
      d="M 140 471 L 115 471 L 115 430 L 96.37 430"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 91.12 430 L 98.12 426.5 L 96.37 430 L 98.12 433.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <g transform="translate(105.5,446.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={19}
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
              pull
            </div>
          </div>
        </foreignObject>
        <text
          x={10}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          pull
        </text>
      </switch>
    </g>
    <path
      d="M 188 420 L 190 420 L 190 399.37"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 190 394.12 L 193.5 401.12 L 190 399.37 L 186.5 401.12 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={130}
      y={420}
      width={230}
      height={80}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(132.5,427.5)">
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
              fontFamily: "Helvetica",
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
              Prometheus
            </div>
          </div>
        </foreignObject>
        <text
          x={33}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Prometheus
        </text>
      </switch>
    </g>
    <path
      d="M 200 471 L 208.63 471"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 213.88 471 L 206.88 474.5 L 208.63 471 L 206.88 467.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 170 488 L 170 513.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 170 518.88 L 166.5 511.88 L 170 513.63 L 173.5 511.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={140}
      y={453}
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(145.5,464.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={48}
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
              width: 48,
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
              Retrieval
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
          Retrieval
        </text>
      </switch>
    </g>
    <path
      d="M 140 471 L 115 471 L 115 480 L 96.37 480"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 91.12 480 L 98.12 476.5 L 96.37 480 L 98.12 483.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={140}
      y={520}
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(141.5,524.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={56}
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
              width: 56,
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
              Service Discovery
            </div>
          </div>
        </foreignObject>
        <text
          x={28}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Service Discovery
        </text>
      </switch>
    </g>
    <path
      d="M 275 471 L 283.63 471"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 288.88 471 L 281.88 474.5 L 283.63 471 L 281.88 467.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={215}
      y={453}
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(223.5,464.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={42}
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
              Storage
            </div>
          </div>
        </foreignObject>
        <text
          x={21}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Storage
        </text>
      </switch>
    </g>
    <path
      d="M 320 488 L 323 488 L 323 514.63"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 323 519.88 L 319.5 512.88 L 323 514.63 L 326.5 512.88 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={290}
      y={453}
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(297.5,464.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={44}
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
              width: 46,
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
              PromQL
            </div>
          </div>
        </foreignObject>
        <text
          x={22}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          PromQL
        </text>
      </switch>
    </g>
    <path
      d="M 250 377 L 270 377 L 270 348 L 283.63 348"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 288.88 348 L 281.88 351.5 L 283.63 348 L 281.88 344.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 250 377 L 270 377 L 270 393 L 283.63 393"
      fill="none"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <path
      d="M 288.88 393 L 281.88 396.5 L 283.63 393 L 281.88 389.5 Z"
      fill="#000000"
      stroke="#000000"
      strokeMiterlimit={10}
      pointerEvents="none"
    />
    <rect
      x={130}
      y={360}
      width={120}
      height={33}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(153.5,370.5)">
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
              Alertmanager
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
          Alertmanager
        </text>
      </switch>
    </g>
    <rect
      x={240}
      y={520}
      width={120}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(241.5,524.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={116}
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
              Web UI / Grafana / API Clients
            </div>
          </div>
        </foreignObject>
        <text
          x={58}
          y={19}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          Web UI / Grafana / API Clients
        </text>
      </switch>
    </g>
    <rect
      x={290}
      y={330}
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(291.5,341.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={56}
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
              width: 58,
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
              PagerDuty
            </div>
          </div>
        </foreignObject>
        <text
          x={28}
          y={12}
          fill="#000000"
          textAnchor="middle"
          fontSize="12px"
          fontFamily="Helvetica"
        >
          PagerDuty
        </text>
      </switch>
    </g>
    <rect
      x={290}
      y={375}
      width={60}
      height={35}
      fill="#ffffff"
      stroke="#000000"
      pointerEvents="none"
    />
    <g transform="translate(304.5,386.5)">
      <switch>
        <foreignObject
          style={{ overflow: "visible" }}
          pointerEvents="all"
          width={30}
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
              width: 32,
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
              Email
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
          Email
        </text>
      </switch>
    </g>
  </g>
</svg>

## Features and Components

### Measuring Sign-up Funnel

Take a four-step sign up on the mobile app for example

```txt
INPUT_PHONE_NUMBER -> VERIFY_SMS_CODE -> INPUT_NAME -> INPUT_PASSWORD
```

Every step has `IMPRESSION` and `POST_VERIFICATION` phases. And emit metrics like this:

```json5
{
  "sign_up_session_id": "uuid",
  "step": "VERIFY_SMS_CODE",
  "os": "iOS",
  "phase": "POST_VERIFICATION",
  "status": "SUCCESS",
  // ... ts, contexts, ...
}
```

Consequently, we can query the overall conversion rate of `VERIFY_SMS_CODE` step on `iOS` like

```txt
(counts of step=VERIFY_SMS_CODE, os=iOS, status: SUCCESS, phase: POST_VERIFICATION) / (counts of step=VERIFY_SMS_CODE, os=iOS, phase: IMPRESSION)
```

### Data Visualization

Graphana is mature enough for the data visualization work. If you do not want to expose the whole site, you can use [Embed Panel with iframe](https://grafana.com/docs/reference/sharing/#embed-panel).
