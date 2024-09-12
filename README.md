# 스파르타 뉴스 Backend (Django REST Framework)

## 1. 목표
스파르타 뉴스의 백엔드 기능을 Django REST Framework를 사용하여 구현합니다.

## 2. DRF (Django REST Framework) 소개
- DRF는 Django의 확장 패키지로, RESTful API를 쉽게 만들 수 있도록 도와줍니다.
- **REST API**는 클라이언트-서버 간 데이터를 JSON, XML 형식으로 주고받기 위한 방식입니다.
- **Serializer**는 Django 모델을 JSON, XML 등으로 변환하거나 반대로 변환하는 역할을 합니다.

## 3. spartanews_drf
- 프로젝트명 'spartanews_drf'
- 각 유저는 자신의 기사를 등록할 수 있습니다.
- 프론트엔드 구현 대신, Postman을 사용하여 API를 테스트하였습니다.
## ⏲️ 개발기간


## 📚️ 기술스택
- 백엔드(Backend) 
    - Python
    - Django

- 데이터베이스(Database)
  	- SQLite

- 기타 도구 및 라이브러리
  	- Git/GitHub
  	- django-extensions

### ✔️ Language
- Python: 백엔드 로직, 데이터 처리 및 API 개발을 위한 언어.
- SQL: 데이터베이스 쿼리 및 관리에 사용.
  
### ✔️ Version Control
- Git: 소스 코드 버전 관리 시스템. 프로젝트의 버전 기록을 유지하고 협업을 지원함.
- GitHub: 원격 저장소 호스팅 서비스, 코드 리뷰 및 협업을 지원.

### ✔️ IDE
- Visual Studio Code: Python의 개발을 위한 통합 개발 환경. 확장성 높은 플러그인 시스템 지원.
  
### ✔️ Framework
- Django: Python 기반의 웹 프레임워크, 모델-뷰-템플릿(MVT) 패턴을 사용하여 효율적인 웹 애플리케이션 개발.

### ✔️  DBMS
- SQLite: 가벼운 관계형 데이터베이스 관리 시스템. 파일 기반의 데이터베이스로, 설정과 유지 관리가 간편하며, 로컬 개발과 작은 규모의 배포에 적합.
  
## 서비스 구조
- 백엔드: 데이터 처리, 비즈니스 로직 및 API를 처리.
- 데이터베이스: SQLite를 사용하여 사용자 및 기사 데이터를 저장 및 관리.
- API: 프론트엔드와 백엔드 간의 데이터 교환을 처리.


## API 명세서


## 프로젝트 파일 구조

```plaintext
SpartaMarket/
├── accounts/               # 사용자 계정 관련 앱
│   └── *                   # 앱 관련 파일들 
├── media/                  # 미디어 파일 저장소
├── articles/               # 기사 관련 앱
│   └── *                   # 앱 관련 파일들
├── spartanews/             # 프로젝트 설정 디렉터리
│   ├── settings.py         # 프로젝트 설정 파일
│   ├── urls.py             # 전역 URL 패턴 정의
├── manage.py               # Django 관리 커맨드 파일
└── README.md               # 프로젝트 설명서
