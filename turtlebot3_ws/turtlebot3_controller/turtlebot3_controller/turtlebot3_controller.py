# Author : Khantaphon Chaiyo & 
import math
import random
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import LaserScan, BatteryState
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
#from std_msgs.msg import String
turncase = ''
startdegree = 0.0
b4dif = 0.0
bount = 0
step = 1 
deltaturn = 0.0
totalturn = 0.0
previousturn = 0.0
previousx = 0.0
previousy = 0.0
totaldistance = 0.0
deltadistance = 0.0
goaldistance = 0.0
count = 0
direction = 0
forcal = 0.0
forwalk = 0.0
turninterval = 0
stop = False
ob1 = []
ob2 = []
ob3 = []
ob4 = []
obstacle = [0,0,0,0] # front,left,back,right
case = 0
secondcase = 0
thirdcase = 0
fourthcase = 0
special = 0
noforever = 0
presentpose = 0
presentorient = 0 # 0 = front , 1 = left , 2 = back , 3 = right
endSST = False
end = False
check = False

class Turtlebot3Controller(Node):
    
    global destination
    global kp
    global turncase
    global case
    
    def __init__(self):
        super().__init__('turtlebot3_controller')   #node name
        self.cmdVelPublisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.scanSubscriber = self.create_subscription(LaserScan, 'scan', self.scanCallback, qos_profile=qos_profile_sensor_data)
        self.batteryStateSubscriber = self.create_subscription(BatteryState, 'battery_state', self.batteryStateCallback, 1)
        self.odomSubscriber = self.create_subscription(Odometry, 'odom', self.odomCallback, 1)
        self.valueLaserRaw = {
            'range_min':0.0,
            'range_max':0.0,
            'ranges':[0.0]*360,
        }
        self.valueBatteryState = None
        self.valueOdometry = {
            'position':None,        #Datatype: geometry_msg/Point   (x,y,z)
            'positionX':0.0,
            'positionY':0.0,
            'positionZ':0.0,
            'orientation':None,     #Datatype: geometry_msg/Quaternion (x,y,z,w)
            'orientationX':0.0,
            'orientationY':0.0,
            'orientationZ':0.0,
            'orientationW':0.0,
            'linearVelocity':None,  #Datatype: geometry_msg/Vector3 (x,y,z)
            'XlinearVelocity':0.0,
            'YlinearVelocity':0.0,
            'ZlinearVelocity':0.0,
            'angularVelocity':None, #Datatype: geometry_msg/Vector3 (x,y,z)
        }

        #Use this timer for the job that should be looping until interrupted
        self.timer = self.create_timer(0.1,self.timerCallback)

    def publishVelocityCommand(self, linearVelocity, angularVelocity):
        msg = Twist()
        msg.linear.x = linearVelocity
        msg.angular.z = angularVelocity
        self.cmdVelPublisher.publish(msg)
        #self.get_logger().info('Publishing cmd_vel: "%s", "%s"' % linearVelocity, angularVelocity)

    def scanCallback(self, msg):
        self.valueLaserRaw = {
            'range_min':msg.range_min,
            'range_max':msg.range_max,
            'ranges':list(msg.ranges),
        }

    def batteryStateCallback(self, msg):
        self.valueBatteryState = msg

    def odomCallback(self, msg):
        self.valueOdometry = {
            'position':msg.pose.pose.position,
            'positionX':msg.pose.pose.position.x,
            'positionY':msg.pose.pose.position.y,
            'positionZ':msg.pose.pose.position.z,
            'orientation':msg.pose.pose.orientation,
            'orientationX':msg.pose.pose.orientation.x,
            'orientationY':msg.pose.pose.orientation.y,
            'orientationZ':msg.pose.pose.orientation.z,
            'orientationW':msg.pose.pose.orientation.w,
            'linearVelocity':msg.twist.twist.linear,
            'XlinearVelocity':msg.twist.twist.linear.x,
            'YlinearVelocity':msg.twist.twist.linear.y,
            'ZlinearVelocity':msg.twist.twist.linear.z,
            'angularVelocity':msg.twist.twist.angular,
        }
    def timerCallback(self):
        #print(self.valueLaserRaw["ranges"][-180])
        global lidar_degree
        global lidar_degree1
        global lidar_degree2
        global lidar_degree3
        global lidar_degree4
        lidar_degree=[]
        lidar_degree1=[]
        lidar_degree2=[]
        lidar_degree3=[]
        lidar_degree4=[]
        global average1
        global average2
        global average3
        global average4
        average1 = []
        average2 = []
        average3 = []
        average4 = []
        global av1 
        global av2 
        global av3 
        global av4
        global avall 
        for x in range (0,360):
            lidar_degree.append(self.valueLaserRaw["ranges"][x])
            if x >= 0 and x <= 45 or x >= 316 and x <= 359 :
                lidar_degree1.append(self.valueLaserRaw["ranges"][x]) 
                if x == 0 :
                    average1.append(70*self.valueLaserRaw["ranges"][x])
                elif x >= 1 and x <= 10 or x >= 350 and x <= 359 :
                    average1.append(5*self.valueLaserRaw["ranges"][x])
                # elif x >= 11 and x <= 25 or x >= 335 and x <= 349 :
                #     average1.append(2*self.valueLaserRaw["ranges"][x])
                # elif x >= 26 and x <= 45 or x >= 315 and x <= 334 :
                #     average1.append(0.5*self.valueLaserRaw["ranges"][x])
            elif x >= 46 and x <= 135 :
                lidar_degree2.append(self.valueLaserRaw["ranges"][x])    
                if x == 90 :
                    average2.append(70*self.valueLaserRaw["ranges"][x])
                # elif x >= 46 and x <= 64 or x >= 116 and x <= 135 :
                #     average2.append(0.5*self.valueLaserRaw["ranges"][x])
                # elif x >= 65 and x <= 79 or x >= 101 and x <= 115 :
                #     average2.append(2*self.valueLaserRaw["ranges"][x])
                elif x >= 80 and x <= 89 or x >= 91 and x <= 100 :
                    average2.append(5*self.valueLaserRaw["ranges"][x])
            elif x >= 136 and x <= 225 :
                lidar_degree3.append(self.valueLaserRaw["ranges"][x])    
                if x == 180 :
                    average3.append(70*self.valueLaserRaw["ranges"][x])
                # elif x >= 136 and x <= 154 or x >= 206 and x <= 225 :
                #     average3.append(0.5*self.valueLaserRaw["ranges"][x])
                # elif x >= 155 and x <= 169 or x >= 191  and x <= 205 :
                #     average3.append(2*self.valueLaserRaw["ranges"][x])
                elif x >= 170 and x <= 179 or x >= 181 and x <= 190 :
                    average3.append(5*self.valueLaserRaw["ranges"][x])
            elif x >= 226 and x <= 315 :
                lidar_degree4.append(self.valueLaserRaw["ranges"][x])    
                if x == 270 :
                    average4.append(70*self.valueLaserRaw["ranges"][x])
                # elif x >= 226 and x <= 245 or x >= 296 and x <= 315 :
                #     average4.append(0.5*self.valueLaserRaw["ranges"][x])
                # elif x >= 246 and x <= 260 or x >= 281 and x <= 295 :
                #     average4.append(2*self.valueLaserRaw["ranges"][x])
                elif x >= 261 and x <= 269 or x >= 271 and x <= 280 :
                    average4.append(5*self.valueLaserRaw["ranges"][x])
        else:
            pass    
        av1 = sum(average1)/170
        av2 = sum(average2)/170
        av3 = sum(average3)/170
        av4 = sum(average4)/170
        avall = [av1 ,av2 ,av3 ,av4]
        #lidar_degree[]=self.valueLaserRaw["ranges"][-180]
        #read sensors values
        #print(self.valueBatteryState)
        #print(self.valueLaserRaw)
        #print(self.valueOdometry)

        #calculate command movement
        #linearVelocity = 0.0 #m/s
        #angularVelocity = 0.00 #rad/s
        global recentx
        global recenty
        global theta
       
        recentx = self.valueOdometry['positionX']
        recenty = self.valueOdometry['positionY']

        siny_cosp =  2 * ((self.valueOdometry["orientationW"]*self.valueOdometry["orientationZ"]) + (self.valueOdometry["orientationX"]*self.valueOdometry["orientationY"]))
        cosy_cosp = 1 - ( 2 * ((self.valueOdometry["orientationY"]*self.valueOdometry["orientationY"]) + (self.valueOdometry["orientationZ"]*self.valueOdometry["orientationZ"])))
        theta = math.atan2(siny_cosp,cosy_cosp)
        #print(theta)

        linearVelocity,angularVelocity = robotloop()
        self.publishVelocityCommand(linearVelocity,angularVelocity)
        

