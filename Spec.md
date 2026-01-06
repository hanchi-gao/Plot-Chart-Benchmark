# 數據比較互動式窗格

實驗數據視覺化與比較工具，支援多次實驗結果的疊圖分析與互動式數據查看。

## 功能特色

- **實驗資料夾選擇**：手動選擇要比較的實驗資料夾（可選 1 個或多個），而非自動載入全部
- **多實驗疊圖比較**：將選中的實驗數據整合繪製在同一張圖表上
- **互動式數據顯示**：滑鼠懸停時顯示各條線在該 X 軸位置對應的 Y 軸數值
- **多指標分頁顯示**：支援多個 TAG（標籤頁），每個頁面顯示不同的效能指標
- **總覽頁面**：特殊的「總覽」TAG，在一個視圖中同時顯示四張圖表（2x2 佈局）

## 資料結構

```
數據比較互動式窗格/
├── output/
│   ├── 4c-9955-rocm7-1to200/      # 實驗1
│   │   ├── gpt-oss-120b_inputlen1024_num1_output8.json
│   │   ├── gpt-oss-120b_inputlen1024_num2_output8.json
│   │   └── ...
│   ├── output_mi1/                # 實驗2
│   │   └── ...
│   └── [其他實驗資料夾]/
├── P1.png                          # 範例：單一圖表輸出
├── P2.png                          # 範例：多標籤頁圖表輸出
└── README.md
```

## 數據格式

每個 JSON 檔案包含單次測試的效能指標，例如：

```json
{
  "date": "20251120-071736",
  "model_id": "openai/gpt-oss-120b",
  "num_prompts": 1,
  "max_concurrent_requests": 1,
  "mean_ttft_ms": 40.28,
  "median_ttft_ms": 40.28,
  "mean_tpot_ms": 28.69,
  "output_throughput": 34.73,
  ...
}
```

### 常用指標對應

從 JSON 可提取的關鍵指標：
- `mean_ttft_ms` / `median_ttft_ms` → Time to First Token
- `mean_tpot_ms` / `median_tpot_ms` → Time per Output Token
- `output_throughput` → Output Speed per Query
- `request_throughput` → Request Throughput
- `mean_itl_ms` / `median_itl_ms` → Inter-token Latency
- `max_concurrent_requests` → Concurrency (X 軸)

## 輸出示例

### 單一圖表 (P1.png)
基本圖表特性：
- X 軸：Concurrency (Log scale)
- Y 軸：Output Speed per Query (Tokens per Second)
- 圖例：不同模型或配置的標識
- 互動功能：滑鼠懸停顯示精確數值

### 多標籤頁圖表 (P2.png)
支援多個 TAG（標籤頁）切換：

#### 1. 總覽 TAG
- 在一個視圖中同時顯示 **四張圖表**（2x2 佈局）
- 快速綜覽所有關鍵指標的表現

#### 2. 單一指標 TAG
每個 TAG 顯示一張放大的圖表，例如：
- **End-to-End Latency**：端到端延遲 vs. Concurrency
- **Time to First Token**：首字延遲 vs. Concurrency
- **System Output Throughput**：系統輸出吞吐量 vs. Concurrency
- **Output Speed per Query**：每查詢輸出速度 vs. Concurrency

每個標籤頁都保持相同的互動功能，可快速切換比較不同指標。

## 安裝與執行

### 需求
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)（推薦）或 pip

### 使用 uv 執行（推薦）
```bash
# 執行應用程式
uv run app.py

# 或指定 Python 版本
uv run --python 3.11 app.py
```

### 使用 pip 執行
```bash
# 安裝依賴
pip install -r requirements.txt

# 執行應用程式
python app.py
```

## 使用方式

1. 將實驗數據放入 `output/` 目錄下的各個子資料夾
2. 每個子資料夾代表一次獨立的實驗
3. 執行 `uv run app.py`
4. 瀏覽器會自動開啟應用程式（預設 http://localhost:8050）
5. **選擇要比較的實驗資料夾**（例如：勾選 `4c-9955-rocm7-1to200` 和 `output_mi1`）
6. 圖表將只顯示選中資料夾的數據線
7. 使用標籤頁切換不同指標視圖

## 互動功能

