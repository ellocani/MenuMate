import pandas as pd

class UserDetails:
    def __init__(self, user_data_path):
        """
        사용자 데이터를 로드합니다.
        Args:
            user_data_path (str): 사용자 데이터 파일 경로.
        """
        self.user_data = pd.read_csv(user_data_path)

    def get_user_details(self, user_name):
        """
        특정 사용자의 설문 결과를 반환합니다.
        Args:
            user_name (str): 확인할 사용자 이름.

        Returns:
            dict: 사용자 이름, 설문 데이터 딕셔너리 형태.
        """
        user_row = self.user_data[self.user_data["이름"] == user_name]
        if user_row.empty:
            raise ValueError(
                f"'{user_name}'님을 데이터에서 찾을 수 없습니다. 😥\n"
                "아직 설문을 작성하지 않았거나 이름을 잘못 입력하셨을 수 있습니다.\n"
                "다시 확인해주세요!"
            )
        
        # 사용자 데이터 딕셔너리 생성 (이름 제외)
        user_data_dict = user_row.drop(columns=["이름"]).iloc[0].dropna().to_dict()
        return {
            "user_name": user_name,
            "preferences": user_data_dict
        }
