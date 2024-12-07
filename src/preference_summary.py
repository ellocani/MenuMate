import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import csv
import pandas as pd
from preprocessing.handling_data import USER_PREFERENCES

# menu_details 데이터 로드, 딕셔너리로 저장
def load_menu_details():
    menu_details = {}
    with open('data/menu_details.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 헤더 건너뛰기
        for row in reader:
            menu = row[0]
            menu_details[menu] = {
                "음식종류": row[1],
                "재료": row[2],
                "맛 프로파일": row[3],
                "식사상황": row[4],
                "조리 방식": row[5],
                "계절": row[6],
                "난이도": row[7]
            }
    return menu_details

MENU_DETAILS = load_menu_details()

# 데이터 확인을 위한 코드 추가
print("Available user IDs:", list(USER_PREFERENCES.keys()))

# 특정 사용자(user_id)의 선호도 요약
def user_preference_summary(user_id):
    if user_id not in USER_PREFERENCES:
        print(f"Warning: User ID '{user_id}' not found in preferences")
        return None
        
    user_data = USER_PREFERENCES[user_id]
    
    # 평균 선호도 계산
    ratings = list(user_data.values())
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    # 상위 10개, 하위 10개 메뉴 추출    
    sorted_menus = sorted(user_data.items(), key=lambda x: x[1], reverse=True)
    top_10 = dict(sorted_menus[:10])
    bottom_10 = dict(sorted_menus[-10:])
    
    # 환장함(4점) 메뉴들 추출
    favorite_menus = [menu for menu, rating in user_data.items() if rating == 4]
    
    # 환장함 메뉴들의 카테고리 분석
    favorite_types = [MENU_DETAILS[m]["음식종류"] for m in favorite_menus if m in MENU_DETAILS]
    favorite_type_count = Counter(favorite_types)
    
    # 맛 프로파일 카운트
    favorite_flavors = [MENU_DETAILS[m]["맛 프로파일"] for m in favorite_menus if m in MENU_DETAILS]
    favorite_flavor_count = Counter(favorite_flavors)
    
    return {
        "avg_rating": avg_rating,
        "top_10_menus": top_10,
        "bottom_10_menus": bottom_10,
        "favorite_type_count": favorite_type_count,
        "favorite_flavor_count": favorite_flavor_count
    }

# 사용자 이름 입력 받기
user_name = input("사용자 이름을 입력하세요: ")

# 선호도 요약 생성
summary = user_preference_summary(user_name)

def print_preference_summary(user_name, summary):
    if summary:
        print("\n=== {} 님의 음식 선호도 분석 결과 ===".format(user_name))
        print("\n평균 선호도: {:.2f}".format(summary["avg_rating"]))
        
        print("\n가장 선호하는 상위 10개 메뉴:")
        for menu, rating in summary["top_10_menus"].items():
            print(f"- {menu}: {rating}점")
            
        print("\n가장 기피하는 하위 10개 메뉴:")  
        for menu, rating in summary["bottom_10_menus"].items():
            print(f"- {menu}: {rating}점")
            
        print("\n환장하는 메뉴들의 음식종류 분포:")
        for type, count in summary["favorite_type_count"].items():
            print(f"- {type}: {count}개")
            
        print("\n환장하는 메뉴들의 맛 프로파일 분포:")
        for flavor, count in summary["favorite_flavor_count"].items():
            print(f"- {flavor}: {count}개")

# ============================
# 2. 카테고리별 선호도 분석
# ============================

# 특정 사용자(user_id)의 카테고리별 선호도 분석
def category_preference_analysis(user_id):
    if user_id not in USER_PREFERENCES:
        print(f"Warning: User ID '{user_id}' not found in preferences")
        return {
            "category_mean": {},
            "flavor_mean": {},
            "cooking_mean": {}
        }
        
    user_data = USER_PREFERENCES[user_id]
    
    # 카테고리별 평균 계산
    category_ratings = {}
    flavor_ratings = {}
    cooking_ratings = {}
    
    for menu, rating in user_data.items():
        if menu in MENU_DETAILS:
            # 음식종류별 평균
            category = MENU_DETAILS[menu]["음식종류"]
            if category not in category_ratings:
                category_ratings[category] = {"sum": 0, "count": 0}
            category_ratings[category]["sum"] += rating
            category_ratings[category]["count"] += 1
            
            # 맛 프로파일별 평균
            flavor = MENU_DETAILS[menu]["맛 프로파일"]
            if flavor not in flavor_ratings:
                flavor_ratings[flavor] = {"sum": 0, "count": 0}
            flavor_ratings[flavor]["sum"] += rating
            flavor_ratings[flavor]["count"] += 1
            
            # 조리 방식별 평균
            cooking = MENU_DETAILS[menu]["조리 방식"]
            if cooking not in cooking_ratings:
                cooking_ratings[cooking] = {"sum": 0, "count": 0}
            cooking_ratings[cooking]["sum"] += rating
            cooking_ratings[cooking]["count"] += 1
    
    # 평균 계산 및 Series로 변환
    category_mean = pd.Series({k: v["sum"]/v["count"] for k, v in category_ratings.items()})
    flavor_mean = pd.Series({k: v["sum"]/v["count"] for k, v in flavor_ratings.items()})
    cooking_mean = pd.Series({k: v["sum"]/v["count"] for k, v in cooking_ratings.items()})
    
    return {
        "category_mean": category_mean,
        "flavor_mean": flavor_mean,
        "cooking_mean": cooking_mean
    }

def print_category_analysis(user_id):
    analysis = category_preference_analysis(user_id)
    print("\n음식종류별 평균점수:\n", analysis["category_mean"])
    print("\n맛 프로파일별 평균점수:\n", analysis["flavor_mean"])
    print("\n조리방식별 평균점수:\n", analysis["cooking_mean"])

# ============================
# 3. 시각화
# ============================

# (예: 맛 프로파일별 평균 점수 바 차트)
def plot_flavor_preference(user_id):
    analysis_data = category_preference_analysis(user_id)
    flavor_mean = analysis_data["flavor_mean"]
    
    if len(flavor_mean) > 0:
        plt.figure(figsize=(12, 6))
        flavor_mean.plot(kind='bar')
        plt.title('맛 프로파일별 평균 점수')
        plt.ylabel('평균 선호도')
        plt.xlabel('맛 프로파일')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("맛 프로파일 데이터가 충분하지 않습니다.")

# (예: 조리방식별 평균 점수 레이더 차트)
# 레이더 차트를 그리려면 polar plot을 사용:
def plot_cooking_radar(user_id):
    analysis_data = category_preference_analysis(user_id)
    cooking_mean = analysis_data["cooking_mean"].dropna()
    labels = cooking_mean.index
    values = cooking_mean.values
    
    # 레이더 차트 세팅
    N = len(labels)
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]  # 마지막에 시작점 반복
    
    values = list(values)
    values += values[:1]

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(3.14159 / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], labels)
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, 'skyblue', alpha=0.4)
    ax.set_title("조리방식별 평균 점수 레이더 차트")
    plt.show()

