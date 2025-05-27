from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import json
import pandas as pd

app = FastAPI()



# JSON 데이터 가져오기(Notebook)
# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/cpu_data.json", 'r', encoding='utf-8') as file:
#     cpu_data = json.load(file)
    
# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/cpu_newdata.json", 'r', encoding='utf-8') as file:
#     newcpu_data = json.load(file)    

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/gpu_data.json", 'r', encoding='utf-8') as file:
#     gpu_data = json.load(file)

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/ram_data.json", 'r', encoding='utf-8') as file:
#     ram_data = json.load(file)

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/ssd_data.json", 'r', encoding='utf-8') as file:
#     ssd_data = json.load(file)

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/mainboard_data.json", 'r', encoding='utf-8') as file:
#     mainboard_data = json.load(file)

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/psu_data.json", 'r', encoding='utf-8') as file:
#     psu_data = json.load(file)

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/cooler_data.json", 'r', encoding='utf-8') as file:
#     cooler_data = json.load(file)

# with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/case_data.json", 'r', encoding='utf-8') as file:
#     case_data = json.load(file)

# JSON 데이터 가져오기(Desktop)
with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/cpu_data.json", 'r', encoding='utf-8') as file:
    cpu_data = json.load(file)
    
with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/cpu_newdata.json", 'r', encoding='utf-8') as file:
    newcpu_data = json.load(file)    

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/gpu_data.json", 'r', encoding='utf-8') as file:
    gpu_data = json.load(file)

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/ram_data.json", 'r', encoding='utf-8') as file:
    ram_data = json.load(file)

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/ssd_data.json", 'r', encoding='utf-8') as file:
    ssd_data = json.load(file)

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/mainboard_data.json", 'r', encoding='utf-8') as file:
    mainboard_data = json.load(file)

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/psu_data.json", 'r', encoding='utf-8') as file:
    psu_data = json.load(file)

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/cooler_data.json", 'r', encoding='utf-8') as file:
    cooler_data = json.load(file)

with open("c:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/case_data.json", 'r', encoding='utf-8') as file:
    case_data = json.load(file)

# 데이터프레임으로 변환
cpu_df = pd.DataFrame(cpu_data)
newcpu_df = pd.DataFrame(newcpu_data)
gpu_df = pd.DataFrame(gpu_data)
ram_df = pd.DataFrame(ram_data)
ssd_df = pd.DataFrame(ssd_data)
mainboard_df = pd.DataFrame(mainboard_data)
psu_df = pd.DataFrame(psu_data)
cooler_df = pd.DataFrame(cooler_data)
case_df = pd.DataFrame(case_data)

cpu_df['TDP'] = cpu_df['TDP'].str.replace('W','',regex=False).astype(int)
cpu_df = cpu_df.dropna(subset=['Price'])
cpu_df['TDP'] = pd.to_numeric(cpu_df['TDP'], errors='coerce')

gpu_df['TDP'] = gpu_df['TDP'].str.replace('W','',regex=False).astype(int)
gpu_df = gpu_df.dropna(subset=['Price'])
psu_df['Wattage'] = pd.to_numeric(psu_df['Wattage'], errors='coerce')

# print(cpu_df.dtypes)
# print(psu_df.dtypes)

def recommend_build_with_compat(budget, purpose="gaming",top_n =12, mode="pp_ratio"):
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

    print(cpu_top)
    print(mb_top)
    print(gpu_top)
    print(ram_top)
    print(psu_top)
    print(ssd_top)
    
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
                "Total_Price": total_price,
            }
    return best_combo

@app.get("/recommend")
def recommned(
    budget: float = Query(1000, description="예산(달러)"),
    purpose: str = Query("gaming", description="용도"),
    top_n: int = Query(10, description="부품 후보 개수") 
):
    result = recommend_build_with_compat(budget, purpose, top_n=top_n)
    return result

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})