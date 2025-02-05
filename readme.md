# Legislation Service RSS Maker

이 프로젝트는 EMR 유지보수 관련, 다양한 정부 및 관련 기관의 웹사이트에서 RSS 피드를 생성하는 서비스입니다.

## 주요 기능
- 각 기관 웹사이트의 최신 글을 크롤링하여 RSS 아이템 생성
- SQLite3 데이터베이스에 RSS 아이템 저장
- 설정 파일(config.ini) 기반의 경로 및 환경 설정 지원
- BASEPATH가 없으면 현재 작업 디렉토리 내의 `rss` 폴더를 생성하여 파일 저장

## 구성 파일
- **main.py**: 프로그램 진입점, RSS 생성 함수 호출
- **rssmaker/rss_maker.py**: RSS 피드 생성 및 파일 저장 로직 구현
- **rssmaker/DbHandler.py**: SQLite3 데이터베이스 연결 및 테이블 관리
- **rssmaker/parser_*.py**: 각 기관별 크롤링 파서 모듈들
- **config.ini**: 기본 경로 등 환경설정 파일

## 실행 방법
1. 필요한 종속 라이브러리 설치  
   ```bash
   pip install -r requirements.txt
   ```
2. config.ini 파일에서 `BASEPATH`를 본인의 환경에 맞게 수정합니다.
3. 아래 명령어로 프로그램을 실행합니다.  
   ```bash
   python main.py
   ```

## 로그 및 파일 저장
- RSS 파일은 기본적으로 `BASEPATH`에 저장됩니다.
- `BASEPATH`가 존재하지 않을 경우, 현재 작업 디렉토리 내의 `rss` 폴더를 생성하여 파일을 저장합니다.
- 로그는 콘솔에 기록되며, 필요에 따라 로깅 설정을 수정할 수 있습니다.

## 주의 사항
- SSL 인증서 검증을 비활성화한 상태로 HTTP 요청을 수행하므로, 운영 환경에서는 보안 설정을 재검토하시기 바랍니다.
- Selenium을 이용한 크롤링을 위해 ChromeDriver 설치가 필요합니다.

## 라이선스
This project is licensed under the MIT License.