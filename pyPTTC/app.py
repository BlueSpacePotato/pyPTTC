"""

"""

import serial
import signal
import threading
import sys
import logging
import traceback
from decimal import Decimal

from serial.tools.list_ports import comports

from crc import Configuration, Calculator

# data types
DTYPE_CONTAINER = 0
DTYPE_CSTR = 1
DTYPE_INT8 = 2
DTYPE_UINT8 = 3
DTYPE_INT16 = 4
DTYPE_UINT16 = 5
DTYPE_INT32 = 6
DTYPE_UINT32 = 7
DTYPE_FLOAT = 8
DTYPE_DATE_TIME = 9
DTYPE_SERIAL = 10
DTYPE_BOOL = 11

OBJECT_LENGTH = [None, None, 5, 5, 6, 6, 8, 8, 8, 12, 8, 5]

# get/set - for all types of modules
GET_SERVICE_MODE = 1024
SET_SERVICE_MODE = 1040
SET_TRANSPARENT_MODE = 1104
GET_DEVICE_IDEN = 32
SET_DEVICE_IDEN = 48

# get/set - Commands for module without memory - configuration is stored in the PTTC controller.
GET_SMARTTEC_CONFIG = 1280
SET_SMARTTEC_CONFIG = 1296
GET_SMARTTEC_MONITOR = 1312
GET_SMARTTEC_MOD_NO_MEM_IDEN = 1536
SET_SMARTTEC_MOD_NO_MEM_IDEN = 1552
GET_SMARTTEC_MOD_NO_MEM_DEFAULT = 1568
SET_SMARTTEC_MOD_NO_MEM_DEFAULT = 1584
GET_SMARTTEC_MOD_NO_MEM_USER_SET = 1600
SET_SMARTTEC_MOD_NO_MEM_USER_SET = 1616
GET_SMARTTEC_MOD_NO_MEM_USER_MIN = 1632
SET_SMARTTEC_MOD_NO_MEM_USER_MIN = 1648
GET_SMARTTEC_MOD_NO_MEM_USER_MAX = 1664
SET_SMARTTEC_MOD_NO_MEM_USER_MAX = 1680

# get/set - Commands for module with memory - configuration is stored in the module memory
GET_MODULE_IDEN = 2048
SET_MODULE_IDEN = 2064
GET_MODULE_DEFAULT = 2112
SET_MODULE_DEFAULT = 2128
GET_MODULE_USER_SET = 2144
SET_MODULE_USER_SET = 2160
GET_MODULE_USER_MIN = 2176
SET_MODULE_USER_MIN = 2192
GET_MODULE_USER_MAX = 2208
SET_MODULE_USER_MAX = 2224

# get/set - Commands for module SMIPDC - configuration is stored in the module memory
GET_MODULE_SMIPDC_MONITOR = 2560
GET_MODULE_SMIPDC_DEFAULT = 2688
SET_MODULE_SMIPDC_DEFAULT = 2704
GET_MODULE_SMIPDC_USER_SET = 2720
SET_MODULE_SMIPDC_USER_SET = 2736
GET_MODULE_SMIPDC_USER_MIN = 2752
SET_MODULE_SMIPDC_USER_MIN = 2768
GET_MODULE_SMIPDC_USER_MAX = 2784
SET_MODULE_SMIPDC_USER_MAX = 2800
LOAD_MODULE_SMIPDC_PARAMS = 2880
STORE_MODULE_SMIPDC_PARAMS = 2896

# object list - container
DEVICE_IDEN = 256
DEVICE_CHECK = 512
SERVICE_MODE = 4096
TRANSPARENT_MODE = 5120
SMARTTEC_CONFIG = 6144
SMARTTEC_MONITOR = 7168
MODULE_IDEN = 8192
MODULE_CHECK = 8704
MODULE_BASIC_PARAMS = 9216
MODULE_USER_SET_BANK = 10240
MODULE_SMIPDC_MONITOR = 11264
MODULE_SMIPDC_PARAMS = 12288

# object list - base objects
SERVICE_MODE_ENABLE = 4123


class TemplateMessage:
    """
    Template class TemplateMessage
    """
    def __init__(self, obj_id: int, data: bytes = ''):

        # unique object number
        self.obj_id = obj_id

        self.dlen = self.get_dlen()

        # basic data - only 1 package
        self.data = data

        crc_16 = Configuration(
            width=16,
            polynomial=0x8005,
            init_value=0x0000,
            final_xor_value=0x0000,
            reverse_input=True,
            reverse_output=True,
        )

        self.crc_calculator = Calculator(crc_16)

    def get_field_data(self) -> str:
        data = self.int_to_bytes(self.obj_id) + self.int_to_bytes(self.dlen) + self.data
        return data + self.get_crc(data)

    def get_crc(self, data) -> str:
        """
        Wrapper method for calculation the crc of a given data string.

        :param data: str with data
        :return: str with crc
        """
        return self.int_to_bytes(self.crc_calculator.checksum(bytes.fromhex(data)))

    @staticmethod
    def int_to_bytes(n: int) -> str:
        """
        Build a hex style byte string from an int value.
        A byte contains always 2 chars. So if the number is uneven it adds leading zeros.

        :param n:
        :return:
        """
        return hex(n)[2:].zfill(4)

    def get_dlen(self):
        pass


class QueryMessage(TemplateMessage):
    """
    QueryMessages includes commands with `get` prefix
    """

    @staticmethod
    def get_dlen():
        return 4


