import pandas as pd

class DataLoader:
    def __init__(self, menu_file_path, user_file_path):
        self.menu_file_path = menu_file_path
        self.user_file_path = user_file_path

    def load_data(self):
        """
        메뉴 데이터와 사용자 데이터를 로드하는 함수
        """
        try:
            # CSV 파일 읽기
            menu_data = pd.read_csv(self.menu_file_path)
            user_data = pd.read_csv(self.user_file_path)
            return menu_data, user_data
        except FileNotFoundError as e:
            # 파일을 찾을 수 없는 경우 에러 메시지 출력
            print(f"에러: {e}")
            return None, None
