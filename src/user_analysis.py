class UserAnalysis:
    def __init__(self, menu_data, user_data):
        self.menu_data = menu_data
        self.user_data = user_data

    def analyze_user(self, user_name, top_n=5):
        """
        특정 사용자의 선호 메뉴와 기피 메뉴를 분석하는 함수
        :param user_name: 분석할 사용자 이름
        :param top_n: 상위 N개의 대표 메뉴를 선택
        """
        # 사용자 이름이 데이터에 있는지 확인
        if user_name not in self.user_data['이름'].values:
            raise ValueError(f"사용자 '{user_name}'를 데이터에서 찾을 수 없습니다.")

        # 사용자의 선호도 데이터 추출
        user_row = self.user_data[self.user_data['이름'] == user_name].iloc[:, 1:]

        # 3점 이상인 메뉴(선호하는 메뉴)
        favorite_menus = user_row.loc[:, (user_row >= 3).any()].columns.tolist()
        # 2점 이하인 메뉴(기피하는 메뉴)
        disliked_menus = user_row.loc[:, (user_row <= 2).any()].columns.tolist()

        # 선호 메뉴와 기피 메뉴의 상세 정보
        favorite_menu_details = self.menu_data[self.menu_data['메뉴'].isin(favorite_menus)]
        disliked_menu_details = self.menu_data[self.menu_data['메뉴'].isin(disliked_menus)]

        # 선호 속성과 기피 속성 요약
        favorite_attributes = favorite_menu_details.drop(columns=["메뉴", "분류", "간편성"]).mean()
        disliked_attributes = disliked_menu_details.drop(columns=["메뉴", "분류", "간편성"]).mean()

        # 상위 N개 제한
        favorite_menus_top_n = favorite_menu_details.head(top_n)["메뉴"].tolist()
        disliked_menus_top_n = disliked_menu_details.head(top_n)["메뉴"].tolist()

        return {
            "favorite_menus": favorite_menus_top_n,
            "favorite_attributes": favorite_attributes,
            "disliked_menus": disliked_menus_top_n,
            "disliked_attributes": disliked_attributes,
        }
