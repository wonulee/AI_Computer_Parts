# data_loader.py
import json
import pandas as pd

def load_json_dataset(path_prefix="./Json_dataset"):
    def load(filename):
        with open(f"{path_prefix}/{filename}", 'r', encoding='utf-8') as f:
            return json.load(f)

    return {
        "cpu": load("cpu_data.json"),
        "newcpu": load("cpu_newdata.json"),
        "gpu": load("gpu_data.json"),
        "ram": load("ram_data.json"),
        "ssd": load("ssd_data.json"),
        "mainboard": load("mainboard_data.json"),
        "psu": load("psu_data.json"),
        "cooler": load("cooler_data.json"),
        "case": load("case_data.json"),
    }

def preprocess_datasets(data):
    cpu_df = pd.DataFrame(data["cpu"])
    cpu_df['TDP'] = pd.to_numeric(cpu_df['TDP'].str.replace('W','',regex=False), errors='coerce')
    cpu_df = cpu_df.dropna(subset=['Price'])

    gpu_df = pd.DataFrame(data["gpu"])
    gpu_df['TDP'] = pd.to_numeric(gpu_df['TDP'].str.replace('W','',regex=False), errors='coerce')
    gpu_df = gpu_df.dropna(subset=['Price'])

    psu_df = pd.DataFrame(data["psu"])
    psu_df['Wattage'] = pd.to_numeric(psu_df['Wattage'], errors='coerce')

    # 나머지도 필요시 반환
    return {
        "cpu": cpu_df,
        "newcpu": pd.DataFrame(data["newcpu"]),
        "gpu": gpu_df,
        "ram": pd.DataFrame(data["ram"]),
        "ssd": pd.DataFrame(data["ssd"]),
        "mainboard": pd.DataFrame(data["mainboard"]),
        "psu": psu_df,
        "cooler": pd.DataFrame(data["cooler"]),
        "case": pd.DataFrame(data["case"]),
    }