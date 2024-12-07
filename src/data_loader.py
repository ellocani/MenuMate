# CSV 데이터 로딩 및 전처리 함수

import pandas as pd

def load_survey_data(path: str) -> pd.DataFrame:
    """
    설문 결과 CSV를 로드하고 전처리
    """
    try:
        df = pd.read_csv(path)
        
        # 필수 컬럼 체크
        required_cols = ['이름']
        if not all(col in df.columns for col in required_cols):
            raise ValueError("사용자를 찾을 수수 없습니다.")
            
        preference_map = {
            "1. 환장함": 4,
            "2. 좋아함": 3,
            "3. 그럭저럭": 2,
            "4. 싫어함": 1
        }
        
        menu_cols = [c for c in df.columns if c != "이름"]
        for col in menu_cols:
            # 잘못된 값이 있는지 체크
            invalid_values = df[col][~df[col].isin(preference_map.keys())].unique()
            if len(invalid_values) > 0:
                raise ValueError(f"컬럼 {col}에 잘못된 값이 있습니다: {invalid_values}")
            df[col] = df[col].map(preference_map)
            
        return df
        
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {path}")
        return None
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {str(e)}")
        return None

def load_menu_details(path: str) -> pd.DataFrame:
    """
    메뉴별 디테일 정보 CSV 로드 및 검증
    """
    try:
        menu_df = pd.read_csv(path)
        
        # 필수 컬럼 체크
        required_cols = ['메뉴', '주재료', '맛 프로파일', '분류']
        if not all(col in menu_df.columns for col in required_cols):
            raise ValueError(f"필수 컬럼이 없습니다. 필요한 컬럼: {required_cols}")
            
        # 메뉴 중복 체크
        if menu_df['메뉴'].duplicated().any():
            dupes = menu_df[menu_df['메뉴'].duplicated()]['메뉴'].tolist()
            raise ValueError(f"중복된 메뉴이 있습니다: {dupes}")
            
        return menu_df
        
    except Exception as e:
        print(f"메뉴 상세 정보 로드 중 오류 발생: {str(e)}")
        return None
