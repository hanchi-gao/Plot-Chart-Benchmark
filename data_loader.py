"""數據讀取模組"""

import json
from pathlib import Path
from typing import List, Dict
import pandas as pd


def get_experiment_folders(output_dir: str = "output") -> List[str]:
    """
    取得 output 目錄下的所有實驗資料夾名稱

    Args:
        output_dir: output 資料夾路徑

    Returns:
        資料夾名稱列表
    """
    output_path = Path(output_dir)
    if not output_path.exists():
        return []

    folders = [f.name for f in output_path.iterdir() if f.is_dir()]
    return sorted(folders)


def load_experiment_data(folder_name: str, output_dir: str = "output") -> pd.DataFrame:
    """
    讀取指定實驗資料夾內的所有 JSON 檔案

    Args:
        folder_name: 實驗資料夾名稱
        output_dir: output 資料夾路徑

    Returns:
        包含所有數據的 DataFrame
    """
    folder_path = Path(output_dir) / folder_name
    if not folder_path.exists():
        return pd.DataFrame()

    data_list = []
    json_files = sorted(folder_path.glob("*.json"))

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data_list.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    if not data_list:
        return pd.DataFrame()

    df = pd.DataFrame(data_list)

    # 如果缺少 max_concurrent_requests，使用 num_prompts 作為替代
    if 'max_concurrent_requests' not in df.columns and 'num_prompts' in df.columns:
        df['max_concurrent_requests'] = df['num_prompts']

    # 計算 output_speed_per_query（如果原本沒有的話）
    # 優先使用原本的 output_speed_per_query，如果沒有才計算
    if 'output_speed_per_query' not in df.columns:
        if 'output_throughput' in df.columns and 'max_concurrent_requests' in df.columns:
            df['output_speed_per_query'] = df['output_throughput'] / df['max_concurrent_requests']

    return df


def load_multiple_experiments(folder_names: List[str], output_dir: str = "output") -> Dict[str, pd.DataFrame]:
    """
    讀取多個實驗資料夾的數據

    Args:
        folder_names: 實驗資料夾名稱列表
        output_dir: output 資料夾路徑

    Returns:
        字典，key 為資料夾名稱，value 為對應的 DataFrame
    """
    result = {}
    for folder_name in folder_names:
        df = load_experiment_data(folder_name, output_dir)
        if not df.empty:
            result[folder_name] = df
    return result
