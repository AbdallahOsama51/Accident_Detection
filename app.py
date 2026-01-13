from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from detection import is_video_accident 
from notification import send_notification
from datetime import date 
import requests
import json

app = Flask(__name__)

uploaded_videos_dir = './static/uploads/'

@app.route('/')
def home_page():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        f = request.files['file']
        video = uploaded_videos_dir + secure_filename(f.filename)
        f.save(video)

        #Detect accidents 
        is_accident = is_video_accident(video)
        #Send data to backend for the statistics
        URL = '' #Here should be the URL for the create_accident backend module.
        city_id = '1'
        city_name = 'Cairo, Road 101'
        accident_date = date.today()    

        PARAMS = {'city_id': city_id, 'city_name': city_name , 'accident_date': accident_date}
        response = requests.post(url= URL, params= PARAMS)
        print(response.json())

        if is_accident:
            send_notification(city_name)
        
        return render_template('result.html')
    
if __name__ == '__main__':
    app.run(debug=True)