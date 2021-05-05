#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/15 上午11:26
# @Author : Chenan_Wang
# @File : updatePID_node.py
# @Software: CLion

from pid.cfg import PIDConfig
from dynamic_reconfigure.server import Server
from std_msgs.msg import Float32MultiArray
import rospy


class UpdatePID():

    def __init__(self):
        rospy.init_node("update_pid")

        rospy.on_shutdown(self.shutdown)

        # 执行频率
        rate = rospy.Rate(20)

        # 声明一个消息发布者, 将消息发布到driver
        self.publisher_pid = rospy.Publisher("/pid", Float32MultiArray, queue_size=100)

        # 启动参数配置服务器         当参数变化时的回调
        Server(PIDConfig, self.dynamic_callback)

        # 打印一个启动成功的日志
        rospy.loginfo("updatePID_node start success! Bring up rqt_reconfigure to control the pid ...")

        # 让ros节点跑起来
        while not rospy.is_shutdown():
            rate.sleep()

    def dynamic_callback(self, config, level):
        """
        当参数发生变化时的回调函数
        :param config: 配置文件
        :param level: 修改的状态
        :return:
        """
        # 封装消息
        kp = config["p"]
        ki = config["i"]
        kd = config["d"]

        pid_msg = Float32MultiArray()
        pid_msg.data.append(kp)
        pid_msg.data.append(ki)
        pid_msg.data.append(kd)

        # 将消息发布出去
        self.publisher_pid.publish(pid_msg)

        print (config, level)
        return config

    def shutdown(self):
        print ("stop robot ...")


if __name__ == '__main__':
    UpdatePID()