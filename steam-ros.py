#!/usr/bin/env python3

from evdev import InputDevice, categorize, ecodes
import asyncio
import time

class SteamRos(object):
    def __init__(self):
        self.gamepad = InputDevice('/dev/input/by-id/usb-Valve_Software_Steam_Controller-if01-event-joystick')
        self.deadmans = [ecodes.BTN_THUMB, ecodes.BTN_THUMB2]
        self.buttons = {
            ecodes.BTN_THUMB: False,
            ecodes.BTN_THUMB2: False,
            }
        self.axes = {
            4: 0,
            16: 0,
        }

    def __repr__(self):
        return str(self.gamepad.capabilities())
    
    def check_active(self):
        return all([self.buttons[deadman] for deadman in self.deadmans])

    def update(self):
        for event in self.gamepad.read_loop():
            if event.type == ecodes.BTN_THUMB:
                print(categorize(event))

    def button_callback(self, event):
        print(self.buttons)
        print('active = {}'.format(self.check_active()))

    def axis_callback(self, event):
        if not self.check_active():
            return
        print(self.axes)

    async def update_async(self):
        async for event in self.gamepad.async_read_loop():
            if event.type == ecodes.EV_KEY and event.code in self.buttons:
                self.buttons[event.code] = bool(event.value)
                self.button_callback(event)
            elif event.type == ecodes.EV_ABS and event.code in self.axes:
                self.axes[event.code] = int(event.value)
                self.axis_callback(event)

if __name__ == "__main__":
    try:
        print(ecodes)
        s = SteamRos()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.update_async())
    except KeyboardInterrupt:
        pass
