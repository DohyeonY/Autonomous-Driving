# SUBPJT2

# 필수 지식 학습

## 1. 좌표계

- 공간상에서 물체 위치를 표현하는 체계
- 목적에 따라 물체의 위치와 자세를 여러 좌표로 표현
- 직교좌표계, 원통좌표계, 구면좌표계 등
- 하나의 좌표계만을 사용하지 않는 경우도 있음
    - 다절링크의 경우 물체 운동을 기술하거나 계산할 때 월드좌표계와 로컬좌표계를 모두 이용할 수 있음
    - 기준좌표에 따라 차량이 같은 자리, 같은 자세로 있다 하더라도 표현이 다르게 될 수 있음

### 직교좌표계

- 가장 익숙하고 흔히 쓰는 방법
- 3개의 축 x, y, z 가 서로 직각을 이루고 3개 축이 3차원을 표현하는 좌표계
- IMU 가 직교좌표계를 대표적으로 사용함

### 원통좌표계

- 극좌표계 : 물체 위치를 반지름과 각도로 표현
    - 반지름 : 물체와의 거리
    - 각도 : 기준각도와 이루는 각
    - 반지름 값이 음값이라면 각도가 가리키는 방향과 반대방향으로 절대값만큼 떨어진 위치를 말함
- 원통좌표계 : 극좌표계에 3차원 공간을 표현하기 위해 평면 극좌표계에 평면에서부터 높이값을 더해 만들어진 좌표계
- 라이다가 원통좌표계를 사용함

### 구면좌표계

- 3차원 공간의 위치를 나타내는 좌표계
- 물체의 위치 : 원점에서 물체와의 반지름, x축과 이루는 각도, z축과 이루는 각도로 표현
- x축과 이루는 각도를 경도, z축과 이루는 각도를 위도로 표현하기도 함
- GPS 센서가 구면좌표계를 사용함

![제목 없음.png](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/%25EC%25A0%259C%25EB%25AA%25A9_%25EC%2597%2586%25EC%259D%258C.png)

## 2. GPS 좌표계

### WGS84 좌표계

- WGS84 : 위도 경도 좌표로 받아와지는 GPS 데이터
- WGS (world geodetic system) : 세계 지구 좌표 시스템
- 지구의 중심(타원체 중심)을 원점으로 하고 지구 회전 축이 z축과 평행한 좌표계
- 위도의 경우 적도(0도) 기준으로 남북을 나눔
- 경도의 경우 영국 그리니치 천문대를 기준으로 동서로 구분
- 자율주행에서 사용될 2D 좌표계 기준 경로 계획 문제를 해결할 수 없으므로, GPS 위도, 경도를 평면 좌표계로 변환하여 사용해야 함

→ TM 좌표계 사용

### TM 좌표계

- 횡축 메르카토르 도법으로 구성됨
- 기준 평면, 원점, 타원체 모델에 따라 다르게 Projection 됨
- TM 중부 좌표계 : 원점이 한반도 어딘가, UTM 52 는 원점이 적도 어딘가
- 한반도의 경우 UTM 좌표 상 52번째 zone 에 위치하므로 UTM 52 좌표를 사용해야 함

## 3. 물체의 자세

- 좌표계에서 물체가 얼마나 회전되어 있는지로 표현
- 같은 위치라도 다른 자세를 취할 수 있음
- 오일러각과 쿼터니언으로 표현

### 오일러 각

- 물체 자세를 3축의 회전 Roll Pitch Yaw 3가지로 표현 가능
- 직관적이지만 몇몇 자세를 표현하지 못하는 짐벌락 현상이 존재

### 짐벌락

- 두 회전축이 겹치는 현상으로 회전축이 겹치게 되면 돌릴 수 있는 축 하나가 사라지므로 문제가 생김

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled.png)

### 쿼터니언 각

- x(벡터), y(벡터), z(벡터), w(스칼라) 변수로 표현
- 각 축을 한꺼번에 계산하지 않아 짐벌락 피할 수 있음
- 어떤 회전각도 계산 가능, 빠른 연산 처리
- 직관적으로 이해하기 어려움
- 보통 IMU 센서에서 얻은 각속도 데이터로 물체 자세를 추정
    - 이 때 쿼터니언에서 오일러 각을 변환하거나 오일러에서 쿼터니언으로 변환하는 식을 사용해야
    - ROS 의 TF 패키지 : 어려운 수식 없이 손쉽게 변환 가능

## 4. 정밀도로 지도

- 자율주행 등에 필요한 정보를 3차원으로 제작한 전자지도
- 크게 차선, 도로시설, 표지시설 3가지 범주로 구성
- 해상도 : 0.25m 급
- 국토지리정보원 제작 및 배포
- m 단위 오차가 발생하면 사고 유발 가능성 높음
- 도로폭 : 2.5~3.5m 정도
    - 3m 도로에서 1.8m 차폭인 중형세단이 주행중일 경우 여유 공간은 양쪽이 0.6m
    - 만약 m 단위의 오차 발생 시 차량은 다른 차선을 넘을 수 있고, 근접해 있는 차선에서 주행중인 차량과 추돌할 조건이 됨

### 고정밀도로 지도 필요성 및 중요성

- 센서가 갖는 기술적 한계를 보완하여 신뢰성 있게 자율주행차를 구동시키는데 정밀한 위치 정보를 가지고 차량에 미리 입력되어 있는 지도 정보가 필수적
- 라이다의 최대 인식거리 : 250m
    - 고속으로 달리는 차량이 250m 앞의 표지판을 제대로 인식하지 못할 경우 피할 시간은 몇 초에 불과
    - 인지센서와 함께 정밀도로지도를 매칭하여 도로와 주변상황 식별 시 사고 예방 가능
- 안전이 무엇보다 최우선시 되는 자율주행에서 정밀도로 지도는 필수 불가결
    - 센서로 인식한 정보를 도로정보와 비교
    - 센서로 감지못하는 도로정보로 대체하여 사용
    - 다양한 센서로 도로 상 많은 데이터를 처리하는데, 이 양이 방대하므로 미리 정밀지도로 파악하는 용도로 사용

### 차선

- 규제선
- 도로경계선
- 정지선
- 차로중심선

### 도로시설

- 중앙분리대
- 터널
- 교량
- 지하차도

