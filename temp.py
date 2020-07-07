import requests
import json

def send_fcm_notification(ids, title, body):
    # fcm 푸시 메세지 요청 주소
    url = 'https://fcm.googleapis.com/fcm/send'

    # 인증 정보(서버 키)를 헤더에 담아 전달
    headers = {
        'Authorization': 'key=AAAA60plg9s:APA91bEOcbyXmpOJrjphK1sOBh3BGHKG5qYw2ctgthqFrY4Y4Il_RfP-54_r8cOUcXq9HnpqSJKBnhRqXkl7HbkCMejtuT3fRUX_fAUZKxKjMerr3GDlwtTCSYxvd8avqVel2ht6TfUg',
        'Content-Type': 'application/json; UTF-8',
    }

    # 보낼 내용과 대상을 지정
    content = {
        'to': ids,
        'notification': {
            'title': title,
            'body': body
        },
        "data": {
            "id": "id"
        }
    }  # data가 아닌 notification으로 보낼 때 앱이 실행중일 때 알림 오지 않음

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    requests.post(url, data=json.dumps(content), headers=headers)


# id2 = 'cNYp75vTEkA:APA91bHg9Mfhdx3sDkGi0PwKGQBHKVVurtLrrl1zZCYBYtcIhrU1qmLSM6pQPT0tg0cIZa3Jx7A6yVaVcUKdtj-8wk-bhIVWmS7fF6_ERwNOKDzF0eHJFkZ_odFqNlbzg-grFCY3XB9V'

# send_fcm_notification(id2, 'test', 'this is test')
