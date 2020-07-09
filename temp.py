import requests
import json

def send_fcm_notification(ids, title, body):
    url = 'https://fcm.googleapis.com/fcm/send'

    headers = {
        'Authorization': 'key=AAAA60plg9s:APA91bEOcbyXmpOJrjphK1sOBh3BGHKG5qYw2ctgthqFrY4Y4Il_RfP-54_r8cOUcXq9HnpqSJKBnhRqXkl7HbkCMejtuT3fRUX_fAUZKxKjMerr3GDlwtTCSYxvd8avqVel2ht6TfUg',
        'Content-Type': 'application/json; UTF-8',
    }

    content = {
        'to': ids,
        'notification': {
            'title': title,
            'body': body
        },
        "data": {
            "id": "id"
        }
    }

    requests.post(url, data=json.dumps(content), headers=headers)


id2 = 'cNYp75vTEkA:APA91bHg9Mfhdx3sDkGi0PwKGQBHKVVurtLrrl1zZCYBYtcIhrU1qmLSM6pQPT0tg0cIZa3Jx7A6yVaVcUKdtj-8wk-bhIVWmS7fF6_ERwNOKDzF0eHJFkZ_odFqNlbzg-grFCY3XB9V'

send_fcm_notification(id2, 'test', 'this is test')
