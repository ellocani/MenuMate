import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('data/processed_menu_details.csv')

# '맛 프로파일_소스별 상이' 컬럼 삭제
df = df.drop('맛 프로파일_소스별 상이', axis=1)

# 수정된 데이터프레임을 CSV 파일로 저장
df.to_csv('data/processed_menu_details.csv', index=False)