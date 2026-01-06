# 數據比較互動式窗格

實驗數據視覺化與比較工具，支援多次實驗結果的疊圖分析與互動式數據查看。

## 目錄

- [功能特色](#功能特色)
- [快速開始](#快速開始)
- [使用流程](#使用流程)
- [專案架構](#專案架構)
- [核心模組說明](#核心模組說明)
- [圖表配置與調整](#圖表配置與調整)
- [數據格式](#數據格式)
- [常見問題](#常見問題)

---

## 功能特色

- **實驗資料夾選擇**：手動選擇要比較的實驗資料夾（可選 1 個或多個），而非自動載入全部
- **多實驗疊圖比較**：將選中的實驗數據整合繪製在同一張圖表上
- **互動式數據顯示**：滑鼠懸停時顯示各條線在該 X 軸位置對應的 Y 軸數值
- **多指標分頁顯示**：支援多個 TAG（標籤頁），每個頁面顯示不同的效能指標
- **總覽頁面**：特殊的「總覽」TAG，在一個視圖中同時顯示四張圖表（2x2 佈局）

---

## 快速開始

### 系統需求

- Python 3.10 或更高版本
- [uv](https://github.com/astral-sh/uv)（推薦）或 pip

### 安裝與執行

#### 方法 1：使用 uv（推薦）

```bash
# 1. 進入專案目錄
cd "數據比較互動式窗格"

# 2. 執行應用程式（uv 會自動安裝依賴）
uv run app.py

# 3. 瀏覽器會自動開啟 http://localhost:8050
```

#### 方法 2：使用 pip

```bash
# 1. 建立虛擬環境（可選）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安裝依賴
pip install dash plotly pandas

# 3. 執行應用程式
python app.py
```

---

## 使用流程

### 步驟 1：準備數據

將實驗數據放入 `output/` 目錄下的各個子資料夾：

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
```

每個子資料夾代表一次獨立的實驗，資料夾內包含多個 JSON 檔案。

### 步驟 2：啟動應用程式

```bash
uv run app.py
```

終端會顯示：
```
找到 2 個實驗資料夾: ['4c-9955-rocm7-1to200', 'output_mi1']
啟動應用程式於 http://localhost:8050
Dash is running on http://127.0.0.1:8050/
```

### 步驟 3：選擇實驗資料夾

1. 瀏覽器自動開啟後，會看到所有可用的實驗資料夾
2. 使用勾選框選擇要比較的資料夾（可選 1 個或多個）
3. 圖表會即時更新，只顯示選中資料夾的數據線

### 步驟 4：切換 TAG 查看不同指標

應用程式提供 5 個標籤頁：

- **總覽**：同時顯示 4 張圖表（2x2 佈局）
- **Time to First Token**：首字延遲指標
- **Output Speed per Query**：每查詢輸出速度
- **System Output Throughput**：系統總吞吐量
- **End-to-End Latency**：端到端延遲

點擊標籤頁即可切換視圖。

### 步驟 5：互動式查看數據

- **滑鼠懸停**：將滑鼠移到圖表上任意位置，會顯示：
  - 當前 X 軸數值（Concurrency）
  - 所有選中實驗在該點的 Y 軸數值
  - 實驗名稱
- **縮放**：使用滑鼠滾輪或拖曳選取區域進行縮放
- **重置**：雙擊圖表可重置視圖

---

## 專案架構

```
數據比較互動式窗格/
├── app.py                  # 主應用程式入口
├── config.py              # 圖表配置檔案
├── data_loader.py         # 數據讀取模組
├── pyproject.toml         # 專案依賴配置
├── output/                # 實驗數據目錄
│   ├── [實驗資料夾1]/
│   └── [實驗資料夾2]/
├── P1.png                 # 範例圖表
├── P2.png                 # 範例圖表
└── README.md              # 本文件
```

---

## 核心模組說明

### 1. `app.py` - 主應用程式

**位置**：`app.py`

**功能**：Dash 應用程式主入口，負責 UI 渲染與互動邏輯。

#### 重要函式

##### `create_single_chart(data_dict, y_field, y_label, title)`
**位置**：`app.py:20-63`

**功能**：創建單一指標的圖表（用於非總覽 TAG）

**參數**：
- `data_dict` (dict): 實驗數據字典，格式為 `{資料夾名稱: DataFrame}`
- `y_field` (str): Y 軸數據欄位名稱（如 `"mean_ttft_ms"`）
- `y_label` (str): Y 軸標籤文字（如 `"Time to First Token (ms)"`）
- `title` (str): 圖表標題

**返回**：plotly Figure 物件

**使用範例**：
```python
fig = create_single_chart(
    data_dict,
    y_field="output_throughput",
    y_label="Output Speed (Tokens/s)",
    title="Output Speed per Query vs. Concurrency"
)
```

---

##### `create_overview_chart(data_dict)`
**位置**：`app.py:66-125`

**功能**：創建總覽頁面的 2x2 子圖佈局

**參數**：
- `data_dict` (dict): 實驗數據字典

**返回**：plotly Figure 物件（包含 4 個子圖）

**內部邏輯**：
1. 從 `config.CHART_TABS["總覽"]["charts"]` 讀取 4 個圖表配置
2. 使用 `plotly.subplots.make_subplots` 創建 2x2 佈局
3. 按位置 `(1,1), (1,2), (2,1), (2,2)` 填充各子圖
4. 只在第一個子圖顯示圖例（避免重複）

---

##### `update_chart(selected_folders, selected_tab)`
**位置**：`app.py:167-211`

**功能**：Dash callback 函式，響應用戶選擇並更新圖表

**觸發條件**：
- 用戶勾選/取消勾選資料夾
- 用戶切換 TAG 標籤頁

**參數**：
- `selected_folders` (list): 選中的資料夾名稱列表
- `selected_tab` (str): 選中的 TAG 名稱

**流程**：
```
1. 檢查是否有選中資料夾
   ├─ 無 → 顯示提示訊息
   └─ 有 → 繼續
2. 載入選中資料夾的數據
3. 根據選中的 TAG 類型
   ├─ "overview" → 調用 create_overview_chart()
   └─ "single" → 調用 create_single_chart()
4. 返回圖表給前端顯示
```

---

##### 應用程式佈局 (`app.layout`)
**位置**：`app.py:129-159`

**結構**：
```html
<div>
  <h1>數據比較互動式窗格</h1>

  <!-- 資料夾選擇區 -->
  <div id="folder-selection">
    <h3>選擇實驗資料夾：</h3>
    <dcc.Checklist id="folder-checklist" />
  </div>

  <!-- TAG 標籤頁 -->
  <div id="tabs-container">
    <dcc.Tabs id="chart-tabs" />
  </div>

  <!-- 圖表顯示區 -->
  <div id="chart-container">
    <dcc.Graph id="chart-display" />
  </div>
</div>
```

---

### 2. `config.py` - 圖表配置

**位置**：`config.py`

**功能**：集中管理所有圖表的配置，包括 TAG 定義、軸標籤、數據欄位映射等。

#### 核心變數

##### `CHART_TABS`
**位置**：`config.py:3-54`

**結構**：
```python
CHART_TABS = {
    "總覽": {
        "type": "overview",      # 圖表類型
        "layout": "2x2",         # 佈局方式
        "charts": [              # 4 個子圖的配置
            {
                "title": "...",
                "y_field": "...",
                "y_label": "..."
            },
            ...
        ]
    },
    "Time to First Token": {
        "type": "single",        # 單一圖表
        "y_field": "mean_ttft_ms",
        "y_label": "Time to First Token (ms)",
        "title": "Time to First Token vs. Concurrency"
    },
    ...
}
```

**用途**：
- 定義所有可用的 TAG
- 指定每個 TAG 使用的數據欄位
- 設定圖表標題與軸標籤

---

##### `X_AXIS_FIELD`
**位置**：`config.py:57`

**值**：`"max_concurrent_requests"`

**用途**：指定 X 軸使用的數據欄位（Concurrency）

---

##### `X_AXIS_LABEL`
**位置**：`config.py:58`

**值**：`"Concurrency"`

**用途**：X 軸顯示的標籤文字

---

##### `OUTPUT_DIR`
**位置**：`config.py:59`

**值**：`"output"`

**用途**：實驗數據所在的根目錄

---

### 3. `data_loader.py` - 數據讀取模組

**位置**：`data_loader.py`

**功能**：處理檔案系統操作與 JSON 數據載入。

#### 核心函式

##### `get_experiment_folders(output_dir="output")`
**位置**：`data_loader.py:9-24`

**功能**：掃描 output 目錄，返回所有實驗資料夾名稱

**參數**：
- `output_dir` (str): 要掃描的目錄路徑

**返回**：`List[str]` - 排序後的資料夾名稱列表

**使用範例**：
```python
folders = get_experiment_folders("output")
# 返回: ['4c-9955-rocm7-1to200', 'output_mi1']
```

---

##### `load_experiment_data(folder_name, output_dir="output")`
**位置**：`data_loader.py:27-57`

**功能**：讀取指定資料夾內的所有 JSON 檔案，合併成單一 DataFrame

**參數**：
- `folder_name` (str): 實驗資料夾名稱
- `output_dir` (str): output 根目錄路徑

**返回**：`pandas.DataFrame` - 包含該資料夾所有數據的 DataFrame

**內部流程**：
1. 檢查資料夾是否存在
2. 遍歷資料夾內所有 `.json` 檔案
3. 逐個讀取 JSON 並解析
4. 將所有數據合併成 DataFrame
5. 錯誤處理：若 JSON 格式錯誤，印出錯誤訊息並跳過

---

##### `load_multiple_experiments(folder_names, output_dir="output")`
**位置**：`data_loader.py:60-76`

**功能**：批次讀取多個實驗資料夾的數據

**參數**：
- `folder_names` (List[str]): 資料夾名稱列表
- `output_dir` (str): output 根目錄路徑

**返回**：`Dict[str, pd.DataFrame]` - 字典，key 為資料夾名稱，value 為對應的 DataFrame

**使用範例**：
```python
data_dict = load_multiple_experiments(
    ["4c-9955-rocm7-1to200", "output_mi1"]
)
# 返回: {
#   "4c-9955-rocm7-1to200": DataFrame(...),
#   "output_mi1": DataFrame(...)
# }
```

---

## 圖表配置與調整

### 如何新增 TAG

**步驟 1**：編輯 `config.py`

在 `CHART_TABS` 字典中新增一個項目：

```python
# config.py
CHART_TABS = {
    # ... 現有的 TAG ...

    "新指標名稱": {
        "type": "single",                    # 單一圖表
        "y_field": "你的數據欄位名稱",        # JSON 中的欄位
        "y_label": "Y 軸標籤文字",           # 顯示在圖表上的標籤
        "title": "圖表標題 vs. Concurrency"  # 完整標題
    }
}
```

**步驟 2**：重新啟動應用程式

```bash
# 終止當前運行（Ctrl+C）
# 重新啟動
uv run app.py
```

新的 TAG 會自動出現在標籤頁列表中。

---

### 如何修改總覽頁面的圖表

**步驟 1**：編輯 `config.py` 中的總覽配置

```python
# config.py
CHART_TABS = {
    "總覽": {
        "type": "overview",
        "layout": "2x2",
        "charts": [
            # 修改這裡的 4 個子圖配置
            {
                "title": "你的圖表標題",
                "y_field": "JSON 欄位名稱",
                "y_label": "Y 軸標籤"
            },
            # ... 另外 3 個子圖
        ]
    }
}
```

**注意**：總覽頁面固定顯示 4 個子圖，若要改變數量需修改 `app.py:80` 的 `make_subplots` 參數。

---

### 如何調整圖表樣式

#### 修改圖表高度

**單一圖表**：編輯 `app.py:60`

```python
fig.update_layout(
    height=500,  # 改成你想要的高度（像素）
)
```

**總覽頁面**：編輯 `app.py:120`

```python
fig.update_layout(
    height=800,  # 改成你想要的高度（像素）
)
```

---

#### 修改圖表主題

編輯 `app.py:59` 或 `app.py:121`

```python
fig.update_layout(
    template="plotly_white",  # 可選: plotly, plotly_white, plotly_dark, ggplot2, seaborn 等
)
```

---

#### 修改線條樣式

編輯 `app.py:40-51`（單一圖表）或 `app.py:97-113`（總覽）

```python
fig.add_trace(go.Scatter(
    x=...,
    y=...,
    mode='lines+markers',      # 可選: 'lines', 'markers', 'lines+markers'
    line=dict(width=2),        # 線條寬度
    marker=dict(size=6),       # 標記大小
    ...
))
```

---

#### 調整子圖間距

編輯 `app.py:83-84`

```python
fig = make_subplots(
    rows=2, cols=2,
    vertical_spacing=0.12,     # 垂直間距 (0-1)
    horizontal_spacing=0.10    # 水平間距 (0-1)
)
```

---

### 如何更改 X 軸數據欄位

編輯 `config.py:57`

```python
X_AXIS_FIELD = "你的X軸欄位名稱"  # 例如: "request_rate", "num_prompts" 等
X_AXIS_LABEL = "X 軸顯示標籤"    # 例如: "Request Rate"
```

---

### 如何禁用 Log Scale

編輯 `app.py:57`（單一圖表）或 `app.py:116`（總覽）

```python
# 單一圖表
fig.update_layout(
    xaxis_type="log",  # 改成 "linear" 使用線性刻度
)

# 總覽頁面
fig.update_xaxes(
    type="log",  # 改成 "linear"
    row=row, col=col
)
```

---

## 數據格式

### JSON 檔案結構

每個 JSON 檔案代表一次測試的結果：

```json
{
  "date": "20251120-071736",
  "endpoint_type": "vllm",
  "backend": "vllm",
  "model_id": "openai/gpt-oss-120b",
  "tokenizer_id": "openai/gpt-oss-120b",
  "num_prompts": 1,
  "max_concurrency": null,
  "max_concurrent_requests": 1,
  "completed": 1,
  "total_input_tokens": 1024,
  "total_output_tokens": 128,
  "request_throughput": 0.271,
  "output_throughput": 34.73,
  "total_token_throughput": 312.60,
  "mean_ttft_ms": 40.28,
  "median_ttft_ms": 40.28,
  "std_ttft_ms": 0.0,
  "p99_ttft_ms": 40.28,
  "mean_tpot_ms": 28.69,
  "median_tpot_ms": 28.69,
  "std_tpot_ms": 0.0,
  "p99_tpot_ms": 28.69,
  "mean_itl_ms": 28.69,
  "median_itl_ms": 28.68,
  "std_itl_ms": 0.20,
  "p99_itl_ms": 29.22
}
```

### 常用指標對應

| JSON 欄位                  | 說明                     | 單位      |
|---------------------------|--------------------------|-----------|
| `max_concurrent_requests` | 並發請求數（Concurrency）  | 個        |
| `mean_ttft_ms`            | 平均首字延遲              | 毫秒 (ms) |
| `median_ttft_ms`          | 中位數首字延遲            | 毫秒 (ms) |
| `mean_tpot_ms`            | 平均每字延遲              | 毫秒 (ms) |
| `output_throughput`       | 輸出吞吐量（每查詢）       | tokens/s  |
| `total_token_throughput`  | 系統總吞吐量              | tokens/s  |
| `request_throughput`      | 請求吞吐量                | 請求/s    |
| `mean_itl_ms`             | 平均字間延遲              | 毫秒 (ms) |

---

## 常見問題

### Q1: 如何停止應用程式？

在終端按 `Ctrl+C`。

---

### Q2: 應用程式啟動後瀏覽器沒有自動開啟？

手動開啟瀏覽器並訪問：http://localhost:8050

---

### Q3: 如何更改埠號？

編輯 `app.py:217`：

```python
app.run(debug=True, port=8888)  # 改成你想要的埠號
```

---

### Q4: 圖表沒有顯示數據？

檢查以下項目：

1. **是否選擇了資料夾**：在資料夾選擇區至少勾選一個資料夾
2. **JSON 欄位名稱是否正確**：檢查 `config.py` 中的 `y_field` 是否與 JSON 檔案中的欄位名稱一致
3. **數據是否存在**：確認 `output/` 目錄下有對應的資料夾和 JSON 檔案

---

### Q5: 如何新增更多實驗數據？

1. 在 `output/` 目錄下創建新的資料夾（資料夾名稱即為實驗名稱）
2. 將 JSON 檔案放入該資料夾
3. 重新啟動應用程式（或重新整理頁面）

---

### Q6: 圖表可以匯出嗎？

是的。Plotly 提供內建的匯出功能：

- 滑鼠移到圖表右上角
- 點擊相機圖標
- 可匯出為 PNG 圖片

或在程式碼中使用：

```python
fig.write_image("output.png")      # 需安裝 kaleido
fig.write_html("output.html")      # 保存為互動式 HTML
```

---

### Q7: 如何在總覽頁面顯示更多/更少的子圖？

需要修改兩處：

**1. 修改 `config.py` 中的總覽配置**：

```python
"總覽": {
    "type": "overview",
    "layout": "3x2",  # 改成你想要的佈局（例如 3 行 2 列）
    "charts": [
        # 新增或刪除子圖配置
        {...},
        {...},
        # ... 共 6 個（3x2）
    ]
}
```

**2. 修改 `app.py:80` 的 `make_subplots` 參數**：

```python
fig = make_subplots(
    rows=3, cols=2,  # 與 config.py 保持一致
    subplot_titles=[...],
)
```

**3. 更新 `positions` 列表**（`app.py:87`）：

```python
positions = [
    (1, 1), (1, 2),
    (2, 1), (2, 2),
    (3, 1), (3, 2)
]
```

---

### Q8: 能否支援其他數據格式（CSV, Excel）？

可以。修改 `data_loader.py` 中的 `load_experiment_data` 函式：

```python
def load_experiment_data(folder_name: str, output_dir: str = "output") -> pd.DataFrame:
    folder_path = Path(output_dir) / folder_name
    if not folder_path.exists():
        return pd.DataFrame()

    # 讀取 CSV
    csv_files = sorted(folder_path.glob("*.csv"))
    dfs = [pd.read_csv(f) for f in csv_files]

    # 或讀取 Excel
    excel_files = sorted(folder_path.glob("*.xlsx"))
    dfs = [pd.read_excel(f) for f in excel_files]

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
```

---

## 授權

本專案使用 MIT License。

---

## 聯絡方式

如有問題或建議，歡迎提交 Issue 或 Pull Request。
