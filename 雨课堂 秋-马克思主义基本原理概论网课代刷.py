
# Writed by 河南大学 2020 电子信息科学与技术 GTY

import time
import requests
import re
import json
import csv
# csrftoken = "QMeGCq9yl8x2luCecyamGc0aCaFFBLo8"
# sessionid = "s43c22l99fk9ayd8xduv0815coxpgzfh"
# user_id= "38783482"
# skuid = '3286440' GTY

# csrftoken = "3zjirMBRUZf0G4cGBLf46l2fny2nyLZA"
# sessionid = "om6gci2yayxow6894zo9l9kgo772v7ct"
# user_id= "38783485"
# skuid = '3286440'

csrftoken = ""  # 填自己的
sessionid = ""  # 填自己的
user_id= ""  # 填自己的
skuid = ""  # 填自己的

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid + '; university_id=2731; platform_id=3',
    'x-csrftoken': csrftoken,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id': '2731',
    'xtbz': 'ykt',
}
headers_to_course_id = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid + '; university_id=2731; platform_id=3',
    'x-csrftoken': csrftoken,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id': '2731',
    'xtbz': 'ykt',
    'classroom-id': '8234287' # 这个需要填教室id

}
leaf_type = {
    "video": 0,
    "homework": 6,
    "exam": 5,
    "recommend": 3,
    "discussion": 4
}

def Get_ALL_NeedStudy_Course():
    Course = []
    with open('Course.csv','w') as f :
        csv_writer = csv.writer(f,lineterminator='\n')
        for i in range(2):
            RequestURL = 'https://www.yuketang.cn/v2/api/web/logs/learn/8234287?actype=-1&page='+str(i)+'&offset=20&sort=-1'
            Course_res = requests.get(url=RequestURL, headers=headers_to_course_id)
            Json_Course =  json.loads(Course_res.text) #Course_res
            if (i == 0):
                for j in range(3,20):
                    Course.append([Json_Course['data']['activities'][j]['title'] , Json_Course['data']['activities'][j]['content']['leaf_id'] ])
            else:
                for j in range(1,18):
                    Course.append([Json_Course['data']['activities'][j]['title'] , Json_Course['data']['activities'][j]['content']['leaf_id'] ])

        csv_writer.writerows(Course)


def Get_state(video_id):
    RequestURL = 'https://www.yuketang.cn/video-log/get_video_watch_progress/?cid=1102785&user_id='+user_id+'&classroom_id=8234287&video_type=video&vtype=rate&video_id='+video_id+'&snapshot=1'
    try:
        state = requests.get(url=RequestURL, headers=headers)
    except:
        return -1 # ip被拉黑
    is_completed = '0'
    try:
        is_completed = re.search(r'"completed":(.+?),', state.text).group(1)
    except:
        pass
    if is_completed == '1':
        return 0 # 已经完成

    # 没有完成
    state_json = json.loads(state.text)
    return state_json

def Get_LastPoint_Len(state_json,video_id):
    return state_json['data'][video_id]['last_point'] , state_json['data'][video_id]['video_length']

def get_relevant_val(video_id): #获得cid ccid

    RequestURL = 'https://www.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/8234287/'+video_id+'/'
    try:
        relevant_val =  requests.get(url=RequestURL, headers=headers_to_course_id)
    except:
        return 0,0

    relevant_val_json = json.loads(relevant_val.text)
    try:
        cid = relevant_val_json['data']['course_id']
        ccid = relevant_val_json['data']['content_info']['media']['ccid']
    except:
        return -1,-1
    return str(cid) ,str(ccid)

