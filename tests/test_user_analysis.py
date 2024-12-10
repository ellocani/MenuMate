import os
import sys
import unittest

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.user_analysis import UserAnalysis
import pandas as pd

class TestUserAnalysis(unittest.TestCase):
    def setUp(self):
        # 테스트용 데이터 준비
        self.menu_data = pd.read_csv("data/processed_menu_details.csv")
        self.user_data = pd.read_csv("data/processed_user_data.csv")
        self.user_analysis = UserAnalysis(self.menu_data, self.user_data)

    def test_analyze_user(self):
        # 특정 사용자의 선호도 분석 테스트
        result = self.user_analysis.analyze_user("연누")
        self.assertIsNotNone(result)
        self.assertFalse(result.empty)

if __name__ == "__main__":
    unittest.main()
