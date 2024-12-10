import pandas as pd
import re

# menu_details.csv 전처리
# 복합 특성을 개별 특성으로 분리하는 함수
def split_compound_features(df: pd.DataFrame) -> pd.DataFrame:
    # 기본 컬럼으로 시작
    base_df = df[['메뉴', '간편성', '분류']].copy()
    
    # 각 특성별 이진 컬럼을 저장할 딕셔너리
    feature_dicts = {
        '주재료': {},
        '맛 프로파일': {},
        '식사 타입/상황': {},
        '조리 방식': {},
        '계절/날씨': {}
    }
    
    # 각 특성에 대해 이진 컬럼 생성
    for column in feature_dicts.keys():
        unique_features = set()
        for features in df[column].str.split(r'[+\/\(\),]'):
            if isinstance(features, list):
                unique_features.update(feat.strip() for feat in features if feat.strip())
        
        # 각 고유 특성에 대한 이진 값 계산
        for feature in unique_features:
            col_name = f'{column}_{feature}'
            feature_dicts[column][col_name] = df[column].str.contains(feature, na=False).astype(int)
    
    # 모든 특성 DataFrames를 한 번에 결합
    feature_dfs = [pd.DataFrame(d) for d in feature_dicts.values()]
    result_df = pd.concat([base_df] + feature_dfs, axis=1)
    
    return result_df
    
df = pd.read_csv('data/raw/menu_details.csv')
processed_df = split_compound_features(df)
        
# 결과를 새로운 CSV 파일로 저장
processed_df.to_csv('data/processed/processed_menu_details.csv', index=False, encoding='utf-8')
     
     
# user_data.csv 전처리
# CSV 파일 읽기
df = pd.read_csv('data/raw/user_data.csv')

# 이름이 없는 행 제거 (이름 열이 비어있거나 공백인 경우)
df = df[df['이름'].notna() & (df['이름'].str.strip() != '')]

# 선호도 점수 매핑 함수
def map_preference_to_score(preference):
    mapping = {
        '1. 환장함': 4,
        '2. 좋아함': 3,
        '3. 그럭저럭': 2,
        '4. 싫어함': 1
    }
    return mapping.get(preference, None)

# 첫 번째 열(이름)을 제외한 모든 열에 대해 매핑 적용
for column in df.columns[1:]:
    df[column] = df[column].map(map_preference_to_score)

# 새로운 CSV 파일로 저장
df.to_csv('data/processed/processed_user_data.csv', index=False, encoding='utf-8')