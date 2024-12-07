# 설문조사 데이터를 처리하여 사용자별 선호도를 파싱하고 이를 전역 변수로 저장하는 파이썬 스크립트
import csv

# 설문조사의 평점 문자열을 정수로 변환하는 함수
def parse_rating(rating_str):
    # 평점 변환을 위한 매핑 딕셔너리
    rating_map = {
        "1. 환장함": 4,
        "2. 좋아함": 3, 
        "3. 그럭저럭": 2,
        "4. 싫어함": 1
    }
    return rating_map.get(rating_str, 0)

# 설문조사 데이터를 읽어 사용자별 선호도를 딕셔너리 형태로 정리하는 함수
def load_user_preferences():
    user_preferences = {}
    
    # 설문조사 데이터 파일을 읽어 사용자별 선호도를 딕셔너리 형태로 정리
    with open('data/survey_results.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        menus = [menu.split('.')[1].strip() if '.' in menu else menu for menu in header[2:]]
        
        # 각 행을 순회하며 사용자별 선호도를 딕셔너리에 저장
        for row in reader:
            if not row:
                continue
                
            user_id = row[1].strip()
            if not user_id:
                continue
                
            user_preferences[user_id] = {}
            for menu, rating in zip(menus, row[2:]):
                if rating:
                    user_preferences[user_id][menu] = parse_rating(rating)
    
    return user_preferences

# 다른 파일에서 바로 사용할 수 있도록 전역 변수로 저장
USER_PREFERENCES = load_user_preferences()
