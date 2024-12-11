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
    print("⚠️ 진행 중 설문을 종료하려면 'q'를 입력하세요.")
    user_preferences = {}
    total_menus = len(menu_names)  # 전체 메뉴 개수

    for idx, menu in enumerate(menu_names, start=1):
        while True:
            try:
                # 진행 상황 출력
                print(f"\n[{idx}/{total_menus}] '{menu}'에 대한 선호도를 입력해주세요.")
                response = input(f"  선호도 점수 (1~4 또는 'q' 종료): ")
                
                # 종료 옵션 처리
                if response.lower() == 'q':
                    print("\n🚪 설문을 종료합니다. 입력된 데이터는 저장되지 않습니다.")
                    return
                
                # 점수 입력 확인
                score = int(response)
                if score < 1 or score > 4:
                    raise ValueError("점수는 1에서 4 사이여야 합니다.")
                user_preferences[menu] = score
                break
            except ValueError as e:
                print(f"⚠️ 올바른 점수를 입력해주세요. {e}")

        # 진행 상황 알림
        completed = idx
        remaining = total_menus - completed
        print(f"✅ 진행 상황: {completed}/{total_menus} 완료, {remaining}개 남음")

    # 새로운 유저 데이터 생성
    new_user_row = pd.DataFrame([{**{"이름": user_name}, **user_preferences}])

    # 기존 데이터와 병합
    user_data = pd.concat([user_data, new_user_row], ignore_index=True)

    # CSV 저장
    user_data.to_csv(user_file_path, index=False)
    print(f"\n✅ 새로운 사용자 '{user_name}'님의 데이터가 저장되었습니다!")
    print("\n⚠️ 주의 : 새로운 사용자 추가 후에는 프로그램을 재시작 해야합니다!")
    print("0번을 눌러 프로그램을 종료 후 재시작 해주세요 😊")
