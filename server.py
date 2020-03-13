#!/usr/bin/env python3
import datetime
import os
import threading
import time

import pigpio

from helperfunc import printcmds
from cmd_switch import cmd_switch
from ErrorCode import ErrorCode


class I2Cserver(object):
    """
    A class used to repesent the CUAVA I2C I2C slave server on a rasp pi

    ...

    Attributes
    ----------
    I2C_ADDR : hex
        I2C address of the I2C. (i.e. slave address)
    usbpath : str
        full path of USB mass storage device
    pi : pigpio.pi()
        an instance of the pigpio.pi() object for implementing rasppi bsc slave.
    e : pigpio.pi.event_callback
        reference to callback that to responds to bsc ic2 events.
    sw : cmd_switch
        object used to parse and generate reponses to I2C commands.
    cam : picamera.PiCamera()
        an instance of the picamera class to control rasp pi cameras.

    Methods
    -------
    __i2c(id, tick)
        function that is linked to callback that responds to bsc ic2 events

    """

    I2C_ADDR = 0x31

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

        self.pi = pigpio.pi()

        # Respond to BSC slave activity
        self.e = self.pi.event_callback(
            pigpio.EVENT_BSC, lambda id, tick: self.__i2c(id, tick)
        )

        # Configure BSC as I2C slave
        self.pi.bsc_i2c(self.I2C_ADDR)

        # cmd switch
        self.sw = cmd_switch(self)

        self._lock = threading.Lock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.e.cancel()
        self.pi.bsc_i2c(0)  # Disable BSC peripheral
        self.pi.stop()

    def __i2c(self, id, tick):
        """Function that is linked to callback that responds to bsc ic2 events.

        Retives data from I2C input buffer, if data is found it is bassed to CMD paraser.
+
        Parameters
        ----------
        id : int
            event id that generated callback
        tick : 32 bit
            The number of microseconds since boot WARNING: this wraps around from 4294967295 to 0 roughly
            every 72 minutes

        Raises
        ------
        None
            Try catches any exception, and prints error. Ideally this code should never run.
        """
        try:
            s, b, d = self.pi.bsc_i2c(self.I2C_ADDR)
            if b:
                # printcmds(
                #     d, "CMD Recieved: FR={} received={}: ".format(s & 0xfff, d))
                self.lasterror = self.sw.action_for_cmd(d)
        except Exception as err:
            print(
                str(datetime.datetime.now()) + " | " + "Callback Error: {0}".format(err)
            )
            self.lasterror = ErrorCode.CommandError


def main():
    # with daemon.DaemonContext():
    with I2Cserver() as runningI2CServer:
        if not runningI2CServer.pi.connected:
            print("PIGPIO not connected. Exiting.")
            exit()
        print(
            str(datetime.datetime.now())
            + " | "
            + "I2C Server Started with i2c address "
            + "0x%0.2X" % runningI2CServer.I2C_ADDR
            + ". Waiting for CMD from OBC."
        )
        try:
            # time.sleep(10)
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nTerminated by KeyboardInterrupt.")
            exit()
    # os.system('systemctl poweroff')


if __name__ == "__main__":
    main()
