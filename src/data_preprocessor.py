import pandas as pd
import numpy as np

def preprocess_menu_details(df: pd.DataFrame) -> pd.DataFrame:
    """
    메뉴 상세 정보 데이터프레임 전처리
    - 결측값을 'Unknown'으로 대체
    - 컬럼명 일관성 확인
    """
    # 깊은 복사로 원본 데이터 보존
    processed_df = df.copy()
    
    # 모든 컬럼의 결측값을 'Unknown'으로 대체
    processed_df = processed_df.fillna('Unknown')
    
    # 문자열 데이터 양쪽 공백 제거
    for col in processed_df.columns:
        if processed_df[col].dtype == 'object':
            processed_df[col] = processed_df[col].str.strip()
    
    # 컬럼명 일관성 확인 및 수정
    column_mapping = {
        '메뉴': '메뉴',
        '음식종류': '분류',
        # 필요한 경우 더 추가
    }
    processed_df = processed_df.rename(columns=column_mapping)
    
    return processed_df

def normalize_menu_name(menu_name: str) -> str:
    """
    메뉴 정규화 함수
    - 번호와 공백 제거
    - 괄호 안의 내용 제거
    """
    # 번호와 점(.) 제거 (예: "1. 김치찌개" -> "김치찌개")
    menu_name = ''.join(c for c in menu_name if not (c.isdigit() or c == '.'))
    # 앞뒤 공백 제거
    menu_name = menu_name.strip()
    # 괄호와 그 안의 내용 제거 (예: "사케동 (연어덮밥)" -> "사케동")
    menu_name = menu_name.split('(')[0].strip()
    return menu_name

def preprocess_survey_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    설문 데이터 전처리
    - 메뉴 정규화
    - 선호도 점수 매핑
    """
    processed_df = df.copy()
    
    # 이름 컬럼 공백 제거
    if '이름' in processed_df.columns:
        processed_df['이름'] = processed_df['이름'].str.strip()
    
    # 선호도 매핑
    preference_map = {
        "1. 환장함": 4,
        "2. 좋아함": 3,
        "3. 그럭저럭": 2,
        "4. 싫어함": 1
    }
    
    # 컬럼명(메뉴) 정규화
    rename_dict = {}
    for col in processed_df.columns:
        if col != '이름':
            normalized_name = normalize_menu_name(col)
            rename_dict[col] = normalized_name
    
    # 컬럼명 변경
    processed_df = processed_df.rename(columns=rename_dict)
    
    # 이름을 제외한 모든 컬럼에 대해 선호도 매핑
    menu_cols = [col for col in processed_df.columns if col != '이름']
    for col in menu_cols:
        processed_df[col] = processed_df[col].map(preference_map)
    
    return processed_df

def validate_data(survey_df: pd.DataFrame, menu_df: pd.DataFrame) -> tuple:
    """
    전처리된 데이터의 유효성 검증
    """
    try:
        # 메뉴 컬럼 확인 및 통일
        if '메뉴' in menu_df.columns:
            menu_df = menu_df.rename(columns={'메뉴': '메뉴'})
        
        # 필수 컬럼 존재 확인
        required_menu_cols = ['메뉴', '주재료', '맛 프로파일', '분류']
        required_survey_cols = ['이름']
        
        if not all(col in menu_df.columns for col in required_menu_cols):
            print(f"메뉴 데이터에 필수 컬럼이 없습니다. 필요한 컬럼: {required_menu_cols}")
            return False, None
            
        if not all(col in survey_df.columns for col in required_survey_cols):
            print(f"설문 데이터에 필수 컬럼이 없습니다. 필요한 컬럼: {required_survey_cols}")
            return False, None
        
        # 메뉴 중복 체크
        if menu_df['메뉴'].duplicated().any():
            dupes = menu_df[menu_df['메뉴'].duplicated()]['메뉴'].tolist()
            print(f"중복된 메뉴이 있습니다: {dupes}")
            return False, None
            
        # 설문 데이터의 메뉴와 메뉴 상세 정보의 메뉴 일치 확인
        survey_menus = set([col for col in survey_df.columns if col != '이름'])
        menu_names = set(menu_df['메뉴'])
        
        missing_menus = survey_menus - menu_names
        if missing_menus:
            print(f"설문에 있는 메뉴 중 상세정보가 없는 메뉴가 있습니다: {missing_menus}")
            print("해당 메뉴들은 분석에서 제외됩니다.")
            
            # 누락된 메뉴 컬럼 제거
            survey_df = survey_df.drop(columns=missing_menus)
        
        return True, menu_df
        
    except Exception as e:
        print(f"데이터 검증 중 오류 발생: {str(e)}")
        return False, None

def load_and_preprocess_data(survey_path: str, menu_path: str) -> tuple:
    """
    데이터 로드 및 전처리를 수행하는 메인 함수
    """
    try:
        # 데이터 로드
        survey_df = pd.read_csv(survey_path)
        menu_df = pd.read_csv(menu_path)
        
        # 전처리 수행
        processed_survey = preprocess_survey_data(survey_df)
        processed_menu = preprocess_menu_details(menu_df)
        
        # 데이터 검증 및 누락 메뉴 처리
        is_valid, updated_menu_df = validate_data(processed_survey, processed_menu)
        if not is_valid:
            return None, None
            
        return processed_survey, updated_menu_df
        
    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {str(e)}")
        return None, None
    except Exception as e:
        print(f"데이터 처리 중 오류가 발생했습니다: {str(e)}")
        return None, None 