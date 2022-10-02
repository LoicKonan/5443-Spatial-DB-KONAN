# calculate trajetory
# @author: Mashoko Blessing
# @ http://www.facebook.com/blessing.mashcom
# @mashcom digimedia http://www.hookd-up.com

from math import sin, cos, pi


def calculateTraf(angle, velocity):

    # defining gravity
    gravity = 9.8

    # converting angle to radians
    angle = angle * pi / 180

    # calculating horizontal and vertical components of the velocity
    velocity_h = velocity * cos(angle)
    velocity_v = velocity * sin(angle)

    # computing time and distance of flight
    time_of_flight = 2 * float(velocity_v) / gravity
    range = float(time_of_flight) * velocity_h

    return range, time_of_flight


print("please enter the angle you are dealing with")
angle = input()

print("enter the velocity")
velocity = input()

ans_range, ans_tof = calculateTraf(float(angle), float(velocity))
print(
    "the range is %.1f metres and time of flight is %.0f  seconds"
    % (ans_range, ans_tof)
)
