import requests
import json

def send_notification(city_name):
    server_token = '' 
    device_token = ''

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + server_token
    }

    body = {
        'notification': {
            'title': 'ALERT',
            'body': 'Accident at' + city_name
        },
        
        'to': device_token,
        'priority': 'high'
    }

    #Sending a post request to firebase
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers= headers, data= json.dumps(body))
    if response.status_code == 200:
        return True
    return False