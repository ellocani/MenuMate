import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 파일 경로 정의
input_file_path = "data/processed_menu_details.csv"  # 입력 파일 경로
output_file_path = "data/menu_correlation_matrix.csv"  # 출력 파일 경로

# 파일 로드
processed_menu_details = pd.read_csv(input_file_path)

# 수치형 데이터만 선택
numeric_features = processed_menu_details.select_dtypes(include=[int, float])

# 코사인 유사도 계산
correlation_matrix = cosine_similarity(numeric_features)

# DataFrame으로 변환
correlation_matrix_df = pd.DataFrame(
    correlation_matrix, 
    index=processed_menu_details['메뉴'], 
    columns=processed_menu_details['메뉴']
)

# 결과를 CSV 파일로 저장
correlation_matrix_df.to_csv(output_file_path, index=True)

print(f"메뉴 간 상관관계 데이터가 '{output_file_path}'에 저장되었습니다.")
