import numpy as np
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
        tuple: (추천 메뉴 리스트, 랜덤 추천 메뉴 리스트)
    """
    # 데이터 로드
    user_data = pd.read_csv(user_data_path)
    correlation_matrix = pd.read_csv(correlation_matrix_path, index_col=0)

    # 사용자 선호 메뉴 추출
    preferred_menus = set()
    total_scores = pd.Series(0.0, index=correlation_matrix.index)  # 초기화된 점수 시리즈, 명시적으로 float 타입 지정

    for user_name in user_names:
        if user_name not in user_data["이름"].values:
            print(f"사용자 '{user_name}' 데이터가 없습니다. 무시합니다.")
            continue
        user_row = user_data[user_data["이름"] == user_name]
        user_preferences = user_row.iloc[0, 1:]  # 메뉴별 점수
        preferred_menus.update(user_preferences[user_preferences >= 4].index)

        # 결측값 처리 및 타입 변환 방식 수정
        user_preferences_filled = (
            user_preferences
            .astype(float)  # 먼저 float 타입으로 변환
            .fillna(0.0)    # 명시적으로 float 타입의 0 사용
        )
        total_scores += user_preferences_filled

    if not preferred_menus:
        raise ValueError("입력한 사용자들에 대해 선호 메뉴가 없습니다.")

    # 1. 상관관계 기반 점수 계산
    weighted_scores = correlation_matrix[list(preferred_menus)] * weight
    normalized_scores = weighted_scores.mean(axis=1)  # 평균화
    penalized_scores = normalized_scores / (1 + diversity_penalty * weighted_scores.std(axis=1))  # 다양성 보정

    # 2. 사용자 점수 기반 점수 계산
    user_preference_scores = total_scores / len(user_names)  # 사용자별 평균 점수

    # 3. 상관관계 점수와 사용자 점수를 3:7으로 결합
    combined_scores = 0.3 * penalized_scores + 0.7 * user_preference_scores

    # 4. 랜덤성 추가
    random_scores = np.random.rand(len(combined_scores)) * 0.1  # 랜덤 요소 추가
    final_scores = combined_scores + random_scores
    final_scores = final_scores.sort_values(ascending=False)

    # 상위 N개의 메뉴 추천 (선호 메뉴 제외)
    recommended_menus = final_scores.index[~final_scores.index.isin(preferred_menus)].tolist()
    recommended_menus = recommended_menus[:top_n]

    # 랜덤 추천 메뉴 (중복되지 않도록 선호 메뉴와 추천 메뉴 제외)
    remaining_menus = final_scores.index.difference(preferred_menus.union(recommended_menus))
    random_recommendations = np.random.choice(remaining_menus, size=top_n, replace=False)

    # 상세 이유 포함
    detailed_recommendations = [
        {
            "menu": menu,
            "score": final_scores[menu],
            "reason": ", ".join(
                f"{preferred_menu} (유사도: {correlation_matrix.loc[menu, preferred_menu]:.2f})"
                for preferred_menu in sorted(preferred_menus, key=lambda x: correlation_matrix.loc[menu, x], reverse=True)[:top_reasons]
                if preferred_menu in correlation_matrix.columns
            )
        }
        for menu in recommended_menus
    ]

    return detailed_recommendations, list(random_recommendations)
