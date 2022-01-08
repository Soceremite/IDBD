from django.shortcuts import render

from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Admin,AdminToken,Police,PoliceToken,User,UserToken,Userinfo,Mobile,Drink,Tired,Yawn,Blink,Smoke
from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from server.serializers import AdminSerializer,PoliceSerializer,UserSerializer,UserinfoSerializer,MobileSerializer,DrinkSerializer,TiredSerializer,YawnSerializer,BlinkSerializer,SmokeSerializer
from rest_framework import permissions
from rest_framework.decorators import action
import hashlib,time
import json
import rest_framework.status as status
import base64
import myframe 
import numpy as np
import cv2
import server.kuangshi  
from django.utils import timezone
import datetime
import pandas as pd
# 眼睛闭合判断
EYE_AR_THRESH = 0.15        # 眼睛长宽比
EYE_AR_CONSEC_FRAMES = 2    # 闪烁阈值

#嘴巴开合判断
MAR_THRESH = 0.65           # 打哈欠长宽比
MOUTH_AR_CONSEC_FRAMES = 3  # 闪烁阈值

# 定义检测变量，并初始化
COUNTER = 0                 #眨眼帧计数器
TOTAL = 0                   #眨眼总数
mCOUNTER = 0                #打哈欠帧计数器
mTOTAL = 0                  #打哈欠总数
ActionCOUNTER = 0           #分心行为计数器器

# 疲劳判断变量
# Perclos模型
# perclos = (Rolleye/Roll) + (Rollmouth/Roll)*0.2
Roll = 0                    #整个循环内的帧技术
Rolleye = 0                 #循环内闭眼帧数
Rollmouth = 0               #循环内打哈欠数
tired_start_time = timezone.now()
drink_start_time = timezone.now()
smoke_start_time = timezone.now()
mobile_start_time = timezone.now()
on_tired = False
on_drink = False
on_smoke = False
on_phone = False
userstatus = {}
#分割时间
def split_time_ranges(from_time, to_time, frequency):
    from_time, to_time = pd.to_datetime(from_time), pd.to_datetime(to_time)
    time_range = list(pd.date_range(from_time, to_time, freq='%sS' % frequency))
    if to_time not in time_range:
        time_range.append(to_time)
    time_range = [item.strftime("%Y-%m-%d %H:%M:%S") for item in time_range]
    time_ranges = []
    for item in time_range:
        f_time = item
        t_time = (datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=frequency))
        if t_time >= to_time:
            t_time = to_time.strftime("%Y-%m-%d %H:%M:%S")
            time_ranges.append([f_time, t_time])
            break
        time_ranges.append([f_time, t_time.strftime("%Y-%m-%d %H:%M:%S")])
    return time_ranges

def recorddrink(userid,start_time):
    try:
        user = User.objects.filter(id=userid).first()
        drink=Drink(user=user,start_time=start_time)
        drink.save()

    except Exception as e:
        print(e)
def recordsmoke(userid,start_time):
    try:
        user = User.objects.filter(id=userid).first()
        smoke=Smoke(user=user,start_time=start_time)
        smoke.save()

    except Exception as e:
        print(e)
def recordmobile(userid,start_time):
    try:
        user = User.objects.filter(id=userid).first()
        mobile=Mobile(user=user,start_time=start_time)
        mobile.save()

    except Exception as e:
        print(e)