### 표지시설

- 교통안전표지
- 노면표시
- 신호기

## 5. MGeo

- MORAI + Geometry data
- 시뮬레이터에서 사용되는 정밀지도 포맷
- 실제와 동일한 표면도로, 표지판, 신호등 등 생성에 사용
- 차량 주행용 경로에 사용
- 다양한 곳에서 다양한 포맷으로 사용
- 실제 HDMap 을 표현한다는 점은 항상 공통

### 형상 표현 클래스

- BasePoint : 한 개의 점으로 표현
- BaseLine : 여러 개 점이 모인 Line
- BasePlane : 여러 개 점이 모여 시작점과 끝을 연결

### 주행 경로 표현 데이터

- Node : 서로 다른 두 개 이상 Link 간 연결 여부
- Line : 단방향, 연결성 표현선 → Line 전후 Node 찾음
- Link : 차량 주행 경로 → 좌우 Link 검색, 차선 변경 가능 링크인지 표현

### 노드 정보 - 필드

- idx : 노드 이름
- to_links : 노드에서 나가는 링크 리스트
- from_links : 노드로 들어오는 링크 리스트
- on_stop_line : 정지선 여부(true or false)

### 노드 정보 - 메소드

- get_to_links() : 노드에서 나가는 링크 리스트 리턴
- get_from_links() : 노드로 들어오는 링크 리스트 리턴
- get_to_links_idx_list() : 나가는 링크 아이디 리스트 리턴
- get_from_nodes() : 이전 연결된 노드 리스트 리턴
- get_to_nodes() : 다음 연결될 노드 리스트 리턴
- print_all_related_nodes_and_links() : 연결된 노드, 링크 모두 출력

### 링크 정보 - 필드

- idx : 링크 이름
- from_node : 링크 시작 노드
- to_node : 링크 끝 노드
- lazy_point_init : 차선 변경 링크 여부
- lane_change_pair_list : 차선 변경 링크 리스트
- max_speed_kph : 링크에서 주행가능한 최대 속도
- min_speed_kph : 링크에서 주행가능한 최저 속도
- traffic_signs : 신호등 연결된 신호등
- traffic_lights : 받아야하는 신호등 신호

### 링크 정보 - 메소드

- get_to_node() : 링크 끝 노드 리턴
- get_from_node() : 링크 시작 노드 리턴
- get_to_links() : 나가는 링크 리스트 리턴
- get_from_links() : 들어오는 링크 리스트 리턴
- is_it_for_lane_change() : 차선변경 링크인지 리턴(True or False)
- get_lane_change_pair_list() : 차선변경할 수 있는 링크 리스트 리턴
- get_number_of_lane_change() : 차선변경할 수 있는 링크 갯수 리턴

## 6. 경로계획

- 차량이 주행할 경로를 만들어주는 과정
- 안전한지, 최적화된 경로인지 고려
- 전역경로 계획과 지역경로 계획으로 나눠짐

### 전역경로 계획

- 출발지(현재지점)에서 목적지를 직으면 전체적인 경로가 만들어지는데 이것을 전역경로 계획이라고 함

### 지역경로 계획

- 주행 도중 실수로 다른 길을 들어가면 새로운 경로를 찾음
- 지역경로 계획 : 전체경로에서 일부분을 수정해서 주행하는 것

## 7. Dijkstra

- 그래프에서 노드 간 최단 경로를 찾는 알고리즘
- 시작 노트부터 다른 모든 노드까지의 최단 경로를 찾는 알고리즘으로 사용됨
- 맵퀘스트(Mapquest) 나 구글맵스(Google Maps)같은 웹 서비스에 사용됨
- 인공위성 GPS 등의 소프트웨어에 사용됨

### Dijkstra 알고리즘 동작 과정

1. 시작 노드 지정
2. 시작 노드를 기준으로 다른 노드와의 비용을 저장
3. 방문하지 않은 노드 중 거리비용이 가장 적은 노드부터 방문
4. 방문한 노으와 인접한 노드들을 조사해서 새로 조사된 최단 거리가 발견된 최단 거리보다 작으면 정보 갱신
    - 새로 조사된 최단 거리 : 시작 노드에서 방문 노드까지 거리 비용 + 방문노드에서 인접 노드까지 거리 비용
    - 기존에 발견된 최단 거리 : 시작 노드에서부터 인접 노드까지의 거리비용
5. 3~4번 반복

## 8. Pure pursuit

- 경로 위 한 점을 원 호를 그리며 따라가는 방법
- 자동차 기구학과 전방주시거리(Look-Ahead-Distance) 라는 하나의 파라미터만 가지고 조향각 간단히 계산 가능

→ 자율차 경로 추종에 사용하는 대표적인 알고리즘 중 하나

- 실제 자동차 모델(Ackermann geometry) 을 단순화한 Bicycle 모델 사용
    - 뒷바퀴 1개와 조향 가능한 앞바퀴 1개로 이루어짐
    - 명세서2 Figure 16, 17, 18 참고

### Bicycle 모델

- 경로, 차량의 위치, 축거, 전방주시거리(l_d) 가 주어지면 조향각(델타)를 구할 수 있음
- 전방주시거리는 현재 차량 속도에 따라 변해야 함
    - 속도가 빠르면 멀리보고 운전하고, 느리면 가까이보고 운전하는 것과 같음
    - 적절한 l_d 를 찾아 Overshoot(목표점을 넘어가는 것)은 줄이고, Saturation Time(목표 도달 시간), Lateral Error(경로 중 차량과 가장 가까운 경로점과 차량과의 직선 거리)를 줄여야 함

## 9. PID

- PID 제어 : 원하는 값에 도달하기 위한 기초적인 자동 피드백 제어 방법 중 하나
- 간단한 수식, 제어 대상의 모델이 필요없음, 구현 난이도 대비 목표치 추종이나 외란 감쇄 효과에 탁월한 성능을 얻을 수 있어 대부분의 선형 시불변 시스템에서 사용하는 제어기
- 목표속도(목표), 현재속도(현재), 목표속도-현재속도(오차)
- 오차 값을 가지고 P(비례), I(적분), D(미분)을 통해 현재 값을 목표값으로 수렴시킬 수 있음
    - 원하는 성능을 얻기 위해 P, I, D 이득값을 적절히 튜닝해야함
    - 그렇지 않으면 시간이 지나도 오차값이 계속 남아있거나, 목표 값에서 더 멀어져 시스템이 불안정해질 수 있음
    - Figure 19 : PID 수식