def Video_Watcher(cid,ccid,video_id,video_name):
    RequestURL = 'https://www.yuketang.cn/video-log/heartbeat/'

    is_End = Get_state(video_id)
    if(is_End == 0):
        print(video_name +' 已经完成 ! 不需要再次刷取 ! 为了防止雨课堂拉黑ip地址请耐心等待5s !!! ')
        return 2 # 代表这个课已经刷过了
    elif(is_End == -1 ):
        return -1
    print(video_name  + ' 没有被学习  现在这个脚本正在帮您学习 ! ')
    if (is_End != {'message': None, 'code': 0, 'data': {}}):
        Now ,Video_len =  Get_LastPoint_Len(is_End,video_id)
    else:
        Now = 0
        Video_len = 4976.5 #随便设置一个比较大的值
    video_frame = Now
    Learn_Rate = 60
    timestap = int(round(time.time() * 1000))

    while(is_End): #只要没有完成就一直循环
        heart_data = []
        if (is_End != {'message': None, 'code': 0, 'data': {}}):
            Now, Video_len = Get_LastPoint_Len(is_End, video_id)
        else:
            Now = video_frame
            Video_len = 4976.5  # 随便设置一个比较大的值
        print(video_name +' 学习进度 ：' + str(Now * 100 / Video_len) + '% 为了防止雨课堂拉黑ip地址请耐心等待1s 1s后将继续为你刷取本视频')
        for i in range(6):
            heart_data.append(
                {
                    "c": cid, #这个是这节课的标识符 int
                    'cards_id': "",
                    'cc' :ccid , #ccid由get_ccid函数获得 str
                    'classroomid': "8234287",
                    "cp": video_frame,
                    "d": Video_len, # 设置长度
                    "et": "play", #开始
                    "fp": 0,
                    "i": 5,
                    "lob": "ykt",
                    "n": "ali-cdn.xuetangx.com",
                    "p": "web",
                    'pg': video_id + "_qpxo", #这个前面的数字是video_id
                    'skuid': int(skuid), # 这个skuid每一个学生都不一样
                    'slide': 0 ,
                    "sp": 1,
                    "sq" :2 ,
                    't': "video",
                    'tp':0,
                    "ts": str(timestap),
                    "u": int(user_id),  # 这个是你账号的标识
                    "uip": "",
                    'v': video_id,  # video_id
                    'v_url': "",
                }
            )
            video_frame += Learn_Rate
            max_time = int((time.time() + 3600) * 1000)
            timestap = min(max_time, timestap + 1000 * 15)
        data = {"heart_data": heart_data}

        requests.post(url=RequestURL, headers=headers_to_course_id, json=data)
        time.sleep(1)
        is_End = Get_state(video_id)
        if(is_End == -1):
            return -1
    print('Congratulations on finishing this ' + video_name  + ' has been completed ! Do not need to be Learned !!! ')
    return 1


'''
Get_ALL_NeedStudy_Course() 已经写入了Course到文件中
'''

if __name__ == "__main__":
    i = 0
    with open('Course.csv', 'r') as f:
        csv_data = csv.reader(f)
        for Video_name ,Video_id in csv_data :

            print(" ")
            print('正在代刷 序号: '+str(i+1)+" "+Video_name+'。。。。。。')

            cid ,ccid = get_relevant_val(Video_id)
            if(cid == 0 and ccid == 0):
                print(' ip暂时很可能被拉黑请等一段时间再使用本脚本!!! ')
                break
            elif(cid == -1 and ccid == -1 ):
                print('Get cid ccid fail 暂时跳过此 Video')
                continue

            Result = Video_Watcher(int(cid),str(ccid),Video_id,Video_name)
            if(Result == -1):
                print(' ip暂时很可能被拉黑请等一段时间再使用本脚本!!! ')
                break
            elif( Result == 2):  #该课程你之前自己刷过
                print(Video_name + '已经刷过！')
                time.sleep(3)
            else: # 没刷过
                print('该课程已经刷完 为了防止雨课堂拉黑ip地址请耐心等待3s')
                time.sleep(3)
            if(i == 7 or i == 15 or i== 20 ):
                time.sleep(8)
            i += 1

    print(' 迈阿密学院 2020 电子信息科学与技术 秋-马克思主义基本原理概论 (周三晚10-18 21-22-1) 晏传英 视频课程已经完全刷完 ！！！')