def show_pic(frame,userid):
    # 全局变量
    # 在函数中引入定义的全局变量
    global EYE_AR_THRESH,EYE_AR_CONSEC_FRAMES,MAR_THRESH,MOUTH_AR_CONSEC_FRAMES,COUNTER,TOTAL,mCOUNTER,mTOTAL,ActionCOUNTER,Roll,Rolleye,Rollmouth
    global tired_start_time,drink_start_time,mobile_start_time,smoke_start_time,on_tired,on_drink,on_smoke,on_phone,userstatus
    uuid=str(userid)
    if not userstatus :
        userstatus[uuid]={}
    userstatus[uuid]["status"]="清醒"
    if frame.any():
        
        # 检测
        # 将摄像头读到的frame传入检测函数myframe.frametest()
        ret,frame = myframe.frametest(frame)  
        lab,eye,mouth = ret
        # ret和frame，为函数返回
        # ret为检测结果，ret的格式为[lab,eye,mouth],lab为yolo的识别结果包含'phone' 'smoke' 'drink',eye为眼睛的开合程度（长宽比），mouth为嘴巴的开合程度
        # frame为标注了识别结果的帧画面，画上了标识框

        # 分心行为判断
        # 分心行为检测以15帧为一个循环
        ActionCOUNTER += 1

        # 如果检测到分心行为
        # 将信息返回到前端ui，使用红色字体来体现
        # 并加ActionCOUNTER减1，以延长循环时间
        if "phone"  in lab: 
            if on_phone == False:
                print(str(userid)+'开始使用手机')
                on_phone = True;
                mobile_start_time = timezone.now()
            userstatus[uuid]["phone"]=1
            if ActionCOUNTER > 0:
                ActionCOUNTER -= 1
        else:
            userstatus[uuid]["phone"]=0
            if on_phone == True:
                print(str(userid)+'结束使用手机')
                on_phone = False;
                recordmobile(userid,mobile_start_time)
        if "smoke" in lab:
            if on_smoke == False:
                print(str(userid)+'开始抽烟')
                on_smoke = True;
                smoke_start_time = timezone.now()
            userstatus[uuid]["smoke"]=1
            if ActionCOUNTER > 0:
                ActionCOUNTER -= 1
        else:
            userstatus[uuid]["smoke"]=0
            if on_smoke == True:
                print(str(userid)+'结束抽烟')
                on_smoke = False;
                recordsmoke(userid,smoke_start_time)
        if "drink" in lab:
            if on_drink == False:
                print(str(userid)+'开始喝水')
                on_drink = True;
                drink_start_time = timezone.now()
            userstatus[uuid]["drink"]=1
            if ActionCOUNTER > 0:
                ActionCOUNTER -= 1
        else:
            userstatus[uuid]["drink"]=0
            if on_drink == True:
                print(str(userid)+'结束喝水')
                on_drink = False;
                recorddrink(userid,drink_start_time)

        # 如果超过15帧未检测到分心行为，将label修改为平时状态
        if ActionCOUNTER == 15:
            ActionCOUNTER = 0
    
        # 疲劳判断
        # 眨眼判断
        if eye < EYE_AR_THRESH:
            # 如果眼睛开合程度小于设定好的阈值
            # 则两个和眼睛相关的计数器加1
            COUNTER += 1
            Rolleye += 1
        else:
            # 如果连续2次都小于阈值，则表示进行了一次眨眼活动
            if COUNTER >= EYE_AR_CONSEC_FRAMES:  
                TOTAL += 1
                userstatus[uuid]["eye"]=TOTAL
                # 重置眼帧计数器
                COUNTER = 0

        # 哈欠判断，同上
        if mouth > MAR_THRESH: 
            mCOUNTER += 1
            Rollmouth += 1
        else:
            # 如果连续3次都小于阈值，则表示打了一次哈欠
            if mCOUNTER >= MOUTH_AR_CONSEC_FRAMES:  
                mTOTAL += 1
                userstatus[uuid]["yawn"]=mTOTAL
                # 重置嘴帧计数器
                mCOUNTER = 0
            
        # 将画面显示在前端UI上
        #show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        #window.label.setPixmap(QPixmap.fromImage(showImage))

        # 疲劳模型
        # 疲劳模型以150帧为一个循环
        # 每一帧Roll加1
        Roll += 1
        # 当检测满150帧时，计算模型得分
        if Roll == 150:
            # 计算Perclos模型得分
            perclos = (Rolleye/Roll) + (Rollmouth/Roll)*0.2
            # 在前端UI输出perclos值
            userstatus[uuid]["perclos"]=round(perclos,3)
            if perclos > 0.38:
                userstatus[uuid]["status"] = '疲劳'
                try:
                    user = User.objects.filter(id=userid).first()
                    tired=Tired(user=user,degree=str(round(perclos,3)),start_time=tired_start_time)
                    tired_start_time= timezone.now
                    tired.save()
                except Exception as e:
                    print(e)
            # 归零
            # 将三个计数器归零
            # 重新开始新一轮的检测
            Roll = 0
            Rolleye = 0
            Rollmouth = 0
    return userstatus[uuid]

