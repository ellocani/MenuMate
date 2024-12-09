# 분석 결과 레포트 생성(텍스트, 시각화)

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import matplotlib.font_manager as fm
import platform
import numpy as np

def set_matplotlib_korean_font():
    """한글 폰트 설정"""
    system_name = platform.system()
    
    if system_name == "Windows":
        # Windows 전용 설정
        from matplotlib import font_manager as fm
        font_path = r'C:\Windows\Fonts\malgun.ttf'
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
    elif system_name == "Darwin":  # macOS
        plt.rc('font', family='AppleGothic')
    else:  # Linux
        plt.rc('font', family='NanumGothic')
    
    plt.rcParams['axes.unicode_minus'] = False
    return True

def plot_flavor_preference(flavor_mean):
    """맛 선호도 시각화"""
    # 폰트 설정 적용
    set_matplotlib_korean_font()
    
    # 데이터 정규화
    normalized_values = (flavor_mean - flavor_mean.min()) / (flavor_mean.max() - flavor_mean.min())
    
    # 데이터프레임 생성
    df = pd.DataFrame({
        'Flavor': normalized_values.index,
        'Score': normalized_values.values
    })
    
    # Seaborn 스타일 설정
    sns.set_style("whitegrid")
    
    # Figure 및 Axes 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 바 플롯 생성
    sns.barplot(
        data=df,
        x='Flavor',
        y='Score',
        palette="RdYlBu_r",
        ax=ax
    )
    
    # 그래프 스타일링
    ax.set_title('맛 유형별 선호도 (정규화)', size=15, pad=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel('선호도 점수 (정규화)')
    
    # 값 레이블 추가
    for i, v in enumerate(normalized_values):
        ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def create_preference_radar(category_analysis):
    """카테고리 선호도 시각화"""
    # 폰트 설정 적용
    set_matplotlib_korean_font()
    
    categories = category_analysis['category_mean'].index
    values = category_analysis['category_mean'].values
    
    # 정규화
    normalized_values = (values - values.min()) / (values.max() - values.min())
    
    # 데이터프레임 생성
    df = pd.DataFrame({
        'Category': categories,
        'Score': normalized_values
    })
    
    # Figure 및 Axes 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Seaborn 스타일 설정
    sns.set_style("whitegrid")
    
    # 바 플롯 생성
    sns.barplot(
        data=df,
        x='Category',
        y='Score',
        palette="coolwarm_r",
        ax=ax
    )
    
    # 그래프 스타일링
    ax.set_title('카테고리별 선호도 (정규화)', size=15, pad=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel('선호도 점수 (정규화)')
    
    # 값 레이블 추가
    for i, v in enumerate(normalized_values):
        ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

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
    
    if not category_analysis:
        return
        
    # 폰트 설정
    set_matplotlib_korean_font()
    
    # 데이터가 있는 경우에만 그래프 생성
    has_flavor = not category_analysis['flavor_mean'].empty
    has_category = not category_analysis['category_mean'].empty
    
    if has_flavor or has_category:
        # 서브플롯 생성
        fig = plt.figure(figsize=(15, 6))
        
        if has_flavor and has_category:
            # 두 그래프 모두 있는 경우
            ax1 = plt.subplot(121)
            ax2 = plt.subplot(122)
            create_flavor_plot(category_analysis['flavor_mean'], ax1)
            create_category_plot(category_analysis['category_mean'], ax2)
        elif has_flavor:
            # 맛 선호도만 있는 경우
            ax = plt.subplot(111)
            create_flavor_plot(category_analysis['flavor_mean'], ax)
        else:
            # 카테고리 선호도만 있는 경우
            ax = plt.subplot(111)
            create_category_plot(category_analysis['category_mean'], ax)
        
        plt.tight_layout()
        plt.show()

def create_flavor_plot(flavor_mean, ax):
    """맛 선호도 그래프 생성"""
    # 데이터 정규화
    normalized_values = (flavor_mean - flavor_mean.min()) / (flavor_mean.max() - flavor_mean.min())
    
    # 데이터프레임 생성
    df = pd.DataFrame({
        'Flavor': normalized_values.index,
        'Score': normalized_values.values
    })
    
    # 바 플롯 생성 (경고 메시지 해결)
    sns.barplot(
        data=df,
        x='Flavor',
        y='Score',
        hue='Flavor',  # hue 파라미터 추가
        legend=False,  # 범례 숨기기
        palette="RdYlBu_r",
        ax=ax
    )
    
    # 그래프 스타일링 (경고 메시지 해결)
    ax.set_title('맛 유형별 선호도 (정규화)', size=12, pad=20)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')  # ticklabels 설정 방식 변경
    ax.set_ylabel('선호도 점수 (정규화)')
    
    # 값 레이블 추가 (에러 방지)
    for i, v in enumerate(normalized_values):
        if pd.notna(v):  # NaN 값 체크
            ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')

def create_category_plot(category_mean, ax):
    """카테고리 선호도 그래프 생성"""
    # '기타' 카테고리 제외
    category_mean = category_mean[category_mean.index != '기타']
    
    # 데이터 정규화
    normalized_values = (category_mean - category_mean.min()) / (category_mean.max() - category_mean.min())
    
    # 데이터프레임 생성
    df = pd.DataFrame({
        'Category': normalized_values.index,
        'Score': normalized_values.values
    })
    
    # 바 플롯 생성 (경고 메시지 해결)
    sns.barplot(
        data=df,
        x='Category',
        y='Score',
        hue='Category',  # hue 파라미터 추가
        legend=False,    # 범례 숨기기
        palette="coolwarm_r",
        ax=ax
    )
    
    # 그래프 스타일링 (경고 메시지 해결)
    ax.set_title('카테고리별 선호도 (정규화)', size=12, pad=20)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')  # ticklabels 설정 방식 변경
    ax.set_ylabel('선호도 점수 (정규화)')
    
    # 값 레이블 추가 (에러 방지)
    for i, v in enumerate(normalized_values):
        if pd.notna(v):  # NaN 값 체크
            ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')

