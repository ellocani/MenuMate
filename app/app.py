import os
import sys
import pandas as pd

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 절대 경로로 import
from src.data_loader import DataLoader
from src.user_analysis import UserAnalysis
from src.group_analysis import recommend_menus
from src.visualizations import visualize_group_recommendations, visualize_user_preferences
from src.menu_interactive_map import generate_menu_map
from src.add_user import add_new_user

# 파일 경로 설정
menu_file_path = "data/processed_menu_details.csv"
user_file_path = "data/processed_user_data.csv"
raw_menu_data = "data\menu_details.csv"
correlation_matrix_path = "data/menu_correlation_matrix.csv"

# 데이터 로드
loader = DataLoader(menu_file_path, user_file_path)
menu_data, user_data = loader.load_data()

def load_user_preferences(user_name, user_data_path):
    """
    특정 사용자의 선호도를 로드합니다.

    Args:
        user_name (str): 사용자 이름.
        user_data_path (str): 사용자 데이터 파일 경로.

    Returns:
        dict: {메뉴: 선호도 점수} 형식의 사용자 선호도.
    """
    user_data = pd.read_csv(user_data_path)

    # 사용자 데이터에서 해당 사용자의 행 필터링
    user_preferences = user_data[user_data["이름"] == user_name]
    if user_preferences.empty:
        raise ValueError(f"'{user_name}' 사용자의 데이터가 없습니다.")

    # '이름' 열 제외하고, 음식과 점수 매핑
    return user_preferences.drop(columns=["이름"]).iloc[0].dropna().to_dict()