# token加密处理
def token_md5(user):
    ctime = str(time.time())  # 当前时间
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))  # 加上时间戳
    return m.hexdigest()

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class UserInfoView(APIView):
    def get(self,request):
        result = {"userinfo":None}
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"result":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid:
                userinfo = Userinfo.objects.filter(user_id=uuid).first()
                if userinfo:
                    response['msg'] = '用户基本信息获取成功'
                    response['code'] = status.HTTP_200_OK
                    result["userinfo"]=UserinfoSerializer(instance=userinfo).data
                    #print(result["userinfo"])
                else:
                    print('error')  
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        response["result"] = result
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"userinfo":None}
        try:
            userid = request.data.get('userid')
            userinfo_obj = Userinfo.objects.filter(user_id = userid).first()
            userinfo = UserinfoSerializer(instance=userinfo_obj, data=request.data.get('userinfo'))
            if userinfo.is_valid():    
                userinfo.save()         
                response["userinfo"] = userinfo.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '用户信息录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)

class RegisterView(APIView):
    def post(self, request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"Token":None}
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username):
            response["code"] = status.HTTP_400_BAD_REQUEST
            response["msg"] = '该用户已经注册'
        elif username and password:
            user_data = {'username': username, 'password': make_password(password)}
            try:
                user_serializer = UserSerializer(data = user_data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    Userinfo.objects.update_or_create(user=user, defaults={})
                    response["code"] = status.HTTP_200_OK
                    response["msg"] = '注册成功'
                else:
                    response["code"] = status.HTTP_400_BAD_REQUEST
                    response["msg"] = user_serializer.errors 
            except Exception as e:
                response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response["msg"] = response["msg"].update(e)
        return JsonResponse(response)

class AdminRegisterView(APIView):
    def post(self, request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"Token":None}
        adminname = request.data.get('username')
        password = request.data.get('password')
        if Admin.objects.filter(adminname=adminname):
            response["code"] = status.HTTP_400_BAD_REQUEST
            response["msg"] = '该用户已经注册'
        elif adminname and password:
            admin_data = {'adminname': adminname, 'password': make_password(password)}
            try:
                admin_serializer = AdminSerializer(data = admin_data)
                if admin_serializer.is_valid():
                    admin = admin_serializer.save()
                    response["code"] = status.HTTP_200_OK
                    response["msg"] = '注册成功'
                else:
                    response["code"] = status.HTTP_400_BAD_REQUEST
                    response["msg"] = admin_serializer.errors 
            except Exception as e:
                response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response["msg"] = response["msg"].update(e)
        return JsonResponse(response)
class AutoLoginView(APIView):
    def post(self, request):
        accessToken={"token":None,"expiresIn":None}
        result = {"user":None,"accessToken":None}
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":"无法获取","result":None,"roles":['user']}
        try:
            photo = request.data.get('photo')
            if photo:
                data=server.kuangshi.find_biggest_face(photo)
                username = None
                print(data)
                if data and data[0]['confidence']>75:
                    username = data[0]['user_id']
                if username:
                    print("autologin:"+username)
                    user = User.objects.filter(username=username).first()
                    if user:
                        response["code"] = status.HTTP_200_OK
                        response["msg"] = '登录成功'
                        token = token_md5(username)
                        UserToken.objects.update_or_create(user=user, defaults={"token": token})
                        result["user"]=UserSerializer(instance=user).data
                        accessToken["token"] = token
                    else:
                        response["code"] = status.HTTP_400_BAD_REQUEST
                        response["msg"] = '用户不存在'
                else:
                    response["code"] = 504
                    response["msg"] = '无法识别'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        result["accessToken"]=accessToken
        response["result"] = result
        return JsonResponse(response)
class LoginView(APIView):
    def post(self, request):
        accessToken={"token":None,"expiresIn":None}
        result = {"user":None,"accessToken":None}
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"result":None,"roles":None}
        try:
            data=request.data
            username = data.get('username')
            password = data.get('password')
            
            admin = Admin.objects.filter(adminname=username).first()
            user = User.objects.filter(username=username).first()
            if admin:
                print('管理员'+username+'正在登录')
                if check_password(password, admin.password):
                    response["roles"]=['admin']
                    response["code"] = status.HTTP_200_OK
                    response["msg"] = '登录成功'
                    token = token_md5(username)
                    AdminToken.objects.update_or_create(user=admin, defaults={"token": token})
                    result["user"]=AdminSerializer(instance=admin).data
                    accessToken["token"] = token
                else:
                    response["code"] = status.HTTP_400_BAD_REQUEST
                    response["msg"] = '密码错误'
            elif user:
                print('普通用户'+username+'正在登录')
                if check_password(password, user.password):
                    response["roles"]=['user']
                    response["code"] = status.HTTP_200_OK
                    response["msg"] = '登录成功'
                    token = token_md5(username)
                    UserToken.objects.update_or_create(user=user, defaults={"token": token})
                    result["user"]=UserSerializer(instance=user).data
                    accessToken["token"] = token
                else:
                    response["code"] = status.HTTP_400_BAD_REQUEST
                    response["msg"] = '密码错误'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST
                response["msg"] = '账号不存在'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        result["accessToken"]=accessToken
        response["result"] = result
        return JsonResponse(response)
