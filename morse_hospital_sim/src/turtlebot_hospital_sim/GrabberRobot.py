import rospy
from morse.builder import *
from turtlebot_hospital_sim.Turtlebot import Turtlebot
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger
from std_msgs.msg import String
import time

PATH = "/".join(__file__.split("/")[:-3])

def formatlog(severity, who, loginfo, skill, params):
    global simulation_init_time
    return ('['+severity+'],'+
               who+','+
               loginfo+','+
               skill+','+
               params)

class GrabberRobot(FakeRobot):
    def __init__(self, name, path=f"{PATH}/models/turtlebot.blend"):
        FakeRobot.__init__(self, name=name)
        # Turtlebot.__init__(self, name=name, path=path)
        # Turtlebot.add_to_simulation(self, battery_discharge_rate=0.0)
        self.name = name
        self.path = path
        self.item_exchanger = ItemExchanger(name=name, obj="sphere")
        self.sub_comms = rospy.Subscriber("/"+name+"/comms", String, self.comms)
        self.sub_comms = rospy.Subscriber("/"+name+"/comms", String, self.comms)
        self.pub_action = rospy.Publisher(f"{name}/action", String, queue_size=5)
        self.pub_invent = rospy.Publisher(f"/inventory", String, queue_size=5)
        self.pub_log = rospy.Publisher("/log", String, queue_size=5)
        self.pub_dum1 = rospy.Publisher("/"+name+"/comms", String, queue_size=5)
        self.add_pose_sensor()

    def add_to_simulation(self, x=-19, y=-3, z=0,
                          x_rot=0, y_rot=0, z_rot=0):
        self.translate(x, y, z)
        self.rotate(x_rot, y_rot, z_rot)

    def add_pose_sensor(self):
        # Current position
        self.pose = Pose()
        self.pose.frequency(10)
        self.append(self.pose)
        self.pose.add_interface('ros', topic=f"{self.name}/pose", frame_id="map")

    def comms(self, com_data):
        rospy.logwarn(com_data)
        log = String()
        # log.data = self.name + ": received sample from "+str(com_data)+" at "+str(rospy.get_rostime())
        # log.data = self.name + ","+ str(rospy.get_rostime()) + ",received sample from "+str(com_data)
        log.data = formatlog('info',
            self.name,
            'sync',
            'wait-message',
            '(status=message-received)')
        print(self.name)
        print(log.data)
        print(com_data.data)
        print(self.name)
        self.pub_log.publish(log)
        self.pub_invent.publish(str(log))
        pub_str = String()
        pub_str.data = "r1"
        self.pub_comms = rospy.Publisher(f"{pub_str.data}/comms", String, queue_size=5)
        print(pub_str.data)
        rate = rospy.Rate(.5)
        for i in range(0,5):
            rospy.loginfo(pub_str)
            self.pub_comms.publish(pub_str)
            rate.sleep()
        pub_str.data = "r1 reached goal"
        self.pub_invent.publish(pub_str)
