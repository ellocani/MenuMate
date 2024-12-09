# 분석 결과 레포트 생성(텍스트, 시각화)

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import matplotlib.font_manager as fm
import platform
import numpy as np

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
    # NaN이나 inf 값 제거
    flavor_mean = flavor_mean.replace([np.inf, -np.inf], np.nan).dropna()
    
    # 데이터가 비어있는지 확인
    if flavor_mean.empty:
        print("시각화할 데이터가 없습니다.")
        return
    
    # 한글 폰트 설정
    set_matplotlib_korean_font()
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(flavor_mean)), flavor_mean.values)
    plt.title('맛 프로파일별 평균 선호도')
    plt.ylabel('평균 선호도')
    plt.xlabel('맛 프로파일')
    
    # x축 레이블 설정
    plt.xticks(range(len(flavor_mean)), flavor_mean.index, rotation=45, ha='right')
    
    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        if np.isfinite(height):  # height가 유한한 값인지 확인
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
    
    plt.tight_layout()
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
        print(f"\n[선호하는 맛 프로파일]")
        print("상위 3개 선호 맛:")
        for flavor, score in category_analysis['flavor_mean'].head(3).items():
            print(f"- {flavor}: {score:.2f}")
    else:
        print("\n[선호하는 맛 프로파일]")
        print("맛 프로파일 정보가 충분하지 않습니다.")

def generate_report(summary, category_analysis):
    """통합 리포트 생성 함수"""
    print_insight_text(summary, category_analysis)
    
    if category_analysis and not category_analysis['flavor_mean'].empty:
        plot_flavor_preference(category_analysis['flavor_mean'])
    
    # 워드 클라우드: 환장함 메뉴만
    top_10 = summary['top_10']
    fav_menus = top_10[top_10 == 4].index.tolist()
    if fav_menus:
        generate_wordcloud(fav_menus)
