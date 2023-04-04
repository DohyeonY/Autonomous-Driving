#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os, sys
import rospy
import rospkg
import tf
from math import cos,sin,pi,sqrt,pow,atan2
import numpy as np
from geometry_msgs.msg import Point32,PoseStamped
from nav_msgs.msg import Odometry,Path
from morai_msgs.msg import ObjectStatus, ObjectStatusList, EgoVehicleStatus

# lane_change 는 차량의 차선변경 예제입니다.
# 차량 경로상의 장애물을 탐색하여 경로 상에 장애물이 있다면 차선 변경으로 회피 기동을 합니다.
# lane_change_1 예제와 차이점은 차선 변경 시 단순히 목표 차선을 바꾸는 것이 아닌
# 시작차선과 목표 차선 사이 경로를 그려 자연스러운 차선변경이 가능 하도록 경로를 만듭니다.
# 해당 예제에서는 차선 변경 시작 점과 끝점 사이를 3차곡선 으로 연결하여 차량이 주행 할 경로를 만듭니다.

# 노드 실행 순서 
# 0. 필수 학습 지식
# 1. subscriber, publisher 선언
# 2. 두개의 차선 경로 의 텍스트파일을 읽기 모드로 열기
# 3. 읽어 온 경로 데이터를 Global Path 변수에 넣기
# 4. 주행 경로상의 장애물 유무 확인
# 5. 장애물이 있다면 주행 경로를 변경 하도록 로직 작성.
# 6. 좌표 변환 행렬 생성
# 7. 3차 곡선을 이용한 주행 경로 생성
# 8. ros path 메시지 형식 경로 데이터 생성
# 9. 경로 데이터 Publish

