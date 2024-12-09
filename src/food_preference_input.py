import os

def get_preference_text(num):
    preferences = {
        1: "1. 환장함",
        2: "2. 좋아함",
        3: "3. 그럭저럭",
        4: "4. 싫어함"
    }
    return preferences.get(num, "잘못된 입력입니다.")

def input_preferences():
    # 파일 경로 설정
    base_path = os.path.dirname(os.path.abspath(__file__))
    survey_path = os.path.join(os.path.dirname(base_path), 'data', 'user_data.csv')
    
    # CSV 파일에서 첫 번째 행(메뉴 목록) 읽기
    with open(survey_path, 'r', encoding='utf-8') as f:
        menus = f.readline().strip().split(',')[1:]  # 첫 번째 열(이름) 제외
    
    # 사용자 이름 입력
    user_name = input("이름을 입력해주세요: ").strip()
    if not user_name:  # 이름이 비어있으면 종료
        return None
    
    preferences = []
    print("\n각 메뉴에 대한 선호도를 입력해주세요 (1: 환장함, 2: 좋아함, 3: 그럭저럭, 4: 싫어함)")
    print("입력을 중단하려면 'q'를 입력하세요.\n")
    
    # 각 메뉴에 대한 선호도 입력
    for i, menu in enumerate(menus, 1):
        while True:
            print(f"{i}/100 - {menu}")
            choice = input("선호도 (1-4): ").strip().lower()
            
            if choice == 'q':
                return None  # 입력 중단
            
            try:
                choice = int(choice)
                if 1 <= choice <= 4:
                    preferences.append(get_preference_text(choice))
                    break
                else:
                    print("1에서 4 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("올바른 숫자를 입력해주세요.")
    
    # CSV 파일에 새로운 데이터 추가
    with open(survey_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{user_name},{','.join(preferences)}")
    
    return user_name
