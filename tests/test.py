import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('data/processed_menu_details.csv')

# 변경할 메뉴 리스트
menu_list = ['삼계탕', '생선까스', '육전', '생선구이']

# 각 메뉴에 대해 값 변경
for menu in menu_list:
    df.loc[df['메뉴'] == menu, '맛 프로파일_담백/고소'] = 0
    df.loc[df['메뉴'] == menu, '맛 프로파일_짭짤'] = 1

# 수정된 데이터프레임을 CSV 파일로 저장
df.to_csv('data/processed_menu_details.csv', index=False)