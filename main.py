from preprocessing.handling_data import USER_PREFERENCES

# 특정 사용자의 선호도 확인
print(USER_PREFERENCES["연누"]["김치찌개"])

# 전체 사용자 목록 확인
users = USER_PREFERENCES.keys()
print(users)

# 특정 사용자의 모든 메뉴 선호도 확인
user_ratings = USER_PREFERENCES["연누"]
print(user_ratings)