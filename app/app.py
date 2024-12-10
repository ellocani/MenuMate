import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 절대 경로로 import
from src.data_loader import DataLoader
from src.user_analysis import UserAnalysis
from src.group_analysis import GroupAnalysis
from src.visualizations import visualize_group_recommendations, visualize_user_preferences


# 파일 경로 설정
menu_file_path = "data/processed_menu_details.csv"
user_file_path = "data/processed_user_data.csv"

# 데이터 로드
loader = DataLoader(menu_file_path, user_file_path)
menu_data, user_data = loader.load_data()

# 사용자 분석
user_analysis = UserAnalysis(menu_data, user_data)  # UserAnalysis 객체 생성
user_name = "연누"  # 분석할 사용자 이름
try:
    # 사용자 분석 메서드 호출
    analysis_results = user_analysis.analyze_user(user_name, top_n=5)  # 대표 메뉴 5개

    # 콘솔 출력
    print(f"\n'{user_name}' 사용자의 대표 선호 메뉴:")
    print(analysis_results["favorite_menus"])

    print(f"\n'{user_name}' 사용자의 대표 기피 메뉴:")
    print(analysis_results["disliked_menus"])

    # 시각화: 선호 속성, 기피 속성
    visualize_user_preferences(user_name, analysis_results, save_path=f"{user_name}_analysis")
except ValueError as e:
    print(e)

# 그룹 분석
group_analysis = GroupAnalysis(menu_data, user_data)
group_names = ["연누", "김정민", "안태우"]  # 테스트할 사용자 그룹
try:
    print(f"\n그룹({', '.join(group_names)})의 분석 결과:")

    # 그룹 추천 메뉴 요약 (상위 5개 메뉴만 표시)
    recommended_summary = group_analysis.analyze_group_summary(group_names, preference_threshold=3, top_n=5)
    print("\n그룹에 추천되는 상위 메뉴 요약:")
    print(recommended_summary)

    # 그룹 추천 메뉴 시각화
    from src.visualizations import visualize_group_recommendations
    visualize_group_recommendations(
        recommended_summary, 
        group_name=", ".join(group_names), 
        save_path="group_recommendations.png"
    )

except ValueError as e:
    print(e)