### 資料夾選擇
- 啟動時顯示 `output/` 下的所有實驗資料夾列表
- 使用勾選框或多選列表選擇要比較的資料夾
- 可選擇 1 個資料夾（單一實驗分析）或多個資料夾（多實驗比較）
- 只有選中的資料夾數據會顯示在圖表上

### 滑鼠懸停
在圖表上移動滑鼠時，會顯示：
- 當前 X 軸數值
- **各條線在該位置的 Y 軸數值**（每個選中的實驗都會顯示）
- 對應的實驗名稱/標籤

## 開發計劃

- [ ] 實作數據讀取模組
- [ ] 實作資料夾選擇介面（勾選框/多選列表）
- [ ] 實作互動式繪圖功能（建議使用 Plotly 或 Dash）
- [ ] 實作多標籤頁 (TAG) 切換功能
- [ ] 實作「總覽」TAG（2x2 佈局顯示四張圖）
- [ ] 實作單一指標 TAG（放大顯示單張圖）
- [ ] 支援自定義指標配置（可選擇要顯示的 TAG）
- [ ] 支援自定義 X/Y 軸指標選擇
- [ ] 支援匯出高解析度圖表

## 圖表配置建議

### UI 結構
```
┌─────────────────────────────────────────────────────┐
│ 資料夾選擇區                                          │
│ ☑ 4c-9955-rocm7-1to200                              │
│ ☑ output_mi1                                        │
│ ☐ [其他實驗資料夾]                                   │
├─────────────────────────────────────────────────────┤
│ [總覽] [Time to First Token] [Output Speed] ...    │  ← TAG 標籤頁
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┬─────────────┐  ← 總覽 TAG 顯示    │
│  │   圖表 1    │   圖表 2    │    四張圖 (2x2)    │
│  ├─────────────┼─────────────┤                     │
│  │   圖表 3    │   圖表 4    │                     │
│  └─────────────┴─────────────┘                     │
│                                                     │
│  或單一放大圖表（其他 TAG）                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 標籤頁配置

```python
CHART_TABS = {
    "總覽": {
        "type": "overview",  # 特殊類型：顯示四張圖
        "layout": "2x2"
    },
    "Time to First Token": {
        "type": "single",
        "y_field": "mean_ttft_ms",
        "y_label": "Time to First Token (s)",
        "y_unit": "s"
    },
    "Output Speed per Query": {
        "type": "single",
        "y_field": "output_throughput",
        "y_label": "Output Speed per Query (Tokens per Second)",
        "y_unit": "tokens/s"
    },
    "System Output Throughput": {
        "type": "single",
        "y_field": "total_token_throughput",
        "y_label": "System Output Throughput (Tokens per Second)",
        "y_unit": "tokens/s"
    },
    "End-to-End Latency": {
        "type": "single",
        "y_field": "mean_tpot_ms",
        "y_label": "End-to-End Latency (s)",
        "y_unit": "s"
    }
}
```

## Vibe Coding 提示

使用 AI 輔助開發時，可提供以下上下文：
- 資料格式：JSON 檔案包含效能測試指標
- 預期輸出：類似 P1.png 的互動式多線圖，或 P2.png 的多標籤頁圖表
- 關鍵需求：
  1. **資料夾選擇**：
     - 不要自動載入全部 output 內的資料夾
     - 提供選擇介面（勾選框/多選列表）讓使用者挑選 1 個或多個實驗資料夾
     - 只繪製選中資料夾的數據線
  2. **總覽 TAG**：
     - 第一個 TAG 是「總覽」，顯示四張圖表（2x2 佈局）
     - 四張圖分別是：Time to First Token、Output Speed per Query、System Output Throughput、End-to-End Latency
  3. **單一指標 TAG**：
     - 其他 TAG 各自顯示一張放大的圖表
     - 方便單獨檢視特定指標
  4. **互動功能**：
     - 支援滑鼠懸停顯示各條線的精確數值
     - 所有圖表使用 Log scale X 軸（Concurrency）
  5. **技術建議**：
     - 使用 Plotly + Dash 可輕鬆實現多選介面和標籤頁切換
     - 使用 `plotly.subplots` 製作 2x2 佈局的總覽頁面
