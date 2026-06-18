1) 프로젝트 파일 용도 설명
startup.bat: 서버 실행 파일
    1. localhost:8000
    2. 파일 실행 후 URL/docs로 접속하여 swagger 기능 확인 가능(SQLite 활용하여 DB동작가능)
    3. 사전에 requirements.txt에 있는 라이브러리가 있는지 검사 및 설치합니다.

clean_and_zip.bat: 파일 재압축
    1. __pycache__ 파일이 자동 생성되는데, 이를 삭제하고 압축하기 위함

common_code.db: SQLite의 데이터베이스 공간(뷰어로 열어볼 수 있습니다.)

2) 프로젝트 디렉토리 구조 설명
app: application 관련 파일
    db: 
        init_db(웹앱 서버 시작시 데이터베이스 접속)
        session(각 crud 트랜젝션에서 session을 가져와 작업 후 종료)
    models:
        common_code(SQLite에 필요한 관계 모델링을 정의한 파일)
    routers:
        실제 request요청 url이 정의된 곳(최종적인 결정은 router를 등록할 때 prefix와 함꼐 결정된다)
    schemas:
        router에서 사용하는 DTO 정의(계층적 구조)
    