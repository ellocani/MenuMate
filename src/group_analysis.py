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