class TransportStreamView(APIView):
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":"数据错误","data":None,"result":None}
        photo = request.data.get('photo')
        userid = request.data.get('userid')
        if photo and userid:
            img_data = base64.b64decode(photo)
            nparr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            data=show_pic(image,userid)
            response["data"] = json.dumps(data)
            response["code"] = status.HTTP_200_OK
            response["msg"] = "处理成功"
        return JsonResponse(response)
class GetStatusView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"result":None,"msg":"无法获取"}
        uuid = request.query_params.get('viewUserUuid')
        if uuid:
            if userstatus and userstatus[str(uuid)]:
                response["result"]=userstatus[str(uuid)]
                response["code"] = status.HTTP_200_OK
                response["msg"] = "获取用户状态成功"
            else:
                response["msg"] = "驾驶员没有开始监测"
                response["code"] = 504
        return JsonResponse(response)
class GetIllegalDataView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"result":None,"msg":"无法获取违规数据"}
        result = {}
        piechartdata = [0,0,0,0]
        try:
            uuid = request.query_params.get('viewUserUuid')
            start_time = request.query_params.get('start_time')
            if start_time:
                st = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
            end_time = request.query_params.get('end_time')
            if end_time:
                et = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
            split = int(request.query_params.get('split'))
            if st and et and split:
                frequency=int((et-st).seconds/split)
                timelist = split_time_ranges(st,et,frequency)
            if uuid and timelist:
                #喝水数据    
                drink = Drink.objects.filter(user_id=uuid,start_time__gte=st,end_time__lte=et)
                piechartdata[0] =len(drink)
                subdrink=[0 for i in range(split)]
                for i in range(split):
                    subdrink[i] =len(drink.filter(start_time__gte=timelist[i][0],end_time__lte=timelist[i][1]))
                result["drink"]=subdrink
                #抽烟
                smoke = Smoke.objects.filter(user_id=uuid,start_time__gte=st,end_time__lte=et)
                piechartdata[1] =len(smoke)
                subsmoke=[0 for i in range(split)]
                for i in range(split):
                    subsmoke[i] =len(smoke.filter(start_time__gte=timelist[i][0],end_time__lte=timelist[i][1]))
                result["smoke"]=subsmoke
                #玩手机
                mobile = Mobile.objects.filter(user_id=uuid,start_time__gte=st,end_time__lte=et)
                piechartdata[2] =len(mobile)
                submobile=[0 for i in range(split)]
                for i in range(split):
                    submobile[i] =len(mobile.filter(start_time__gte=timelist[i][0],end_time__lte=timelist[i][1]))
                result["mobile"]=submobile
                #疲劳驾驶
                tired = Tired.objects.filter(user_id=uuid,start_time__gte=st,end_time__lte=et)
                piechartdata[3] =len(tired)
                subtired=[0 for i in range(split)]
                for i in range(split):
                    subtired[i] =len(tired.filter(start_time__gte=timelist[i][0],end_time__lte=timelist[i][1]))
                result["tired"]=subtired
                response["msg"] = "获取用违规数据成功"
                response["code"]=status.HTTP_200_OK
            unit = request.query_params.get('unit')
            if st and et and unit and split:
                axisx = ['' for i in range(split)]
                if unit == 'hour':
                    st=st+datetime.timedelta(minutes=30)
                    hour = st.hour
                    minute = str(st.minute)
                    for i in range(split):
                        axisx[i]=str(hour+i)+':'+minute
                elif unit == 'minute':
                    st=st+datetime.timedelta(minutes=5)
                    for i in range(split):
                        axisx[i]=str(st.hour)+':'+str(st.minute)
                        st=st+datetime.timedelta(minutes=10)
                elif unit == 'second':
                    frequency=(et-st).seconds/split
                    st=st+datetime.timedelta(seconds=frequency/2)
                    for i in range(split):
                        axisx[i]=str(st.hour)+':'+str(st.minute)+':'+str(st.second)
                        st=st+datetime.timedelta(seconds=frequency)
                result['axisx']=axisx
        except Exception as e:
                print(e)
        result["piechartdata"] = piechartdata
        response["result"]=result
        return JsonResponse(response)     
