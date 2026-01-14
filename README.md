# GPU Benchmark 數據視覺化工具

實驗數據視覺化與比較工具，支援多次實驗結果的疊圖分析與互動式數據查看。

## 功能特色

- **多實驗比較**：選擇多個實驗資料夾，在同一張圖上疊加比較
- **互動式圖表**：滑鼠懸停顯示詳細數據，支援縮放與導覽
- **多指標分頁**：切換不同效能指標（TTFT、吞吐量、延遲等）
- **總覽頁面**：2×3 佈局同時顯示 6 個關鍵指標

## 快速開始

### 系統需求
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (推薦) 或 pip

### 安裝與執行

```bash
# 使用 uv（推薦）
uv run app.py

# 或使用 pip
pip install dash plotly pandas
python app.py
```

瀏覽器會自動開啟 http://localhost:8050

## 使用方式

1. **準備數據**：將實驗數據放入 `output/` 目錄的子資料夾中
2. **選擇實驗**：在頁面上勾選要比較的實驗資料夾
3. **切換指標**：點擊標籤頁查看不同的效能指標
4. **互動檢視**：滑鼠懸停查看數值、拖曳縮放、雙擊重置

## 專案結構

```
Plot-Chart-Benchmark/
├── app.py                  # 主應用程式
├── config.py              # 圖表配置
├── data_loader.py         # 數據載入
├── output/                # 實驗數據目錄
│   ├── [實驗1]/
│   ├── [實驗2]/
│   └── C_CONFIG_README.md # C 方案配置說明
└── README.md
```

## 硬體配置說明

本專案包含多種 GPU 配置的測試結果：

- **R9700 系列**: 1卡、2卡、4卡、8卡配置測試
- **Threadripper PRO CPU 對比**: 7955WX, 7995WX, 9955WX, 9975WX
- **AMD Pro/Instinct**: Pro4500, MI350, MI300X
- **NVIDIA**: H100-SXM, H200-SXM

**重要提示：** `2xR9700_x16_*` 資料夾的測試是在**四卡機上只使用兩張卡**進行的，每張卡享有完整 PCIe x16 頻寬。

所有 AMD GPU 測試均使用 ROCm 7.0。

## 數據格式

每個 JSON 檔案代表一次測試結果，包含以下關鍵指標：

```json
{
  "max_concurrent_requests": 1,    // 並發數
  "mean_ttft_ms": 40.28,          // 首字延遲 (ms)
  "output_throughput": 34.73,     // 輸出吞吐量 (tokens/s)
  "total_token_throughput": 312.60,// 系統總吞吐量 (tokens/s)
  "mean_tpot_ms": 28.69,          // 每字延遲 (ms)
  "mean_itl_ms": 28.69            // 字間延遲 (ms)
}
```

## 自訂配置

### 新增指標標籤

編輯 `config.py` 中的 `CHART_TABS`：

```python
CHART_TABS = {
    "新指標名稱": {
        "type": "single",
        "y_field": "json_欄位名稱",
        "y_label": "Y 軸標籤",
        "title": "圖表標題 vs. Concurrency"
    }
}
```

### 修改總覽佈局

1. 編輯 `config.py` 的總覽配置
2. 修改 `app.py` 中的 `make_subplots` 參數

## 常見問題

**Q: 圖表沒有顯示數據？**
- 確認已勾選至少一個實驗資料夾
- 檢查 JSON 檔案欄位名稱是否與 `config.py` 一致

**Q: 如何匯出圖表？**
- 滑鼠移到圖表右上角，點擊相機圖標匯出 PNG

**Q: 如何更改埠號？**
- 編輯 `app.py` 最後一行：`app.run(debug=True, port=8888)`

## 授權

MIT License
