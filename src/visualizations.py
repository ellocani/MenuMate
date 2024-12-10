import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False    # 마이너스 기호 깨짐 방지

def plot_attributes(attributes, title, color, save_path=None):
    """
    속성을 시각화하는 공통 함수
    :param attributes: 속성 데이터 (Pandas Series)
    :param title: 그래프 제목
    :param color: 막대 그래프 색상
    :param save_path: 그래프를 저장할 파일 경로 (기본값: None)
    """
    plt.figure(figsize=(12, 6))
    attributes.sort_values(ascending=False).head(10).plot(kind='bar', color=color, edgecolor='black')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("속성", fontsize=12)
    plt.ylabel("빈도", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"그래프가 {save_path}에 저장되었습니다.")
    else:
        plt.show()



def visualize_user_preferences(user_name, analysis_results, save_path=None):
    """
    사용자의 선호 및 기피 메뉴 분석 결과를 시각화
    :param user_name: 사용자 이름
    :param analysis_results: 분석 결과 (딕셔너리)
    :param save_path: 그래프를 저장할 파일 경로 (기본값: None)
    """
    # 선호 및 기피 속성
    favorite_attributes = analysis_results["favorite_attributes"]
    disliked_attributes = analysis_results["disliked_attributes"]

    # 선호 속성 시각화
    plot_attributes(
        favorite_attributes,
        title=f"{user_name}의 선호 메뉴 속성",
        color="green",
        save_path=f"{save_path}_favorite.png" if save_path else None,
    )

    # 기피 속성 시각화
    plot_attributes(
        disliked_attributes,
        title=f"{user_name}의 기피 메뉴 속성",
        color="red",
        save_path=f"{save_path}_disliked.png" if save_path else None,
    )


import matplotlib.pyplot as plt

def visualize_group_recommendations(recommended_menus, group_name, save_path=None):
    """
    그룹에 추천되는 메뉴를 시각화하는 함수
    :param recommended_menus: 추천되는 메뉴 데이터프레임 (Pandas DataFrame)
    :param group_name: 그룹 이름
    :param save_path: 그래프를 저장할 파일 경로 (기본값: None)
    """
    if recommended_menus.empty:
        print("추천 메뉴 데이터가 없습니다.")
        return

    # 그래프 설정
    plt.figure(figsize=(12, 6))
    bar_plot = plt.bar(
        recommended_menus["메뉴"],
        recommended_menus["추천 점수"],
        color="skyblue",
        edgecolor="black",
    )

    # 그래프 타이틀 및 축 설정
    plt.title(f"그룹({group_name}) 추천 메뉴 상위 {len(recommended_menus)}개", fontsize=16, fontweight="bold")
    plt.xlabel("메뉴", fontsize=12)
    plt.ylabel("추천 점수", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # 막대 위에 추천 점수 표시
    for bar, score in zip(bar_plot, recommended_menus["추천 점수"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{score:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # 그래프 저장 또는 출력
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"추천 메뉴 그래프가 {save_path}에 저장되었습니다.")
    else:
        plt.show()
