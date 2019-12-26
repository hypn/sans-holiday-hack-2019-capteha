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

    return predictions[0]

def main():
    prediction = setup_prediction_engine()

    yourREALemailAddress = "test@example.com"

    # Creating a session to handle cookies
    s = requests.Session()
    url = "https://fridosleigh.com/"

    json_resp = json.loads(s.get("{}api/capteha/request".format(url)).text)
    b64_images = json_resp['images']                    # A list of dictionaries eaching containing the keys 'base64' and 'uuid'
    challenge_image_type = json_resp['select_type'].split(',')     # The Image types the CAPTEHA Challenge is looking for.
    challenge_image_types = [challenge_image_type[0].strip(), challenge_image_type[1].strip(), challenge_image_type[2].replace(' and ','').strip()] # cleaning and formatting

    print('challenge_image_types = {}'.format(challenge_image_types))

    selected_images = []

    for image in b64_images:
      image_type = predict_image_type(prediction, image)

      if image_type in challenge_image_types:
        print('Image {} = {}'.format(image['uuid'], image_type))
        selected_images.append(image['uuid'])
      # else:
      #   print('Image {} = {} (no match)'.format(image['uuid'], image_type))

    final_answer = ','.join(selected_images)
    print("Final answer: {}".format(final_answer))

    json_resp = json.loads(s.post("{}api/capteha/submit".format(url), data={'answer':final_answer}).text)
    if not json_resp['request']:
        # If it fails just run again. ML might get one wrong occasionally
        print('FAILED MACHINE LEARNING GUESS')
        # print('--------------------\nOur ML Guess:\n--------------------\n{}'.format(final_answer))
        print('--------------------\nServer Response:\n--------------------\n{}'.format(json_resp['data']))
        sys.exit(1)

    print('CAPTEHA Solved!')
    # If we get to here, we are successful and can submit a bunch of entries till we win
    userinfo = {
        'name':'Krampus Hollyfeld',
        'email':yourREALemailAddress,
        'age':180,
        'about':"Cause they're so flippin yummy!",
        'favorites':'thickmints'
    }
    # If we win the once-per minute drawing, it will tell us we were emailed.
    # Should be no more than 200 times before we win. If more, somethings wrong.
    entry_response = ''
    entry_count = 1
    while yourREALemailAddress not in entry_response and entry_count < 200:
        print('Submitting lots of entries until we win the contest! Entry #{}'.format(entry_count))
        entry_response = s.post("{}api/entry".format(url), data=userinfo).text
        entry_count += 1
    print(entry_response)


if __name__ == "__main__":
    main()
