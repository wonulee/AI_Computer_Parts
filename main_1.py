import json
import pandas as pd
import itertools
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# JSON 데이터 가져오기
with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/cpu_data.json", 'r', encoding='utf-8') as file:
    cpu_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/gpu_data.json", 'r', encoding='utf-8') as file:
    gpu_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/ram_data.json", 'r', encoding='utf-8') as file:
    ram_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/ssd_data.json", 'r', encoding='utf-8') as file:
    ssd_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/mainboard_data.json", 'r', encoding='utf-8') as file:
    mainboard_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/psu_data.json", 'r', encoding='utf-8') as file:
    psu_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/cooler_data.json", 'r', encoding='utf-8') as file:
    cooler_data = json.load(file)

with open("C:/Users/이원우/Documents/Project/AI_Computer_Parts/Json_dataset/case_data.json", 'r', encoding='utf-8') as file:
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
le = LabelEncoder()
compatible_only_df['Wifi'] = le.fit_transform(compatible_only_df['Wifi'].astype(str).str.strip().str.lower())

# iGPU "Yes" → 1, 아니면 0
compatible_only_df['iGPU'] = le.fit_transform(compatible_only_df['iGPU'].astype(str).apply(lambda x: x.strip().lower()))

# OneHotEncoder 객체 생성 (sparse=False: 넘파이 배열로 반환)
ohe = OneHotEncoder(sparse=False)

# 'Profile' 컬럼을 문자열로 변환한 뒤, 원-핫 인코딩하여 numpy 배열로 변환
ram_profiles = ohe.fit_transform(ram_df[['Profile']].astype(str))

# OneHotEncoder가 자동으로 생성한 각 범주의 이름 앞에 'Profile_'을 붙여 컬럼명 리스트 생성 ????
profile_labels = [f"Profile_{m}" for m in ohe.categories_[0]]

# 인코딩된 numpy 배열을 DataFrame으로 변환, 컬럼명은 위에서 만든 profile_labels 사용
ram_profile_df = pd.DataFrame(ram_profiles, columns=profile_labels)

# 기존 ram_df에서 'Profile' 컬럼을 삭제하고, 인코딩된 DataFrame을 옆에 합침(axis=1)
ram_df = pd.concat([ram_df.drop(columns=['Profile']), ram_profile_df], axis=1)


print(ram_df)

# index 초기화
compatible_only_df = compatible_only_df.reset_index(drop=True)

# CPU 제조사(Intel/AMD) 파생 컬럼 추가 (intel=1, amd= 0)
def get_cpu_maker(model):
    model = str(model).lower()
    if 'intel' in model:
        return '1'
    elif 'amd' in model:
        return '0'
    else:
        return 'null'

# CPU_Maker 컬럼 추가하기
compatible_only_df['CPU_Maker'] = compatible_only_df['CPU_Model'].apply(get_cpu_maker)

# CPU_Socket, Mainboard_Socket 컬럼 지우기
cpu_mb_compatible_df = compatible_only_df.drop(['CPU_Socket', 'Mainboard_Socket'], axis=1)

# 결과 출력
print(compatible_only_df)
print(cpu_mb_compatible_df)