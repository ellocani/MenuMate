# 다수 사용자 취향 통합 및 추천 로직 구현

import pandas as pd

def recommend_for_group(survey_df: pd.DataFrame, menu_df: pd.DataFrame, user_names: list):
    """
    여러 명의 사용자(user_names 리스트)가 함께 있을 때, 공통된 선호도를 고려한 메뉴 추천.
    간단한 예: 해당 사용자들이 준 점수의 평균을 내어 상위 10개 메뉴 추천.
    """
    # user_names에 해당하는 행 추출
    group_data = survey_df[survey_df['이름'].isin(user_names)]
    if group_data.empty:
        return None
    
    # 여러 행(사용자)의 평균 계산
    menu_cols = [c for c in survey_df.columns if c not in ["이름"]]
    group_mean = group_data[menu_cols].mean().sort_values(ascending=False)
    
    # 상위 10개 메뉴
    top_10 = group_mean.head(10)
    
    # 여기서 더 정교하게 필터링(예: 모두 2점 이상인 메뉴 중 평균 상위) 등 가능
    return top_10
