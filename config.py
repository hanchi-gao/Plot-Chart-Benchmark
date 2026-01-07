"""圖表配置"""

CHART_TABS = {
    "總覽": {
        "type": "overview",
        "layout": "2x3",
        "charts": [
            {
                "title": "System Output Throughput",
                "y_field": "output_throughput",
                "y_label": "System Output Throughput (Tokens/s)",
            },
            {
                "title": "System Output Throughput per Query",
                "y_field": "output_speed_per_query",
                "y_label": "System Output Throughput per Query (Tokens/s)",
            },
            {
                "title": "Time to First Token",
                "y_field": "mean_ttft_ms",
                "y_label": "Time to First Token (ms)",
            },
            {
                "title": "Time per Output Token",
                "y_field": "mean_tpot_ms",
                "y_label": "Time per Output Token (ms)",
            },
            {
                "title": "End-to-End Latency",
                "y_field": "mean_itl_ms",
                "y_label": "End-to-End Latency (ms)",
            },
            {
                "title": "Request Throughput",
                "y_field": "request_throughput",
                "y_label": "Request Throughput (Requests/s)",
            },
        ]
    },
    "System Output Throughput": {
        "type": "single",
        "y_field": "output_throughput",
        "y_label": "System Output Throughput (Tokens/s)",
        "title": "System Output Throughput vs. Concurrency"
    },
    "System Output Throughput per Query": {
        "type": "single",
        "y_field": "output_speed_per_query",
        "y_label": "System Output Throughput per Query (Tokens/s)",
        "title": "System Output Throughput per Query vs. Concurrency"
    },
    "Time to First Token": {
        "type": "single",
        "y_field": "mean_ttft_ms",
        "y_label": "Time to First Token (ms)",
        "title": "Time to First Token vs. Concurrency"
    },
    "Time per Output Token": {
        "type": "single",
        "y_field": "mean_tpot_ms",
        "y_label": "Time per Output Token (ms)",
        "title": "Time per Output Token vs. Concurrency"
    },
    "End-to-End Latency": {
        "type": "single",
        "y_field": "mean_itl_ms",
        "y_label": "End-to-End Latency (ms)",
        "title": "End-to-End Latency vs. Concurrency"
    }
}

# 共用設定
X_AXIS_FIELD = "max_concurrent_requests"
X_AXIS_LABEL = "Concurrency"
OUTPUT_DIR = "output"
