#!/usr/bin/env python3
# Fridosleigh.com CAPTEHA API - Made by Krampus Hollyfeld
import requests
import json
import sys
import base64
import io
import datetime

from imageai.Prediction.Custom import CustomImagePrediction
import os

def setup_prediction_engine():
    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath("models\\sansholidayhack-model.h5")
    prediction.setJsonPath("json\\model_class.json")
    prediction.loadModel(num_objects=6)
    return prediction

def predict_image_type(prediction, image_data):
    #  see also https://github.com/OlafenwaMoses/ImageAI/blob/4672a424cf99da7efc3b1e458c843844a53b33b2/imageai/Prediction/__init__.py#L163
    data = base64.b64decode(image_data['base64'])

    with open("temp.png", "wb") as file:
      file.write(data)
    predictions, probabilities = prediction.predictImage("temp.png", result_count=1)

    return predictions[0], probabilities[0]

def main():
    prediction = setup_prediction_engine()

    # Creating a session to handle cookies
    s = requests.Session()
    url = "https://fridosleigh.com/"
    json_resp = json.loads(s.get("{}api/capteha/request".format(url)).text)
    b64_images = json_resp['images']                    # A list of dictionaries eaching containing the keys 'base64' and 'uuid'
    challenge_image_type = json_resp['select_type'].split(',')     # The Image types the CAPTEHA Challenge is looking for.
    challenge_image_types = [challenge_image_type[0].strip(), challenge_image_type[1].strip(), challenge_image_type[2].replace(' and ','').strip()] # cleaning and formatting
    print('challenge_image_types = {}'.format(challenge_image_types))

    for image in b64_images:
      image_type, probability = predict_image_type(prediction, image)
      print('Image {} = {} ({} probability)'.format(image['uuid'], image_type, probability))


if __name__ == "__main__":
    main()
