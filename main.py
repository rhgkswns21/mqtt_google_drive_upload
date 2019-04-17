from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as date
import os

try :
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('E:\MyFolder\Source\google_drive_key\storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('E:\MyFolder\Source\google_drive_key\client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

google_drive = build('drive', 'v3', http=creds.authorize(Http()))

##현재 시간을 가진 txt파일 로컬에 생성
now_time = date.datetime.now().strftime('%Y%m%d%H%M%S')
f = open(now_time+'.txt', 'w')
f.write(now_time)
f.close()

##파일 업로드.
FILES = ((now_time + '.txt'),)
for file_title in FILES:
    file_name = file_title
    metadata = {'name': file_name,
                'mimeType': None}
    res = google_drive.files().create(body=metadata, media_body=file_name).execute()
    if res:
        print('Uploaded "%s" (%s)' % (file_name, res['mimeType']))

##업로드 완료 파일 삭제
os.remove(now_time + '.txt')


print('hello wordl...')