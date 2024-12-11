# MenuMate (메뉴메이트)

MenuMate는 사용자의 음식 취향을 분석하고 개인 및 그룹을 위한 메뉴를 추천해주는 CLI 애플리케이션입니다.

## 주요 기능

- 🍽️ **개인 취향 분석**: 사용자별 음식 선호도를 분석하여 상세 리포트 제공
- 👥 **그룹 추천**: 여러 사용자의 취향을 고려한 최적의 메뉴 추천
- 📊 **시각화**: 선호도 분석 결과를 그래프로 시각화
- ➕ **사용자 추가**: 새로운 사용자의 음식 선호도 정보 등록

## 설치 방법

1. 저장소 클론

bash
git clone https://github.com/yourusername/menumate.git
cd menumate

2. 가상환경 생성 및 활성화 (선택사항)

bash
python -m venv venv

Windows
venv\Scripts\activate

macOS/Linux
source venv/bin/activate

3. 패키지 설치

bash
pip install -e .

## 사용 방법

### 1. 새로운 사용자 등록

bash
menumate add

- 프롬프트에 따라 이름과 각 메뉴에 대한 선호도를 입력합니다
- 선호도는 1(환장함) ~ 4(싫어함) 사이의 숫자로 입력
- 중간에 'q'를 입력하면 취소할 수 있습니다

### 2. 개인 취향 분석 리포트 조회

bash
menumate report 홍길동

다음 정보를 확인할 수 있습니다:
- 전체 평균 선호도
- 가장 좋아하는 메뉴 TOP 10
- 가장 싫어하는 메뉴 TOP 10
- 선호하는 음식 카테고리 분석
- 선호하는 맛 프로파일 분석
- 시각화된 분석 그래프

### 3. 그룹 메뉴 추천

bash
menumate group 홍길동 김철수 이영희

- 입력된 모든 사용자의 선호도를 고려하여 TOP 10 메뉴를 추천합니다
- 각 메뉴의 평균 선호도 점수도 함께 표시됩니다

## 데이터 파일

프로그램은 다음 두 개의 CSV 파일을 사용합니다:
- `data/user_data.csv`: 사용자별 메뉴 선호도 데이터
- `data/menu_details.csv`: 메뉴별 상세 정보 (주재료, 맛 프로파일, 분류 등)

## 시스템 요구사항

- Python 3.7 이상
- pandas
- matplotlib
- seaborn

## 문제 해결

1. 한글 폰트 관련 문제
   - Windows: 'Malgun Gothic' 폰트가 자동으로 설정됩니다
   - macOS: 'AppleGothic' 폰트가 사용됩니다
   - Linux: 'NanumGothic' 폰트 설치가 필요할 수 있습니다

2. 데이터 파일을 찾을 수 없는 경우
   - `data` 디렉토리가 프로젝트 루트에 있는지 확인하세요
   - CSV 파일의 이름이 정확한지 확인하세요








