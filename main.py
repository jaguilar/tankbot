#! /usr/bin/env pybricks-micropython

from controller import Controller
from micropython import const
from pybricks.ev3devices import Motor
from pybricks.tools import wait
from pybricks.parameters import Port

motor_r = Motor(Port.A)
motor_l = Motor(Port.D)

CONTROLLER_FILENAME = (
    "/dev/input/by-id/usb-Razer_Razer_Wolverine_V2_Pro_2.4-event-joystick"
)


def scale_joystick(value):
    _JOYSTICK_SCALE = 2**15
    sign = value < 0 and -1 or 1
    raw = float(value) / _JOYSTICK_SCALE
    return sign * raw * raw


def main():
    c = Controller()
    c.watch(CONTROLLER_FILENAME)

    while True:
        # Note: negative joystick y is forward.
        frac_power = -scale_joystick(c.axis_lstick_y())
        frac_lr = scale_joystick(c.axis_lstick_x())

        # Note: if frac_lr is negative, we're trying to drive left. That
        # means that the power of the left motor should be decreased.
        power_l = int(frac_power * 100 + frac_lr * 20)
        power_r = int(frac_power * 100 - frac_lr * 20)

        if power_l > 100:
            excess = power_l - 100
            power_r -= excess
            power_l -= excess
        if power_l < -100:
            excess = -100 - power_l
            power_r += excess
            power_l += excess
        if power_r > 100:
            excess = power_r - 100
            power_l -= excess
            power_r -= excess
        if power_r < -100:
            excess = -100 - power_r
            power_l += excess
            power_r += excess

        motor_l.dc(power_l)
        motor_r.dc(power_r)
        wait(15)


if __name__ == "__main__":
    main()
