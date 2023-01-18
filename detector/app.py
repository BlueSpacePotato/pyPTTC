"""

The “OBJECT” is made of:
1) OBJ_ID – field of object identifier, each object has own unique number
2) DLEN – field of data length, size of object
3) DATA – field includes one basic data type or container. DATA field includes one of these two components
a) one of the basic data: cstr, int8, uint8, int16, uint16, int32, uint32, float, date_time, serial, bool (Fig. a),
b) encapsulated data - container for other objects. It contains several other objects. (Fig. b).

"""


import serial
import signal
import threading
import sys
import logging
import traceback
from decimal import Decimal

from serial.tools.list_ports import comports



class Detector:

    DRIVER_NAME = 'FTDI'
    BAUDRATE = 57600
    DATA_BITS = 8
    STOP_BIT = 1
    PARITY = None
    FLOW_CONTROLL = None
    TIMEOUT = 0.2

    def __init__(self, portname='auto'):

        self._serial = serial.Serial()
        if portname == 'auto':
            try:
                self._serial.port = self.find_com_port()
            except ConnectionError as ce:
                print('Stepper driver not found!')
                self._serial.port = None
        else:
            self._serial.port = portname

        self._serial.baudrate = self.BAUDRATE
        self._serial.timeout = self.TIMEOUT

        self._connection_error = False
        self._status = 1
        self._context_depth = 0

    def __enter__(self):
        if not self._connection_error:
            try:
                if self._context_depth == 0 and not self._serial.port is None and not self._serial.is_open:
                    self._serial.open()

            except ConnectionError as ex:
                self._connection_error = True
                logging.error("stage control: error entering context: \n" + str(ex))
                raise
            self._context_depth += 1
            logging.debug(f"stage control: entered context at level {self._context_depth}")
            return self
        else:
            return None

    def __exit__(self, exc, value, trace):
        logging.debug(f"stage control: leaving context from level {self._context_depth}")
        self._context_depth -= 1
        if self._context_depth == 0:
            self._serial.close()
        if exc:
            if exc is type(ConnectionError): self._connection_error = True
            logging.error("".join(traceback.format_exception(exc, value=value, tb=trace)))
        return True


    def find_com_port(self) -> str:
        ports = comports()
        for i in ports:
            if i.manufacturer == self.DRIVER_NAME:
                return i.device
        else:
            raise ConnectionError(f'No stepper driver found - may you need to define the DRIVER_NAME to one of them: {[i.manufacturer for i in ports]}')

    def write(self, mes):
        self._serial.write(mes)
        return self._serial.readline()

    def get_service_mode(self):
        """
        command is used to check if service mode is enabled /disabled.
        """
        res = self.write(b'$04000004F300#')
        print(res)

    def set_service_mode(self):
        """
        command is used to set service mode, enabled/disable
        """
        res = self.write(b'$0410000D10000009101B0005016F96#')
        print(res)

    def set_transparent_mode(self):
        """
        command is used to set transparent mode, enabled/disable
        """
        pass

    def get_device_iden(self):
        """
        command is used to read configuration data
        """
        pass

    def set_divice_iden(self):
        """
        command is used to set and save configuration data
        """
        pass


if __name__ == '__main__':
    with Detector() as x:
        x.get_service_mode()
        x.set_service_mode()
        x.set_service_mode()
        x.get_service_mode()
