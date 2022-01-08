#--------------------利用旷视api进行人脸检测和识别---------------------
import requests
from json import JSONDecoder
import os
import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import base64 
#定义key和sercet，
key = 'rAHAWuz5Y_1Z9dTRdASwBnvqMk832eaE'
secret = 'WamUAFJ1VRThDPeHIJdOY9S27pQco0Zt'


def detect_face(filepath):#传入图片文件
    http_url ="https://api-cn.faceplusplus.com/facepp/v3/detect"
    files = {"image_file": open(filepath, "rb")}
    data = {"api_key":key, "api_secret": secret}
    response = requests.post(http_url, data=data, files=files)
    req_dict = response.json()
    print(req_dict)
    return req_dict

def detect_face2(image_base64):#传入base64
    http_url ="https://api-cn.faceplusplus.com/facepp/v3/detect"
    data = {"api_key":key, "api_secret": secret,"image_base64":image_base64}
    response = requests.post(http_url, data=data)
    req_dict = response.json()
    print(req_dict)
    return req_dict

def set_face(outer_id):#创建face_set
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
    params = {
            'api_key':key,
            'api_secret':secret,
            'outer_id':outer_id
            }
    response = requests.post(url,data = params)
    req_dict = response.json()
    print(req_dict)
    return req_dict
 
def addface(outer_id,facetokens):#将face加入到faceset
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
    params = {
            'api_key':key,
            'api_secret':secret,
            #'faceset_token':faceset,
            'outer_id':outer_id,
            'face_tokens':facetokens
            }
    r = requests.post(url,data = params)
    req_dict = r.json()
    print(req_dict)
    return req_dict


def face_search(image_file1,outer_id):#查找face库里有无对应人脸，默认返回result是最大脸结果
    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    imgfile = open(image_file1, "rb")
    print(imgfile)
    files = {"image_file":imfile }
    params = {
            'api_key':key,
            'api_secret':secret,
            #'faceset_token':faceset_token,
            'outer_id':outer_id
            }
    r = requests.post(url,files = files,data = params)
    req_dict = r.json()
    return req_dict
 
def face_search2(facetoken,outer_id):#根据facetoken来返回结果
    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    params = {
            'api_key':key,
            'api_secret':secret,
            'face_token':facetoken,
            'outer_id':outer_id
            }
    r = requests.post(url,data = params)
    req_dict = r.json()
    print("req_dict:\n"+req_dict)
    return req_dict

def face_search3(img,outer_id):#查找face库里有无对应人脸，默认返回result是最大脸结果
    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    params = {
            'api_key':key,
            'api_secret':secret,
            "image_base64": img,
            #'faceset_token':faceset_token,
            'outer_id':outer_id
            }
    r = requests.post(url,data = params)
    req_dict = r.json()
    return req_dict
 
def getfaceset():#获取faceset信息
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'
    params = {
            'api_key':key,
            'api_secret':secret,
            }
    response = requests.post(url,data = params)
    req_dict = response.json()
    print(req_dict)
    return req_dict
 
def deletefaceset(outer_id):#删除faceset
    url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/delete'
    params = {
            'api_key':key,
            'api_secret':secret,
            'outer_id':outer_id,
            'check_empty':0
            }
    response = requests.post(url,data = params)
    req_dict = response.json()
    print(req_dict)
    return req_dict
 
def face_SetUserID(face_token,user_id):#为检测出的某一个人脸添加标识信息，该信息会在Search接口结果中返回，用来确定用户身份。
    url = 'https://api-cn.faceplusplus.com/facepp/v3/face/setuserid'
    params = {
            'api_key':key,
            'api_secret':secret,
            'face_token':face_token,
            'user_id':user_id
            }
    r = requests.post(url,data = params)
    req_dict = r.json()
    print(req_dict)
    return req_dict
 
def makedataset(dataset_path='./img',outer_id='IDBD'):
    img_paths=os.listdir(dataset_path)
    user_ids=[img_path.split('.')[0] for img_path in img_paths] #解析人名
    img_paths=[os.path.join(dataset_path,img_path) for img_path in img_paths]#解析图片地址
    print(user_ids+img_paths)
    #1.创建Faceset,outerid为’IDBD‘
    set_face(outer_id)
    #2.IDBD中加入人脸token
    for (user_id,img_path) in zip(user_ids,img_paths):
        face_json = detect_face(img_path)
        face_token= face_json['faces'][0]['face_token']
        addface(outer_id,face_token)
        face_SetUserID(face_token,user_id)
 
 
def find_all_faces(img_path,outer_id='IDBD'):#找到图片里所有脸并标出
    face_json=detect_face(img_path)
    faces=face_json['faces']
    for face in faces:
        face['result']=face_search2(face['face_token'],outer_id)['results'][0]
    return faces
 
def find_biggest_face(img,outer_id='IDBD'):#找到图片里脸最大的并标出
    face_json=face_search3(img,outer_id='IDBD')
    if 'faces' in face_json:
        return face_json['results']
    else:
        return None
 
 

if __name__ == "__main__":
    #makedataset(outer_id='IDBD')
    #dataset=getfaceset()
    #deletefaceset('./img')
    #    data=find_biggest_face(img)
    #print(data[0]['result']['user_id'])
    with open('./../images/huge.jpg','rb') as f:
        base64_data =base64.b64encode(f.read())
        face_json = detect_face2(base64_data)
        face_token= face_json['faces'][0]['face_token']
        addface('IDBD',face_token)
        face_SetUserID(face_token,'huge')
        