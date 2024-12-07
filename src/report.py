# 분석 결과 레포트 생성(텍스트, 시각화)

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import matplotlib.font_manager as fm
import platform

def set_matplotlib_korean_font():
    """
    운영체제별 한글 폰트 설정
    """
    system_name = platform.system()
    
    if system_name == "Windows":
        plt.rc('font', family='Malgun Gothic')
    elif system_name == "Darwin":  # macOS
        plt.rc('font', family='AppleGothic')
    elif system_name == "Linux":
        plt.rc('font', family='NanumGothic')
    
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def plot_flavor_preference(flavor_mean: pd.Series):
    # 한글 폰트 설정
    set_matplotlib_korean_font()
    
    plt.figure(figsize=(12, 6))  # 그래프 크기 조정
    flavor_mean.plot(kind='bar', title='맛 프로파일별 평균 점수')
    plt.ylabel('평균 선호도')
    plt.xlabel('맛 프로파일')
    plt.xticks(rotation=45, ha='right')  # x축 레이블 회전 및 정렬
    plt.tight_layout()  # 레이아웃 조정
    plt.show()

def generate_wordcloud(menus: list):
    # 한글 폰트 설정
    set_matplotlib_korean_font()
    
    # 워드클라우드용 폰트 경로 설정 (Windows 기준)
    if platform.system() == "Windows":
        font_path = "c:/Windows/Fonts/malgun.ttf"
    else:
        font_path = None  # 시스템 기본 폰트 사용
    
    text = " ".join(menus)
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        font_path=font_path,  # 한글 폰트 경로 지정
        max_font_size=100
    ).generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("좋아하는 메뉴 워드클라우드")
    plt.tight_layout()
    plt.show()

def print_insight_text(summary, category_analysis):
    # 요약 문구 예시 출력
    print(f"\n=== 선호도 분석 결과 ===")
    print(f"평균 선호도: {summary['avg_score']:.2f}")
    print("\n[가장 선호하는 상위 메뉴]")
    for menu, score in summary['top_10'].items():
        print(f"- {menu}: {score}")
    
    print("\n[가장 기피하는 하위 메뉴]")
    for menu, score in summary['bottom_10'].items():
        print(f"- {menu}: {score}")
    
    # 카테고리 선호도 분석 결과 활용
    if category_analysis and not category_analysis['category_mean'].empty:
        top_category = category_analysis['category_mean'].idxmax()
        print(f"\n[선호하는 음식 분류]")
        print(f"가장 선호하는 분류: {top_category}")
    else:
        print("\n[선호하는 음식 분류]")
        print("분류 정보가 충분하지 않습니다.")
        
    if category_analysis and not category_analysis['flavor_mean'].empty:
        top_flavor = category_analysis['flavor_mean'].idxmax()
        print(f"\n[선호하는 맛 프로파일]")
        print(f"가장 선호하는 맛: {top_flavor}")
    else:
        print("\n[선호하는 맛 프로파일]")
        print("맛 프로파일 정보가 충분하지 않습니다.")