### 비례항(P)

- 현재 상태에서의 오차 값의 크기에 비례한 제어작용

### 적분항(I)

- 정상상태(steady_state) 오차를 없애는 작용

### 미분항(D)

- 출력 값의 급격한 변화에 제동을 걸어 오버슛을 줄이고 안정성 향상

### PID 성능 측정

- Rise Time : 목표값의 10% 에서 90% 까지 도달하는데 걸리는 시간
- Overshoot : 현재값이 목표값보다 커졌을 때의 값
- Setting Time : 목표 값의 5% 이내에 들어갈 때의 시간
- Steady_State Error : 정상상테에 도달하고 나서 존재하는 에러

## 10. 경로기반 속도 계획

- 말 그대로 경로(경로점)에서 얼마만큼의 속도를 내야하는가를 계획하는 것
- 직선에서는 비교적 빠르지만 곡선에서는 빠르게 주행하기 어려움
- 곡선 주행시 구심력의 작용 반작용 힘에 의해 원심력을 받게됨
- 회전반경에 반비례, 속도 제곱에 비례하므로 속도가 클수록, 회적반경이 작을수록 차량이 쉽게 전복됨
- 경로기반 속도 계획을 통해 차량 전복을 방지할 수 있음

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%201.png)

### 곡선도로에서 최대속도

- Flat roadway 일 때, 경로의 곡률반지름(r)을 알면 곡선도로에서의 최대속도를 알 수 있음
- u_s : 운동마찰계수
- 아스팔트는 0.7~0.8 이지만 시뮬레이터 환경에 맞게 조절해서 사용해야함
- 최소자승법 : 경로점들을 가지고 경로와 근사한 모델을 만듦
- 곡률반지름 : 원 방정식이나 3차방정식을 통해 구할 수 있음

## 11. ACC(Adaptive Cruise Control)

- ACC 모듈 : 운전자(EgoCar)가 설정한 속도로 주행을 하다가 레이다, 라이다, 카메라 등과 같은 환경인지 센서로 앞 차(LeadCar)를 인지하고 앞 차와의 간격을 유지하는 시스템

### Classic ACC

- 상대거리 > 안전거리 : Speed Control 모드
- 상대거리 < 안전거리 : Spacing Control 모드
- D_safe(안전거리) : 현재속도에서 time_gap 거리와 defaultSpace(기본유지거리) 를 더한값
    - time_gap : 판단에서 제어까지 차량을 안전하게 멈추는 시간
    - 보통 two-second-rule 을 따라 2초로 지정
- V_rel(상대속도)
- D_rel(상대거리)
- gain_vel(속도에 대한 이득 값)
- gain_dis(거리에 대한 이득 값)
- 목표 : 적절한 이득값 조절을 통해 앞 차의 급격한 속도변화에도 D_rel 이 D_safe 와 같게 유지하는 것
- ACC 는 앞 차와의 거리간격 유지뿐만 아니라 보행자, 정지선, 장애물에도 적용 가능
- 정지해있는 장애물은 속도가 0인 자동차와 같다고 여기기

# 기능 명세

## 1. 기능/과제 목록

### 1-1. Localization (WGS84 → UTM 좌표변환)

- GPS 에서 받은 경위도 데이터(WGS)를 UTM 좌표계로 변환
- zone = 52, ellps = ‘WGS84’

### 1-2. Odometry ROS 메시지 생성

- GPS 에서 받은 경위도 데이터(WGS)를 UTM 좌표계로 변환
- IMU 에서 quaternion 자세 데이터 사용
- ROS Odometry 메시지 형식으로 차량데이터 변환 후 송신

### 1-3. ROS TF 좌표계 생성

- ROS Odometry 메시지를 통한 차량 데이터 수신
- TF 브로드캐스터 생성 및 Ego 상태 tf 브로드캐스팅

### 2 - 정밀도로 지도

### 2-1. Mgeo 데이터 확인 및 시각화

- JSON 형식의 MGeo 데이터 읽어온 뒤 확인
- Node 와 Link 데이터를 ROS Point Cloud 형식으로 변환 후 송신
- Rviz 시각화 기능을 통해 Node Link 데이터 확인

### 3 - 경로계획

### 3-1. Odometry 를 이용한 차량의 주행 경로 기록

- ROS Odometry 메시지를 통한 차량 데이터 수신
- 차량의 주행 데이터를 txt 파일로 저장

### 3-2. 저장된 주행 경로를 읽어 차량의 global path(전역경로) 생성

- 차량의 주행데이터가 기록된 txt 파일을 확인
- 읽어온 차량의 주행 데이터를 ROS Path 메시지 형식으로 할당
- 할당된 Path 데이터를 ROS Path 메시지 형식으로 송신

### 3-3. global path(전역경로)를 이용한 local path(지역경로) 생성

- 차량 상태 데이터와 전역 경로 데이터를 수신
- 전역경로 중 차량과 가장 가까운 위치의 Point(Current Waypoint) 를 탐색
- Current Waypoint 를 기준으로 지역 경로 생성
- 생성된 지역 경로를 ROS Path 메시지 형식으로 송신

### 3-4. MGeo 데이터에 Dijkstra 알고리즘 적용한 global path(전역경로) 생성

- 경로 생성을 위한 시작 Node 와 종료 Node 설정
- Dijkstra 알고리즘 적용을 위한 각 Node 간 이동시 발생 비용 계산
- Dijkstra 알고리즘을 적용한 최단 거리 탐색
- 탐색된 최단거리의 좌표데이터를 이용한 Path 생성
- 생성된 Dijkstra 최단거리 경로를 ROS Path 메시지 형식으로 송신

### 4 - 판단/제어

### 4-1. Pure pursuit 알고리즘을 적용한 횡방향 제어

- 차량 상태 데이터와 지역 경로 데이터를 수신
- 차량의 전방주시거리(Look Forward Distance) 설정
- 전방 주시거리와 가장 가까운 지역경로 포인트 위치 확인
- 차량 위치에서 전방주시거리와 가장 가까운 포인트 사이 각도 계산
- 차량 각도값과 전방주시거리와의 사이값 비교
- 차량 제어입력을 위한 Pure pursuit 수식을 통해 조향 각도 설정
- 제어 입력값을 ROS 메시지 형식으로 송신

