from datetime import datetime
import pigpio


def return_true(pi: pigpio.pi):
    """
    does nothing
        :param pi: pycamera object
    """
    pass
    # s, b, d = pi.bsc_i2c(I2C_ADDR, int(255).to_bytes(1, 'big'))


def return_false(pi: pigpio.pi):
    """
    does nothing.
        :param pi: pycamera object
    """
    pass
    # s, b, d = pi.bsc_i2c(I2C_ADDR, int(0).to_bytes(1, 'big'))


def printcmds(argument, preamble=""):
    """
    Helper method to print bytes array received from i2c as hex values.
        :param argument: raw cmds from i2c in byte array
        :param preamble='': text to print before printing argumemt.
    """
    print(
        str(datetime.now())
        + " | "
        + preamble
        + "cmd=["
        + " ".join("0x{:02x}".format(x) for x in argument)
        + "]"
    )

def print_not_implemented(argument, preamble=""):
    """
    Helper method to print bytes array received from i2c as hex values.
        :param argument: raw cmds from i2c in byte array
        :param preamble='': text to print before printing argumemt.
    """
    print(
        str(datetime.now())
        + " | "
        + "!!!NOT IMPLEMENTED!!! "
        + preamble
        + "cmd=["
        + " ".join("0x{:02x}".format(x) for x in argument)
        + "]"
    )


def printreturn(data, preamble=""):
    """
    Helper method to print bytes array thta will be sent over i2c.
        :param data: 
        :param preamble='': text to print before printing data.
    """
    print(str(datetime.now()) + " | " + preamble + "DATA SENT: {}".format(data))
