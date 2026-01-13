import cv2
import numpy as np # linear algebra
import tensorflow as tf


def load_model():

    model_path = 'model'
    loaded_model = tf.keras.models.load_model(model_path)
    return loaded_model

def process_frame(frame):

    resized_frame = tf.keras.preprocessing.image.smart_resize(frame, (48, 48), interpolation='bilinear')
    resized_gray_frame = np.dot(resized_frame[..., :3], [0.299, 0.587, 0.114])
    image_array = tf.keras.utils.img_to_array(resized_gray_frame)
    image_batch = np.expand_dims(image_array, axis=0)
    return image_batch

def predict_frame(model, frame):

    processed_frame = process_frame(frame)
    full_prediction = (model.predict(processed_frame) > 0.5).astype('int32')
    return full_prediction

def is_frame_accident(model, frame):

    prediction = predict_frame(model, frame)
    if prediction[0][0] == 1: 
        return "Accident detected"
    else:
        return "Not accident"
    
def predict_every_video_frame(model, video_path):

    frames=[]
    labels=[]
    video = cv2.VideoCapture(video_path)
    video_frames_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for x in range(video_frames_count):
        if x%30 == 0:
            print(x)
            _, frame = video.read()
            frames.append(frame)
            labels.append(is_frame_accident(model, frame)) 
    
    video.release()
    video_preds = [labels, frames]

    return video_preds

def is_video_accident(video_path):

    model = load_model()
    labels = predict_every_video_frame(model, video_path)[0] 
    print(labels)
    for label in labels:
        if label == 'Accident detected':
            return True
    return False