class SetMessage(TemplateMessage):
    """
    SetMessages includes commands with `set` prefix and requires arguments
    """

    def get_dlen(self):
        self.obj_id = 4


class ResponseMessage(TemplateMessage):
    """
    ResponseMessages includes object container from `device response` field
    """

    def parse_data(self):
        """
        pase field data to an return all values from the objects
        :return:
        """
        data = None

        # obj = int(self.data[1:5], base=16)
        # dlen = int(self.data[5:9], base=16)
        dtype = int(self.data[1:5], base=16) & 1028

        if dtype == DTYPE_CONTAINER:
            data = self.parse_container(self.data[9:-5])
        elif dtype == DTYPE_CONTAINER:
            pass
        elif dtype == DTYPE_CSTR:
            pass
        elif dtype == DTYPE_INT8:
            pass
        elif dtype == DTYPE_UINT8:
            pass
        elif dtype == DTYPE_INT16:
            pass
        elif dtype == DTYPE_UINT16:
            pass
        elif dtype == DTYPE_INT32:
            pass
        elif dtype == DTYPE_UINT32:
            pass
        elif dtype == DTYPE_FLOAT:
            pass
        elif dtype == DTYPE_DATE_TIME:
            pass
        elif dtype == DTYPE_SERIAL:
            pass
        elif dtype == DTYPE_BOOL:
            pass
        return data
    @staticmethod
    def parse_container(container):

        n = 0
        dlen_start = 4
        dlen_stop = 8

        obj_id = []
        data = []

        while n != len(container):
            tmp = int(container[dlen_start:dlen_stop], base=16)
            obj_id.append(container[dlen_start-4:dlen_start])
            data.append(container[dlen_stop:dlen_stop + tmp * 2 - 8])

            n += tmp * 2
            dlen_start += tmp*2
            dlen_stop = dlen_start + 4

        return data


class Detector:

    DRIVER_NAME = 'FTDI'

    def __init__(self, port_name='auto'):
        """
        magic method - init function

        By default, the value is for `port_name` is `auto`, in this case the Detector is searching automatically for the
        detector. If you use multiple serial devices you may need to define the `port_name` manuele.

        :param port_name: str with port name e.g. `com3` or `/dev/ttyUSB0`
        """

        self._serial = serial.Serial()
        if port_name == 'auto':
            try:
                self._serial.port = self.find_com_port()
            except ConnectionError as ce:
                raise IOError('Detector not found!')
        else:
            self._serial.port = port_name

        self._serial.baudrate = 57600
        self._serial.timeout = 0.2

        self._connection_error = False
        self._status = 1
        self._context_depth = 0

        # device iden container
        self.device_iden_type = None
        self.device_iden_firm_ver = None
        self.device_iden_hard_ver = None
        self.device_iden_name = None
        self.device_iden_serial = None
        self.device_iden_prod_date = None

        # device check
        self.device_check_value = None

    def __enter__(self):
        """
        magic method - enter
        """
        if not self._connection_error:
            try:
                if self._context_depth == 0 and self._serial.port is not None and not self._serial.is_open:
                    self._serial.open()
            except ConnectionError as ex:
                self._connection_error = True
                raise IOError(f'detector: error entering context: {ex}')
            self._context_depth += 1
            logging.debug(f'detector: entered context at level {self._context_depth}')
            return self
        else:
            return None

    def __exit__(self, exc, value, trace) -> bool:
        """
        magic method - exit

        :param exc:
        :param value:
        :param trace:
        :return: bool - ture if no errors
        """
        self._context_depth -= 1
        if self._context_depth == 0:
            self._serial.close()
        if exc:
            if exc is type(ConnectionError):
                self._connection_error = True
                raise IOError(traceback.format_exception(exc, value=value, tb=trace))
            else:
                raise traceback.format_exception(exc, value=value, tb=trace)
        return True

    def find_com_port(self) -> str:
        """
        Method to automatically connect the detector, if the `port_name` of the init function is set to `auto`.

        :return: str with port_name
        """
        ports = comports()
        for i in ports:
            if i.manufacturer == self.DRIVER_NAME:
                return i.device
        else:
            raise ConnectionError(
                f'No Device found - may you need to define the DRIVER_NAME to one of them: '
                f'{[i.manufacturer for i in ports]}'
            )

    def write_and_read(self, obj: TemplateMessage) -> bytes:

        if not isinstance(obj, TemplateMessage):
            raise TypeError('Obj should be a BasicObject')

        mes = '$' + obj.get_field_data() + '#'
        self._serial.write(mes.upper().encode('UTF-8'))

        return self._serial.readline()

    def get_service_mode(self):
        obj = QueryMessage(obj_id=GET_SERVICE_MODE)
        rm = ResponseMessage(obj_id=SERVICE_MODE, data=self.write_and_read(obj))
        self.device_check_value = rm.parse_data()[0]

    def get_device_iden(self):
        obj = QueryMessage(obj_id=GET_DEVICE_IDEN)
        rm = ResponseMessage(obj_id=DEVICE_IDEN, data=self.write_and_read(obj))

        self.device_iden_type, self.device_iden_firm_ver, self.device_iden_hard_ver, self.device_iden_name, \
            self.device_iden_serial, self.device_iden_prod_date = rm.parse_data()


if __name__ == '__main__':
    with Detector() as x:
        x.get_service_mode()
        x.get_device_iden()
        print(x.device_iden_name.decode('UTF-8'))

