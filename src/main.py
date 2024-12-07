# 사용자 입력(ex : 사용자명, 여러 사용자명 리스트)을 받아 기능 실행

import sys
import os
from data_preprocessor import load_and_preprocess_data
from analysis import get_user_preference_summary, get_user_category_preference
from recommendation import recommend_for_group
from report import plot_flavor_preference, generate_wordcloud, print_insight_text
from data_preprocessor import preprocess_menu_details, preprocess_survey_data, validate_data, load_and_preprocess_data

def main():
    try:
        # 파일 경로 설정
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        survey_path = os.path.join(base_dir, "data", "user_data.csv")
        menu_path = os.path.join(base_dir, "data", "menu_details.csv")
        
        # 인자 확인
        if len(sys.argv) < 3:
            print("사용법:")
            print("  개인 리포트 조회:")
            print("    python src/main.py user_report 사용자이름")
            print("  그룹 추천:")
            print("    python src/main.py group_recommend 사용자1 사용자2 ...")
            print("\n예시:")
            print("  python src/main.py user_report 연누")
            print("  python src/main.py group_recommend 연누 철수 영희")
            return
            
        # 파일 존재 여부 확인
        if not os.path.exists(survey_path):
            print(f"사용자 데이터 파일이 없습니다: {survey_path}")
            return
            
        if not os.path.exists(menu_path):
            print(f"메뉴 상세 데이터 파일이 없습니다: {menu_path}")
            return
        
        # 데이터 로드 및 전처리
        survey_df, menu_df = load_and_preprocess_data(survey_path, menu_path)
        
        if survey_df is None or menu_df is None:
            print("데이터 로드 및 전처리에 실패했습니다.")
            return
            
        # 데이터 정합성 검증
        if survey_df.empty or menu_df.empty:
            print("빈 데이터셋이 있습니다.")
            return
            
        # 메뉴 일치성 검증
        survey_menus = set([col for col in survey_df.columns if col != "이름"])
        menu_names = set(menu_df['메뉴'])
        
        if not survey_menus.issubset(menu_names):
            missing_menus = survey_menus - menu_names
            print(f"설문에 있는 메뉴 중 상세정보가 없는 메뉴가 있습니다: {missing_menus}")
            return
            
        # 간단한 CLI 인터페이스 예시
        # 예: python main.py user_report 홍길동
        #    python main.py group_recommend 홍길동 김민수 이영희
        args = sys.argv[1:]
        if len(args) < 2:
            print("Usage:")
            print("  python main.py user_report [username]")
            print("  python main.py group_recommend [username1] [username2] ...")
            return
        
        command = args[0]
        
        if command == "user_report":
            user_name = args[1]
            summary = get_user_preference_summary(survey_df, menu_df, user_name)
            if summary is None:
                print("해당 사용자를 찾을 수 없습니다.")
                return
            category_analysis = get_user_category_preference(survey_df, menu_df, user_name)
            print_insight_text(summary, category_analysis)
            # 맛 프로파일 그래프 예시
            if category_analysis and not category_analysis['flavor_mean'].empty:
                plot_flavor_preference(category_analysis['flavor_mean'])
            
            # 워드 클라우드: 환장함 메뉴만 예시 (summary에서 top_10 중 rating=4인 메뉴)
            top_10 = summary['top_10']
            fav_menus = top_10[top_10 == 4].index.tolist()
            if fav_menus:
                generate_wordcloud(fav_menus)
        
        elif command == "group_recommend":
            user_names = args[1:]
            recommended = recommend_for_group(survey_df, menu_df, user_names)
            if recommended is None:
                print("해당 사용자들을 찾을 수 없습니다.")
                return
            print("그룹 선호도 기반 추천 메뉴 Top 10:", recommended.index.tolist())
        else:
            print("알 수 없는 명령어입니다.")

    except Exception as e:
        print(f"실행 중 오류가 발생했습니다: {str(e)}")
        return

if __name__ == "__main__":
    main()
