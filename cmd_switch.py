import binascii
import io
import struct
import threading
import time
from datetime import datetime
from time import gmtime, strftime

from ErrorCode import ErrorCode
from helperfunc import (
    printcmds,
    printreturn,
    return_false,
    return_true,
    print_not_implemented,
)


class cmd_switch(object):
    def __init__(self, so):
        self.so = so

    def action_for_cmd(self, argument: bytes):
        """Dispatch method"""
        # prefix the method_name with 'number_' because method names
        # cannot begin with an integer.
        method_name = "cmd_" + "0x{:02x}".format(argument[0])
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, self.default)
        # Call the method as we return it
        return method(argument)

    def default(self, argument: bytes):
        printcmds(argument, "CMD Not Implemented: ")
        return ErrorCode.UnknownCommand
        # print(int.from_bytes(argument[1:], "big"))

    def cmd_0x01(self, argument: bytes):
        # i2c test, alway return 0x50
        val = 0x50
        s, b, d = self.so.pi.bsc_i2c(self.so.I2C_ADDR, int(val).to_bytes(1, "big"))
        printreturn(val)
        return ErrorCode.Ok

    def cmd_0x03(self, argument: bytes):
        # last error
        val = self.so.lasterror
        s, b, d = self.so.pi.bsc_i2c(self.so.I2C_ADDR, int(val).to_bytes(1, "big"))
        printreturn(val)
        return self.so.lasterror

    def cmd_0x21(self, argument: bytes):
        # set time
        newtime = int.from_bytes(argument[1:], "big")
        print("Previous Time:\t {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        time.clock_settime(time.CLOCK_REALTIME, newtime)
        print(
            "New Time: \t {} ({})".format(
                datetime.utcfromtimestamp(newtime).strftime("%Y-%m-%d %H:%M:%S"),
                newtime,
                ss,
            )
        )
        return ErrorCode.Ok

    def cmd_0x22(self, argument: bytes):
        print_not_implemented(argument, "0x22 not implemented")
        return ErrorCode.Ok
