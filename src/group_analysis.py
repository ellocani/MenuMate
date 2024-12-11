import pandas as pd

def recommend_menus(user_names, user_data_path, correlation_matrix_path, top_n=3, top_reasons=10, weight=2.0, diversity_penalty=0.8):
    """
    여러 사용자에 대해 최적 메뉴를 추천합니다. 특정 메뉴의 독점 문제를 완화합니다.

    Args:
        user_names (list): 사용자 이름 리스트.
        user_data_path (str): 사용자 데이터 파일 경로.
        correlation_matrix_path (str): 메뉴 상관관계 행렬 파일 경로.
        top_n (int): 추천할 메뉴의 개수.
        top_reasons (int): 각 메뉴 추천 이유로 보여줄 상위 유사도 메뉴의 개수.
        weight (float): 사용자 선호 메뉴에 부여할 가중치. 기본값은 2.0.
        diversity_penalty (float): 상관관계의 집중도를 완화하는 계수. 기본값은 0.8.

    Returns:
        list: 추천 메뉴 리스트 (추천 메뉴와 점수, 이유 포함).
    """
    # 데이터 로드
    user_data = pd.read_csv(user_data_path)
    correlation_matrix = pd.read_csv(correlation_matrix_path, index_col=0)

    # 사용자 선호 메뉴 추출
    preferred_menus = set()
    for user_name in user_names:
        if user_name not in user_data["이름"].values:
            print(f"사용자 '{user_name}' 데이터가 없습니다. 무시합니다.")
            continue
        user_row = user_data[user_data["이름"] == user_name]
        user_preferences = user_row.iloc[0, 1:]  # 메뉴별 점수
        preferred_menus.update(user_preferences[user_preferences >= 4].index)

    if not preferred_menus:
        raise ValueError("입력한 사용자들에 대해 선호 메뉴가 없습니다.")

    # 추천 점수 계산 (상위 유사도 제한 + 다양성 규제)
    weighted_scores = correlation_matrix[list(preferred_menus)] * weight
    top_correlated_scores = weighted_scores.apply(lambda x: x.nlargest(5).mean(), axis=1)  # 상위 5개 유사도 평균
    recommendation_scores = top_correlated_scores / (1 + diversity_penalty * correlation_matrix.std(axis=1))  # 다양성 강화
    recommendation_scores = recommendation_scores.sort_values(ascending=False)

    # 상위 N개의 메뉴 추천 (선호 메뉴 제외)
    recommended_menus = recommendation_scores.index[~recommendation_scores.index.isin(preferred_menus)].tolist()
    recommended_menus = recommended_menus[:top_n]

    # 상세 이유 포함
    detailed_recommendations = [
        {
            "menu": menu,
            "score": recommendation_scores[menu],
            "reason": ", ".join(
                f"{preferred_menu} (유사도: {correlation_matrix.loc[menu, preferred_menu]:.2f})"
                for preferred_menu in sorted(preferred_menus, key=lambda x: correlation_matrix.loc[menu, x], reverse=True)[:top_reasons]
                if preferred_menu in correlation_matrix.columns
            )
        }
        for menu in recommended_menus
    ]

    return detailed_recommendations
