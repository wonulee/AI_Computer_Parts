import pandas as pd
from app.utils.load_data import load_json_dataset, preprocess_datasets

raw_data = load_json_dataset()
dataframes = preprocess_datasets(raw_data)

def recommend_build_with_compat(budget, purpose="gaming",top_n =12, mode="pp_ratio"):
    
    cpu_df = dataframes["cpu"]
    gpu_df = dataframes["gpu"]
    ram_df = dataframes["ram"]
    ssd_df = dataframes["ssd"]
    mainboard_df = dataframes["mainboard"]
    psu_df = dataframes["psu"]

    # 1. 가중치 세팅
    if purpose == "gaming":
        weights = {"cpu": 3, "gpu": 5, "ram": 1, "ssd": 1}
    elif purpose == "office":
        weights = {"cpu": 4, "gpu": 1, "ram": 3, "ssd": 2}
    elif purpose == "editing":
        weights = {"cpu": 2, "gpu": 2, "ram": 4, "ssd": 2}
    elif purpose == "AI/ML":
        weights = {"cpu": 2, "gpu": 5, "ram": 2, "ssd": 1}
    else:
        weights = {"cpu": 2.5, "gpu": 2.5, "ram": 2.5, "ssd": 2.5}
    # 2. 예산 분배
    cpu_budget = budget * 0.23
    mb_budget  = budget * 0.12
    gpu_budget = budget * 0.40
    ram_budget = budget * 0.10
    ssd_budget = budget * 0.08
    psu_budget = budget * 0.07
    
    # 3. 각 부품 후보군 선정
    cpu_top = cpu_df[cpu_df["Price"] <= cpu_budget].sort_values("Performance_MT", ascending=False).head(top_n)
    mb_top  = mainboard_df[mainboard_df["Price"] <= mb_budget].sort_values("Price", ascending=False).head(top_n)
    gpu_top = gpu_df[gpu_df["Price"] <= gpu_budget].sort_values("Performance", ascending=False).head(top_n)
    ram_top = ram_df[ram_df["Price"] <= ram_budget].sort_values("Performance", ascending=False).head(top_n)
    ssd_top = ssd_df[ssd_df["Price"] <= ssd_budget].sort_values("Capacity", ascending=False).head(top_n)
    psu_top = psu_df[psu_df["Price"] <= psu_budget].sort_values("Wattage", ascending=False).head(top_n)
    
    # print(cpu_top)
    # print(mb_top)
    # print(gpu_top)
    # print(ram_top)
    # print(psu_top)
    # print(ssd_top)
    
    import itertools
    best_combo = None
    best_score = -1
    
    for cpu, mb, gpu, ram, ssd, psu in itertools.product(
        cpu_top.itertuples(),
        mb_top.itertuples(),
        gpu_top.itertuples(),
        ram_top.itertuples(),
        ssd_top.itertuples(),
        psu_top.itertuples()
    ):
        cpu_dict = cpu._asdict()
        mb_dict = mb._asdict()
        gpu_dict = gpu._asdict()
        ram_dict = ram._asdict()
        ssd_dict = ssd._asdict()
        psu_dict = psu._asdict()
        total_price = (
            cpu_dict['Price'] + mb_dict['Price'] + gpu_dict['Price'] +
            ram_dict['Price'] + ssd_dict['Price'] + psu_dict['Price']
        )
    
        if total_price > budget:
            continue
        
        # [1] 소켓 호환 (CPU-MB)
        if cpu_dict['Socket'] != mb_dict['Socket']:
            continue
        
        # [2] RAM 타입 호환
        if ram_dict['Type'] != mb_dict['RAM']:
            continue
        
        # [3] SSD 타입 호환 (예: NVMe/SATA)
        # if "ssd_type" in mb._fields and "type" in ssd._fields:
        #     if ssd.type not in mb.ssd_type:
        #         continue
        
        # [4] 파워 용량 체크 (합산 TDP가 psu 용량 이내)
        required_power = cpu_dict['TDP'] + gpu_dict['TDP'] + 150  # 시스템 여유 포함
        if psu_dict['Wattage'] < required_power:
            continue
        
        # [5] 가중치 성능 + 가격 고려
        weighted_perf = (
            cpu_dict['Performance_MT'] * weights["cpu"] +
            gpu_dict["Performance"] * weights["gpu"] +
            ram_dict['Performance'] * weights["ram"] +
            ssd_dict['Performance'] * weights["ssd"]
        )
        
        if mode == "pp_ratio":
            score = weighted_perf
        if score > best_score:
            best_score = score
            best_combo = {
                "Purpose" : purpose,
                "CPU": cpu_dict['Model'],
                "Mainboard": mb_dict['Model'],
                "GPU": gpu_dict['Model'],
                "RAM": ram_dict['Model'],
                "SSD": ssd_dict['Model'],
                "PSU": psu_dict['Model'],
                "Total_Performance": weighted_perf,
                "Total_Price": total_price
            }
    return best_combo

# result = recommend_build_with_compat(1200, purpose='gaming', top_n=12)
# print(result)