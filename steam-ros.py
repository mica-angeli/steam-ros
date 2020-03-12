#!/usr/bin/env python3

from evdev import InputDevice, categorize, ecodes
import asyncio
import time

class SteamRos(object):
    def __init__(self):
        self.gamepad = InputDevice('/dev/input/by-id/usb-Valve_Software_Steam_Controller-if01-event-joystick')
        self.active = False
        self.buttons = {
            ecodes.ecodes['BTN_THUMB']: False,
            ecodes.ecodes['BTN_THUMB2']: False,
            }

    def __repr__(self):
        return str(self.gamepad.capabilities())
    
    def update(self):
        for event in self.gamepad.read_loop():
            if event.type == ecodes.BTN_THUMB:
                print(categorize(event))

    def button_callback(self, event):
        print(self.buttons)

    async def update_async(self):
        async for event in self.gamepad.async_read_loop():
            if event.code in self.buttons:
                self.buttons[event.code] = bool(event.value)
                self.button_callback(event)
            else:
                pass
                # print(repr(event))

if __name__ == "__main__":
    try:
        print(ecodes)
        s = SteamRos()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.update_async())
    except KeyboardInterrupt:
        pass
