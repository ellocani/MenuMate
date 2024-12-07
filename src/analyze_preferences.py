from preference_summary import (
    user_preference_summary,
    print_preference_summary,
    print_category_analysis,
    plot_flavor_preference,
    plot_cooking_radar,
    plot_wordcloud_of_favorites,
    generate_insights_text
)

def main():
    print("=== 메뉴메이트 사용자 취향 분석 시스템 ===\n")
    
    # 사용자 이름 입력 받기
    user_name = input("분석할 사용자 이름을 입력하세요: ")
    
    # 1. 기본 선호도 요약
    print("\n[1. 기본 선호도 분석]")
    summary = user_preference_summary(user_name)
    if summary:
        print_preference_summary(user_name, summary)
    
    # 2. 카테고리별 분석
    print("\n[2. 카테고리별 선호도 분석]")
    print_category_analysis(user_name)
    
    # 3. 시각화
    print("\n[3. 시각화 분석]")
    print("맛 프로파일 차트를 생성합니다...")
    plot_flavor_preference(user_name)
    
    print("조리방식 레이더 차트를 생성합니다...")
    plot_cooking_radar(user_name)
    
    print("선호 메뉴 워드클라우드를 생성합니다...")
    plot_wordcloud_of_favorites(user_name)
    
    # 4. 종합 인사이트
    print("\n[4. 종합 인사이트]")
    insight = generate_insights_text(user_name)
    print(insight)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n오류가 발생했습니다: {str(e)}")