### 4-2. PID 제어를 적용한 종 방향 제어

- 차량 상태 데이터와 지역 경로 데이터를 수신
- PID 제어의 Gain 값을 결정
- 현재 차량 속도와 목표 속도와의 오차를 비교
- 오차값 이용한 PID 제어 수식 완성
- 제어 입력값을 ROS 메시지 형식으로 송신

### 4-3. 도로의 곡률을 고려한 차량 주행 속도 계획

- 차량 상태 데이터와 지역 경로 데이터 전역 경로 데이터 수신
- 전역 경로 이용한 차량 주행 경로 곡률 계산
- 곡률반경을 이용 경로에서 주행할 수 있는 최대 속도 계산
- 제어 입력값을 ROS 메시지 형식으로 송신

### 4-4. Pure pursuit 알고리즘을 강화한 Advanced Pure pursuit 알고리즘

- 차량 상태 데이터와 지역 경로 데이터 전역 경로 데이터를 수신
- 전방주시거리(Look Forward Distance)를 계산하기 위한 최대 최소값 설정
- 속도에 비례한 전방주시거리계산을 위한 전방주시거리 Gain 값 설정
- 속도에 비례한 전방주시거리 계산
- 차량의 제어 입력을 위한 Pure pursuit 수식으로 조향각 설정
- 제어 입력값을 ROS 메시지 형식으로 송신

### 4-5. Adaptive Cruise Control

- 차량 상태 정보와 주행 경로정보 및 장애물 정보 수신
- 장애물 정보, 지역 경로 이용해 주행경로 상 장애물 유무 파악
- 장애물 위치 좌표와 속도를 Ego 차량 위치 속도와 비교
- 비교한 상대 거리와 상대 속도를 통해 현재 차량의 목표 속도 설정
- 목표속도를 이용한 차량의 제어입력 결정
- 제어 입력 값을 ROS 메시지 형식으로 송신

# 스켈레톤 프로젝트

## ROS 패키지에 내장된 공용 메시지 파일

