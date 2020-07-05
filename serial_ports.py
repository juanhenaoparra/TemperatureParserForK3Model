from serial.tools import list_ports


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    return list(map(lambda listportinfo: listportinfo.device, list_ports.comports()))
