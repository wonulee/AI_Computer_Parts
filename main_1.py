import json
import pandas as pd

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

# cpu와 mainboard 호환성 검증 함수
def check_cpu_mainboard_compatibility(cpu_df, mainboard_df):
    compatible_combinations = []  # 호환되는 조합을 저장
    
    # CPU와 메인보드의 소켓 
    for cpu_index, cpu in cpu_df.iterrows():  # 각 CPU 모델 반복
        for mb_index, mainboard in mainboard_df.iterrows():  # 각 메인보드 모델 반복
            if cpu['Socket'] == mainboard['Socket'] :
                compatible_combinations.append({
                    'cpu_index': cpu_index,
                    'cpu_model': cpu['Model'],
                    'mainboard_index': mb_index,
                    'mainboard_model': mainboard['Model']
                })
    
    return compatible_combinations

# 호환성 검사 실행
compatible_combinations = check_cpu_mainboard_compatibility(cpu_df, mainboard_df)

# 호환되는 항목 출력
if compatible_combinations:
    for item in compatible_combinations:
        print(f"Compatible: {item['cpu_model']} (CPU) and {item['mainboard_model']} (Mainboard)")
else:
    print("No compatible combinations found.")