[https://github.com/ros/common_msgs](https://github.com/ros/common_msgs)

## Req 1

### req 1-1. gps_parser.py

- 시뮬레이터에서 출력되는 GPS 센서 데이터를 UTM 좌표로 변환하는 예제
- Pyproj 라이브러리 사용
- 실행 코드
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    import rospy
    import numpy as np
    import tf
    import os
    #TODO: (0) pyproj 라이브러리 Import [ pip install pyproj ]
    from pyproj import Proj
    from std_msgs.msg import Float32MultiArray
    from morai_msgs.msg import GPSMessage, EgoVehicleStatus
    
    # gps_parser 는 GPS의 위경도 데이터를 UTM 좌표로 변환하는 예제입니다.
    # Pyproj 라이브러리를 사용 
    
    # 노드 실행 순서 
    # 1. 변환 하고자 하는 좌표계를 선언  
    # 2. 시뮬레이터에서 GPS 데이터를 받아오는 Callback 함수 생성 
    # 3. 위도 경도 데이터를 UTM 좌표로 변환   
    # 4. 위도 경도 데이터와 변환한 UTM 좌표를 터미널 창에 출력 하여 확인  
    
    class LL2UTMConverter:
        def __init__(self, zone=52) :
            self.gps_sub = rospy.Subscriber("/gps", GPSMessage, self.navsat_callback)
            # 초기화
            self.x, self.y = None, None
    
            #TODO: (1) 변환 하고자 하는 좌표계를 선언
            # GPS 센서에서 수신되는 위도, 경도 데이터를 UTM 좌표료 변환 하기 위한 예제이다.
            # 해당 예제는 WGS84 좌표계에서 UTM 좌표계로의 변환을 진행한다.
            # 시뮬레이터 K-City Map 의 경우 UTM 좌표계를 사용하며 실제 지도 상 위치는 UTM 좌표계의 52 Zone 에 존재한다.
            # 맵 좌표계는 m 단위를 사용한다.
            # 아래 주소의 링크를 클릭하여 Ptoj 의 사용 방법을 확인한다.
            # https://pyproj4.github.io/pyproj/stable/api/proj.html
            # " proj= , zone= , ellps =  , preserve_units = "
            self.proj_UTM = Proj(proj='utm', zone=52, ellps='WGS84', preserve_units = False)
    
        #TODO: (2) 시뮬레이터에서 GPS 데이터를 받아오는 Callback 함수 생성
        def navsat_callback(self, gps_msg):
            # GPS 센서에서 수신되는 위도 경도 데이터를 확인한다.
            self.lat = gps_msg.latitude
            self.lon = gps_msg.longitude
    
            self.convertLL2UTM()
    
            utm_msg = Float32MultiArray()
    
            #TODO: (4) 위도 경도 데이터와 변환한 UTM 좌표를 터미널 창에 출력 하여 확인
            # UTM 으로 변환 된 좌표 데이터와 위도 경도 데이터를 터미널 창에 출력되도록 한다.
            utm_msg.data = [self.x, self.y]
            os.system('clear')
            print(' lat : ', self.lat)
            print(' lon : ', self.lon)
            print(' utm X : ', utm_msg.data[0])
            print(' utm Y : ', utm_msg.data[1])
    
        #TODO: (3) 위도 경도 데이터를 UTM 좌표로 변환
        def convertLL2UTM(self):
            # pyproj 라이브러리를 이용해 정의한 좌표 변환 변수를 이용하여 위 경도 데이터를 변환한다.
            xy_zone = self.proj_UTM(self.lon, self.lat)
    
            self.x = xy_zone[0]
            self.y = xy_zone[1]
    
    if __name__ == '__main__':
    
        rospy.init_node('gps_parser', anonymous=True)
    
        gps_parser = LL2UTMConverter()
    
        rospy.spin()
    ```
    
- 실행 결과

```python
(' lat : ', 37.242617833251046)
(' lon : ', 126.77457989117718)
(' utm X : ', 302608.37333550456)
(' utm Y : ', 4124107.9364122474)
```

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%202.png)

### req 1-2. gpsimu_parser.py

- gps_parser 노드에서 IMU 데이터를 추가로 입력한 예제
- GPS 와 IMU 데이터를 받아 차량의 위치 자세 데이터를 얻음
- 얻은 차량의 데이터는 ROS Odometry 형식으로 Publish 하여 다른 노드에서 사용할 수 있도록 함
- 실행 코드
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
     
    import rospy
    import tf
    import os
    from std_msgs.msg import Float32MultiArray
    from sensor_msgs.msg import Imu
    from morai_msgs.msg import GPSMessage
    from nav_msgs.msg import Odometry
    from pyproj import Proj
    from math import pi
    
    # gpsimu_parser 는 GPS, IMU 센서 데이터를 받아 차량의 상대위치를 추정하는 예제입니다.
    
    # 노드 실행 순서 
    # 1. 변환 하고자 하는 좌표계를 선언
    # 2. 송신 될 Odometry 메세지 변수 생성
    # 3. 위도 경도 데이터 UTM 죄표로 변환
    # 4. Odometry 메세지 변수에 차량의 위치 및 상태 데이터 담기
    # 5. Odometry 메세지 Publish
    
    class GPSIMUParser:
        def __init__(self):
            rospy.init_node('GPS_IMU_parser', anonymous=True)
            self.gps_sub = rospy.Subscriber("/gps", GPSMessage, self.navsat_callback)
            self.imu_sub = rospy.Subscriber("/imu", Imu, self.imu_callback)
            self.odom_pub = rospy.Publisher('/odom',Odometry, queue_size=1)
            # 초기화
            self.x, self.y = None, None
            self.is_imu = False
            self.is_gps = False
    
            #TODO: (1) 변환 하고자 하는 좌표계를 선언
            # GPS 센서에서 수신되는 위도, 경도 데이터를 UTM 좌표료 변환 하기 위한 예제이다.
            # 해당 예제는 WGS84 좌표계에서 UTM 좌표계로의 변환을 진행한다.
            # 시뮬레이터 K-City Map 의 경우 UTM 좌표계를 사용하며 실제 지도 상 위치는 UTM 좌표계의 52 Zone 에 존제한다.
            # 맵 좌표계는 m 단위를 사용한다.
            # 아래 주소의 링크를 클릭하여 Ptoj 의 사용 방법을 확인한다.
            # https://pyproj4.github.io/pyproj/stable/api/proj.html
            # " proj= , zone= , ellps =  , preserve_units = "
            self.proj_UTM = Proj(proj='utm', zone=52, ellps='WGS84', preserve_units=False)
    
            #TODO: (2) 송신 될 Odometry 메세지 변수 생성
            # ROS 메세지 중 물체의 위치와 자세 데이터를 나타내는 Odometry 메세지를 사용한다.
            # 차량의 현재 위치와 자세 데이터를 GPS IMU 센서에 담아서 Publsih 한다.
            # 이때 frame_id 는 '/odom' child_frame_id 는 '/base_link' 로 한다.
    
            self.odom_msg = Odometry()
            self.odom_msg.header.frame_id = '/odom'
            self.odom_msg.child_frame_id = '/base_link'
    
            rate = rospy.Rate(30) # 30hz
            while not rospy.is_shutdown():
                if self.is_imu==True and self.is_gps == True:
                    self.convertLL2UTM()
    
                    #TODO: (5) Odometry 메세지 Publish
                    # Odometry 메세지 를 전송하는 publisher 를 만든다.
                    self.odom_pub.publish(self.odom_msg)
                    
                    os.system('clear')
                    print(" ROS Odometry Msgs Pose ")
                    print(self.odom_msg.pose.pose.position)
                    print(" ROS Odometry Msgs Orientation ")
                    print(self.odom_msg.pose.pose.orientation)
    
                    rate.sleep()
    
        def navsat_callback(self, gps_msg):
    
            self.lat = gps_msg.latitude
            self.lon = gps_msg.longitude
            self.e_o = gps_msg.eastOffset
            self.n_o = gps_msg.northOffset
    
            self.is_gps=True
    
        #TODO: (3) 위도 경도 데이터 UTM 죄표로 변환
        def convertLL2UTM(self):
            # pyproj 라이브러리를 이용해 정의한 좌표 변환 변수를 이용하여 위 경도 데이터를 변환한다.
            # 변환 시 이전 gps_parser.py 예제와 달리 시뮬레이터 GPS 센서의 offset 값을 적용 한다.
            # GPS 센서에서 출력되는 Offset 값은 시뮬레이터에 맵 좌표계로 변경을 위한 값이다.
            # UTM 좌표로 변환 된 x, y 값에 offset 값을 빼주면 된다.
            xy_zone = self.proj_UTM(self.lon, self.lat)
    
            # if 문을 이용 예외처리를 하는 이유는 시뮬레이터 음영 구간 설정 센서 데이터가 0.0 으로 나오기 때문이다.
            if self.lon == 0 and self.lat == 0:
                self.x = 0.0
                self.y = 0.0
            else:
                self.x = xy_zone[0] - self.e_o
                self.y = xy_zone[1] - self.n_o
    
            #TODO: (4) Odometry 메세지 변수에 차량의 위치 및 상태 데이터 담기
            # Offset 을 적용하여 시뮬레이터 맵 좌표계 값으로 변환 된 좌표 데이터를 Odometry 메세지에 넣는다.
            self.odom_msg.header.stamp = rospy.get_rostime()
            self.odom_msg.pose.pose.position.x = self.x
            self.odom_msg.pose.pose.position.y = self.y
            self.odom_msg.pose.pose.position.z = 0
    
        def imu_callback(self, data):
    
            #TODO: (4) Odometry 메세지 변수에 차량의 위치 및 상태 데이터 담기
            # IMU 를 통해 받은 물체의 자세 데이터를 Odometry 메세지에 넣는다.
            # if 문을 이용 예외처리를 하는 이유는 시뮬레이터 음영 구간 설정 센서 데이터가 0.0 으로 나오기 때문이다.
            if data.orientation.w == 0:
                self.odom_msg.pose.pose.orientation.x = 0.0
                self.odom_msg.pose.pose.orientation.y = 0.0
                self.odom_msg.pose.pose.orientation.z = 0.0
                self.odom_msg.pose.pose.orientation.w = 1.0
            else:
                self.odom_msg.pose.pose.orientation.x = data.orientation.x
                self.odom_msg.pose.pose.orientation.y = data.orientation.y
                self.odom_msg.pose.pose.orientation.z = data.orientation.z
                self.odom_msg.pose.pose.orientation.w = data.orientation.w
    
            self.is_imu=True
    
    if __name__ == '__main__':
        try:
            GPS_IMU_parser = GPSIMUParser()
        except rospy.ROSInterruptException:
            pass
    ```
    
- 실행 결과

```python
ROS Odometry Msgs Pose 
x: 148.521225029
y: 1472.38256654
z: 0
 ROS Odometry Msgs Orientation 
x: 0.0459366701543
y: -0.0529919676483
z: -0.780060231686
w: -0.621761798859
```

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%203.png)

