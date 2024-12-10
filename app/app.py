import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 절대 경로로 import
from src.data_loader import DataLoader
from src.user_analysis import UserAnalysis
from src.group_analysis import GroupAnalysis, recommend_menus_with_attributes, align_menu_and_user_data
from src.visualizations import visualize_group_recommendations, visualize_user_preferences

# 파일 경로 설정
menu_file_path = "data/processed_menu_details.csv"
user_file_path = "data/processed_user_data.csv"

# 데이터 로드
loader = DataLoader(menu_file_path, user_file_path)
menu_data, user_data = loader.load_data()

# 메인 함수
def main():
    while True:
        print("\n=== MenuMate 실행 ===")
        print("1. 개인 레포트 분석")
        print("2. 그룹 메뉴 추천")
        print("0. 종료")
        choice = input("선택할 작업 번호를 입력하세요: ")

        if choice == "1":
            # 개인 레포트 분석
            user_name = input("\n분석할 사용자 이름을 입력하세요: ")
            user_analysis = UserAnalysis(menu_data, user_data)
            try:
                # 사용자 분석 결과
                analysis_results = user_analysis.analyze_user(user_name, top_n=5)

                # 개인 분석 결과 출력
                print(f"\n'{user_name}' 사용자의 대표 선호 메뉴:")
                print(analysis_results["favorite_menus"])

                print(f"\n'{user_name}' 사용자의 대표 기피 메뉴:")
                print(analysis_results["disliked_menus"])

                # 시각화 저장
                visualize_user_preferences(user_name, analysis_results, save_path=f"{user_name}_analysis")
                print(f"'{user_name}'의 분석 결과가 저장되었습니다.")
            except ValueError as e:
                print(f"오류 발생: {e}")

        elif choice == "2":
            # 그룹 메뉴 추천
            group_names = input("\n분석할 그룹의 사용자 이름을 ','로 구분하여 입력하세요: ").split(",")
            try:
                # 메뉴 데이터와 사용자 데이터 매핑
                aligned_menu_data, aligned_user_data = align_menu_and_user_data(menu_data, user_data)

                # 그룹 추천 메뉴
                recommended_menus = recommend_menus_with_attributes(
                    aligned_menu_data, aligned_user_data, group_names, top_n=5
                )

                # 추천 결과 출력
                print("\n추천 메뉴:")
                print(recommended_menus)

                # 추천 결과 시각화 저장
                visualize_group_recommendations(
                    recommended_menus,
                    group_name=", ".join(group_names),
                    save_path="content_based_recommendations.png"
                )
                print("그룹 추천 메뉴 시각화가 저장되었습니다.")
            except ValueError as e:
                print(f"오류 발생: {e}")

        elif choice == "0":
            # 프로그램 종료
            print("프로그램을 종료합니다.")
            break

        else:
            print("올바른 번호를 입력하세요.")

# 프로그램 실행
if __name__ == "__main__":
    main()
