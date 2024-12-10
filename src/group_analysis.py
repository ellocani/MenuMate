from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class GroupAnalysis:
    def __init__(self, menu_data, user_data):
        self.menu_data = menu_data
        self.user_data = user_data

    def analyze_group_summary(self, user_names, preference_threshold=2, top_n=5):
        """
        그룹의 선호 메뉴를 요약 분석하여 상위 메뉴만 반환하는 함수
        :param user_names: 분석할 사용자 리스트
        :param preference_threshold: 선호도를 판단할 기준 값 (기본값 2)
        :param top_n: 상위 N개의 메뉴만 반환
        """
        # 그룹 데이터 필터링 및 평균 계산
        group_data = self.user_data[self.user_data['이름'].isin(user_names)]
        if group_data.empty:
            raise ValueError("제공된 사용자 리스트에서 데이터를 찾을 수 없습니다.")

        group_preferences = group_data.iloc[:, 1:].mean()
        top_menus = group_preferences[group_preferences > preference_threshold].sort_values(ascending=False).head(top_n)

        # 메뉴 상세 정보 추출
        recommended_menus = self.menu_data[self.menu_data['메뉴'].isin(top_menus.index)]
        recommended_menus = recommended_menus[["메뉴", "간편성", "분류"]].copy()
        recommended_menus["평균 점수"] = top_menus.values

        return recommended_menus

def normalize_names(series):
    """
    메뉴 이름을 정규화하는 함수
    :param series: 메뉴 이름이 포함된 Pandas Series
    :return: 정규화된 메뉴 이름
    """
    return (
        series.str.strip()               # 공백 제거
        .str.lower()                     # 소문자 변환
        .str.replace(r"[^a-z가-힣0-9 ]", "", regex=True)  # 특수 문자 제거
    )


def align_menu_and_user_data(menu_data, user_data):
    """
    menu_data와 user_data를 공통 메뉴를 기준으로 매핑
    """
    # 메뉴 이름 정규화
    menu_data["메뉴"] = normalize_names(menu_data["메뉴"])
    user_data.columns = ["이름"] + normalize_names(pd.Series(user_data.columns[1:]))

    # 공통 메뉴 확인
    common_menus = set(menu_data["메뉴"]).intersection(set(user_data.columns[1:]))
    
    if not common_menus:
        raise ValueError(
            f"menu_data와 user_data 간의 공통 메뉴가 없습니다. "
            f"menu_data 메뉴: {menu_data['메뉴'].tolist()} "
            f"user_data 메뉴: {user_data.columns[1:].tolist()}"
        )
    
    # 공통 메뉴 필터링
    filtered_menu_data = menu_data[menu_data["메뉴"].isin(common_menus)]
    filtered_user_data = user_data[["이름"] + list(common_menus)]

    return filtered_menu_data, filtered_user_data


def recommend_menus_with_attributes(menu_data, user_data, group_names, top_n=5):
    """
    콘텐츠 기반 필터링을 활용한 메뉴 추천
    :param menu_data: 메뉴 데이터 (DataFrame)
    :param user_data: 사용자 데이터 (DataFrame)
    :param group_names: 그룹 사용자 이름 리스트
    :param top_n: 추천할 메뉴 개수
    :return: 추천 메뉴 DataFrame
    """
    # 데이터 매핑
    aligned_menu_data, aligned_user_data = align_menu_and_user_data(menu_data, user_data)

    # 그룹의 사용자 데이터 필터링
    group_data = aligned_user_data[aligned_user_data['이름'].isin(group_names)]
    if group_data.empty:
        raise ValueError("제공된 사용자 리스트에서 데이터를 찾을 수 없습니다.")

    # 그룹의 선호도 평균 계산
    group_preferences = group_data.iloc[:, 1:].mean()

    # 메뉴 속성 데이터 추출
    menu_attributes = aligned_menu_data.drop(columns=["메뉴", "분류", "간편성"], errors="ignore").set_index(aligned_menu_data["메뉴"])

    # 메뉴 속성과 그룹 선호도 데이터의 공통 열 선택
    common_columns = menu_attributes.columns.intersection(group_preferences.index)
    if common_columns.empty:
        raise ValueError("사용자 데이터와 메뉴 데이터 간의 공통 속성이 없습니다.")

    menu_attributes = menu_attributes[common_columns]
    group_preferences = group_preferences[common_columns]

    # 코사인 유사도 계산
    similarity_scores = cosine_similarity(menu_attributes, [group_preferences])
    aligned_menu_data["추천 점수"] = similarity_scores

    # 추천 점수를 기준으로 상위 N개의 메뉴 선택
    recommended_menus = aligned_menu_data.sort_values(by="추천 점수", ascending=False).head(top_n)

    return recommended_menus[["메뉴", "분류", "간편성", "추천 점수"]]