### req 1-3. tf_pub.py

- 물체 위치와 자세 데이터를 좌표계로 나타내는 예제
- 차량의 자세 데이터인 Odometry ROS 메시지를 받아 현재 차량의 위치와 자세를 표현할 수 있음
- 실행 코드
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import rospy
    import tf
    from math import pi
    from nav_msgs.msg import Odometry
    
    # tf 는 물체의 위치와 자세 데이터를 좌표계로 나타내는 예제입니다.
    
    # 노드 실행 순서 
    # 1. Callback 함수 생성
    # 2. 브로드캐스터 생성 및 Ego 상태 tf 브로드캐스팅
    
    class Ego_listener():
        def __init__(self):
            rospy.init_node('status_listener', anonymous=True)
            
            rospy.Subscriber("/odom", Odometry, self.odom_callback)
            rospy.spin()
    
        #TODO: (1) Callback 함수 생성
        def odom_callback(self,msg):
            self.is_odom = True
    
            # gpsimu_parser.py 예제에서 Publish 해주는 Odometry 메세지 데이터를 Subscrib 한다.
            # Odometry 메세지 에 담긴 물체의 위치 와 자세 데이터를 아래 변수에 넣어준다.
            self.x = msg.pose.pose.position.x
            self.y = msg.pose.pose.position.y
    
            self.orientation_x = msg.pose.pose.orientation.x
            self.orientation_y = msg.pose.pose.orientation.y
            self.orientation_z = msg.pose.pose.orientation.z
            self.orientation_w = msg.pose.pose.orientation.w
    
            #TODO: (2) 브로드캐스터 생성 및 Ego 상태 tf 브로드캐스팅
            # TF 데이터를 broadcast 해주는 변수를 선언한다.
            # TF 데이터에 물체의 좌표와 자세 데이터를 시간 그리고 Frame ID 를 넣어주면 된다.
            # TF 예제는 map 좌표 를 기준으로 Ego 차량의 위치를 좌표를 나타낸다
            br = tf.TransformBroadcaster()
            print('brodcast tf')
            br.sendTransform((self.x, self.y, 0),
                            (self.orientation_x, self.orientation_y, self.orientation_z, self.orientation_w),
                            rospy.Time.now(),
                            "Ego",
                            "map")
    
    if __name__ == '__main__':
        try:
            tl=Ego_listener()
        except rospy.ROSInternalException:
            pass
    ```
    
- 실행 결과

```python
brodcast tf
brodcast tf
brodcast tf
brodcast tf
brodcast tf
```

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%204.png)

## Req 2

### req 2-1. mgeo.py

- 정밀도로지도 데이터 인 MGeo(MORAI Geometry) 데이터를 읽어오는 예제
- Json 파일 형식으로 되어 있는 MGeo 데이터를 dictionary 형태로 읽어옴
- 실행 코드
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    import os
    import sys
    
    current_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(current_path)
    
    from lib.mgeo.class_defs import *
    
    # mgeo 는 정밀도로지도 데이터 인 MGeo(MORAI Geometry) 데이터를 읽어오는 예제입니다.
    # Json 파일 형식으로 되어 있는 MGeo 데이터를 dictionary 형태로 읽어옵니다.
    
    # 노드 실행 순서 
    # 1. Mgeo data 읽어온 후 데이터 확인
    
    #TODO: (1) Mgeo data 읽어온 후 데이터 확인
    # Json 파일 형식으로 저장된 MGeo 데이터를 읽어오는 예제 입니다.
    # VScode 의 debug 기능을 이용하여 MGeo 데이터를 확인 할 수 있습니다.
    # MGeo 데이터는 인접 리스트 방식의 그래프 구조 입니다.
    # 정밀도로지도의 도로 간의 연결 관계를 표현 합니다.
    # MGeo 에는 도로의 형상을 나타내는 Node 와 Link 데이터가 있습니다.
    # Node 와 Link 는 모두 Point 데이터 들의 집합입니다.
    # Node 는 서로 다른 두개 이상의 Link 간의 연결 여부를 나타냅니다.
    # Link 는 도로를 표현하며 도로 의 중심 선이 됩니다.
    # Link 와 Node 정보가 모여 도로의 형상을 표현합니다.
    # 각각의 Node Link 정보는 이름인 idx 정보를 가집니다 idx 는 중복 될 수 없습니다. 
    # to_links , from_links , to_node , from_node ... 등 
    # MGeo에 정의되어 있는 데이터를 활용해 각 Node 와 Link 간 연결 성을 나타낼 수 있습니다.
    
    load_path = os.path.normpath(os.path.join(current_path, 'lib/mgeo_data/R_KR_PG_K-City'))
    mgeo_planner_map = MGeo.create_instance_from_json(load_path)
    
    node_set = mgeo_planner_map.node_set
    link_set = mgeo_planner_map.link_set
    nodes=node_set.nodes
    links=link_set.lines
    
    print('# of nodes: ', len(node_set.nodes))
    print('# of links: ', len(link_set.lines))
    ```
    
- 실행 결과

```python
('# of nodes: ', 203)
('# of links: ', 374)
```

### req 2-1. mgeo_pub.py

- Mgeo 데이터를 읽어온 뒤 도로 정보를 Point Cloud Data 로 변환하는 예제
- Point Cloud 형식으로 변환 후 Rviz 를 이용해 정밀도로지도 데이터를 시각화 할 수 있음
- catkin_ws/src/chapter7/scripts/mgeo_pub.py 에서 힌트 얻을 것!
- 모라이에서 토글 열어두기 TF2Publisher
    
    → jh 말로는 gpsimu, tf_pub 이런 걸 실행하지 않아도 할 수 있게 된다고 함
    
