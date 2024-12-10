import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data_loader import DataLoader
from src.group_analysis import GroupAnalysis, recommend_menus_with_attributes, align_menu_and_user_data

# 파일 경로 설정
menu_file_path = "data/processed_menu_details.csv"
user_file_path = "data/processed_user_data.csv"

# 데이터 로드
loader = DataLoader(menu_file_path, user_file_path)
menu_data, user_data = loader.load_data()

aligned_menu_data, aligned_user_data = align_menu_and_user_data(menu_data, user_data)
print("공통 메뉴:")
print(aligned_menu_data["메뉴"].tolist())