class LogoutView(APIView):
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"result":None}
        token = request.query_params.get('token')
        roles = request.query_params.get('roles')
        print(request)
        if token and ('user' in roles):
            print('user logout')
            try:
                usertoken = UserToken.objects.get(token=token)
                usertoken.delete()
                response["code"] = status.HTTP_200_OK
                response["msg"] = '退出成功'
            except UserToken.DoesNotExist:
                response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response["msg"] = '未曾登录'
        if token and ('admin' in roles):
            print('admin logout')
            try:
                admintoken = AdminToken.objects.get(token=token)
                admintoken.delete()
                response["code"] = status.HTTP_200_OK
                response["msg"] = '退出成功'
            except AdminToken.DoesNotExist:
                response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                response["msg"] = '未曾登录'
        return JsonResponse(response)

class UserMobileView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'无玩手机数据',"mobile":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid != None:
                #普通用户
                if int(uuid) != 0:
                    #print("uuid:"+uuid)
                    mobile = Mobile.objects.filter(user_id=uuid)
                    response['code'] = status.HTTP_200_OK
                    if mobile:
                        response['msg'] = '用户使用手机记录获取成功'
                        response["mobile"]=MobileSerializer(instance=mobile,many=True).data
                #管理员
                else:
                    mobile = Mobile.objects.filter()
                    search = request.query_params.get('search')
                    search = json.loads(search) 
                    userid = search["userid"]
                    if userid:
                        mobile = mobile.filter(user_id = userid)
                    start_time = search["start_time"]
                    if start_time:
                        mobile = mobile.filter(start_time__gte = start_time)
                    end_time = search["end_time"]
                    if end_time:
                        mobile = mobile.filter(end_time__lte = end_time)
                    if mobile:
                        response['msg'] = '管理员获取用户使用手机记录成功'
                        response["mobile"] = MobileSerializer(instance=mobile, many=True).data
                    response['code'] = status.HTTP_200_OK
        except Exception as e:
            print(e)
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"mobile":None}
        try:
            userid = request.data.get('userid')
            mobile_obj = Mobile.objects.filter(user_id = userid).first()
            mobile = MobileSerializer(instance=mobile_obj, data=request.data.get('mobile'))
            if mobile.is_valid():    
                mobile.save()         
                response["mobile"] = mobile.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '使用手机记录录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)

class UserDrinkView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'无喝水数据',"drink":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid != None:
                if int(uuid) != 0:
                    #print("uuid:"+uuid)
                    drink = Drink.objects.filter(user_id=uuid)
                    response['code'] = status.HTTP_200_OK
                    if drink:
                        response['msg'] = '用户饮用饮料记录获取成功'
                        response["drink"]=DrinkSerializer(instance=drink,many=True).data
                else:
                    drink = Drink.objects.filter()
                    search = request.query_params.get('search')
                    search = json.loads(search) 
                    userid = search["userid"]
                    if userid:
                        drink = drink.filter(user_id = userid)
                    start_time = search["start_time"]
                    if start_time:
                        drink = drink.filter(start_time__gte = start_time)
                    end_time = search["end_time"]
                    if end_time:
                        drink = drink.filter(end_time__lte = end_time)
                    if drink:
                        response['msg'] = '管理员获取用户喝水记录成功'
                        response["drink"] = DrinkSerializer(instance=drink, many=True).data
                    response['code'] = status.HTTP_200_OK
        except Exception as e:
            print(e)
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"drink":None}
        try:
            userid = request.data.get('userid')
            print(userid)
            drink_obj = Drink.objects.filter(user_id = userid).first()
            drink = DrinkSerializer(instance=drink_obj, data=request.data.get('drink'))
            print(drink)
            if drink.is_valid():    
                drink.save()         
                response["drink"] = drink.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '饮用饮料记录录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)