- rviz : By Topic - link - pointcloud Add / By Topic - node - pointcloud Add
- 실행 코드
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    import os
    import sys
    import rospy
    
    from geometry_msgs.msg import Point32
    from sensor_msgs.msg import PointCloud
    
    current_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(current_path)
    
    from lib.mgeo.class_defs import *
    
    class get_mgeo :
    
        def __init__(self):
            rospy.init_node('mgeo_pub', anonymous=True)
            self.link_pub = rospy.Publisher('link',PointCloud, queue_size=1)
            self.node_pub = rospy.Publisher('node',PointCloud, queue_size=1)
    
            load_path = os.path.normpath(os.path.join(current_path, 'lib/mgeo_data/kcity'))
            mgeo_planner_map = MGeoPlannerMap.create_instance_from_json(load_path)
    
            node_set = mgeo_planner_map.node_set
            link_set = mgeo_planner_map.link_set
            self.nodes=node_set.nodes
            self.links=link_set.lines
            self.link_msg=self.getAllLinks()
            self.node_msg=self.getAllNode()
    
            rate = rospy.Rate(1) 
            while not rospy.is_shutdown():
                self.link_pub.publish(self.link_msg)
                self.node_pub.publish(self.node_msg)
                print("MGeo node , link data >>>> publish success !!")
                    
                rate.sleep()
    
        def getAllLinks(self):
            all_link=PointCloud()
            all_link.header.frame_id='map'
            
            for link_idx in self.links :
                for link_point in self.links[link_idx].points:
                    tmp_point=Point32()
                    tmp_point.x=link_point[0]
                    tmp_point.y=link_point[1]
                    tmp_point.z=link_point[2]
                    all_link.points.append(tmp_point)
    
            return all_link
        
        def getAllNode(self):
            all_node=PointCloud()
            all_node.header.frame_id='map'
            for node_idx in self.nodes :
                tmp_point=Point32()
                tmp_point.x=self.nodes[node_idx].point[0]
                tmp_point.y=self.nodes[node_idx].point[1]
                tmp_point.z=self.nodes[node_idx].point[2]
                all_node.points.append(tmp_point)
    
            return all_node
    
    if __name__ == '__main__':
        
        test_track=get_mgeo()
    ```
    
- 실행 결과

```python
('# of nodes: ', 203)
('# of links: ', 374)
mgeo_pub.py success
mgeo_pub.py success
mgeo_pub.py success
mgeo_pub.py success
```

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%205.png)

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%206.png)

## Req 3

### req 3-1. path_maker.py

- 차량의 위치 데이터를 받아 txt 파일로 저장하는 예제
- 저장한 txt 파일은 차량의 주행 경로가 되며 경로 계획에 이용 할 수 있음
- 실행 코드
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    from re import I
    import rospy
    import rospkg
    from math import sqrt
    from geometry_msgs.msg import Point32,PoseStamped
    from nav_msgs.msg import Odometry
    
    # path_maker 는 차량의 위치 데이터를 받아 txt 파일로 저장하는 예제입니다.
    # 저장한 txt 파일은 차량의 주행 경로가 되며 경로 계획에 이용 할 수 있습니다.
    
    # 노드 실행 순서 
    # 1. 저장할 경로 및 텍스트파일 이름을 정하고, 쓰기 모드로 열기
    # 2. 콜백함수에서 처음 메시지가 들어오면 초기 위치를 저장
    # 3. 콜백함수에서 이전 위치와 현재 위치의 거리 계산
    # 4. 이전 위치보다 0.5m 이상일 때 위치를 저장
    
    class pathMaker :    
        def __init__(self, pkg_name = 'ssafy_2', path_name = 'make_path'):
            rospy.init_node('path_maker', anonymous=True)
    
            rospy.Subscriber("/odom", Odometry, self.odom_callback)
    
            # 초기화
            self.prev_x = 0
            self.prev_y = 0
            self.is_odom=False
    
            #TODO: (1) 저장할 경로 및 텍스트파일 이름을 정하고, 쓰기 모드로 열기
            '''
            # Path 데이터를 기록 하고 저장 할 경로와 txt 파일의 이름을 정한다.
            # 이후 쓰기 모드로 연다.
            # pkg_name 과 path_name 은 22 번 줄 참고한다.
            rospack = rospkg.RosPack()
            pkg_path = rospack.get_path(pkg_name)
            full_path = 이곳에 txt 파일이 저장될 경로와 이름을 적는다
            self.f = 
    
            '''
            rospack = rospkg.RosPack()
            pkg_path = rospack.get_path(pkg_name)
            full_path = "/home/ssafy/mobility-autodriving-skeleton/ssafy_ad/src/ssafy_2/path/yubin_test.txt"
            self.f = open(full_path, 'w')
    
            while not rospy.is_shutdown():
                if self.is_odom == True :
                    # Ego 위치 기록
                    self.path_make()
            self.f.close()
    
        def path_make(self):
            x = self.x
            y = self.y
            z = 0.0
    
            #TODO: (3) 콜백함수에서 이전 위치와 현재 위치의 거리 계산
            '''
            # 현재 차량의 위치와 이전에 지나온 위치의 좌표 데이터를 구한다.
            # 구해진 좌표 사이의 거리를 계산한다.
            # 이전 위치 좌표는 아래 #TODO: (4)에서 정의 한다.
            distance = 
    
            '''
            distance = sqrt((x-self.prev_x)**2 + (y-self.prev_y)**2)
    
            #TODO: (4) 이전 위치보다 0.5m 이상일 때 위치를 저장        
            if distance > 0.5:
                '''
                # distance 가 0.5 보다 커야지만 동작한다.
                # 현재 위치 좌표를 data 에 담은 뒤 txt 파일로 작성한다.
                # data 는 문자열 이며 x y z 사이는 \t 로 구분한다
                data ='{0}\t{1}\t{2}\n'.format(x,y,z)
                self.f.write(data 변수를 넣는 위치이다)
                self.prev_x = 
                self.prev_y = 
                self.prev_z = 
                
                print(기록 된 위치 좌표를 출력한다)
    
                '''
                data ='{0}\t{1}\t{2}\n'.format(x,y,z)
                self.f.write(data)
                self.prev_x = x
                self.prev_y = y
                self.prev_z = z
                
                print(data)
    
        def odom_callback(self, msg):
            self.is_odom = True
            #TODO: (2) 콜백함수에서 처음 메시지가 들어오면 초기 위치를 저장
    
            '''
            # gpsimu_parser.py 예제에서 Publish 해주는 Odometry 메세지 데이터를 Subscrib 한다.
            # Odometry 메세지 에 담긴 물체의 위치 데이터를 아래 변수에 넣어준다.
            self.x = 물체의 x 좌표 
            self.y = 물체의 y 좌표
    
            '''
            self.x = msg.pose.pose.position.x
            self.y = msg.pose.pose.position.y
    
    if __name__ == '__main__' :
        try:
            p_m=pathMaker()
        except rospy.ROSInternalException:
            pass
    ```
    
