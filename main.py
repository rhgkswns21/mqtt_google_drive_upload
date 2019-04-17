from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as date
import os

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('E:\MyFolder\Source\google_drive_key\storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('E:\MyFolder\Source\google_drive_key\client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

google_drive = build('drive', 'v3', http=creds.authorize(Http()))
folder_status = False
folder_dic = {}
today = date.datetime.now().strftime('%Y%m%d')

##폴더 이름 및 ID검색. ##Search for folder name, ID
page_token = None
RSP = google_drive.files().list(
                        q="mimeType='application/vnd.google-apps.folder'",
                        spaces='drive',
                        fields='nextPageToken, files(id, name, parents)',
                        pageToken=page_token).execute()

##검색된 폴더 이름, ID 출력 및 폴더 이름을 키로 가진 딕셔너리 생성. ##Create a Dictionary with the Folder Name as Key
for file in RSP.get('files', []):
    # Process change
    folder_dic[file.get('name')] = [file.get('id'), file.get('parents')]
    print("Key : " , file.get('name') + "\nid : ", folder_dic[file.get('name')][0] + "\nparents : ", folder_dic[file.get('name')][1])
    if('MQTT_Data' == file.get('name')):
        folder_status = True
page_token = RSP.get('nextPageToken', None)

##google_drive에 MQTT_data 폴더가 없으면 생성 ##if google drive is haven't MQTT_data folder.make MQTT_data folder
if ('MQTT_data' in folder_dic) == False:
    file_metadata = {'name': 'MQTT_data', 'mimeType': 'application/vnd.google-apps.folder'}
    file = google_drive.files().create(body=file_metadata, fields='id, parents').execute()
    folder_dic['MQTT_data'] = [file.get('id'), file.get('parents')]
    print('make folder...')

if (today in folder_dic) == False:
    file_metadata = {'name': today, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [folder_dic['MQTT_data'][0]]}
    file = google_drive.files().create(body=file_metadata, fields='id, parents').execute()
    folder_dic[today] = [file.get('id'), file.get('parents')]
    print('make folder...\nfolder_name : ', today + '\nid : ', folder_dic[today][0] + '\nparents : ', folder_dic[today][1])


'''
##만약 Test폴더가 없을 경우 폴더 생성, ID값은 folder_id.txt로 로컬에 저장
if(folder_status == False):
    file_metadata = {
        'name': 'MQTT_data',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = google_drive.files().create(body=file_metadata, fields='id').execute()
    print('Folder ID: %s' % file.get('id'))
    f = open('folder_id.txt', 'w')
    f.write('mqtt,' + file.get('id'))
    f.close()

##현재 시간을 가진 txt파일 로컬에 생성
now_time = date.datetime.now().strftime('%Y%m%d%H%M%S')
f = open(now_time + '.txt', 'w')
f.write(now_time)
f.close()

##파일 업로드.
FILES = ((now_time + '.txt'),)
for file_title in FILES:
    file_name = file_title
    metadata = {'name': file_name,
                'mimeType': None,
                'parant': }
    res = google_drive.files().create(body=metadata, media_body=file_name).execute()
    if res:
        print('Uploaded "%s" (%s)' % (file_name, res['mimeType']))

##업로드 완료 파일 삭제
os.remove(now_time + '.txt')

'''