class UserSmokeView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'无抽烟数据',"smoke":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid != None:
                if int(uuid) != 0:
                    #print("uuid:"+uuid)
                    smoke = Smoke.objects.filter(user_id=uuid)
                    response['code'] = status.HTTP_200_OK
                    if smoke:
                        response['msg'] = '用户吸烟记录获取成功'
                        response["smoke"]=SmokeSerializer(instance=smoke,many=True).data
                else:
                    smoke = Smoke.objects.filter()
                    search = request.query_params.get('search')
                    search = json.loads(search) 
                    userid = search["userid"]
                    if userid:
                        smoke = smoke.filter(user_id = userid)
                    start_time = search["start_time"]
                    if start_time:
                        smoke = smoke.filter(start_time__gte = start_time)
                    end_time = search["end_time"]
                    if end_time:
                        smoke = smoke.filter(end_time__lte = end_time)
                    if smoke:
                        response['msg'] = '管理员获取用户抽烟记录成功'
                        response["smoke"] = SmokeSerializer(instance=smoke, many=True).data
                    response['code'] = status.HTTP_200_OK
        except Exception as e:
            print(e)
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"smoke":None}
        try:
            userid = request.data.get('userid')
            print(userid)
            smoke_obj = Smoke.objects.filter(user_id = userid).first()
            smoke = DrinkSerializer(instance=smoke_obj, data=request.data.get('smoke'))
            print(smoke)
            if smoke.is_valid():    
                smoke.save()         
                response["smoke"] = smoke.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '吸烟记录录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)

class UserTiredView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'无疲劳驾驶数据',"tired":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid != None:
                if int(uuid) != 0:
                    #print("uuid:"+uuid)
                    tired = Tired.objects.filter(user_id=uuid)
                    response['code'] = status.HTTP_200_OK
                    if tired:
                        response['msg'] = '用户疲劳驾驶记录获取成功'
                        response["tired"]=TiredSerializer(instance=tired,many=True).data
                else:
                    tired = Tired.objects.filter()
                    search = request.query_params.get('search')
                    search = json.loads(search) 
                    userid = search["userid"]
                    if userid:
                        tired = tired.filter(user_id = userid)
                    start_time = search["start_time"]
                    if start_time:
                        tired = tired.filter(start_time__gte = start_time)
                    end_time = search["end_time"]
                    if end_time:
                        tired = tired.filter(end_time__lte = end_time)
                    if tired:
                        response['msg'] = '管理员获取用户疲劳驾驶记录成功'
                        response["tired"] = TiredSerializer(instance=tired, many=True).data
                    response['code'] = status.HTTP_200_OK
        except Exception as e:
            print(e)
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"tired":None}
        try:
            userid = request.data.get('userid')
            print(userid)
            tired_obj = Tired.objects.filter(user_id = userid).first()
            tired = TiredSerializer(instance=tired_obj, data=request.data.get('tired'))
            print(tired)
            if tired.is_valid():    
                tired.save()         
                response["tired"] = tired.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '疲劳驾驶记录录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)

