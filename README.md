# 기능
MQTT Broker에 접속하여 특정 Topic을 Subscribe.
구글 드라이브에 접속하여 폴더 검색, 파일 업로드.

# 사전 준비
- MQTT Info
    - Broker addr
    - Topic
- Google Drive Info
    - API Key

#사용법
1. 아래 변수에 google drive API Key의 file path를 넣어준다.
    ```python
    store = file.Storage('storage.json Path')
    flow = client.flow_from_clientsecrets('client_secret_drive.json Path', SCOPES)
 
    ```
2. Broker, Topic, mqtt_message 저장 폴더를 지정.
    ```
    broker = 'Broker addr'
    mqtt_topic = 'Topic'
    file_path = 'Message save folder path'
    ```

# Google Drive API
1. 접속 'https://console.developers.google.com/flows/enableapi?apiid=drive'
2. 프로젝트 만들기 -> 계속
3. 사용자 인증정보로 이동
4. 사용자 인증 정보
5. OAuth 동의 화면
6. 애플리케이션 이름 작성. 지원 이메일 확인. -> 저장
7. OAuth 클라이언트 ID 만들기 -> 기타 -> 확인
8. 생성된 ID 다운로드. -> 이름 변경 'client_secret_drive.json'
9. 파이썬 실행시 웹에 구글 로그인 페이지 생성. 로그인 사용할 계정 선택 후 Completed 팝업.
10. 폴더안에 storage.json파일 자동 생성.