def remap(num, in_min, in_max, out_min, out_max):
    return (num - in_min)*(out_max - out_min) / (in_max - in_min) + out_min

def updatestep():
    global step
    step = step + 1
    return step

def stopsign():
    global endSST
    global end
    global step
    endSST = True   
    end = False
    step = 1

def GoTo(centimeter):
    global direction
    global previousx
    global previousy
    global totaldistance
    global deltadistance
    global goaldistance 
    global count
    goaldistance = centimeter/100
    if centimeter >= 0:
        direction = 1
        while totaldistance < goaldistance :    
            deltadistance = math.sqrt(((recentx-previousx)*(recentx-previousx))+((recenty-previousy)*(recenty-previousy)))  
            #print('deltadistane = ',deltadistance)
            #print('recentx = ',recentx)
            #print('recenty = ',recenty)
            #print('previousx = ',previousx)
            #print('previousy = ',previousy)
            totaldistance = totaldistance + deltadistance
            previousx = recentx
            previousy = recenty
            # print(totaldistance)

            if(deltadistance==0.0) and count != 1:
                count = 1
            else:
                pass

            if count == 1:
                linearVelocity = direction * 0.1 #m/s
                angularVelocity = 0.0


            else:
                totaldistance = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0

            return linearVelocity,angularVelocity#,0
        else:
            print("walkreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            count = 0
            direction = 0
            updatestep()
        passwalk = goaldistance - totaldistance
        totaldistance = 0.0    
        return linearVelocity,angularVelocity#,passwalk
    else:
        direction = -1
        while totaldistance > goaldistance :    
            deltadistance = math.sqrt(((recentx-previousx)*(recentx-previousx))+((recenty-previousy)*(recenty-previousy)))  
            #print('deltadistane = ',deltadistance)
            #print('recentx = ',recentx)
            #print('recenty = ',recenty)
            #print('previousx = ',previousx)
            #print('previousy = ',previousy)
            totaldistance = totaldistance - deltadistance
            previousx = recentx
            previousy = recenty
            #print(totaldistance)

            if(deltadistance==0.0) and count != 1:
                count = 1
            else:
                pass

            if count == 1:
                linearVelocity = direction * 0.1 #m/s
                angularVelocity = 0.0

            else:
                totaldistance = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0

            return linearVelocity,angularVelocity#,0
        else:
            print("walkreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            count = 0
            direction = 0
            updatestep()
        passwalk = goaldistance - totaldistance
        totaldistance = 0.0    
        return linearVelocity,angularVelocity#,passwalk

def calibratewalk(centimeters,forwalk):
    global direction
    global previousx
    global previousy
    global totaldistance
    global deltadistance
    global goaldistance 
    global count
    centimeters = centimeters/100
    goaldistance = forwalk
    #print(forwalk)
    if centimeters >= 0:
        direction = -1
        while goaldistance - totaldistance <= -0.001 :    
            deltadistance = math.sqrt(((recentx-previousx)*(recentx-previousx))+((recenty-previousy)*(recenty-previousy)))  
            #print('deltadistane = ',deltadistance)
            #print('recentx = ',recentx)
            #print('recenty = ',recenty)
            #print('previousx = ',previousx)
            #print('previousy = ',previousy)
            totaldistance = totaldistance - deltadistance
            previousx = recentx
            previousy = recenty
            #print(goaldistance-totaldistance)

            if(deltadistance==0.0) and count != 1:
                count = 1
            else:
                pass

            if count == 1:
                linearVelocity = direction * 0.01 #m/s
                angularVelocity = 0.0


            else:
                totaldistance = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0

            return linearVelocity,angularVelocity
        else:
            print("calibrate walkreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            count = 0
            direction = 0
            updatestep()
        totaldistance = 0.0    
        return linearVelocity,angularVelocity
    else:
        direction = 1
        while goaldistance - totaldistance >= 0.001  :    
            deltadistance = math.sqrt(((recentx-previousx)*(recentx-previousx))+((recenty-previousy)*(recenty-previousy)))  
            #print('deltadistane = ',deltadistance)
            #print('recentx = ',recentx)
            #print('recenty = ',recenty)
            #print('previousx = ',previousx)
            #print('previousy = ',previousy)
            totaldistance = totaldistance + deltadistance
            previousx = recentx
            previousy = recenty
            #print(goaldistance - totaldistance)

            if(deltadistance==0.0) and count != 1:
                count = 1
            else:
                pass

            if count == 1:
                linearVelocity = direction * 0.01 #m/s
                angularVelocity = 0.0

            else:
                totaldistance = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0

            return linearVelocity,angularVelocity 
        else:
            print("calibrate walkreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            count = 0
            direction = 0
            updatestep()
        totaldistance = 0.0    
        return linearVelocity,angularVelocity

def TurnTo(degrees):
    global previousturn
    global deltaturn
    global totalturn
    global bount
    global turncase
    passcal = 0.0
    diff = 0.0
    fordir = 0.0
    kp = 2
    #destination config
    destination = degrees
    if destination >= 360  :
        destination = destination % 360
    elif destination <= -360 :
        destination = destination % -360
    else:
        pass

    #print(destination)
    if destination >= 0 :
        if destination >= 180 :
            #print('rotateright')
            turncase = 'right'
            destination = 360 - destination
        elif destination < 180 :
             #print('rotateleft')
            turncase = 'left'   
    elif destination < 0 :
        if destination >= -180 :
            #print('rotateright')
            turncase = 'right'
        elif destination < -180 :
             #print('rotateleft')
            turncase = 'left'  
            destination = -360 - destination

    #find a solution to change orient.z to degree then boom finish
    if degrees >= 0 : 
        while destination-totalturn >= 0.1 :
            startdegree = theta
            if startdegree >= 0.0 :
                startdegree = remap(startdegree,0.0,3.141592653589793238462643383279502,0.0,180)
            else:
                startdegree = remap(startdegree,-3.141592653589793238462643383279502,-0.0,0.0,180) + 180
            #print('after map =',startdegree)

            deltaturn = abs(startdegree - previousturn)
            if deltaturn >= 100:
                deltaturn = abs(360-deltaturn)
            else:
                pass

            totalturn = totalturn + deltaturn
            previousturn = startdegree
            # print(totalturn)

            #กันerror
            b4dif = abs(totalturn-destination) 
            if b4dif > 180:
                b4dif = abs(b4dif - 360) 
            else:
                pass
            #print(b4dif)    
            diff = b4dif/180
            diff = (kp*diff)+0.4
            diff = round(diff,1)

            if(deltaturn<=0.1) and bount != 1:
                bount = 1
            else:
                pass

            if bount == 1:
                if turncase == 'right':
                    #print('rotatingright')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = -0.2 #-1*diff #rad/s
                elif turncase == 'left':
                    #print('rotatingleft')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = 0.2  #diff #rad/s  
            else:
                totalturn = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0        
            return linearVelocity,angularVelocity,0

        else:
            print("turnreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            passcal = destination-totalturn
            bount = 0
            totalturn = 0.0
            updatestep()
            return linearVelocity,angularVelocity,passcal
        

    else :
        while destination-totalturn <= -0.1 :
            startdegree = theta
            if startdegree >= 0.0 :
                startdegree = remap(startdegree,0.0,3.14,0.0,180)
            else:
                startdegree = remap(startdegree,-3.14,-0.0,0.0,180) + 180
            #print('after map =',startdegree)

            deltaturn = abs(startdegree - previousturn)
            if deltaturn >= 100:
                deltaturn = abs(360-deltaturn)
            else:
                pass

            totalturn = totalturn - deltaturn
            previousturn = startdegree
            # print(totalturn)

            #กันerror
            b4dif = abs(totalturn-destination) 
            if b4dif > 180:
                b4dif = abs(b4dif - 360) 
            else:
                pass
            #print(b4dif)    
            diff = b4dif/180
            diff = (kp*diff)+0.4
            diff = round(diff,1)

            if(deltaturn<=0.1) and bount != 1:
                bount = 1
            else:
                pass

            if bount == 1:
                if turncase == 'right':
                    #print('rotatingright')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = -0.2  #-1*diff #rad/s
                elif turncase == 'left':
                    #print('rotatingleft')
                    linearVelocity = 0.0 #m/s
                    angularVelocity =  0.2  #diff #rad/s  
            else:
                totalturn = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0        
            return linearVelocity,angularVelocity,0

        else:
            print("turnreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            passcal = destination-totalturn
            bount = 0
            totalturn = 0.0
            updatestep()
            return linearVelocity,angularVelocity,passcal
    
def calibrate(degrees,cal):
    global previousturn
    global deltaturn
    global totalturn
    global bount
    global turncase
    passcal = 0.0
    diff = 0.0
    fordir = 0.0
    kp = 2
    #destination config
    destination = degrees
    if destination >= 360  :
        destination = destination % 360
    elif destination <= -360 :
        destination = destination % -360
    else:
        pass

    if destination >= 0 :
        if cal >= 0 :
            #print('rotateright')
            turncase = 'right'
        elif cal < 0 :
            #print('rotateleft')
            turncase = 'left'   
    elif destination < 0 :
        if cal >= 0 :
            #print('rotateright')
            turncase = 'left'
        elif cal < 0 :
             #print('rotateleft')
            turncase = 'right'  
    #find a solution to change orient.z to degree then boom finish
    if cal>= 0 : 
        while cal-totalturn >= 0.05 :
            startdegree = theta
            if startdegree >= 0.0 :
                startdegree = remap(startdegree,0.0,3.14,0.0,180)
            else:
                startdegree = remap(startdegree,-3.14,-0.0,0.0,180) + 180
            #print('after map =',startdegree)

            deltaturn = abs(startdegree - previousturn)
            if deltaturn >= 100:
                deltaturn = abs(360-deltaturn)
            else:
                pass

            totalturn = totalturn + deltaturn
            previousturn = startdegree
            #print(totalturn)

            #กันerror
            b4dif = abs(totalturn-destination) 
            if b4dif > 180:
                b4dif = abs(b4dif - 360) 
            else:
                pass
            #print(b4dif)    
            diff = 0.13 #default 1 1.25 need to june

            if(deltaturn<=0.1) and bount != 1:
                bount = 1
            else:
                pass

            if bount == 1:
                if turncase == 'right':
                    #print('rotatingright')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = -0.2  #-1*diff #rad/s
                elif turncase == 'left':
                    #print('rotatingleft')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = 0.2  #diff #rad/s  
            else:
                totalturn = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0        
            return linearVelocity,angularVelocity

        else:
            print("calibrate turnreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            bount = 0
            totalturn = 0.0
            updatestep()
            return linearVelocity,angularVelocity
        

    else :
        while cal-totalturn <= -0.05 :
            startdegree = theta
            if startdegree >= 0.0 :
                startdegree = remap(startdegree,0.0,3.14,0.0,180)
            else:
                startdegree = remap(startdegree,-3.14,-0.0,0.0,180) + 180
            #print('after map =',startdegree)

            deltaturn = abs(startdegree - previousturn)
            if deltaturn >= 100:
                deltaturn = abs(360-deltaturn)
            else:
                pass

            totalturn = totalturn - deltaturn
            previousturn = startdegree
            #print(totalturn)

            #กันerror
            b4dif = abs(totalturn-destination) 
            if b4dif > 180:
                b4dif = abs(b4dif - 360) 
            else:
                pass
            #print(b4dif)    
            diff = 0.13 #default 1 1.25 need to june

            if(deltaturn<=0.1) and bount != 1:
                bount = 1
            else:
                pass

            if bount == 1:
                if turncase == 'right':
                    #print('rotatingright')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = -0.2 #-1*diff #rad/s
                elif turncase == 'left':
                    #print('rotatingleft')
                    linearVelocity = 0.0 #m/s
                    angularVelocity = 0.2 #diff #rad/s  
            else:
                totalturn = 0.0
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0        
            return linearVelocity,angularVelocity

        else:
            print("calibrate turnreach")
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            bount = 0
            totalturn = 0.0
            updatestep()
            return linearVelocity,angularVelocity
def WhatDoIsee():
    global obstacle
    global ob1
    global ob2
    global ob3
    global ob4
    for y in range (0,len(lidar_degree)):
        #print(lidar_degree[y])
        if y >= 0 and y <= 5 or y >= 355 and y <= 359 :
            if lidar_degree[y] != 0.0 and lidar_degree[y] < 0.30 :

                ob1.append(1)
            elif lidar_degree[y] != 0.0 and lidar_degree[y] > 0.30 :
                ob1.append(0)    
        elif y >= 85 and y <= 95 :
            if lidar_degree[y] != 0.0 and lidar_degree[y] < 0.30 :
                ob2.append(1)
            elif lidar_degree[y] != 0.0 and lidar_degree[y] > 0.30 :
                ob2.append(0)
        elif y >= 175 and y <= 185 :
            if lidar_degree[y] != 0.0 and lidar_degree[y] < 0.30 :
                ob3.append(1)
            elif lidar_degree[y] != 0.0 and lidar_degree[y] > 0.30 :
                ob3.append(0)
        elif y >= 265 and y <= 275 :
            if lidar_degree[y] != 0.0 and lidar_degree[y] < 0.30 :
                ob4.append(1)
            elif lidar_degree[y] != 0.0 and lidar_degree[y] > 0.30 :
                ob4.append(0)                          
        
    else :
        if any(ob1) ==  True :
            obstacle[0] = 1
        else :
            obstacle[0] = 0
        if any(ob2) ==  True :
            obstacle[1] = 1
        else :
            obstacle[1] = 0
        if any(ob3) ==  True :
            obstacle[2] = 1
        else :
            obstacle[2] = 0
        if any(ob4) ==  True :
            obstacle[3] = 1
        else :
            obstacle[3] = 0
        
        ob1 = []
        ob2 = []
        ob3 = []
        ob4 = []
        
        #print(obstacle)
        return obstacle
    # WhatDoIsee.func_code = (lambda:None).func_code

def GTNN(node):
    global direction
    global previousx
    global previousy
    global totaldistance
    global deltadistance
    global goaldistance 
    global count
    global forcal
    global end
    end = False
    goaldistance = node*0.3
    if node >= 0 :
        while totaldistance < goaldistance :    
            deltadistance = math.sqrt(((recentx-previousx)*(recentx-previousx))+((recenty-previousy)*(recenty-previousy)))  
            #print('deltadistane = ',deltadistance)
            #print('recentx = ',recentx)
            #print('recenty = ',recenty)
            #print('previousx = ',previousx)
            #print('previousy = ',previousy)
            totaldistance = totaldistance + deltadistance
            previousx = recentx
            previousy = recenty
            # print(totaldistance)
            if(deltadistance==0.0) and count != 1:
                count = 1
            else:
                pass
            if avall[0] != 0.0 and avall[0] < 0. :
                print('Front Obstacle Found ! Can not continue !!')
                print('Break with ',int(totaldistance/0.3),' node complete')
                node_error = goaldistance - totaldistance
                print(node_error,' m left to complete')
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0

                updatestep()
                end = True
                break
            else :    
                if count == 1 :
                    sum_linearvel = 0.1
                    sum_angularvel = 0.0
                    linearVelocity = sum_linearvel
                    angularVelocity = sum_angularvel
                else:
                    totaldistance = 0.0
                    linearVelocity = 0.0 #m/s
                    angularVelocity = 0.0

                return linearVelocity,angularVelocity,end

        else:
            print("GTNN complete with ",node,' node')
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            count = 0
            direction = 0
            updatestep()
            end = True

        passwalk = goaldistance - totaldistance
        totaldistance = 0.0    
        return linearVelocity,angularVelocity,end

    else :
        while totaldistance > goaldistance :    
            deltadistance = math.sqrt(((recentx-previousx)*(recentx-previousx))+((recenty-previousy)*(recenty-previousy)))  
            #print('deltadistane = ',deltadistance)
            #print('recentx = ',recentx)
            #print('recenty = ',recenty)
            #print('previousx = ',previousx)
            #print('previousy = ',previousy)
            totaldistance = totaldistance - deltadistance
            previousx = recentx
            previousy = recenty
            #print(totaldistance)

            if(deltadistance==0.0) and count != 1:
                count = 1
            else:
                pass
            if avall[2] != 0.0 and avall[2] < 0.2 :
                print('Front Obstacle Found ! Can not continue !!')
                print('Break with ',int(totaldistance/0.3),' node complete')
                node_error = goaldistance - totaldistance
                print(node_error,' m left to complete')
                linearVelocity = 0.0 #m/s
                angularVelocity = 0.0

                updatestep()
                end = True
                break
            else :    
                if count == 1 :
                    sum_linearvel = -0.1
                    sum_angularvel = 0.0
                    linearVelocity = sum_linearvel
                    angularVelocity = sum_angularvel
                else:
                    totaldistance = 0.0
                    linearVelocity = 0.0 #m/s
                    angularVelocity = 0.0
                
                return linearVelocity,angularVelocity,end
        else:
            print("GTNN complete with ",node,' node')
            linearVelocity = 0.0 #m/s
            angularVelocity = 0.0
            count = 0
            direction = 0
            updatestep()
            end = True

        passwalk = goaldistance - totaldistance
        totaldistance = 0.0    
        return linearVelocity,angularVelocity,end

def GoHome(startpose):
    global forcal
    global end
    end = False
    if startpose == 00 :  
        if step == 1 :       
            linearVelocity,angularVelocity,forcal = TurnTo(90)    
        # elif step == 2 :
        #     linearVelocity,angularVelocity = calibrate(90,forcal)
        elif step == 2 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 3 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 5 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 4 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 5 :
            end = True
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif startpose == 20 :
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(85)    
        # elif step == 2 :
        #     linearVelocity,angularVelocity = calibrate(90,forcal)
        elif step == 2 :
            linearVelocity,angularVelocity = GTNN(2.05)
        elif step == 3 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 5 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)   
        elif step == 4 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 5 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 8 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 6 :
            linearVelocity,angularVelocity = GTNN(1.3)
        elif step == 7 :
            end = True
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif startpose == 40 :
        if step == 1 :
            linearVelocity,angularVelocity = GTNN(4.2)
        elif step == 2 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 3 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)   
        elif step == 3 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 4 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 6 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 5 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 6 :
            end = True
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif startpose == 2 :
        if step == 1 :
            linearVelocity,angularVelocity = GTNN(1.9)
        elif step == 2 :
            linearVelocity,angularVelocity,forcal = TurnTo(-80)    
        # elif step == 3 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 3 :
            linearVelocity,angularVelocity = GTNN(2)    
        elif step == 4 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 6 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 5 :
            linearVelocity,angularVelocity = GTNN(2.2)
        elif step == 6 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 9 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)   
        elif step == 7 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 8 :
            linearVelocity,angularVelocity,forcal = TurnTo(-80)    
        # elif step == 12 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 9 :
            linearVelocity,angularVelocity = GTNN(1.4)
        elif step == 10 :
            end = True
            linearVelocity = 0.0
            angularVelocity = 0.0    
    elif startpose == 22 :
        if step == 1 :
            linearVelocity,angularVelocity = GTNN(2)    
        elif step == 2 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 3 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 3 :
            linearVelocity,angularVelocity = GTNN(2.2)
        elif step == 4 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 6 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)   
        elif step == 5 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 6 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 9 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 7 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 8 :
            end = True
            linearVelocity = 0.0
            angularVelocity = 0.0 
    elif startpose == 42 :
        if step == 1 :
            linearVelocity,angularVelocity = GTNN(2)
        elif step == 2 :
            linearVelocity,angularVelocity,forcal = TurnTo(80)    
        # elif step == 3 :
        #     linearVelocity,angularVelocity = calibrate(90,forcal)
        elif step == 3 :
            linearVelocity,angularVelocity = GTNN(2)    
        elif step == 4 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 6 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 5 :
            linearVelocity,angularVelocity = GTNN(2.2)
        elif step == 6 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 9 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)   
        elif step == 7 :
            linearVelocity,angularVelocity = GTNN(1.05)
        elif step == 8 :
            linearVelocity,angularVelocity,forcal = TurnTo(-90)    
        # elif step == 12 :
        #     linearVelocity,angularVelocity = calibrate(-90,forcal)
        elif step == 9 :
            linearVelocity,angularVelocity = GTNN(1.2)
        elif step == 10 :
            end = True
            linearVelocity = 0.0
            angularVelocity = 0.0    
    else :
        print('No data')        
        end = True
        linearVelocity = 0.0
        angularVelocity = 0.0 

    return linearVelocity,angularVelocity,end

def calibrate45(direc):
    dirq = direc
    q = 0
    global forcalibrate
    forcalibrate = WhatDoIsee()
    # print('lidar 0 =', lidar_degree[0],'lidar 45 =', lidar_degree[45],'lidar 315 =',lidar_degree[315])
    if dirq == 0 :
        try :
            cos1 = math.degrees(math.acos(lidar_degree[0]/lidar_degree[45]))
            cos2 = math.degrees(math.acos(lidar_degree[0]/lidar_degree[315]))
        except :
            angularVelocity = 0.0
            cos1 = 0
            cos2 = 0
        while abs(cos1-cos2) < 3.0 :
            if cos1+cos2-90<5 and cos1 != 0 and cos2 != 0 :
                angularVelocity = 0.0
                if abs(cos1-cos2) < 5.0 :
                    print("finish")
                    q = 1
                else:
                    pass
            elif lidar_degree[0] > lidar_degree[45] and lidar_degree[0] != 0 and lidar_degree[45] != 0 :
                print('turn left')
                angularVelocity = 1.0 #rad/s
            elif lidar_degree[0] > lidar_degree[315] and lidar_degree[0] != 0 and lidar_degree[315] != 0:
                print('turn right')
                angularVelocity = -1.0 #rad/s
            elif cos1-45 < 0 and cos2-45 > 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = 0.3 #rad/s
            elif cos1-45 > 0 and cos2-45 < 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = -0.3 #rad/s
            print('cos1 = ',cos1)
            print('cos2 = ',cos2)
            linearVelocity = 0.0
            return linearVelocity,angularVelocity
    elif dirq == 2 :
        try :
            cos1 = math.degrees(math.acos(lidar_degree[180]/lidar_degree[225]))
            cos2 = math.degrees(math.acos(lidar_degree[180]/lidar_degree[135]))
        except :
            angularVelocity = 0.0
            cos1 = 0
            cos2 = 0
        while abs(cos1-cos2) < 3.0 :
            if cos1+cos2-90<5 and cos1 != 0 and cos2 != 0 :
                angularVelocity = 0.0
                if abs(cos1-cos2) < 5.0 :
                    print("finish")
                    q = 1
                else:
                    pass
            elif lidar_degree[180] > lidar_degree[225] and lidar_degree[180] != 0 and lidar_degree[225] != 0 :
                print('turn left')
                angularVelocity = 1.0 #rad/s
            elif lidar_degree[180] > lidar_degree[135] and lidar_degree[180] != 0 and lidar_degree[135] != 0:
                print('turn right')
                angularVelocity = -1.0 #rad/s
            elif cos1-45 < 0 and cos2-45 > 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = 0.3 #rad/s
            elif cos1-45 > 0 and cos2-45 < 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = -0.3 #rad/s
            print('cos1 = ',cos1)
            print('cos2 = ',cos2)
            linearVelocity = 0.0
            return linearVelocity,angularVelocity
    elif dirq == 1 :
        try :
            cos1 = math.degrees(math.acos(lidar_degree[90]/lidar_degree[135]))
            cos2 = math.degrees(math.acos(lidar_degree[90]/lidar_degree[45]))
        except :
            angularVelocity = 0.0
            cos1 = 0
            cos2 = 0
        while abs(cos1-cos2) < 3.0 :
            if cos1+cos2-90<5 and cos1 != 0 and cos2 != 0 :
                angularVelocity = 0.0
                if abs(cos1-cos2) < 5.0 :
                    print("finish")
                    q = 1
                else:
                    pass
            elif lidar_degree[90] > lidar_degree[135] and lidar_degree[90] != 0 and lidar_degree[135] != 0 :
                print('turn left')
                angularVelocity = 1.0 #rad/s
            elif lidar_degree[90] > lidar_degree[45] and lidar_degree[90] != 0 and lidar_degree[45] != 0:
                print('turn right')
                angularVelocity = -1.0 #rad/s
            elif cos1-45 < 0 and cos2-45 > 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = 0.3 #rad/s
            elif cos1-45 > 0 and cos2-45 < 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = -0.3 #rad/s
            print('cos1 = ',cos1)
            print('cos2 = ',cos2)
            linearVelocity = 0.0
            return linearVelocity,angularVelocity
    elif dirq == 3 :
        try :
            cos1 = math.degrees(math.acos(lidar_degree[270]/lidar_degree[315]))
            cos2 = math.degrees(math.acos(lidar_degree[270]/lidar_degree[225]))
        except :
            angularVelocity = 0.0
            cos1 = 0
            cos2 = 0
        while abs(cos1-cos2) < 3.0 :
            if cos1+cos2-90<5 and cos1 != 0 and cos2 != 0 :
                angularVelocity = 0.0
                if abs(cos1-cos2) < 5.0 :
                    print("finish")
                    q = 1
                else:
                    pass
            elif lidar_degree[270] > lidar_degree[315] and lidar_degree[270] != 0 and lidar_degree[315] != 0 :
                print('turn left')
                angularVelocity = 1.0 #rad/s
            elif lidar_degree[270] > lidar_degree[225] and lidar_degree[270] != 0 and lidar_degree[225] != 0:
                print('turn right')
                angularVelocity = -1.0 #rad/s
            elif cos1-45 < 0 and cos2-45 > 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = 0.3 #rad/s
            elif cos1-45 > 0 and cos2-45 < 0 and cos1 != 0 and cos2 != 0 :
                print('turn left')
                angularVelocity = -0.3 #rad/s
            print('cos1 = ',cos1)
            print('cos2 = ',cos2)
            linearVelocity = 0.0
            return linearVelocity,angularVelocity

    linearVelocity = 0.0 
    updatestep()
    angularVelocity = 0.00 #rad/s
    return linearVelocity,angularVelocity

def UniPlan():
    global forcal
    global end
    global step
    global case
    global foruniPlan
    global special
    global noforever
    end = False
    if case == 0 :
        foruniPlan = WhatDoIsee()
    else :
        pass
    # print(foruniPlan)
    if foruniPlan[0] == 1 and foruniPlan[1] == 0 and foruniPlan[2] == 0 and foruniPlan[3] == 0 :
        # print("case2")
        case = 2
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(-85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1) 
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 0 and foruniPlan[2] == 0 and foruniPlan[3] == 1 :
        # print("case3")
        case = 3
        if lidar_degree[90] >= 0.3 or special == 1 :
            special = 1
        else :
            special = 0

        if special == 1 :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85) 
            elif step == 2 :
                linearVelocity,angularVelocity,end = GTNN(1) 
            else :
                special = 0
                case = 0
                end = True
                step = 1
                linearVelocity = 0.0
                angularVelocity = 0.0  
        else :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
            else :
                case = 0
                end = True
                step = 1
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 0 and foruniPlan[2] == 1 and foruniPlan[3] == 0 :
        # print("case4")
        case = 4
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 1 and foruniPlan[2] == 0 and foruniPlan[3] == 0 :
        # print("case5")
        case = 5
        if lidar_degree[270] >= 0.3 or special == 1 :
            if noforever != 1 :
                special = 1
            elif noforever == 1 :
                special = 0
            else:
                pass
        else :
            special = 0

        if special == 1 :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 2 :
                linearVelocity,angularVelocity,end = GTNN(1) 
            else :
                noforever = noforever + 1
                special = 0
                case = 0
                end = True
                step = 1
                linearVelocity = 0.0
                angularVelocity = 0.0  
        else :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
            else :
                if noforever == 1 :
                    noforever = 0
                else :
                    pass
                case = 0
                end = True
                step = 1
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 0 and foruniPlan[2] == 0 and foruniPlan[3] == 1 :
        # print("case6")
        case = 6
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1) 
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 0 and foruniPlan[2] == 1 and foruniPlan[3] == 1 :
    #     # print("case7")
        case = 7
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 1 and foruniPlan[2] == 1 and foruniPlan[3] == 0 :
        # print("case8")
        case = 8 
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 1 and foruniPlan[2] == 0 and foruniPlan[3] == 0 :
        # print("case9")
        case = 9
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(-85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1) 
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 1 and foruniPlan[2] == 0 and foruniPlan[3] == 1 :
        # print("case10")
        case = 10
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 0 and foruniPlan[2] == 1 and foruniPlan[3] == 0 :
        # print("case11")
        case = 11
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(-85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1) 
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 0 and foruniPlan[2] == 1 and foruniPlan[3] == 1 :
        # print("case12")
        case = 12
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1)  
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 0 and foruniPlan[1] == 1 and foruniPlan[2] == 1 and foruniPlan[3] == 1 :
        # print("case13")
        case = 13
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 1 and foruniPlan[2] == 1 and foruniPlan[3] == 0 :
        # print("case14")
        case = 14
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(-85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1) 
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 1 and foruniPlan[2] == 0 and foruniPlan[3] == 1 :
        # print("case15")
        case = 15
        if step == 1 :
            linearVelocity = 0.0
            angularVelocity = 0.0
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0 
    elif foruniPlan[0] == 0 and foruniPlan[1] == 0 and foruniPlan[2] == 0 and foruniPlan[3] == 0 :
        # print("case1")
        case = 1
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0
    elif foruniPlan[0] == 1 and foruniPlan[1] == 1 and foruniPlan[2] == 1 and foruniPlan[3] == 1 :
        # print("case0") 
        case = 0
        if step == 1 :
            linearVelocity = 0.0
            angularVelocity = 0.0
        else :
            case = 0
            end = True
            step = 1
            linearVelocity = 0.0
            angularVelocity = 0.0

    print("case = ",case)
    return linearVelocity,angularVelocity,end