class UserYawnView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'无打哈欠数据',"yawn":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid != None:
                if int(uuid) != 0:
                    #print("uuid:"+uuid)
                    yawn = Yawn.objects.filter(user_id=uuid)
                    response['code'] = status.HTTP_200_OK
                    if yawn:
                        response['msg'] = '用户打哈欠记录获取成功'
                        response["yawn"]=YawnSerializer(instance=yawn,many=True).data
                else:
                    #print('error')
                    yawn = Yawn.objects.filter()
                    response['code'] = status.HTTP_200_OK
                    if yawn:
                        response['msg'] = '管理员获取用户打哈欠记录成功'
                        response["yawn"] = YawnSerializer(instance=yawn, many=True).data
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"yawn":None}
        try:
            userid = request.data.get('userid')
            print(userid)
            yawn_obj = Yawn.objects.filter(user_id = userid).first()
            yawn = YawnSerializer(instance=yawn_obj, data=request.data.get('yawn'))
            print(yawn)
            if yawn.is_valid():    
                yawn.save()         
                response["yawn"] = yawn.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '打哈欠记录录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)

class UserBlinkView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'无眨眼数据',"blink":None}
        try:
            uuid = request.query_params.get('viewUserUuid')
            if uuid!=None:
                if int(uuid)!=0:
                    #print("uuid:"+uuid)
                    blink = Blink.objects.filter(user_id=uuid)
                    response['code'] = status.HTTP_200_OK
                    if blink:
                        response['msg'] = '用户眨眼记录获取成功'
                        response["blink"]=BlinkSerializer(instance=blink,many=True).data
                else:
                    #print('error')
                    blink = Blink.objects.filter()
                    response['code'] = status.HTTP_200_OK
                    if blink:
                        response['msg'] = '管理员获取用户眨眼记录成功'
                        response["blink"] = BlinkSerializer(instance=blink, many=True).data
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
    def post(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":None,"blink":None}
        try:
            userid = request.data.get('userid')
            print(userid)
            blink_obj = Blink.objects.filter(user_id = userid).first()
            blink = BlinkSerializer(instance=blink_obj, data=request.data.get('blink'))
            print(blink)
            if blink.is_valid():    
                blink.save()         
                response["blink"] = blink.data
                response["code"] = status.HTTP_200_OK
                response["msg"] = '眨眼记录录入成功'
            else:
                response["code"] = status.HTTP_400_BAD_REQUEST    
                response["msg"] = '操作失败'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
class AdminGetUserView(APIView):
    def get(self, request):
        response = {"code": status.HTTP_400_BAD_REQUEST, "msg": '无用户数据', "User": None}
        try:
            userdata = User.objects.filter()
            response['code'] = status.HTTP_200_OK
            if userdata:
                response['msg'] = '用户数据获取成功'
                response["User"] = UserSerializer(instance=userdata, many=True).data
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
class AdminDeleteUserView(APIView):
    def get(self, request):
        uuid = request.query_params.get('userid')
        response = {"code": status.HTTP_400_BAD_REQUEST, "msg": '操作失败'}
        try:
            userdata = User.objects.filter(id=uuid).first()
            if userdata:
                userdata.delete()
                response['code'] = status.HTTP_200_OK
                response['msg'] = '用户删除成功'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
class DeleteDrinkView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'删除失败'}
        try:
            id = request.query_params.get('id')
            if id != None:
                drink = Drink.objects.filter(id=id).first()
                response['code'] = status.HTTP_200_OK
                if drink:
                    drink.delete()
                    response['msg'] = '管理员删除用户饮用饮料记录成功'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
class DeleteMobileView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'删除失败'}
        try:
            id = request.query_params.get('id')
            if id != None:
                mobile = Mobile.objects.filter(id=id).first()
                response['code'] = status.HTTP_200_OK
                if mobile:
                    mobile.delete()
                    response['msg'] = '管理员删除用户使用电话记录成功'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
class DeleteSmokeView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'删除失败'}
        try:
            id = request.query_params.get('id')
            if id != None:
                smoke = Smoke.objects.filter(id=id).first()
                response['code'] = status.HTTP_200_OK
                if smoke:
                    smoke.delete()
                    response['msg'] = '管理员删除用户抽烟记录成功'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)
class DeleteTiredView(APIView):
    def get(self,request):
        response ={"code":status.HTTP_400_BAD_REQUEST,"msg":'删除失败'}
        try:
            id = request.query_params.get('id')
            if id != None:
                tired = Tired.objects.filter(id=id).first()
                response['code'] = status.HTTP_200_OK
                if tired:
                    tired.delete()
                    response['msg'] = '管理员删除用户疲劳程度记录成功'
        except Exception as e:
            response["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response["msg"] = e
        return JsonResponse(response)