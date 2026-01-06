"""主應用程式 - Dash 互動式介面"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_loader import get_experiment_folders, load_multiple_experiments
from config import CHART_TABS, X_AXIS_FIELD, X_AXIS_LABEL, OUTPUT_DIR


# 初始化 Dash 應用程式
app = dash.Dash(__name__)
app.title = "數據比較互動式窗格"

# 取得可用的實驗資料夾
available_folders = get_experiment_folders(OUTPUT_DIR)


def create_single_chart(data_dict, y_field, y_label, title):
    """
    創建單一圖表

    Args:
        data_dict: 實驗數據字典 {folder_name: DataFrame}
        y_field: Y 軸數據欄位
        y_label: Y 軸標籤
        title: 圖表標題

    Returns:
        plotly Figure 物件
    """
    fig = go.Figure()

    for folder_name, df in data_dict.items():
        if X_AXIS_FIELD in df.columns and y_field in df.columns:
            # 按 concurrency 排序
            df_sorted = df.sort_values(X_AXIS_FIELD)

            fig.add_trace(go.Scatter(
                x=df_sorted[X_AXIS_FIELD],
                y=df_sorted[y_field],
                mode='lines+markers',
                name=folder_name,
                hovertemplate=(
                    f'<b>{folder_name}</b><br>' +
                    f'{X_AXIS_LABEL}: %{{x}}<br>' +
                    f'{y_label}: %{{y:.2f}}<br>' +
                    '<extra></extra>'
                )
            ))

    fig.update_layout(
        title=title,
        xaxis_title=X_AXIS_LABEL,
        yaxis_title=y_label,
        xaxis_type="linear",
        hovermode='x unified',
        template="plotly_white",
        height=500,
    )

    return fig


def create_overview_chart(data_dict):
    """
    創建總覽圖表（2x2 佈局）

    Args:
        data_dict: 實驗數據字典 {folder_name: DataFrame}

    Returns:
        plotly Figure 物件
    """
    overview_config = CHART_TABS["總覽"]
    charts = overview_config["charts"]

    # 創建 2x2 子圖
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[chart["title"] for chart in charts],
        vertical_spacing=0.12,
        horizontal_spacing=0.10
    )

    # 為每個實驗資料夾分配固定顏色
    color_palette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    folder_colors = {folder: color_palette[i % len(color_palette)]
                     for i, folder in enumerate(data_dict.keys())}

    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]

    for idx, (chart_config, (row, col)) in enumerate(zip(charts, positions)):
        y_field = chart_config["y_field"]
        y_label = chart_config["y_label"]

        for folder_name, df in data_dict.items():
            if X_AXIS_FIELD in df.columns and y_field in df.columns:
                df_sorted = df.sort_values(X_AXIS_FIELD)

                fig.add_trace(
                    go.Scatter(
                        x=df_sorted[X_AXIS_FIELD],
                        y=df_sorted[y_field],
                        mode='lines+markers',
                        name=folder_name,
                        legendgroup=folder_name,
                        showlegend=(idx == 0),  # 只在第一個圖顯示圖例
                        line=dict(color=folder_colors[folder_name]),
                        marker=dict(color=folder_colors[folder_name]),
                        hovertemplate=(
                            f'<b>{folder_name}</b><br>' +
                            f'{X_AXIS_LABEL}: %{{x}}<br>' +
                            f'{y_label}: %{{y:.2f}}<br>' +
                            '<extra></extra>'
                        )
                    ),
                    row=row, col=col
                )

        # 更新子圖軸
        fig.update_xaxes(title_text=X_AXIS_LABEL, type="linear", row=row, col=col)
        fig.update_yaxes(title_text=y_label, row=row, col=col)

    fig.update_layout(
        height=800,
        template="plotly_white",
        hovermode='x unified',
    )

    return fig


# 應用程式佈局
app.layout = html.Div([
    html.H1("數據比較互動式窗格", style={'textAlign': 'center', 'marginTop': 20}),

    # 資料夾選擇區
    html.Div([
        html.H3("選擇實驗資料夾："),
        dcc.Checklist(
            id='folder-checklist',
            options=[{'label': folder, 'value': folder} for folder in available_folders],
            value=[],  # 預設不選擇任何資料夾
            style={'marginBottom': 20}
        ),
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px'}),

    # TAG 標籤頁
    html.Div([
        dcc.Tabs(
            id='chart-tabs',
            value='總覽',
            children=[
                dcc.Tab(label=tab_name, value=tab_name)
                for tab_name in CHART_TABS.keys()
            ]
        ),
    ], style={'margin': '20px'}),

    # 圖表顯示區
    html.Div([
        dcc.Graph(id='chart-display')
    ], style={'margin': '20px'}),
])


@app.callback(
    Output('chart-display', 'figure'),
    [Input('folder-checklist', 'value'),
     Input('chart-tabs', 'value')]
)
def update_chart(selected_folders, selected_tab):
    """
    更新圖表顯示

    Args:
        selected_folders: 選中的資料夾列表
        selected_tab: 選中的 TAG

    Returns:
        更新後的圖表
    """
    if not selected_folders:
        # 沒有選擇資料夾時顯示空圖表
        fig = go.Figure()
        fig.update_layout(
            title="請選擇至少一個實驗資料夾",
            template="plotly_white",
            height=500,
        )
        return fig

    # 載入選中的實驗數據
    data_dict = load_multiple_experiments(selected_folders, OUTPUT_DIR)

    if not data_dict:
        fig = go.Figure()
        fig.update_layout(
            title="無法載入數據",
            template="plotly_white",
            height=500,
        )
        return fig

    # 根據選中的 TAG 創建對應的圖表
    tab_config = CHART_TABS[selected_tab]

    if tab_config["type"] == "overview":
        return create_overview_chart(data_dict)
    else:
        return create_single_chart(
            data_dict,
            tab_config["y_field"],
            tab_config["y_label"],
            tab_config["title"]
        )


if __name__ == '__main__':
    print(f"找到 {len(available_folders)} 個實驗資料夾: {available_folders}")
    print("啟動應用程式於 http://0.0.0.0:8050")
    print("本機訪問: http://localhost:8050")
    print("網路訪問: http://<你的IP>:8050")
    app.run(host='0.0.0.0', port=8050, debug=True)
