import pandas as pd

def add_new_user(user_name, user_file_path):
    """
    새로운 유저 데이터를 입력받아 기존 사용자 데이터에 추가합니다.

    Args:
        user_name (str): 새로 추가할 사용자 이름.
        user_file_path (str): 사용자 데이터 파일 경로.

    Returns:
        None: 사용자 데이터 파일에 새로운 행이 추가됩니다.
    """
    # 사용자 데이터 파일 로드
    user_data = pd.read_csv(user_file_path)

    # 메뉴 추출 (1행 2열부터 끝까지 열 이름)
    menu_names = user_data.columns[1:].tolist()

    # 새 유저의 선호도 입력받기
    print(f"'{user_name}'님의 선호도를 입력해주세요.")
    print("1~4 사이의 숫자를 입력해주세요. 각 숫자는 메뉴에 대한 선호도 점수를 나타냅니다.")
    print("1 : 싫어하는 메뉴, 2 : 그럭저럭인 메뉴, 3 : 좋아하는 메뉴, 4 : 매우 좋아하는 메뉴")
    user_preferences = {}
    for menu in menu_names:
        while True:
            try:
                score = int(input(f"'{menu}'에 대한 선호도 (1~4): "))
                if score < 1 or score > 4:
                    raise ValueError("점수는 1에서 4 사이여야 합니다.")
                user_preferences[menu] = score
                break
            except ValueError as e:
                print(f"⚠️ {e}")

    # 새로운 유저 데이터 생성
    new_user_row = pd.DataFrame([{**{"이름": user_name}, **user_preferences}])

    # 기존 데이터와 병합
    user_data = pd.concat([user_data, new_user_row], ignore_index=True)

    # CSV 저장
    user_data.to_csv(user_file_path, index=False)
    print(f"\n✅ 새로운 사용자 '{user_name}'님의 데이터가 저장되었습니다!")
