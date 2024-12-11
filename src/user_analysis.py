import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

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

        # 4점인 메뉴(선호하는 메뉴)
        favorite_menus = user_row.loc[:, (user_row == 4).any()].columns.tolist()
        # 1점인 메뉴(기피하는 메뉴)
        disliked_menus = user_row.loc[:, (user_row == 1).any()].columns.tolist()

        # 선호 메뉴와 기피 메뉴의 상세 정보
        favorite_menu_details = self.menu_data[self.menu_data['메뉴'].isin(favorite_menus)]
        disliked_menu_details = self.menu_data[self.menu_data['메뉴'].isin(disliked_menus)]

        # 속성 정규화
        normalized_menu_data = self.menu_data.drop(columns=["메뉴", "분류", "간편성"])
        normalized_menu_data = normalized_menu_data.div(normalized_menu_data.sum(axis=0), axis=1)

        # 선호 속성과 기피 속성 요약
        favorite_attributes = normalized_menu_data.loc[favorite_menu_details.index].mean()
        disliked_attributes = normalized_menu_data.loc[disliked_menu_details.index].mean()

        # 상위 N개 제한
        favorite_menus_top_n = favorite_menu_details.head(top_n)["메뉴"].tolist()
        disliked_menus_top_n = disliked_menu_details.head(top_n)["메뉴"].tolist()

        return {
            "favorite_menus": favorite_menus_top_n,
            "favorite_attributes": favorite_attributes,
            "disliked_menus": disliked_menus_top_n,
            "disliked_attributes": disliked_attributes,
            "favorite_menu_details": favorite_menu_details
        }

    def visualize_user_preferences(self, user_name, top_k=10):
        """
        특정 사용자의 선호 속성 중 "맛 프로파일"와 "분류"를 시각화
        :param user_name: 분석할 사용자 이름
        :param top_k: 시각화할 상위 속성 개수
        """
        # 사용자 분석 결과 가져오기
        analysis_results = self.analyze_user(user_name)

        # 맛 프로파일 시각화
        taste_profile_columns = [col for col in self.menu_data.columns if "맛 프로파일" in col]
        taste_profile_data = analysis_results["favorite_attributes"].filter(items=taste_profile_columns)
        taste_profile_data = taste_profile_data[taste_profile_data >= 0.003]
        taste_profile_data.index = taste_profile_data.index.str.replace("맛 프로파일_", "")
        taste_profile_data = taste_profile_data.sort_values(ascending=False).head(top_k)

        # 메뉴 분류 시각화
        favorite_menu_details = analysis_results["favorite_menu_details"]
        category_counts = favorite_menu_details["분류"].value_counts()
        category_counts = category_counts / category_counts.sum()  # 정규화

        # 빈도에 따른 색상 설정
        def generate_color_palette(data, base_color):
            max_value = data.max()
            min_value = data.min()
            normalized_values = (data - min_value) / (max_value - min_value)
            return [sns.light_palette(base_color, as_cmap=False, n_colors=256)[int(v * 255)] for v in normalized_values]

        taste_palette = generate_color_palette(taste_profile_data, "green")
        category_palette = generate_color_palette(category_counts, "green")

        # 바 차트 생성
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        sns.barplot(x=taste_profile_data.index, y=taste_profile_data.values, palette=taste_palette, ax=axes[0])
        axes[0].set_title(f"{user_name}님의 맛 프로파일", fontsize=14)
        axes[0].set_ylabel("빈도", fontsize=12)
        axes[0].set_xlabel("속성", fontsize=12)
        axes[0].tick_params(axis="x", rotation=45)

        sns.barplot(x=category_counts.index, y=category_counts.values, palette=category_palette, ax=axes[1])
        axes[1].set_title(f"{user_name}님의 메뉴 분류 선호도", fontsize=14)
        axes[1].set_ylabel("빈도", fontsize=12)
        axes[1].set_xlabel("분류", fontsize=12)
        axes[1].tick_params(axis="x", rotation=45)

        plt.tight_layout()
        plt.show()

        # 레이더 차트 생성 (맛 프로파일)
        radar_taste_data = taste_profile_data.copy()
        radar_taste_data = radar_taste_data.sort_index()  # 비슷한 속성을 붙이기 위해 정렬

        radar_labels_taste = radar_taste_data.index.tolist()
        radar_values_taste = radar_taste_data.values.tolist()
        radar_values_taste += radar_values_taste[:1]  # 레이더 차트를 닫기 위해 첫 값 추가

        radar_angles_taste = np.linspace(0, 2 * np.pi, len(radar_labels_taste), endpoint=False).tolist()
        radar_angles_taste += radar_angles_taste[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        ax.fill(radar_angles_taste, radar_values_taste, color="lightgreen", alpha=0.4)
        ax.plot(radar_angles_taste, radar_values_taste, color="green", linewidth=2)
        ax.set_yticks([])
        ax.set_xticks(radar_angles_taste[:-1])
        ax.set_xticklabels(radar_labels_taste, fontsize=10)
        ax.set_title(f"{user_name}님의 맛 프로파일 (레이더 차트)", size=16, pad=20)

        plt.tight_layout()
        plt.show()