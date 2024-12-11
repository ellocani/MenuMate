import pandas as pd

# 파일 로드
processed_menu_details = pd.read_csv("data\processed_menu_details.csv")  # 파일명에 맞게 수정

# 수치형 데이터만 선택
numeric_features = processed_menu_details.select_dtypes(include=[int, float])

# 상관관계 행렬 계산
correlation_matrix = numeric_features.T.corr()

# 결과를 CSV 파일로 저장
correlation_matrix.to_csv("data/menu_correlation_matrix.csv", index=True)

print("메뉴 간 상관관계 데이터가 'data/menu_correlation_matrix.csv'에 저장되었습니다.")
