#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_iphone')
import rospy

from geometry_msgs.msg import Twist

import tornado.ioloop
import tornado.web
import tornado.websocket

from threading import Thread

MAX_SPEED = 0.5
MAX_ROT = 0.5
pub = None

def go(angular, linear):
    try:
        print(angular, linear)
        twist = Twist()
        twist.linear.x = MAX_SPEED * linear
        twist.linear.y = twist.linear.z = 0
        twist.angular.x = twist.angular.y = 0
        twist.angular.z = MAX_ROT * angular
        pub.publish(twist)
    except Exception as e:
        print(e)

def stop():
    go(0, 0)

class PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/html')
        with open(roslib.packages.resource_file('teleop_twist_iphone', 'data', 'page.html'), 'r') as f:
            self.write(f.read())

class CrossHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        with open(roslib.packages.resource_file('teleop_twist_iphone', 'data', 'cross.png'), 'r') as f:
            self.write(f.read())

class SocketHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        # convert and clamp input
        x, y = [max(-1, min(float(a), 1)) for a in message.split(',')]
        go(x, y)

    def on_close(self):
        stop()

def wait_for_exit():
    rospy.spin()
    tornado.ioloop.IOLoop.instance().stop()

def main():
    global pub
    pub = rospy.Publisher('cmd_vel', Twist)
    rospy.init_node('teleop_twist_iphone')

    server = tornado.web.Application([('/', PageHandler), ('/cross.png', CrossHandler), ('/socket', SocketHandler)])
    server.listen(3000)
    Thread(target = wait_for_exit).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    try:
        main()
    finally:
        stop()
