import vcgencmd
from numpy import random
from .helperfunc import printcmds, printreturn, return_true, return_false
from .ErrorCode import ErrorCode


class telemetery_switch(object):

    cmds = {
        "0x01": ("BlockSize", 1),
        "0x10": ("ResolutionX", 2),
        "0x11": ("ResolutionY", 2),
        "0x12": ("ExposureMode", 2),
        "0x13": ("ExposureTime", 4),
        "0x14": ("ShutterSpeedValue", 4),
        "0x16": ("ExposureTime", 2),
        "0x17": ("ISOSpeedRatings", 2),
        "0x15": ("MeteringMode", 2),
        "0x16": ("UnixTime", 4),
        "0x21": ("NumBlocksJPEG", 4),
        "0x22": ("ImageSizeJPEG", 4),
        "0x23": ("ImageCRCJPEG", 4),
        "0x31": ("NumBlocksRAW", 4),
        "0x32": ("ImageSizeRAW", 4),
        "0x33": ("ImageCRCRAW", 4),
    }

    def __init__(self, so):
        self.so = so

    def action_for_cmd(self, argument: bytes, camdata_attr: str):
        """
        Dispatch method for telemetry commands. 
            :param self: self
            :param argument: byte array of raw cmds recived from i2c.
        """

        cmd_revc = "0x{:02x}".format(argument)
        (tag, numbytes) = self.cmds[cmd_revc]
        try:
            val = getattr(self.so, camdata_attr)[
                getattr(self.so, camdata_attr + "_index")
            ][tag]
            ec = ErrorCode.Ok
        except IndexError as err:
            val = 0
            ec = ErrorCode.ImageIndexNotValid
        s, b, d = self.so.pi.bsc_i2c(
            self.so.I2C_ADDR, int(val).to_bytes(numbytes, "big")
        )
        printreturn(val)
        return ec

    def printruststructs(self):
        """
        Not used in server. Function generates rust code to be used in partner 
        Kubos app to match cmds structure used here.
            :param self: self
        """

        types = {1: "u8", 2: "u16", 4: "u32"}
        print("make_telemetry!(")
        for k, (tag, numbytes) in self.cmds.items():
            print("\t/// {}".format(tag))
            print(
                "\t{} => {{vec![{}], {}, {}}},".format(
                    tag, k, numbytes, types[numbytes]
                )
            )
        print(");")

        print("make_telemetry!(")
        for k, (tag, numbytes) in self.cmds.items():
            print("\t{}".format(tag))
        print(");")
