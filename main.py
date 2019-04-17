from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime as date
import paho.mqtt.client as mqtt
import os

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('E:\MyFolder\Source\Python\PycharmProjects\External Data\google_drive_key\storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('E:\MyFolder\Source\Python\PycharmProjects\External Data\google_drive_key\client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

f = open('E:\MyFolder\Source\Python\PycharmProjects\External Data\mqtt_info\mqtt_info.txt', 'r')

broker = f.readline()
mqtt_topic = f.readline()
file_path = f.readline().strip()
f.close()

# 클라이언트가 서버에게서 CONNACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, rc):
    print ("Connected with result coe " + str(rc))
    client.subscribe("Entity/SHM/Node/353041080754218/Device/Status")

# 서버에게서 PUBLISH 메시지를 받을 때 호출되는 콜백
def on_message(client, userdata, msg):
    now_time = str(date.datetime.now())
    print("Time: ", now_time)
    print("Topic: ", msg.topic)
    mqtt_data = str(msg.payload)
    split_topic = str(msg.topic).split('/')

    now_time = date.datetime.now().strftime('%Y%m%d%H%M%S')
    now_time2 = date.datetime.now().strftime('%H%M%S')
    ##로컬에 폴더 생성
    if not (os.path.isdir(file_path + split_topic[3])):
        os.makedirs(os.path.join(file_path + split_topic[3]))
    path = file_path + split_topic[3] + '/' + now_time
    fi = open(path + ".txt", 'w')
    ##로컬에 데이터 파일 저장
    delete_text = []
    test_data2 = mqtt_data.split('status":"')
    test_data3 = test_data2[1].split('"}')
    split_test = test_data3[0].split('n')
    for i in range(0, len(split_test)-1):
        delete_text.append(split_test[i].rstrip('\\').rstrip('r').rstrip('\\'))
        fi.write(delete_text[i])
        fi.write("\n")
    fi.close()
    ##만약 해당 IMEI폴더가 없다면 생성
    if (split_topic[3] in folder_dic) == False:
        file_metadata = {'name': split_topic[3], 'mimeType': 'application/vnd.google-apps.folder', 'parents': [folder_dic[today][0]]}
        file = google_drive.files().create(body=file_metadata, fields='id, parents').execute()
        folder_dic[split_topic[3]] = [file.get('id'), file.get('parents')]
        print('make folder...\nfolder_name : ', split_topic[3] + '\nid : ', folder_dic[split_topic[3]][0] + '\nparents : ', folder_dic[split_topic[3]][1])
    ##생성된 데이터 파일을 google drive에 업로드
    FILES = ((path + '.txt'),)
    for file_title in FILES:
        file_name = file_title
        metadata = {'name': now_time2+'.txt', 'mimeType': None, 'parents': [folder_dic[split_topic[3]][0]]}
        res = google_drive.files().create(body=metadata, media_body=file_name).execute()
        if res:
            print('Uploaded "%s" (%s)' % (file_name, res['mimeType']))

google_drive = build('drive', 'v3', http=creds.authorize(Http()))
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
page_token = RSP.get('nextPageToken', None)

##google_drive에 MQTT_data 폴더가 없으면 생성 ##if google drive is haven't MQTT_data folder.make MQTT_data folder
if ('MQTT_data' in folder_dic) == False:
    file_metadata = {'name': 'MQTT_data', 'mimeType': 'application/vnd.google-apps.folder'}
    file = google_drive.files().create(body=file_metadata, fields='id, parents').execute()
    folder_dic['MQTT_data'] = [file.get('id'), file.get('parents')]
    print('make folder...\nfolder_name : MQTT_data\nid : ', folder_dic['MQTT_data'][0] + '\nparents : ', folder_dic['MQTT_data'][1])

if (today in folder_dic) == False:
    file_metadata = {'name': today, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [folder_dic['MQTT_data'][0]]}
    file = google_drive.files().create(body=file_metadata, fields='id, parents').execute()
    folder_dic[today] = [file.get('id'), file.get('parents')]
    print('make folder...\nfolder_name : ', today + '\nid : ', folder_dic[today][0] + '\nparents : ', folder_dic[today][1])


client = mqtt.Client()        # MQTT Client 오브젝트 생성
client.on_connect = on_connect     # on_connect callback 설정
client.on_message = on_message   # on_message callback 설정
client.connect(broker.strip())   # MQTT 서버에 연결

client.subscribe(mqtt_topic.strip())

client.loop_forever()