- 실행 결과

```python
98.3103485668	1245.8210431	0.0

98.5934448795	1246.3231183	0.0

98.8260269714	1246.81518373	0.0

99.1468201229	1247.30212221	0.0

99.4381790719	1247.8074933	0.0

99.7137222838	1248.28429994	0.0

99.9697571346	1248.72643861	0.0
```

![Untitled](SUBPJT2%206230021b45e5455fa4a799bd73c7d8cc/Untitled%207.png)

### * req 3-2. global_path_pub.py

- txt 파일로 저장한 Path 데이터를 global Path (전역경로) 로 읽어오는 예제
- 만들어진 global Path(전역경로) 는 Local Path (지역경로) 를 만드는데 사용됨
- 실행 코드 : 근데 이거는 실행안해봤다
    
    ```python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    import rospy
    import rospkg
    from math import cos,sin,pi,sqrt,pow
    from geometry_msgs.msg import Point32,PoseStamped
    from nav_msgs.msg import Odometry,Path
    
    # global_path_pub 은 txt 파일로 저장한 Path 데이터를 global Path (전역경로) 로 읽어오는 예제입니다.
    # 만들어진 global Path(전역경로) 는 Local Path (지역경로) 를 만드는데 사용 된다.
    
    # 노드 실행 순서 
    # 1. Global Path publisher 선언 및 Global Path 변수 생성 
    # 2. 읽어올 경로 의 텍스트파일 이름을 정하고, 읽기 모드로 열기
    # 3. 읽어 온 경로 데이터를 Global Path 변수에 넣기
    # 4. Global Path 정보 Publish
    
    class global_path_pub :
        def __init__(self, pkg_name = 'ssafy_2', path_name = 'kcity'):
            rospy.init_node('global_path_pub', anonymous = True)
    
            #TODO: (1) Global Path publisher 선언 및 Global Path 변수 생성 
            '''
            # Global Path 데이터를 Publish 하는 변수와 메세지를 담고있는 변수를 선언한다.
            # 이때 Global Path 는 map 좌표계를 기준으로 생성한다.
            self.global_path_pub = 
            self.global_path_msg = 
            self.global_path_msg.header.frame_id = 
    
            '''
            self.global_path_pub = rospy.Publisher('/path', Path, queue_size=1)
            self.global_path_msg = Path()
            self.global_path_msg.header.frame_id = '/map'
    
            #TODO: (2) 읽어올 경로 의 텍스트파일 이름을 정하고, 읽기 모드로 열기
            '''
            # Path 데이터가 기록 된 txt 파일의 경로와 이름을 정한다.
            # 이후 읽기 모드로 연다.
            # pkg_name 과 path_name 은 21 번 줄 참고한다.
            rospack = rospkg.RosPack()
            pkg_path = rospack.get_path(pkg_name)
            full_path = 
            self.f =         
            lines = self.f.readlines()
    
            '''
            rospack = rospkg.RosPack()
            pkg_path = rospack.get_path(pkg_name)
            full_path = "/home/ssafy/mobility-autodriving-skeleton/ssafy_ad/src/ssafy_2/path/kcity.txt"
            self.f = open(full_path, 'r')
            lines = self.f.readlines()
    
            #TODO: (3) 읽어 온 경로 데이터를 Global Path 변수에 넣기
            '''
            # 읽어온 x y z 좌표 데이터를 self.global_path_msg 변수에 넣는다.
            # 넣어준 반복 문을 이용하여 작성한다.
            for line in lines :
                tmp = line.split()
                read_pose = 
                read_pose.pose.position.x = 
                read_pose.pose.position.y = 
                read_pose.pose.orientation.w = 1
                self.global_path_msg.poses.append(read_pose)        
            self.f.close()
    
            '''
            for line in lines :
                tmp = line.split()
                read_pose = Odometry.pose
                read_pose.pose.position.x = tmp[0]
                read_pose.pose.position.y = tmp[1]
                read_pose.pose.orientation.w = 1
                self.global_path_msg.poses.append(read_pose)        
            self.f.close()
    
            rate = rospy.Rate(10) # 10hz
            while not rospy.is_shutdown():
                #TODO: (4) Global Path 정보 Publish
                '''
                # Global Path 메세지 를 전송하는 publisher 를 만든다.
                self.global_path_pub.
                
                '''
                self.global_path_pub.publish(self.global_path_msg)
                rate.sleep()
    
    if __name__ == '__main__':
        try:
            test_track = global_path_pub()
        except rospy.ROSInterruptException:
            pass
    ```
    
- 실행 결과

```python

```

### req 3-3. local_path_pub.py

- .
- .
- 실행 코드
    
    ```python
    
    ```
    
- 실행 결과

```python

```

### req 3-4 (1). mgeo_dijkstra_path_1.py

- .
- .
- 실행 코드
    
    ```python
    
    ```
    
- 실행 결과

```python

```

### req 3-4 (2). mgeo_dijkstra_path_2.py

- .
- .
- 실행 코드
    
    ```python
    
    ```
    
- 실행 결과

```python

```

## Req 4

### req 4-1. pure_pursuit.py

- .
- .
- 실행 코드
    
    ```python
    
    ```
    
- 실행 결과

```python

```

### req 4-2. pid_control.py

- .
- .
- 실행 코드
    
    ```python
    
    ```
    
- 실행 결과

```python

```