# (예: 워드 클라우드)
def plot_wordcloud_of_favorites(user_id):
    user_data = USER_PREFERENCES[user_id]
    favorite_data = {menu: rating for menu, rating in user_data.items() if rating == 4}
    favorite_menus = list(favorite_data.keys())
    text = " ".join(favorite_menus)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("환장하는 메뉴 워드클라우드")
    plt.show()

# ============================
# 4. 인사이트 텍스트
# ============================

# 사용자 속성 분석 결과를 바탕으로 문구를 생성하는 함수
def generate_insights_text(user_id):
    # 기본 분석 데이터 가져오기
    analysis_data = category_preference_analysis(user_id)
    summary_data = user_preference_summary(user_id)
    
    category_mean = analysis_data["category_mean"]
    flavor_mean = analysis_data["flavor_mean"]
    cooking_mean = analysis_data["cooking_mean"]
    
    # 가장 선호하는 카테고리/맛/조리법 찾기
    top_category = max(category_mean.items(), key=lambda x: x[1]) if category_mean else None
    top_flavor = max(flavor_mean.items(), key=lambda x: x[1]) if flavor_mean else None
    top_cooking = max(cooking_mean.items(), key=lambda x: x[1]) if cooking_mean else None

    lines = []
    
    # 기본 선호도 정보
    lines.append(f"=== {user_id}님의 음식 취향 분석 ===\n")
    lines.append(f"전체 음식 평균 선호도: {summary_data['avg_rating']:.1f}점")
    
    # 음식 종류별 선호도
    if top_category:
        lines.append(f"\n[음식 종류별 분석]")
        lines.append(f"- 가장 선호하는 음식 종류는 {top_category[0]}입니다. (평균 {top_category[1]:.1f}점)")
        lines.append(f"- {summary_data['favorite_type_count'].most_common(1)[0][0]} 메뉴를 특히 자주 선택하시는 편입니다.")
    
    # 맛 프로파일 분석
    if top_flavor:
        lines.append(f"\n[맛 프로파일 분석]")
        lines.append(f"- 주로 {top_flavor[0]} 맛을 선호하십니다. (평균 {top_flavor[1]:.1f}점)")
        lines.append(f"- 환장하시는 메뉴들 중에서는 {list(summary_data['favorite_flavor_count'].keys())[:2]}와 같은 맛이 두드러집니다.")
    
    # 조리 방식 분석
    if top_cooking:
        lines.append(f"\n[조리 방식 분석]")
        lines.append(f"- {top_cooking[0]} 요리를 가장 선호하시는 것으로 나타났습니다. (평균 {top_cooking[1]:.1f}점)")
    
    # 구체적인 메뉴 추천
    lines.append("\n[메뉴 추천]")
    top_menus = list(summary_data['top_10_menus'].keys())[:3]
    lines.append(f"- 선호도를 바탕으로 {', '.join(top_menus)}와 비슷한 메뉴를 추천드립니다.")
    
    return "\n".join(lines)