def SST():
    global forcal
    global end
    global step
    global case
    global end
    global secondcase
    global thirdcase
    global fourthcase
    global forSST
    global presentpose
    global presentorient
    global endSST


    if case == 0 :
        forSST = WhatDoIsee()
        # print('no')
    else :
        pass

    if forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 0 or case == 2 :
        case = 2
        print("possible case is (2,2) (3,2) (1,1) (0,1) (2,1)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(-1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass

            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 21:
                secondcase = 21
                forSST = [0,0,0,0]
                print("possible case is (2,2) (0,1)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(-1)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass

                    if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 :
                        thirdcase = 211
                        print("possible case is (2,2)")
                        print("but present pose is (2,0)")
                        presentpose = 20
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0  
                    elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 0 :
                        thirdcase = 212
                        print("possible case is (0,1)")
                        print("but present pose is (2,1)")
                        presentpose = 21
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 22
                print("possible case is (2,1)")
                print("but present pose is (1,1)")
                presentpose = 11
                presentorient = 3
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 1 :
                secondcase = 23
                print("possible case is (1,1)")
                print("but present pose is (1,0)")
                presentpose = 10
                presentorient = 0
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 1 :
                secondcase = 24
                print("possible case is (3,2)")
                print("but present pose is (3,1)")
                presentpose = 31
                presentorient = 0
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0

    elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or case == 3 :
        case = 3
        print("possible case is (2,1) (2,2) (3,2) (1,1) (0,1)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass

            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 31
                print("possible case is (3,2)")
                print("but present pose is (2,2)")
                presentpose = 22
                presentorient = 1
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 0 or secondcase == 32 :
                secondcase = 32
                forSST = [0,0,0,0]
                print("possible case is (2,1) (1,1)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(-2)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass

                    if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 :
                        thirdcase = 321
                        print("possible case is (2,1)")
                        print("but present pose is (2,0)")
                        presentpose = 20
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 0 :
                        thirdcase = 322
                        print("possible case is (1,1)")
                        print("but present pose is (2,1)")
                        presentpose = 21
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0        
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 33
                print("possible case is (2,2)")
                print("but present pose is (1,2)")
                presentpose = 12
                presentorient = 1
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 34
                print("possible case is (0,1)")
                print("but present pose is (0,0)")
                presentpose = 0
                presentorient = 2    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0

    elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 0 or case == 4 :
        case = 4
        print("possible case is (2,1) (2,2) (3,2) (1,1)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass
            
            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 41
                print("possible case is (2,1)")
                print("but present pose is (1,1)")
                presentpose = 11
                presentorient = 1
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 42
                print("possible case is (2,2)")
                print("but present pose is (2,1)")
                presentpose = 21
                presentorient = 2
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 43
                print("possible case is (1,1)")
                print("but present pose is (1,0)")
                presentpose = 10
                presentorient = 2
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 44
                print("possible case is (3,2)")
                print("but present pose is (3,1)")
                presentpose = 31
                presentorient = 2     
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0

    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 or case == 5 :
        case = 5
        print("possible case is (0,1) (2,2) (3,2) (1,1) (2,1)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(-1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass

            if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 :
                secondcase = 51
                print("possible case is (0,1)")
                print("but present pose is (0,0)")
                presentpose = 0
                presentorient = 0   
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 0 or secondcase == 52 :
                secondcase = 52
                forSST = [0,0,0,0]
                print("possible case is (2,1) (1,1)") 
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(2)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                   

                    if forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 0 :
                        thirdcase = 521
                        print("possible case is (1,1)")
                        print("but present pose is (2,1)")
                        presentpose = 21
                        presentorient = 3
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 522
                        print("possible case is (2,1)")
                        print("but present pose is (2,0)")
                        presentpose = 20
                        presentorient = 2
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 53
                print("possible case is (2,2)")
                print("but present pose is (1,2)")
                presentpose = 12
                presentorient = 3 
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 1 :
                secondcase = 54
                print("possible case is (3,2)")
                print("but present pose is (2,2)")
                presentpose = 22
                presentorient = 3
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0

    elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or case == 6 :        
        case = 6 
        print("possible case is (4,2) (0,2) (4,0) (1,0) (2,0) (0,0)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(-1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass

            if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 61:
                secondcase = 61
                forSST = [0,0,0,0]
                print("possible case is (0,2) (4,2) (4,0)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(-1)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    print('ok')
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 611
                        print("possible case is (0,2)")
                        print("but present pose is (2,2)")
                        presentpose = 22
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 1 or thirdcase == 612 :
                        thirdcase = 612
                        forSST = [0,0,0,0]
                        print("possible case is (4,0) (4,2)")
                        if step == 3 :
                            linearVelocity,angularVelocity,forcal = TurnTo(85) 
                        elif step == 4 :
                            linearVelocity,angularVelocity,end = GTNN(1) 
                        else :
                            if fourthcase == 0 :
                                forSST = WhatDoIsee()
                                # print(forSST)
                            else :
                                pass
                            
                            if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 6121
                                print("possible case is (4,2)")
                                print("but present pose is (3,0)")
                                presentpose = 30
                                presentorient = 1
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0
                            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 6122
                                print("possible case is (4,0)")
                                print("but present pose is (2,1)")
                                presentpose = 21
                                presentorient = 0
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0                 
            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 1 :
                secondcase = 62
                print("possible case is (1,0)")
                print("but present pose is (0,0)")
                presentpose = 0
                presentorient = 3
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 63
                print("possible case is (0,0)")
                print("but present pose is (0,1)")
                presentpose = 1
                presentorient = 2
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 64
                print("possible case is (2,0)")
                print("but present pose is (2,1)")
                presentpose = 21
                presentorient = 2    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0    

    elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 1 or case == 7 :      
        case = 7
        print("possible case is (1,0) (4,0) (4,2) (0,0) (2,0) (0,2)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass

            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 71:
                secondcase = 71
                forSST = [0,0,0,0]
                print("possible case is (0,2) (4,2)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(1)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass

                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 711
                        print("possible case is (4,2)")
                        print("but present pose is (2,2)")
                        presentpose = 22
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 712
                        print("possible case is (0,2)")
                        print("but present pose is (0,0)")
                        presentpose = 0
                        presentorient = 2
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 72:
                secondcase = 72
                forSST = [0,0,0,0]
                print("possible case is (2,0) (4,0)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(1)
                elif step == 3 :
                    linearVelocity,angularVelocity,forcal = TurnTo(85) 
                elif step == 4 :
                    linearVelocity,angularVelocity,end = GTNN(1) 
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 721
                        print("possible case is (4,0)")
                        print("but present pose is (3,2)")
                        presentpose = 32
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 722
                        print("possible case is (2,0)")
                        print("but present pose is (4,1)")
                        presentpose = 41
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 73
                print("possible case is (1,0)")
                print("but present pose is (1,1)")
                presentpose = 11
                presentorient = 0    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0  
            elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 74
                print("possible case is (0,0)")
                print("but present pose is (1,0)")
                presentpose = 10
                presentorient = 3    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0  
            
    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 or case == 8 :
        case = 8
        print("possible case is (0,0) (2,0) (1,0) (4,0) (4,2) (0,2)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass
            if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 81:
                secondcase = 81
                forSST = [0,0,0,0]
                print("possible case is (0,2) (4,2) (4,0)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(1)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                        thirdcase = 811
                        print("possible case is (0,2)")
                        print("but present pose is (2,2)")
                        presentpose = 22
                        presentorient = 3
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 or thirdcase == 812 :
                        thirdcase = 812
                        forSST = [0,0,0,0]
                        print("possible case is (4,0) (4,2)")
                        if step == 3 :
                            linearVelocity,angularVelocity,forcal = TurnTo(-85) 
                        elif step == 4 :
                            linearVelocity,angularVelocity,end = GTNN(1) 
                        else :
                            if fourthcase == 0 :
                                forSST = WhatDoIsee()
                                # print(forSST)
                            else :
                                pass

                            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 8121
                                print("possible case is (4,0)")
                                print("but present pose is (2,1)")
                                presentpose = 21
                                presentorient = 0
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0
                            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 8122
                                print("possible case is (4,2)")
                                print("but present pose is (3,0)")
                                presentpose = 30
                                presentorient = 1
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0 
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 82
                print("possible case is (0,0)")
                print("but present pose is (0,1)")
                presentpose = 1
                presentorient = 0    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0 
            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                secondcase = 83
                print("possible case is (2,0)")
                print("but present pose is (2,1)")
                presentpose = 21
                presentorient = 0    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0 
            elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 84
                print("possible case is (1,0)")
                print("but present pose is (0,0)")
                presentpose = 0
                presentorient = 1    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0 

    elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 or case == 9 :
        case = 9
        print("possible case is (0,2) (0,0) (2,0) (4,0) (4,2) (1,0)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(-1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass
            if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 or secondcase == 91:
                secondcase = 91
                forSST = [0,0,0,0]
                print("possible case is (0,2) (4,2)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(-1)
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                        thirdcase = 911
                        print("possible case is (4,2)")
                        print("but present pose is (2,2)")
                        presentpose = 22
                        presentorient = 3
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 :
                        thirdcase = 912
                        print("possible case is (0,2)")
                        print("but present pose is (0,0)")
                        presentpose = 0
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 92:
                secondcase = 92
                forSST = [0,0,0,0]
                print("possible case is (4,0) (2,0)")
                if step == 2 :
                    linearVelocity,angularVelocity,end = GTNN(-1)
                elif step == 3 :
                    linearVelocity,angularVelocity,forcal = TurnTo(-85) 
                elif step == 4 :
                    linearVelocity,angularVelocity,end = GTNN(1) 
                else :
                    if thirdcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 921
                        print("possible case is (4,0)")
                        print("but present pose is (3,2)")
                        presentpose = 32
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 922
                        print("possible case is (2,0)")
                        print("but present pose is (4,1)")
                        presentpose = 41
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 :
                secondcase = 93
                print("possible case is (0,0)")
                print("but present pose is (1,0)")
                presentpose = 10
                presentorient = 1    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 0 :
                secondcase = 94
                print("possible case is (1,0)")
                print("but present pose is (1,1)")
                presentpose = 11
                presentorient = 2    
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0      

    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 or case == 10 :
        case = 10
        print("possible case is (4,1) (1,2) (3,0) (1,2) (3,0) (4,1)")
        if step == 1 :
            linearVelocity,angularVelocity,end = GTNN(1)
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass

            if forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 101:
                secondcase = 101
                forSST = [0,0,0,0]
                print("possible case is (1,2) (3,0) (4,1)")
                if step == 2 :
                    linearVelocity,angularVelocity,forcal = TurnTo(85) 
                elif step == 3 :
                    linearVelocity,angularVelocity,end = GTNN(1) 
                else :
                    if fourthcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or thirdcase == 1011 :
                        thirdcase = 1011
                        forSST = [0,0,0,0]
                        print("possible case is (1,2) (4,1)")
                        if step == 4 :
                            linearVelocity,angularVelocity,end = GTNN(1) 
                        else :
                            if fourthcase == 0 :
                                forSST = WhatDoIsee()
                                # print(forSST)
                            else :
                                pass
                            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 10111
                                print("possible case is (4,1)")
                                print("but present pose is (2,2)")
                                presentpose = 22
                                presentorient = 1
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0
                            elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 10112
                                print("possible case is (1,2)")
                                print("but present pose is (0,0)")
                                presentpose = 0
                                presentorient = 2
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0    
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 1012
                        print("possible case is (3,0)")
                        print("but present pose is (4,1)")
                        presentpose = 41
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0     
            elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 or secondcase == 102:
                secondcase = 102
                forSST = [0,0,0,0]
                print("possible case is (3,0) (4,1)")
                if step == 2 :
                    linearVelocity,angularVelocity,forcal = TurnTo(-85) 
                elif step == 3 :
                    linearVelocity,angularVelocity,end = GTNN(1) 
                else :
                    if fourthcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 1021
                        print("possible case is (3,0)")
                        print("but present pose is (2,1)")
                        presentpose = 21
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0    
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 1022
                        print("possible case is (4,1)")
                        print("but present pose is (3,0)")
                        presentpose = 30
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 103
                print("possible case is (1,2)")
                print("but present pose is (2,2)")
                presentpose = 22
                presentorient = 3
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0

    elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 0 or case == 11 :
        case = 11
        print("possible case is (4,1) (1,2) (3,0) (1,2) (3,0) (4,1)")
        if step == 1 :
            linearVelocity,angularVelocity,forcal = TurnTo(85) 
        elif step == 2 :
            linearVelocity,angularVelocity,end = GTNN(1) 
        else :
            if secondcase == 0 :
                forSST = WhatDoIsee()
                # print(forSST)
            else :
                pass
            if forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or secondcase == 111:
                secondcase = 111
                forSST = [0,0,0,0]
                print("possible case is (1,2) (3,0) (4,1)")
                if step == 3 :
                    linearVelocity,angularVelocity,forcal = TurnTo(85) 
                elif step == 4 :
                    linearVelocity,angularVelocity,end = GTNN(1) 
                else :
                    if fourthcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 or thirdcase == 1111 :
                        thirdcase = 1111
                        print("possible case is (1,2) (4,1)")
                        if step == 4 :
                            linearVelocity,angularVelocity,end = GTNN(1) 
                        else :
                            if fourthcase == 0 :
                                forSST = WhatDoIsee()
                                # print(forSST)
                            else :
                                pass
                            if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 11111
                                print("possible case is (4,1)")
                                print("but present pose is (2,2)")
                                presentpose = 22
                                presentorient = 1
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0
                            elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                                fourthcase = 11112
                                print("possible case is (1,2)")
                                print("but present pose is (0,0)")
                                presentpose = 0
                                presentorient = 2
                                stopsign()
                                linearVelocity = 0.0
                                angularVelocity = 0.0    
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 1112
                        print("possible case is (3,0)")
                        print("but present pose is (4,1)")
                        presentpose = 41
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0  
            elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 or secondcase == 112:
                secondcase = 112
                forSST = [0,0,0,0]
                print("possible case is (3,0) (4,1)")
                if step == 3 :
                    linearVelocity,angularVelocity,forcal = TurnTo(-85) 
                elif step == 4 :
                    linearVelocity,angularVelocity,end = GTNN(1) 
                else :
                    if fourthcase == 0 :
                        forSST = WhatDoIsee()
                        # print(forSST)
                    else :
                        pass
                    if forSST[0] == 0 and forSST[1] == 0 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 1121
                        print("possible case is (3,0)")
                        print("but present pose is (2,1)")
                        presentpose = 21
                        presentorient = 0
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0    
                    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 :
                        thirdcase = 1122
                        print("possible case is (4,1)")
                        print("but present pose is (3,0)")
                        presentpose = 30
                        presentorient = 1
                        stopsign()
                        linearVelocity = 0.0
                        angularVelocity = 0.0    
            elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 0 :
                secondcase = 113
                print("possible case is (1,2)")
                print("but present pose is (2,2)")
                presentpose = 22
                presentorient = 3
                stopsign()
                linearVelocity = 0.0
                angularVelocity = 0.0

    elif forSST[0] == 1 and forSST[1] == 0 and forSST[2] == 1 and forSST[3] == 1 or case == 12 :
        case = 12
        print("possible case is (3,1)")
        print("but present pose is (3,1)")
        presentpose = 31
        presentorient = 0
        stopsign()
        linearVelocity = 0.0
        angularVelocity = 0.0    
    elif forSST[0] == 0 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 1 or case == 13 :
        case = 13
        print("possible case is (3,1)")
        print("but present pose is (3,1)")
        presentpose = 31
        presentorient = 0
        stopsign()
        linearVelocity = 0.0
        angularVelocity = 0.0    
    elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 1 and forSST[3] == 0 or case == 14 :
        case = 14
        print("possible case is (3,1)")
        print("but present pose is (3,1)")
        presentpose = 31
        presentorient = 0
        stopsign()
        linearVelocity = 0.0
        angularVelocity = 0.0   
    elif forSST[0] == 1 and forSST[1] == 1 and forSST[2] == 0 and forSST[3] == 1 or case == 15 :
        case = 15
        print("possible case is (3,1)")
        print("but present pose is (3,1)")
        presentpose = 31
        presentorient = 0
        stopsign()
        linearVelocity = 0.0
        angularVelocity = 0.0   

    else :
        linearVelocity = 0.0
        angularVelocity = 0.0     
        end = True

    return linearVelocity,angularVelocity,end,endSST    

def UniPlan2():
    global forcal
    global end
    global step
    global case
    global presentpose
    global presentorient
    global check
    print("presentpose = ",presentpose)
    print("presentorient = ",presentorient)
    
    if presentpose == 0 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(2)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(3)
                end = False  
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 10 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)    
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            elif step == 6 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 7 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            elif step == 8 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 9 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False  
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0                
    elif presentpose == 20 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True    

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(2)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0  
    elif presentpose == 30 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        elif presentorient == 1 and check == False :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
    
        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(2)
                end = False 
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 6 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 7 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0 
    elif presentpose == 40 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(2)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 1 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        
        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(3)
                end = False  
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 11 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        elif presentorient == 3 and check == False :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)    
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            elif step == 6 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 7 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False  
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0 
    elif presentpose == 21 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        
        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False  
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 31 :
        end = True
        linearVelocity = 0.0
        angularVelocity = 0.0
    elif presentpose == 41 :
        if presentorient == 0 and check == False :
            step = 1
            check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 4 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            elif step == 5 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 2 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        elif presentorient == 3 and check == False :
                step = 1  
                check = True
        
        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(3)
                end = False  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 12 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        elif presentorient == 3 and check == False :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(2)
                end = False  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 22 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        elif presentorient == 3 and check == False :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85) 
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 32 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  
        elif presentorient == 1 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        if presentorient == 2 and check == False :
            step = 1
            check = True
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False 
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0
    elif presentpose == 42 :
        if presentorient == 0 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            else :
                step = 1  
                check = True
        elif presentorient == 1 and check == False :
            step = 1
            check = True
        elif presentorient == 2 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1  
                check = True
        elif presentorient == 3 and check == False :
            if step == 1 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(-85)  
            else :
                step = 1
                check = True  

        if check == True :
            if step == 1 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False         
            elif step == 2 :
                linearVelocity,angularVelocity,forcal = TurnTo(85)  
            elif step == 3 :
                linearVelocity,angularVelocity,end = GTNN(1)
                end = False
            else :
                end = True
                linearVelocity = 0.0
                angularVelocity = 0.0

    return linearVelocity,angularVelocity,end

def robotloop():
    global forcal
    global forwalk
    global step
    global turninterval
    global stop
    global forob
    global sum_angularvel
    global sum_linearvel
    global end
    global presentpose
    global presentorient
    global endSST

    listdirection = [-1 ,1]
    Far1 = 0.0
    Near1 = 0.0
    Far2 = 0.0
    Near2 = 0.0
    #WhatDoIsee()
    # forob = WhatDoIsee()
    # if forob[0] == 0 :
    #     avall[0] = 0
    # if forob[1] == 0 :
    #     avall[1] = 0
    # if forob[2] == 0 :
    #     avall[2] = 0
    # if forob[3] == 0 :
    #     avall[3] = 0
    #print(forob)
    # print(avall)
    # print(avall[0])
    # linearVelocity,angularVelocity,end = UniPlan()
    if endSST == False :
        linearVelocity,angularVelocity,end,endSST = SST()
    elif endSST == True and end == False :
        linearVelocity,angularVelocity,end = UniPlan2()
    elif end == True and endSST == True :
        angularVelocity = 0.0
        linearVelocity = 0.0
        print('True end')
    
    return linearVelocity,angularVelocity 

def robotStop():
    node = rclpy.create_node('tb3Stop')
    publisher = node.create_publisher(Twist, 'cmd_vel', 1)
    msg = Twist()
    msg.linear.x = 0.0
    msg.angular.z = 0.0
    publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    tb3ControllerNode = Turtlebot3Controller()
    print('tb3ControllerNode created')
    try:
        #Spin the node in the same thread if only callbacks are used 
        rclpy.spin(tb3ControllerNode)


       #TODO: find method to spin the node asychronously, so that linear non-looped task can be programmed.
    except KeyboardInterrupt:
       pass
    tb3ControllerNode.publishVelocityCommand(0.0,0.0)
    tb3ControllerNode.destroy_node()
    robotStop()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

