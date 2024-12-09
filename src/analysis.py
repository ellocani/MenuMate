# 개별 사용자 취향 분석 기능 구현

import pandas as pd

def get_user_preference_summary(survey_df: pd.DataFrame, menu_df: pd.DataFrame, user_name: str):
    """
    특정 사용자의 선호도 요약:
    - 평균 선호도
    - 상위 10개, 하위 10개 메뉴
    - 환장함(4점) 메뉴들의 공통 특성 파악
    """
    # 해당 사용자 데이터 추출
    user_data = survey_df[survey_df['이름'] == user_name]
    if user_data.empty:
        return None
    
    # 한 명당 한 행이라 가정 (만약 여러 행이면 평균 혹은 최근 것)
    user_row = user_data.iloc[0]
    
    menu_cols = [c for c in survey_df.columns if c not in ["이름"]]
    scores = user_row[menu_cols].dropna()
    
    avg_score = scores.mean()
    top_10 = scores.sort_values(ascending=False).head(10)
    bottom_10 = scores.sort_values(ascending=True).head(10)
    
    # 환장함 메뉴들
    favorite_menus = scores[scores == 4].index.tolist()
    
    # Unknown을 제외한 메뉴 상세 정보 분석
    favorite_details = menu_df[menu_df['메뉴'].isin(favorite_menus)]
    
    # Unknown을 제외하고 공통된 음식 속성 빈도 계산
    common_ingredients = favorite_details[favorite_details['주재료'] != 'Unknown']['주재료'].value_counts()
    common_flavors = favorite_details[favorite_details['맛 프로파일'] != 'Unknown']['맛 프로파일'].value_counts()
    common_meal_types = favorite_details[favorite_details['식사 타입/상황'] != 'Unknown']['식사 타입/상황'].value_counts()
    common_cooking_methods = favorite_details[favorite_details['조리 방식'] != 'Unknown']['조리 방식'].value_counts()
    common_categories = favorite_details[favorite_details['분류'] != 'Unknown']['분류'].value_counts()
    
    summary = {
        "avg_score": avg_score,
        "top_10": top_10,
        "bottom_10": bottom_10,
        "common_ingredients": common_ingredients.to_dict() if not common_ingredients.empty else {},
        "common_flavors": common_flavors.to_dict() if not common_flavors.empty else {},
        "common_meal_types": common_meal_types.to_dict() if not common_meal_types.empty else {},
        "common_cooking_methods": common_cooking_methods.to_dict() if not common_cooking_methods.empty else {},
        "common_categories": common_categories.to_dict() if not common_categories.empty else {}
    }
    return summary

def get_user_category_preference(survey_df: pd.DataFrame, menu_df: pd.DataFrame, user_name: str):
    """
    특정 사용자에 대해 음식종류, 맛 프로파일, 조리방식별 평균 선호도 분석
    맛 프로파일은 개별 속성으로 분리하여 분석
    """
    user_data = survey_df[survey_df['이름'] == user_name]
    if user_data.empty:
        return None
    
    user_row = user_data.iloc[0]
    menu_cols = [c for c in survey_df.columns if c not in ["이름"]]
    user_scores = pd.DataFrame({"메뉴": menu_cols, "rating": user_row[menu_cols].values})
    
    # 메뉴 속성과 조인
    merged = pd.merge(user_scores, menu_df, on="메뉴", how="left")
    
    # 맛 프로파일 분리 및 집계
    flavor_scores = {}
    for idx, row in merged.iterrows():
        if row['맛 프로파일'] != 'Unknown':
            flavors = row['맛 프로파일'].split('/')
            for flavor in flavors:
                if flavor not in flavor_scores:
                    flavor_scores[flavor] = []
                flavor_scores[flavor].append(row['rating'])
    
    # 각 맛 프로파일별 평균 계산
    flavor_mean = pd.Series({
        flavor: sum(scores)/len(scores) 
        for flavor, scores in flavor_scores.items()
    }).sort_values(ascending=False)
    
    # 기존 카테고리와 조리방식 분석
    category_mean = merged[merged['분류'] != 'Unknown'].groupby('분류')['rating'].mean().sort_values(ascending=False)
    cooking_mean = merged[merged['조리 방식'] != 'Unknown'].groupby('조리 방식')['rating'].mean().sort_values(ascending=False)
    
    return {
        "category_mean": category_mean,
        "flavor_mean": flavor_mean,
        "cooking_mean": cooking_mean
    }