# 메인 함수
def main():
    while True:
        print("\n=== MenuMate에 오신 것을 환영합니다! ===")
        print("\n어떤 작업을 진행하시겠습니까?")
        print("1. 개인 레포트 분석 📝")
        print("2. 그룹 메뉴 추천 🍽️")
        print("3. 사용자 선호도 기반 메뉴 지도 생성 🗺️")
        print("4. 유사도 기반 추천 방식에 대해 더 알아보기 🔍")
        print("\n0. 프로그램 종료 ❌")
        print("\n=== MenuMate가 처음이신가요? ===")
        print("\n5. 새로운 사용자 데이터 추가 ➕")
        choice = input("\n작업 번호를 선택해주세요: ")

        if choice == "1":
            # 개인 레포트 분석
            user_name = input("\n분석할 사용자의 이름을 입력해주세요: ")
            user_analysis = UserAnalysis(menu_data, user_data)
            try:
                # 사용자 분석 결과
                analysis_results = user_analysis.analyze_user(user_name, top_n=5)

                # 텍스트로 분석 결과 출력
                print("\n📊 [개인 취향 분석 결과]")
                print(f"'{user_name}'님의 개인 취향 분석 결과는 다음과 같습니다.\n")

                print("[1️⃣ 선호하는 메뉴]")
                if analysis_results["favorite_menus"]:
                    print(f"'{user_name}'님이 가장 선호하는 메뉴는 다음과 같습니다:")
                    for menu in analysis_results["favorite_menus"]:
                        print(f"  - {menu}")
                else:
                    print("  - 선호하는 메뉴가 없습니다.")

                print("\n[2️⃣ 기피하는 메뉴]")
                if analysis_results["disliked_menus"]:
                    print(f"'{user_name}'님이 기피하는 메뉴는 다음과 같습니다:")
                    for menu in analysis_results["disliked_menus"]:
                        print(f"  - {menu}")
                else:
                    print("  - 기피하는 메뉴가 없습니다.")

                print("\n[3️⃣ 맛 프로파일 분석]")
                taste_profile = analysis_results["favorite_attributes"].filter(like="맛 프로파일").sort_values(ascending=False).head(5)
                if not taste_profile.empty:
                    print(f"'{user_name}'님이 선호하는 맛 프로파일은 다음과 같습니다:")
                    for flavor, value in taste_profile.items():
                        flavor_name = flavor.replace("맛 프로파일_", "")
                        print(f"  - {flavor_name}: {value * 100:.2f}")
                else:
                    print("  - 선호하는 맛 프로파일 데이터가 없습니다.")

                print("\n[4️⃣ 메뉴 분류 분석]")
                category_counts = analysis_results["favorite_menu_details"]["분류"].value_counts(normalize=True)
                if not category_counts.empty:
                    print(f"'{user_name}'님이 선호하는 메뉴 분류는 다음과 같습니다:")
                    for category, value in category_counts.items():
                        print(f"  - {category}: {value * 100:.2f}%")
                else:
                    print("  - 선호하는 메뉴 분류 데이터가 없습니다.")

                # 시각화 바로 표시
                user_analysis.visualize_user_preferences(user_name)
                print(f"\n분석 결과를 화면에 시각적으로 표시했습니다. 😊")

            except ValueError as e:
                print(f"⚠️ 오류 발생: {e}")

        elif choice == "2":
            # 그룹 메뉴 추천
            group_names = input("\n추천할 그룹의 사용자 이름을 ','로 구분하여 입력해주세요: ").split(",")
            try:
                recommended_menus, random_recommendations = recommend_menus(
                    group_names, user_file_path, correlation_matrix_path, top_n=3, top_reasons=10
                )

                # 추가 설명
                print("\n[🍴 MenuMate의 추천 알고리즘 🍴]")
                print("MenuMate는 메뉴 간 상관계수를 활용해, 여러분의 선호도를 분석한 뒤 가장 적합한 메뉴를 추천합니다.")
                print("상관계수는 메뉴 간의 선호도 패턴을 바탕으로 얼마나 비슷한지를 나타내며, 1에 가까울수록 유사도가 높습니다.")
                print("\n아래는 여러분의 그룹 선호도를 반영한 최고의 추천 메뉴입니다. 😋")

                # 추천 메뉴 출력
                print("\n[🍽 추천 메뉴 🍽]")
                for idx, recommendation in enumerate(recommended_menus, start=1):
                    print(
                        f"\n⭐ {idx}. {recommendation['menu']}\n"
                        f"  ▶ 추천 점수: {recommendation['score']:.2f}\n"
                        f"  ▶ 추천 이유 (상위 10개 유사 메뉴):\n"
                        f"     {recommendation['reason']}"
                    )

                # 랜덤 추천 메뉴 출력
                print("\n[🎲 오늘의 랜덤 추천 메뉴 🎲]")
                print("👉 오늘은 이런 메뉴를 도전해보는 건 어떨까요?")
                for idx, menu in enumerate(random_recommendations, start=1):
                    print(f"  ⭐ {idx}. {menu}")

                print("\n👉 다음 식사에서 새로운 메뉴를 시도해 보세요! MenuMate가 함께합니다. 😊")
            except ValueError as e:
                print(f"⚠️ 오류 발생: {e}")


        elif choice == "3":
            # 사용자 선호도 기반 메뉴 지도 생성
            user_name = input("\n메뉴 지도를 생성할 사용자의 이름을 입력해주세요: ")
            try:
                # 사용자 선호도 로드
                user_preferences = load_user_preferences(user_name, user_file_path)

                # 메뉴 지도 생성
                fig = generate_menu_map(correlation_matrix_path, user_preferences)

                # 시각화 표시
                fig.show()
                print(f"\n🗺️ '{user_name}'님의 선호도를 반영한 메뉴 지도가 생성되었습니다!")
                
                # 차트 설명 추가
                print(
                    "\n차트 설명:\n"
                    "- 점들은 서로 다른 메뉴를 나타냅니다.\n"
                    "- 점의 색상은 군집을 나타내며, 가까운 점일수록 비슷한 메뉴입니다.\n"
                    "- 초록색 점은 사용자 선호 메뉴로 강조됩니다.\n"
                    "- 점 사이의 선은 상관관계가 높은 메뉴를 연결합니다.\n"
                    "- 상관관계가 높은 메뉴들은 서로 유사합니다.\n"
                    "- 이를 참고하여 새로운 메뉴를 도전해보거나, 오늘의 추천 메뉴를 찾아보세요!"
                )
            except ValueError as e:
                print(f"⚠️ 오류 발생: {e}")

        
        elif choice == "4":
            print("\n[🔍 MenuMate의 추천 알고리즘에 대해 더 알아보기]\n")

            print("MenuMate는 사용자 선호도와 메뉴 간 유사도를 기반으로 최적의 메뉴를 추천합니다.")
            print("이 과정은 다음과 같은 단계로 이루어집니다:\n")

            print("1️⃣ **메뉴 간의 유사도 계산**")
            print("- MenuMate는 메뉴의 맛, 재료, 요리 방식, 선호도 데이터를 활용하여 메뉴 간의 '유사도'를 계산합니다.")
            print("- 유사도는 0에서 1 사이의 값으로 나타나며, 1에 가까울수록 두 메뉴는 매우 비슷하다는 의미입니다.\n")

            print("예를 들어:")
            print("  - 고등어조림과 닭갈비의 유사도: 0.61")
            print("  - 고등어조림과 제육볶음의 유사도: 0.61")
            print("  - 고등어조림과 매운탕의 유사도: 0.55\n")

            print("2️⃣ **사용자 선호도를 반영**")
            print("- 입력된 사용자(예: 권민혁, 연누, 야옹)의 선호 데이터를 분석합니다.")
            print("- 사용자가 좋아하는 메뉴(예: 닭갈비, 제육볶음)와 비슷한 메뉴를 찾습니다.\n")

            print("3️⃣ **추천 메뉴 도출**")
            print("- 고등어조림은 닭갈비(0.61), 제육볶음(0.61), 매운탕(0.55)과 높은 유사도를 보이며, 총점이 가장 높기 때문에 추천됩니다.\n")

            print("[💡 유사도가 의미하는 것]")
            print("- 유사도(예: 닭갈비와 고등어조림의 유사도 0.61)는 두 메뉴의 특성이 얼마나 비슷한지를 나타냅니다.")
            print("예를 들어:")
            print("  - **재료**: 매콤한 양념, 비슷한 재료")
            print("  - **요리 방식**: 조림, 볶음")
            print("  - **선호도 데이터**: 다른 사용자들이 함께 좋아하는 경우\n")

            print("[🤔 왜 유사도를 보여줄까요?]")
            print("- **추천 과정의 투명성**: '왜 이 메뉴가 추천되었는지' 명확히 알 수 있습니다.")
            print("- **선택의 폭 제공**: 고등어조림뿐만 아니라 닭갈비, 제육볶음 같은 비슷한 메뉴도 고려할 수 있습니다.")
            print("- **추천 신뢰도 강화**: '내가 좋아하는 메뉴와 비슷하네!'라는 납득을 제공합니다.\n")

            print("이처럼 MenuMate는 데이터에 기반한 신뢰할 수 있는 추천을 제공합니다! 😊")

        elif choice == "5":
            # 새로운 사용자 추가
            user_name = input("\n새로운 사용자의 이름을 입력해주세요: ")
            try:
                add_new_user(user_name, user_file_path)
            except Exception as e:
                print(f"⚠️ 오류 발생: {e}")    
                
        elif choice == "0":
            # 프로그램 종료
            print("\nMenuMate를 이용해주셔서 감사합니다! 다음에 또 만나요. 😊")
            break
            

                
                
                
        else:
            print("\n⚠️ 잘못된 번호를 입력하셨습니다. 다시 시도해주세요.")

        

# 프로그램 실행
if __name__ == "__main__":
    main()
