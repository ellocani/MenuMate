import os
import sys
import unittest

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.group_analysis import GroupAnalysis
import pandas as pd

class TestGroupAnalysis(unittest.TestCase):
    def setUp(self):
        # 테스트용 데이터 준비
        self.menu_data = pd.read_csv("data/processed_menu_details.csv")
        self.user_data = pd.read_csv("data/processed_user_data.csv")
        self.group_analysis = GroupAnalysis(self.menu_data, self.user_data)

    def test_analyze_group(self):
        # 특정 그룹의 선호도 분석 테스트
        group_names = ["연누", "김정민", "안태우"]
        top_menus, recommended_menus = self.group_analysis.analyze_group(group_names)
        self.assertIsNotNone(top_menus)
        self.assertFalse(recommended_menus.empty)

if __name__ == "__main__":
    unittest.main()
