import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import itertools

# JSON 데이터 가져오기
with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/cpu_data.json", 'r', encoding='utf-8') as file:
    cpu_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/gpu_data.json", 'r', encoding='utf-8') as file:
    gpu_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/ram_data.json", 'r', encoding='utf-8') as file:
    ram_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/ssd_data.json", 'r', encoding='utf-8') as file:
    ssd_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/mainboard_data.json", 'r', encoding='utf-8') as file:
    mainboard_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/psu_data.json", 'r', encoding='utf-8') as file:
    psu_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/cooler_data.json", 'r', encoding='utf-8') as file:
    cooler_data = json.load(file)

with open("C:/Users/Home PC/Documents/AI_Computer_Parts/Json_dataset/case_data.json", 'r', encoding='utf-8') as file:
    case_data = json.load(file)

# 데이터프레임으로 변환
cpu_df = pd.DataFrame(cpu_data)
gpu_df = pd.DataFrame(gpu_data)
ram_df = pd.DataFrame(ram_data)
ssd_df = pd.DataFrame(ssd_data)
mainboard_df = pd.DataFrame(mainboard_data)
psu_df = pd.DataFrame(psu_data)
cooler_df = pd.DataFrame(cooler_data)
case_df = pd.DataFrame(case_data)

# CPU와 Mainboard의 모든 조합 생성
combinations = list(itertools.product(cpu_df.iterrows(), mainboard_df.iterrows()))

# 결과 저장
results = []

# CPU와 Mainboard 교차 체크
for (i, cpu), (j, mb) in combinations:
    compatibility = 1 if cpu['Socket'] == mb['Socket'] else 0
    results.append({
        'CPU_Model': cpu['Model'],
        'Mainboard_Model': mb['Model'],
        'CPU_Socket': cpu['Socket'],
        'Mainboard_Socket': mb['Socket'],
        'Compatible': compatibility,
        'Wifi': mb['WiFi'],
        'iGPU': cpu['iGPU']
    })

# CPU와 Mainboard의 Socket 호환(Compatible) 유무 df
compatibility_df = pd.DataFrame(results)

# Compatible이 1인 경우만 필터링 (호환되는 조합)
compatible_only_df = compatibility_df[compatibility_df['Compatible'] == 1]

# Wifi "Yes" → 1, 아니면 0
compatible_only_df['Wifi'] = compatible_only_df['Wifi'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)

# iGPU "Yes" → 1, 아니면 0
compatible_only_df['iGPU'] = compatible_only_df['iGPU'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)

# index 초기화
compatible_only_df = compatible_only_df.reset_index(drop=True)

# 결과 출력
print(compatible_only_df)