#TODO: (0) 필수 학습 지식
'''
# 고도화된 차선변경 알고리즘을 만들기 위해서는 여러 상황을 고려해야합니다.
# 주행중인 차선의 전 후방 차량, 차선 변경 목표 차선의 전 후방 차량 고려 중인 차량의 속도와 가속도 진행 방향 등 많은 요소를 고려합니다.
# 이번 예제에서는 고도화 된 차선 변경 알고리즘이 아닌 장애물의 위치를 탐색하여 주행 경로 상 장애물이 있으면
# 충돌을 회피하기 위한 판단과 차선 변경 경로 생성 방법에 관한 예제 입니다.
'''
class lc_path_pub :
    def __init__(self):
        rospy.init_node('lc_path_pub', anonymous=True)

        '''
        #TODO: ros Launch File <arg> Tag 
        # ros launch 파일 에는 여러 태그 를 사용 할 수 있지만 
        # 그중 <arg> 태그를 사용하여 변수를 정의 할 수 있습니다.
        # 3 장 에서는 사용하는 Path 정보와 Object 각 예제 별로 다르기 때문에
        # launch 파일의 <arg> 태그를 사용하여 예제에 맞게 변수를 설정합니다.

        '''
        arg = rospy.myargv(argv=sys.argv)
        object_topic_name = arg[1]

        rospy.Subscriber(object_topic_name, ObjectStatusList, self.object_info_callback)

        #TODO: (1) subscriber, publisher 선언
        '''
        # Gloabl Path 와 Odometry, Object 데이터를 수신 할 Subscriber 를 만들고 
        # lane_change_path 를 전송 할 publisher 변수를 만든다.
        # lane_change_path 는 차선변경 예제에서 활용할 지역경로(Loacl Path)이다.
        # lane_change_path 의 Topic 이름은 '/lane_change_path' 이고
        # ROS 메시지 형식은 Path 이다.
        rospy.Subscriber( "odom" )
        self.global_path_pub = 
        self.local_path_pub = 

        '''
        rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.global_path_pub = rospy.Publisher("/global_path", Path, queue_size=2)
        self.local_path_pub = rospy.Publisher("/lane_change_path", Path, queue_size=2)        


        self.lc_1=Path()
        self.lc_1.header.frame_id='/map'
        self.lc_2=Path()
        self.lc_2.header.frame_id='/map'

        #TODO: (2) 두개의 차선 경로 의 텍스트파일을 읽기 모드로 열기
        rospack=rospkg.RosPack()
        pkg_path=rospack.get_path('ssafy_3')

        lc_1 = pkg_path + '/path' + '/lc_1.txt'
        self.f=open(lc_1,'r')
        lines = self.f.readlines()
        for line in lines :
            tmp = line.split()
            read_pose = PoseStamped()
            read_pose.pose.position.x = float(tmp[0])
            read_pose.pose.position.y = float(tmp[1])
            read_pose.pose.orientation.w = 1
            self.lc_1.poses.append(read_pose)
        self.f.close()

        lc_2 = pkg_path + '/path' + '/lc_2.txt'
        self.f=open(lc_2,'r')
        lines = self.f.readlines()
        for line in lines :
            tmp = line.split()
            read_pose = PoseStamped()
            read_pose.pose.position.x = float(tmp[0])
            read_pose.pose.position.y = float(tmp[1])
            read_pose.pose.orientation.w = 1
            self.lc_2.poses.append(read_pose)
        self.f.close()

        self.is_object_info = False
        self.is_odom = False

        self.local_path_size = 50
        
        self.lane_change = False        
        self.current_lane = 1

        #TODO: (3) 읽어 온 경로 데이터를 Global Path 로 지정

        # 읽어 온 Path 데이터 중 Ego 차량의 시작 경로를 지정합니다.
        global_path = self.lc_1

        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            if self.is_object_info == True and self.is_odom == True:

                result = self.calc_vaild_obj([self.x,self.y,self.vehicle_yaw],self.object_data)                
                global_npc_info = result[0] 
                local_npc_info = result[1] 

                self.local_path_make(global_path)

                currnet_waypoint = self.get_current_waypoint(self.x,self.y,global_path)

                global_path = self.lc_planning(global_npc_info,local_npc_info,currnet_waypoint,global_path)

                #TODO: (9) 경로 데이터 Publish

                # 경로 데이터 메세지 를 전송하는 publisher 를 만든다.
                self.local_path_pub.publish(self.local_path_msg)
                self.global_path_pub.publish(global_path)

            rate.sleep()

    def odom_callback(self,msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        odom_quaternion=(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)

        _,_,self.vehicle_yaw=tf.transformations.euler_from_quaternion(odom_quaternion)

        self.is_odom = True

    def object_info_callback(self,data): ## Object information Subscriber
        self.is_object_info = True
        self.object_data = data 
    
    def get_current_waypoint(self,x,y,global_path):
        min_dist = float('inf')        
        currnet_waypoint = -1
        for i,pose in enumerate(global_path.poses):
            dx = x - pose.pose.position.x
            dy = y - pose.pose.position.y

            dist = sqrt(pow(dx,2) + pow(dy,2))
            if min_dist > dist :
                min_dist = dist
                currnet_waypoint = i
        return currnet_waypoint
    
    def local_path_make(self,global_path):                
        self.local_path_msg=Path()
        self.local_path_msg.header.frame_id='/map'
        
        x = self.x
        y = self.y
        min_dis=float('inf')
        current_waypoint=-1
        for i,waypoint in enumerate(global_path.poses) :
            distance=sqrt(pow(x-waypoint.pose.position.x,2)+pow(y-waypoint.pose.position.y,2))
            if distance < min_dis :
                min_dis=distance
                current_waypoint=i
        
        if current_waypoint != -1 :
            if current_waypoint + self.local_path_size < len(global_path.poses):
                for num in range(current_waypoint,current_waypoint + self.local_path_size ) :
                    tmp_pose=PoseStamped()
                    tmp_pose.pose.position.x=global_path.poses[num].pose.position.x
                    tmp_pose.pose.position.y=global_path.poses[num].pose.position.y
                    tmp_pose.pose.orientation.w=1
                    self.local_path_msg.poses.append(tmp_pose)                    
            else :
                for num in range(current_waypoint,len(global_path.poses) ) :
                    tmp_pose=PoseStamped()
                    tmp_pose.pose.position.x=global_path.poses[num].pose.position.x
                    tmp_pose.pose.position.y=global_path.poses[num].pose.position.y
                    tmp_pose.pose.orientation.w=1
                    self.local_path_msg.poses.append(tmp_pose)

    def calc_vaild_obj(self,status_msg,object_data):
        
        self.all_object = object_data        
        ego_pose_x = status_msg[0]
        ego_pose_y = status_msg[1]
        ego_heading = status_msg[2]
        
        global_npc_info = []
        local_npc_info  = []

        num_of_object = self.all_object.num_of_npcs        
        if num_of_object > 0:

            #translation
            tmp_theta=ego_heading
            tmp_translation=[ego_pose_x, ego_pose_y]
            tmp_t=np.array([[cos(tmp_theta), -sin(tmp_theta), tmp_translation[0]],
                            [sin(tmp_theta),  cos(tmp_theta), tmp_translation[1]],
                            [0             ,               0,                  1]])
            tmp_det_t=np.array([[tmp_t[0][0], tmp_t[1][0], -(tmp_t[0][0] * tmp_translation[0] + tmp_t[1][0]*tmp_translation[1])],
                                [tmp_t[0][1], tmp_t[1][1], -(tmp_t[0][1] * tmp_translation[0] + tmp_t[1][1]*tmp_translation[1])],
                                [0,0,1]])
            
            #npc vehicle ranslation        
            for npc_list in self.all_object.npc_list:
                global_result=np.array([[npc_list.position.x],[npc_list.position.y],[1]])
                local_result=tmp_det_t.dot(global_result)
                if local_result[0][0]> 0 :        
                    global_npc_info.append([npc_list.type,npc_list.position.x,npc_list.position.y,npc_list.velocity.x])
                    local_npc_info.append([npc_list.type,local_result[0][0],local_result[1][0],npc_list.velocity.x])    

        return global_npc_info, local_npc_info

    def lc_planning(self,global_obj,local_obj,currnet_waypoint,global_path):
        #TODO: (5) 장애물이 있다면 주행 경로를 변경 하도록 로직 작성

        # 전방에 장애물이 있다면 차선 변경을 시작하는 로직을 작성합니다.
        # 차선 변경을 시작하면 차선 변경을 위한 경로를 생성합니다.
        # 차선 변경을 위한 경로를 주행 중 경로 끝에 도달하면 차선 변경을 한 차선으로 경로를 변경합니다. 
        # 차선변경을 시작하면 경로 상 장애물은 체크 하지 않도록 합니다.

        lane_change_distance = 30 * 2 # (point-to-point distance 0.5m)

        if self.lane_change == True:
            if currnet_waypoint + self.local_path_size > len(global_path.poses):
                self.lane_change = False
                if self.current_lane == 1:
                    global_path = self.lc_1
                elif self.current_lane == 2:
                    global_path = self.lc_2
        else:
            self.check_object(self.local_path_msg,global_obj,local_obj)
        
        if self.object[0] == True:
            if self.current_lane != 1:
                self.current_lane = 1
                start_point         = self.lc_2.poses[currnet_waypoint]  
                end_waypoint_idx = self.get_current_waypoint(self.lc_1.poses[currnet_waypoint+lane_change_distance].pose.position.x,self.lc_1.poses[currnet_waypoint+lane_change_distance].pose.position.y,self.lc_1)
                end_point           = self.lc_1.poses[end_waypoint_idx]
                start_next_point    = self.lc_2.poses[currnet_waypoint+5]  
                global_path = self.getLaneChangePath(self.lc_2,self.lc_1,start_point,end_point,start_next_point, end_waypoint_idx)
                self.lane_change = True
                self.object=[False,0]
            else:
                self.current_lane = 2
                start_point         = self.lc_1.poses[currnet_waypoint]  
                end_waypoint_idx = self.get_current_waypoint(self.lc_2.poses[currnet_waypoint+lane_change_distance].pose.position.x,self.lc_2.poses[currnet_waypoint+lane_change_distance].pose.position.y,self.lc_2)
                end_point           = self.lc_2.poses[end_waypoint_idx]
                start_next_point    = self.lc_1.poses[currnet_waypoint+5]  
                global_path = self.getLaneChangePath(self.lc_1,self.lc_2,start_point,end_point,start_next_point, end_waypoint_idx)
                self.lane_change = True
                self.object=[False,0]

        return global_path

    def check_object(self,ref_path,global_vaild_object,local_vaild_object):
        #TODO: (4) 주행 경로상의 장애물 유무 확인
        self.object=[False,0]
        '''
        # 주행 경로 상의 장애물의 유무를 파악합니다.
        # 장애물이 한개 이상 있다면 self.object 변수의 첫번째 값을 True 로 둡니다.
        # 장애물의 대한 정보는 List 형식으로 self.object 변수의 두번째 값으로 둡니다.
        # 장애물의 유무 판단은 주행 할 경로에서 얼마나 떨어져 있는지를 보고 판단 합니다.
        # 아래 예제는 주행 경로에서 Object 까지의 거리를 파악하여 
        # 경로를 기준으로 2.5 m 안쪽에 있다면 주행 경로 내 장애물이 있다고 판단 합니다.
        # 주행 경로 상 장애물이 여러게 있는 경우 가장 가까이 있는 장애물 정보를 가지도록 합니다.

        if len(global_vaild_object) >0  :
            min_rel_distance = float('inf')
            for i in range(len(global_vaild_object)):
                for path in ref_path.poses :   
                    if global_vaild_object[i][0]==1 or global_vaild_object[i][0]==2 :  
                        dis = 
                        if dis<2.5:
                            rel_distance=                         
                            if rel_distance < min_rel_distance:
                                min_rel_distance = 
                                self.object=[True,i]
        '''
        if len(global_vaild_object) > 0  :
            min_rel_distance = float('inf')
            for i in range(len(global_vaild_object)):
                for path in ref_path.poses :   
                    if global_vaild_object[i][0]==1 or global_vaild_object[i][0]==2 :  
                        dis = sqrt((path.pose.position.x - global_vaild_object[i][1])**2 + (path.pose.position.y - global_vaild_object[i][2])**2)
                        if dis < 2.5:
                            rel_distance = sqrt((local_vaild_object[i][1])**2 + (local_vaild_object[i][2])**2)
                            if rel_distance < min_rel_distance:
                                min_rel_distance = rel_distance
                                self.object=[True,i]

    def getLaneChangePath(self,ego_path,lc_path,start_point,end_point,start_next_point, end_waypoint_idx): ## 
        out_path=Path()  
        out_path.header.frame_id='/map'

        # 지역 좌표계로 변환
        #TODO: (6) 좌표 변환 행렬 생성
        '''
        # 좌표 변환 행렬을 만듭니다.
        # 차선 변경 경로를 만들기 위해서 차선변경을 시작하는 Point 좌표에서 
        # 차선 변경이 끝나는 Point 좌표의 상대 위치를 계산해야 합니다.
        # 계산 된 차선변경 종료 지점과 시작 지점을 연결 하기 위한 좌표 변환 행렬을 작성합니다.

        translation = [start_point.pose.position.x, start_point.pose.position.y]
        theta       = atan2(start_next_point.pose.position.y-start_point.pose.position.y,start_next_point.pose.position.x-start_point.pose.position.x)

        trans_matrix = np.array([   [           ,              ,               ],
                                    [           ,              ,               ],
                                    [          0,             0,              1] ])

        det_trans_matrix = np.linalg.inv(trans_matrix)

        '''
        translation = [start_point.pose.position.x, start_point.pose.position.y]
        theta       = atan2(start_next_point.pose.position.y-start_point.pose.position.y,start_next_point.pose.position.x-start_point.pose.position.x)

        trans_matrix = np.array([   [cos(theta), -sin(theta), translation[0]], 
                                    [sin(theta),  cos(theta), translation[1]], 
                                    [         0,           0,             1 ]])

        det_trans_matrix = np.linalg.inv(trans_matrix)

        world_end_point=np.array([[end_point.pose.position.x],[end_point.pose.position.y],[1]])
        local_end_point=det_trans_matrix.dot(world_end_point)

        waypoints_x = []
        waypoints_y = []
        x_interval = 0.5 # 생성할 Path 의 Point 간격을 0.5 로 한다.
        x_start = 0
        x_end = local_end_point[0][0]

        y_start = 0.0
        y_end = local_end_point[1][0]

        x_num = x_end / x_interval
        # End Point 까지의 길이를 Point 간 간격으로 나눠 필요한 Point 의 수를 계산한다.
        # 계산된 Point 의 숫자 만큼 X 좌표를 생성한다.
        for i in range(x_start,int(x_num)) : 
            waypoints_x.append(i*x_interval)

        #TODO: (7) 3차 곡선을 이용한 주행 경로 생성
        # 3 차 방정식을 이용하여 부드러운 차량 거동을 위한 차선변경 경로를 만듭니다.
        # 시작 위치와 목표 위치 사이 부드러운 곡선 경로를 주행하도록 합니다.
        # 차량이 차선 변경 시 알맞을 조향 각도를 조절하여 차선을 변경합니다.
        # 이때 큰 조향각을 가진다면 차량의 횡방향 가속도가 커지고 거동의 안정성이 떨어집니다.
        # 차량이 안정적으로 주행 할 수 있는 경로를 만들어 주는 예제입니다.
        # 
        # 차량이 안정적으로 주행 할 수 있는 경로를 만들기 위해 3차 방정식을 이용합니다.
        # EX )  3차 방정식
        #       
        #       f(x) = a*x^3 + b*x^2 + c*x + d
        # 
        # 위에 예시로 작성한 3차 방정식을 아래 예제에 작성 한다.

        d = 0
        c = 0
        b = 3 * (y_end - y_start) / x_end**2
        a = -2 * (y_end - y_start) / x_end**3

        for x in waypoints_x:
            # 3 차 방정식 수식을 작성한다. (f(x) = a*x^3 + b*x^2 + c*x + d)
            result = a*x**3 + b*x**2 + c*x + d
            waypoints_y.append(result)

        #TODO: (8) ros path 메시지 형식 경로 데이터 생성
        # out_path 변수에 정의한 ros path 데이터 형식에 맞춰 경로 데이터를 만든다.
        # Local Result 는 차선 변경 시작 위치 기준 좌표의 Point 정보이고
        # Global Result 는 map 기준 좌표의 Point 좌표 이다.
        # 좌표 변환 행렬을 통해 Local Result 를 이용해 Global Result 를 계산한다.
        # Global Result 는 차선 변경 Path 의 데이터가 된다.

        for i in range(0,len(waypoints_y)) :
            local_result = np.array([[waypoints_x[i]],[waypoints_y[i]],[1]])
            global_result = trans_matrix.dot(local_result)

            read_pose=PoseStamped()
            read_pose.pose.position.x = global_result[0][0]
            read_pose.pose.position.y = global_result[1][0]
            read_pose.pose.position.z = 0.
            read_pose.pose.orientation.x = 0
            read_pose.pose.orientation.y = 0
            read_pose.pose.orientation.z = 0
            read_pose.pose.orientation.w = 1
            
            out_path.poses.append(read_pose)
        
        # 직선 거리 추가
        # 차선 변경 직 후 바로 목표 차선으로의 경로 변경이 아닌 안전정인 주행을 위해서 
        # 변경 이후 직선 경로를 일부 추가해 준다.

        for k in range(end_waypoint_idx,end_waypoint_idx+40):
            read_pose=PoseStamped()
            read_pose.pose.position.x = lc_path.poses[k].pose.position.x
            read_pose.pose.position.y = lc_path.poses[k].pose.position.y
            read_pose.pose.position.z = 0
            read_pose.pose.orientation.x = 0
            read_pose.pose.orientation.y = 0
            read_pose.pose.orientation.z = 0
            read_pose.pose.orientation.w = 1
            out_path.poses.append(read_pose)

        return out_path

if __name__ == '__main__':
    try:
        test_track=lc_path_pub()
    except rospy.ROSInterruptException:
        pass
