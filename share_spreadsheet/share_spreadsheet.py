import gspread
from oauth2client.service_account import ServiceAccountCredentials
import rclpy
from rclpy.node import Node
import std_msgs
from std_msgs.msg import Bool
from std_msgs.msg import Int32

class Lidar_Import(Node):
    def __init__(self):
        super().__init__("lidar_import")
        self.lidar_value = Bool()
        self.lidar_value.data = False
        self.closest_num = 0
        self.sequence_num = 0
        self.shinkuma_pub = self.create_publisher(Bool, "shinkuma_spread", 1)
        self.closest_sub = self.create_subscription(Int32, "closest_waypoint", self.closestCallback, 1)
        self.sequence_sub = self.create_subscription(Int32, "sequence_num", self.sequenceCallback, 1)

    def get_spread_info(self):
        scope = ["****スプレッドシートのURL*****",
         "****ドライブのURL****"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name("<JSONファイル>.json", scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("スプレッドシートの名前").sheet1

        bool_value = bool(wks.acell("A1"))

        if (self.sequence_num == 2) and (self.closest_num < 5):
            self.lidar_value.data = bool_value
        else:
            self.lidar_value.data = False

    def closestCallback(self, msg):
        self.closest_num = msg.data

    def sequenceCallback(self, msg):
        self.sequence_num = msg.data

    def run(self):
        self.get_spread_info()
        self.shinkuma_pub.publish(self.lidar_value)

