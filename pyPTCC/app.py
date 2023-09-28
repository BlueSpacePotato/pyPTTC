"""

"""

import serial
import logging
import traceback

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
SET_SERVICE_MODE = 1040  # 0x0410
SET_TRANSPARENT_MODE = 1104  # 0x0450
GET_DEVICE_IDEN = 32
SET_DEVICE_IDEN = 48

# get/set - Commands for module without memory - configuration is stored in the PTTC controller.
GET_SMARTTEC_CONFIG = 1280
SET_SMARTTEC_CONFIG = 1296
GET_SMARTTEC_MONITOR = 1312
GET_SMARTTEC_MOD_NO_MEM_IDEN = 1536
SET_SMARTTEC_MOD_NO_MEM_IDEN = 1584  # 0x0630
SET_SMARTTEC_MOD_NO_MEM_IDEN_2 = 1552  # 0x0610
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
SERVICE_MODE = 4096  # 0x1000
TRANSPARENT_MODE = 5120  # 0x1400
SMARTTEC_CONFIG = 6144
SMARTTEC_MONITOR = 7168
MODULE_IDEN = 8192
MODULE_CHECK = 8704
MODULE_BASIC_PARAMS = 9216
MODULE_USER_SET_BANK = 10240
MODULE_SMIPDC_MONITOR = 11264
MODULE_SMIPDC_PARAMS = 12288

# object list - base objects
SERVICE_MODE_ENABLE = 4123  # 0x101B

TRANSPARENT_MODE_ENABLE = 5147  # 0x141B

SMARTTEC_CONFIG_VARIANT = 6163
SMARTTEC_CONFIG_NO_MEM_COMPATIBLE = 6187

MODULE_IDEN_TYPE = 8211
MODULE_IDEN_FIRM_VER = 8229
MODULE_IDEN_HARD_VER = 8245
MODULE_IDEN_NAME = 8257
MODULE_IDEN_SERIAL = 8282
MODULE_IDEN_DET_NAME = 8289
MODULE_IDEN_DET_SERIAL = 8314
MODULE_IDEN_PROD_DATE = 8329
MODULE_IDEN_TEC_TYPE = 8339
MODULE_IDEN_TH_TYPE = 8355
MODULE_IDEN_TEC_PARAM1 = 8376
MODULE_IDEN_TEC_PARAM2 = 8392
MODULE_IDEN_TEC_PARAM3 = 8408
MODULE_IDEN_TEC_PARAM4 = 8424
MODULE_IDEN_TH_PARAM1 = 8440
MODULE_IDEN_TH_PARAM2 = 8456
MODULE_IDEN_TH_PARAM3 = 8472
MODULE_IDEN_TH_PARAM4 = 8488
MODULE_IDEN_COOL_TIME = 8581

# no_mem_default -> hex to dec
NO_MEM_DEFAULT_MODULE_IDEN_TYPE_1 = 9235  # hex: 2413
NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_1 = 9252  # hex: 2424
NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_1 = 9268  # hex: 2434
NO_MEM_DEFAULT_MODULE_IDEN_NAME_1 = 9283  # hex: 2443
NO_MEM_DEFAULT_MODULE_IDEN_TYPE_2 = 9299  # 2453
NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_2 = 9317  # 2465
NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_2 = 9332  # 2474
NO_MEM_DEFAULT_MODULE_IDEN_NAME_2 = 9351  # 2487
NO_MEM_DEFAULT_MODULE_IDEN = 9216  # 2400
NO_MEM_DEFAULT_SET_SMARTTEC_MOD_NO_MEM_IDEN = 1584  # 630

# module basic params:
MODULE_BASIC_PARAMS_SUP_CTRL = 9235  # hex: 2413
MODULE_SMIPDC_PARAMS_DET_U = 9235
MODULE_BASIC_PARAMS_DET_1 = 9252
MODULE_BASIC_PARAMS_U_SUP_PLUS = 9252  # hex: 2424
MODULE_BASIC_PARAMS_U_SUP_MINUS = 9268  # hex: 2434
MODULE_BASIC_PARAMS_FAN_CTRL = 9283  # hex: 2443
MODULE_BASIC_PARAMS_TEC_CTRL = 9299  # 2453
MODULE_BASIC_PARAMS_PWM = 9317  # 2465
MODULE_BASIC_PARAMS_I_TEC_MAX = 9332  # 2474
MODULE_BASIC_PARAMS_T_DET = 9351  # 2487
HEAD_MODULE_IDEN = 9216  # 2400
HEAD_SET_SMARTTEC_MOD_NO_MEM_IDEN = 2128  # 0850
MODULE_IDEN_SMIPDC_DEFAULT = 12288

# module_smipdc_user_set/min/max
MODULE_SMIPDC_PARAMS_DET_U_SET = 12309  # 0x3015
MODULE_SMIPDC_PARAMS_DET_I_SET = 12325  # 0x3025
MODULE_SMIPDC_PARAMS_GAIN_SET = 12341  # 0x3035
MODULE_SMIPDC_PARAMS_OFFSET_SET = 12357  # 0x3045
MODULE_SMIPDC_PARAMS_VARACTOR_SET = 12373  # 0x3055
MODULE_SMIPDC_PARAMS_TRANS_SET = 12387  # 0x3063
MODULE_SMIPDC_PARAMS_ACDC_SET = 12403  # 0x3073
MODULE_SMIPDC_PARAMS_BW_SET = 12419  # 0x3083


class TemplateMessage:
    """
    Template class TemplateMessage
    """

    def __init__(self, obj_id: int = None, data: bytes | tuple = None, dtype: int = None):
        # unique object number
        self.obj_id = obj_id

        self.dtype = dtype

        # basic data - only 1 package
        self.data = '' if data is None else data



        self.dlen = self.get_dlen()

        crc_16 = Configuration(
            width=16,
            polynomial=0x8005,
            init_value=0x0000,
            final_xor_value=0x0000,
            reverse_input=True,
            reverse_output=True,
        )

        self.crc_calculator = Calculator(crc_16)

    def get_field_data(self,  **kwargs) -> str:
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
    def int_to_bytes(n: int, n_fill: int = 4) -> str:
        """
        Build a hex style byte string from an int value.
        A byte contains always 2 chars. So if the number is uneven it adds leading zeros.

        :param n:
        :param n_fill:
        :return:
        """
        return hex(n)[2:].zfill(n_fill).upper()

    def get_dlen(self):
        return None


class QueryMessage(TemplateMessage):
    """
    QueryMessages includes commands with `get` prefix
    """

    def get_dlen(self):
        return 4


class SetMessage(TemplateMessage):
    """
    SetMessages includes commands with `set` prefix and requires arguments
    """

    def __init__(self, obj_id: int, dtype: int, data: bytes | tuple | TemplateMessage = ''):
        super().__init__()
        # unique object number
        self.obj_id = obj_id
        # print(self.obj_id)
        if isinstance(data, tuple):
            self.data = b''
            for d in data:
                self.data += d.get_field_data()
        else:
            self.data = data

        self.dtype = dtype

        self.dlen = self.get_dlen()

        crc_16 = Configuration(
            width=16,
            polynomial=0x8005,
            init_value=0x0000,
            final_xor_value=0x0000,
            reverse_input=True,
            reverse_output=True,
        )

        self.crc_calculator = Calculator(crc_16)

    def get_dlen(self):
        len_dtype = 0
        if self.dtype == DTYPE_CONTAINER:
            len_dtype = 4 + self.data.dlen
        elif self.dtype == DTYPE_CSTR:
            # print(self.data)
            if self.data is not None:
                # print(self.data)
                len_dtype = 4 + len(self.data)
            else:
                raise ValueError('data cant be None for dtype cstr')
        elif self.dtype == DTYPE_INT8:
            len_dtype = 5
        elif self.dtype == DTYPE_UINT8:
            len_dtype = 5
        elif self.dtype == DTYPE_INT16:
            len_dtype = 6
        elif self.dtype == DTYPE_UINT16:
            len_dtype = 6
        elif self.dtype == DTYPE_INT32:
            len_dtype = 8
        elif self.dtype == DTYPE_UINT32:
            len_dtype = 8
        elif self.dtype == DTYPE_FLOAT:
            len_dtype = 8
        elif self.dtype == DTYPE_DATE_TIME:
            len_dtype = 12
        elif self.dtype == DTYPE_SERIAL:
            len_dtype = 8
        elif self.dtype == DTYPE_BOOL:
            len_dtype = 5
        return len_dtype

    def get_field_data(self, is_container: bool = False) -> str:
        if self.dtype == DTYPE_CONTAINER:
            self.data = self.data.get_field_data(is_container=True)
            data = self.int_to_bytes(self.obj_id) + self.int_to_bytes(self.dlen) + self.data
        else:
            data = self.int_to_bytes(self.obj_id) + self.int_to_bytes(self.dlen) + self.int_to_bytes(int(self.data), (
                    self.dlen - 4) * 2)
        if is_container:
            return data

        return data + self.get_crc(data)


class ResponseMessage(TemplateMessage):
    """
    ResponseMessages includes object container from `device response` field
    """

    def is_valid(self):

        if self.data == b'':
            return False
        return True

    def parse_data(self, data=None):
        """
        pase field data to an return all values from the objects
        :return:
        """

        if data is None:
            data = self.data
        # print(data)
        dtype = int(data[1:5], base=16) & 1028
        if dtype == DTYPE_CONTAINER:
            data = self.parse_container(self.data[9:-5])
        else:
            raise NotImplementedError('Answer should always be a container?')
        return data

    @staticmethod
    def parse_container(container):

        n = 0
        dlen_start = 4
        dlen_stop = 8

        data = []

        while n != len(container):
            tmp = int(container[dlen_start:dlen_stop], base=16)
            obj_id = container[dlen_start - 4:dlen_start]
            dtype = int(obj_id[-1:], base=16)

            d = container[dlen_stop:dlen_stop + tmp * 2 - 8]
            # print(f'objectID: {int(obj_id, base=16)}, DTYPE: {dtype}, d: {d}')
            if dtype == DTYPE_BOOL:
                data.append(bool(d))
            elif dtype == DTYPE_INT8 or dtype == DTYPE_INT16 or dtype == DTYPE_INT32:
                data.append(int(d, base=16))
            elif dtype == DTYPE_UINT8 or dtype == DTYPE_UINT16 or dtype == DTYPE_UINT32:
                data.append(int(d, base=16))
            elif dtype == DTYPE_FLOAT:
                data.append(float.fromhex(d.decode('utf-8')))
            elif dtype == DTYPE_DATE_TIME:
                ms = int(d[:4], base=16)
                s = int(d[4:6], base=16)
                m = int(d[6:8], base=16)
                h = int(d[8:10], base=16)
                D = int(d[10:12], base=16)
                M = int(d[12:14], base=16)
                Y = int(d[14:], base=16) + 1900
                data.append({'ms': ms, 's': s, 'm': m, 'h': h, 'D': D, 'M': M, 'Y': Y})
            elif dtype == DTYPE_SERIAL:
                data.append(d)
            elif dtype == DTYPE_CSTR:
                # print(str(d))
                data.append(str(d))
                # print(str(d))

            # data.append(container[dlen_stop:dlen_stop + tmp * 2 - 8])

            n += tmp * 2
            dlen_start += tmp * 2
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
        elif port_name == 'dummy':
            self._serial.port = port_name
        else:
            self._serial.port = port_name

        self._serial.baudrate = 57600
        self._serial.timeout = 0.2

        self._connection_error = False
        self._status = 1
        self._context_depth = 0

        # service mode
        self.service_mode = None

        # device iden container
        self.device_iden_type = None
        self.device_iden_firm_ver = None
        self.device_iden_hard_ver = None
        self.device_iden_name = None
        self.device_iden_serial = None
        self.device_iden_prod_date = None

        # device check
        self.device_check_value = None

        # service mode
        self.service_mode_enabled = None

        # transparent mode
        self.transparent_mode_enabled = None
        self.transparent_mode = None

        # smarttec config
        self.smarttec_config_variant = None
        self.smarttec_config_no_mem_compatible = None

        # smarttec monitor
        self.smarttec_monitor_sup_on = None
        self.smarttec_monitor_i_sup_plus = None
        self.smarttec_monitor_i_sup_minus = None
        self.smarttec_monitor_fan_on = None
        self.smarttec_monitor_i_fan_plus = None
        self.smarttec_monitor_i_tec = None
        self.smarttec_monitor_u_tec = None
        self.smarttec_monitor_u_sup_plus = None
        self.smarttec_monitor_u_sup_minus = None
        self.smarttec_monitor_t_det = None
        self.smarttec_monitor_t_int = None
        self.smarttec_monitor_pwm = None
        self.smarttec_monitor_status = None
        self.smarttec_monitor_module_type = None
        self.monitor_th_adc = None

        # module iden
        self.module_iden_type = None
        self.module_iden_firm_ver = None
        self.module_iden_hard_ver = None
        self.module_iden_name = None
        self.module_iden_serial = None
        self.module_iden_det_name = None
        self.module_iden_det_serial = None
        self.module_iden_prod_date = None
        self.module_iden_tec_type = None
        self.module_iden_tec_param1 = None
        self.module_iden_tec_param2 = None
        self.module_iden_tec_param3 = None
        self.module_iden_tec_param4 = None
        self.module_iden_th_type = None
        self.module_iden_th_param1 = None
        self.module_iden_th_param2 = None
        self.module_iden_th_param3 = None
        self.module_iden_th_param4 = None
        self.module_iden_cool_time = None

        # module check
        self.module_check_value = None

        # module basic params
        self.module_basic_params_sup_ctrl = None
        self.module_basic_params_u_sup_plus = None
        self.module_basic_params_u_sup_minus = None
        self.module_basic_params_fan_ctrl = None
        self.module_basic_params_tec_ctrl = None
        self.module_basic_params_pwm = None
        self.module_basic_params_i_tec_max = None
        self.module_basic_params_t_det = None

        # module user set bank
        self.module_user_set_bank_index = None

        # module smipdc monitor
        self.module_smipdc_monitor_sup_plus = None
        self.module_smipdc_monitor_sup_minus = None
        self.module_smipdc_monitor_fan_plus = None
        self.module_smipdc_monitor_tec_plus = None
        self.module_smipdc_monitor_tec_minus = None
        self.module_smipdc_monitor_th1 = None
        self.module_smipdc_monitor_th2 = None
        self.module_smipdc_monitor_u_det = None
        self.module_smipdc_monitor_u_1st = None
        self.module_smipdc_monitor_u_out = None
        self.module_smipdc_monitor_temp = None

        # module smipdc params
        self.module_smipdc_params_det_u = None
        self.module_smipdc_params_det_i = None
        self.module_smipdc_params_gain = None
        self.module_smipdc_params_offset = None
        self.module_smipdc_params_varactor = None
        self.module_smipdc_params_trans = None
        self.module_smipdc_params_acdc = None
        self.module_smipdc_params_bw = None

        # smarttec mod no mem default
        self.smarttec_mod_no_mem_default_module_iden_type1 = None
        self.smarttec_mod_no_mem_default_module_iden_firm_ver1 = None
        self.smarttec_mod_no_mem_default_module_iden_hard_ver1 = None
        self.smarttec_mod_no_mem_default_module_iden_name1 = None
        self.smarttec_mod_no_mem_default_module_iden_type2 = None
        self.smarttec_mod_no_mem_default_module_iden_firm_ver2 = None
        self.smarttec_mod_no_mem_default_module_iden_hard_ver2 = None
        self.smarttec_mod_no_mem_default_module_iden_name2 = None

        # smarttec mod no mem user set
        self.smarttec_mod_no_mem_user_set_module_iden_type1 = None
        self.smarttec_mod_no_mem_user_set_module_iden_firm_ver1 = None
        self.smarttec_mod_no_mem_user_set_module_iden_hard_ver1 = None
        self.smarttec_mod_no_mem_user_set_module_iden_name1 = None
        self.smarttec_mod_no_mem_user_set_module_iden_type2 = None
        self.smarttec_mod_no_mem_user_set_module_iden_firm_ver2 = None
        self.smarttec_mod_no_mem_user_set_module_iden_hard_ver2 = None
        self.smarttec_mod_no_mem_user_set_module_iden_name2 = None

        # smarttec mod no mem user min
        self.smarttec_mod_no_mem_user_min_module_iden_type1 = None
        self.smarttec_mod_no_mem_user_min_module_iden_firm_ver1 = None
        self.smarttec_mod_no_mem_user_min_module_iden_hard_ver1 = None
        self.smarttec_mod_no_mem_user_min_module_iden_name1 = None
        self.smarttec_mod_no_mem_user_min_module_iden_type2 = None
        self.smarttec_mod_no_mem_user_min_module_iden_firm_ver2 = None
        self.smarttec_mod_no_mem_user_min_module_iden_hard_ver2 = None
        self.smarttec_mod_no_mem_user_min_module_iden_name2 = None

        # smarttec mod no mem user max
        self.smarttec_mod_no_mem_user_max_module_iden_type1 = None
        self.smarttec_mod_no_mem_user_max_module_iden_firm_ver1 = None
        self.smarttec_mod_no_mem_user_max_module_iden_hard_ver1 = None
        self.smarttec_mod_no_mem_user_max_module_iden_name1 = None
        self.smarttec_mod_no_mem_user_max_module_iden_type2 = None
        self.smarttec_mod_no_mem_user_max_module_iden_firm_ver2 = None
        self.smarttec_mod_no_mem_user_max_module_iden_hard_ver2 = None
        self.smarttec_mod_no_mem_user_max_module_iden_name2 = None

        # set module iden -> same variables as module iden

    def __enter__(self):
        """
        magic method - enter
        """
        if not self._connection_error:
            try:
                if self._context_depth == 0 and self._serial.port is not None and not self._serial.is_open:
                    if self._serial.port != 'dummy':
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
        """

        """

        if not isinstance(obj, TemplateMessage):
            raise TypeError('Obj should be a BasicObject')

        mes = '$' + obj.get_field_data() + '#'
        # print(mes)
        self._serial.write(mes.encode('UTF-8'))

        return self._serial.readline()

    def get_service_mode(self):
        obj = QueryMessage(obj_id=GET_SERVICE_MODE)
        rm = ResponseMessage(obj_id=SERVICE_MODE, data=self.write_and_read(obj))

        if rm.is_valid():
            self.service_mode = rm.parse_data()[0]
            return self.service_mode

    def get_device_iden(self):
        obj = QueryMessage(obj_id=GET_DEVICE_IDEN)
        rm = ResponseMessage(obj_id=DEVICE_IDEN, data=self.write_and_read(obj))

        if rm.is_valid():
            self.device_iden_type, self.device_iden_firm_ver, self.device_iden_hard_ver, self.device_iden_name, \
                self.device_iden_serial, self.device_iden_prod_date = rm.parse_data()

    def get_smarttec_config(self):
        obj = QueryMessage(obj_id=GET_SMARTTEC_CONFIG)
        rm = ResponseMessage(obj_id=SMARTTEC_CONFIG, data=self.write_and_read(obj))

        if rm.is_valid():
            self.smarttec_config_variant, self.smarttec_config_no_mem_compatible = rm.parse_data()

    def get_smarttec_monitor(self):
        obj = QueryMessage(obj_id=GET_SMARTTEC_MONITOR)
        rm = ResponseMessage(obj_id=SMARTTEC_MONITOR, data=self.write_and_read(obj))

        if rm.is_valid():
            self.smarttec_monitor_sup_on, self.smarttec_monitor_i_sup_plus, self.smarttec_monitor_u_sup_minus, \
                self.smarttec_monitor_fan_on, self.smarttec_monitor_i_fan_plus, self.smarttec_monitor_i_tec, \
                self.smarttec_monitor_u_tec, self.smarttec_monitor_u_sup_plus, self.smarttec_monitor_u_sup_minus, \
                self.smarttec_monitor_t_det, self.smarttec_monitor_t_int, self.smarttec_monitor_pwm, \
                self.smarttec_monitor_status, self.smarttec_monitor_module_type = rm.parse_data()

    def get_smarttec_mod_no_mem_iden(self):
        obj = QueryMessage(obj_id=GET_SMARTTEC_MOD_NO_MEM_IDEN)
        rm = ResponseMessage(obj_id=MODULE_IDEN, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
                self.module_iden_serial, self.module_iden_det_name, self.module_iden_det_serial, \
                self.module_iden_prod_date, self.module_iden_tec_type, self.module_iden_th_type, self.module_iden_tec_param1, \
                self.module_iden_tec_param2, self.module_iden_tec_param3, self.module_iden_tec_param4, \
                self.module_iden_th_param1, self.module_iden_th_param2, self.module_iden_th_param3, \
                self.module_iden_th_param4, self.module_iden_cool_time = rm.parse_data()

    def get_smarttec_mod_no_mem_default(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_smarttec_mod_no_mem_user_set(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_smarttec_mod_no_mem_user_min(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_smarttec_mod_no_mem_user_max(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_module_iden(self):
        obj = QueryMessage(obj_id=GET_MODULE_IDEN)

        rm = ResponseMessage(obj_id=MODULE_IDEN, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
                self.module_iden_serial, self.module_iden_det_name, self.module_iden_det_serial, self.module_iden_prod_date, \
                self.module_iden_tec_type, self.module_iden_th_type, self.module_iden_tec_param1, \
                self.module_iden_tec_param2, self.module_iden_tec_param3, self.module_iden_tec_param4, \
                self.module_iden_th_param1, self.module_iden_th_param2, self.module_iden_th_param3, \
                self.module_iden_th_param4, self.module_iden_cool_time = rm.parse_data()

    def get_module_default(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_module_user_set(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_module_user_min(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_module_user_max(self):
        obj = QueryMessage(obj_id=MODULE_BASIC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
                self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
                self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def get_module_smipdc_monitor(self):
        obj = QueryMessage(obj_id=MODULE_SMIPDC_MONITOR)
        rm = ResponseMessage(obj_id=MODULE_SMIPDC_MONITOR, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_smipdc_monitor_sup_plus, self.module_smipdc_monitor_sup_minus, self.module_smipdc_monitor_fan_plus, \
                self.module_smipdc_monitor_tec_plus, self.module_smipdc_monitor_tec_minus, self.module_smipdc_monitor_th1, \
                self.module_smipdc_monitor_th2, self.module_smipdc_monitor_u_det, self.module_smipdc_monitor_u_1st, \
                self.module_smipdc_monitor_u_out, self.module_smipdc_monitor_temp = rm.parse_data()

    def get_module_smipdc_default(self):
        obj = QueryMessage(obj_id=GET_MODULE_SMIPDC_DEFAULT)
        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
                self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
                self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()
        else:
            raise ValueError('Response not Valid!')

    def get_module_smipdc_user_set(self):
        obj = QueryMessage(obj_id=MODULE_SMIPDC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
                self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
                self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()

    def get_module_smipdc_user_min(self):
        obj = QueryMessage(obj_id=MODULE_SMIPDC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
                self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
                self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()

    def get_module_smipdc_user_max(self):
        obj = QueryMessage(obj_id=MODULE_SMIPDC_PARAMS)
        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(obj))

        if rm.is_valid():
            self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
                self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
                self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()

    def set_service_mode(self, mode: int):
        self.service_mode = mode
        self._set_service_mode()
        return self.service_mode

    def _set_service_mode(self):
        service_mode = SetMessage(obj_id=SERVICE_MODE_ENABLE, data=self.service_mode, dtype=DTYPE_BOOL)
        head_service_mode = SetMessage(obj_id=SERVICE_MODE, data=service_mode, dtype=DTYPE_CONTAINER)
        head_set_service_mode = SetMessage(obj_id=SET_SERVICE_MODE, data=head_service_mode, dtype=DTYPE_CONTAINER)
        # working sets from "inside" to "outside"
        # service_mode contains bool-type true = 1 = enable, false = 0 = disable
        # head_service_mode contains set "service_mode" -> is container
        # head_set_service_mode contains "head_service_mode", that contains "service_mode" -> is container

        rm = ResponseMessage(obj_id=SERVICE_MODE, data=self.write_and_read(head_set_service_mode))
        if rm.is_valid():
            self.service_mode = int(rm.parse_data()[0])

    def set_transparent_mode(self, mode: int):
        # mode -> 0(disable) || 1(enable) für enable, disable
        self.transparent_mode = mode
        self._set_transparent_mode()
        return self.transparent_mode

    def _set_transparent_mode(self):
        # packages
        transparent_mode = SetMessage(obj_id=TRANSPARENT_MODE_ENABLE, data=self.transparent_mode, dtype=DTYPE_BOOL)
        head_transparent_mode = SetMessage(obj_id=TRANSPARENT_MODE, data=transparent_mode, dtype=DTYPE_CONTAINER)
        head_set_transparent_mode = SetMessage(obj_id=SET_TRANSPARENT_MODE, data=head_transparent_mode,
                                               dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=SERVICE_MODE, data=self.write_and_read(head_set_transparent_mode))
        if rm.is_valid():
            self.transparent_mode = int(rm.parse_data()[0])

    def set_smarttec_config_variant(self, variant: int):
        # variant -> val = 0-2 (0= Basic, 1 = OEM, 2 = Advanced)
        if 0 >= variant <= 2:
            self.smarttec_config_variant = variant
            self._set_smarttec_config()
            return self.smarttec_config_variant

    def set_smarttec_config_no_mem_compatible(self, no_mem_com: int):
        # no_mem_com -> val = 0 || 1 (0 = false = no EEPROM, 1 = true = EEPROM)
        self.smarttec_config_no_mem_compatible = no_mem_com
        self._set_smarttec_config()
        return self.smarttec_config_no_mem_compatible

    def _set_smarttec_config(self):
        # packages
        smarttec_config_variant = SetMessage(obj_id=SMARTTEC_CONFIG_VARIANT, data=self.smarttec_config_variant,
                                             dtype=DTYPE_UINT8)
        smarttec_config_no_mem_com = SetMessage(obj_id=SMARTTEC_CONFIG_NO_MEM_COMPATIBLE,
                                                data=self.smarttec_config_no_mem_compatible, dtype=DTYPE_BOOL)
        into_container = bytes(str(smarttec_config_no_mem_com) + str(smarttec_config_variant))
        # connect the two values for container 2 data (sry)
        # what to do if there's only one of the two -> default value? but what

        container2 = SetMessage(obj_id=SMARTTEC_CONFIG, data=into_container, dtype=DTYPE_CONTAINER)
        container1 = SetMessage(obj_id=SET_SMARTTEC_CONFIG, data=container2, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=SMARTTEC_CONFIG, data=self.write_and_read(container1))
        self.set_smarttec_config_variant, self.smarttec_config_no_mem_compatible = rm.parse_data()[0]

    def set_smarttec_mod_no_mem_iden_type(self, iden_type: int):
        # type -> types of memory 0-3 (0 = None, 1 = NoMem, 2 = Wire, 3 = SIMPDC)
        self.module_iden_type = iden_type
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_type

    def set_smarttec_mod_no_mem_iden_firm_ver(self, firm_ver: int):
        # version of firmware
        self.module_iden_firm_ver = firm_ver
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_firm_ver

    def set_smarttec_mod_no_mem_iden_hard_ver(self, hard_ver: int):
        # version of hardware
        self.module_iden_hard_ver = hard_ver
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_hard_ver

    def set_smarttec_mod_no_mem_iden_name(self, name: str):
        # module name
        self.module_iden_name = name
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_name

    def set_smarttec_mod_no_mem_iden_serial(self, iden_serial: DTYPE_SERIAL):
        # module serial number
        self.module_iden_serial = iden_serial
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_serial

    def set_smarttec_mod_no_mem_iden_det_name(self, det_name: str):
        # detector name
        self.module_iden_det_name = det_name
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_det_name

    def set_smarttec_mod_no_mem_iden_det_serial(self, det_serial: DTYPE_SERIAL):
        # detector serial number
        self.module_iden_det_serial = det_serial
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_det_serial

    def set_smarttec_mod_no_mem_iden_prod_date(self, prod_date: DTYPE_DATE_TIME):
        # date of manufacture of module
        self.module_iden_prod_date = prod_date
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_prod_date

    def set_smarttec_mod_no_mem_iden_tec_type(self, tec_type: int):
        # var range 0-3 (0 = None, 1 = No_mem, 2 = Wire, 3 = SIMPDC)
        self.module_iden_tec_type = tec_type
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_tec_type

    def set_smarttec_mod_no_mem_iden_th_type(self, th_type: int):
        # describes thermistor type
        self.module_iden_th_type = th_type
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_th_type

    def set_smarttec_mod_no_mem_iden_tec_param1(self, param1: float):
        self.module_iden_tec_param1 = param1
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_tec_param1

    def set_smarttec_mod_no_mem_iden_tec_param2(self, param2: float):
        self.module_iden_tec_param2 = param2
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_tec_param2

    def set_smarttec_mod_no_mem_iden_tec_param3(self, param3: float):
        self.module_iden_tec_param3 = param3
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_tec_param3

    def set_smarttec_mod_no_mem_iden_tec_param4(self, param4: float):
        self.module_iden_tec_param4 = param4
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_tec_param4

    def set_smarttec_mod_no_mem_iden_th_param1(self, th_param1: float):
        self.module_iden_th_param1 = th_param1
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_th_param1

    def set_smarttec_mod_no_mem_iden_th_param2(self, th_param2: float):
        self.module_iden_th_param2 = th_param2
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_th_param2

    def set_smarttec_mod_no_mem_iden_th_param3(self, th_param3: float):
        self.module_iden_th_param3 = th_param3
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_th_param3

    def set_smarttec_mod_no_mem_iden_th_param4(self, th_param4: float):
        self.module_iden_th_param4 = th_param4
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_th_param4

    def set_smarttec_mod_no_mem_iden_cool_time(self, time: int):
        # setting max time for cooling module
        self.module_iden_cool_time = time
        self._set_smarttec_mod_no_mem_iden()
        return self.module_iden_cool_time

    def _set_smarttec_mod_no_mem_iden(self):
        # packages
        iden_type = SetMessage(obj_id=MODULE_IDEN_TYPE, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver = SetMessage(obj_id=MODULE_IDEN_FIRM_VER, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver = SetMessage(obj_id=MODULE_IDEN_HARD_VER, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name = SetMessage(obj_id=MODULE_IDEN_NAME, data=self.module_iden_name, dtype=DTYPE_CSTR)
        iden_serial = SetMessage(obj_id=MODULE_IDEN_SERIAL, data=self.module_iden_serial, dtype=DTYPE_SERIAL)
        # 5
        det_name = SetMessage(obj_id=MODULE_IDEN_DET_NAME, data=self.module_iden_det_name, dtype=DTYPE_CSTR)
        det_serial = SetMessage(obj_id=MODULE_IDEN_DET_SERIAL, data=self.module_iden_det_serial, dtype=DTYPE_SERIAL)
        prod_date = SetMessage(obj_id=MODULE_IDEN_PROD_DATE, data=self.module_iden_prod_date, dtype=DTYPE_DATE_TIME)
        tec_type = SetMessage(obj_id=MODULE_IDEN_TEC_TYPE, data=self.module_iden_tec_type, dtype=DTYPE_UINT8)
        th_type = SetMessage(obj_id=MODULE_IDEN_TH_TYPE, data=self.module_iden_th_type, dtype=DTYPE_UINT8)
        # 10
        tec_param1 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM1, data=self.module_iden_tec_param1, dtype=DTYPE_FLOAT)
        tec_param2 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM2, data=self.module_iden_tec_param2, dtype=DTYPE_FLOAT)
        tec_param3 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM3, data=self.module_iden_tec_param3, dtype=DTYPE_FLOAT)
        tec_param4 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM4, data=self.module_iden_tec_param4, dtype=DTYPE_FLOAT)
        th_param1 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM1, data=self.module_iden_th_param1, dtype=DTYPE_FLOAT)
        # 15
        th_param2 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM2, data=self.module_iden_th_param2, dtype=DTYPE_FLOAT)
        th_param3 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM3, data=self.module_iden_th_param3, dtype=DTYPE_FLOAT)
        th_param4 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM4, data=self.module_iden_th_param4, dtype=DTYPE_FLOAT)
        cool_time = SetMessage(obj_id=MODULE_IDEN_COOL_TIME, data=self.module_iden_cool_time, dtype=DTYPE_UINT16)

        container2 = SetMessage(
            obj_id=MODULE_IDEN,
            dtype=DTYPE_CONTAINER,
            data=(
                iden_type,
                firm_ver,
                hard_ver,
                name,
                iden_serial,
                det_name,
                det_serial,
                prod_date,
                tec_type,
                th_type,
                tec_param1,
                tec_param2,
                tec_param3,
                tec_param4,
                th_param1,
                th_param2,
                th_param3,
                th_param4,
                cool_time
            )
            # possible to append SetMessage-tuples and byte() conv? -> function that takes tuples and returns bytes?
        )
        container1 = SetMessage(obj_id=SET_SMARTTEC_MOD_NO_MEM_IDEN, data=container2, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_IDEN, data=self.write_and_read(container1))
        self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
            self.module_iden_serial, self.module_iden_det_name, self.module_iden_det_serial, \
            self.module_iden_prod_date, self.module_iden_det_tec_type, self.module_iden_th_type, \
            self.module_iden_tec_param1, self.module_iden_tec_param2, self.module_iden_tec_param3, self.module_iden_tec_param4, \
            self.module_iden_th_param1, self.module_iden_th_param2, self.module_iden_th_param3, self.module_iden_th_param4, \
            self.module_iden_cool_time = rm.parse_data()

    def set_smarttec_mod_no_mem_default_module_iden_type1(self, type1: int):
        self.smarttec_mod_no_mem_default_module_iden_type1 = type1
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_type1

    def set_smarttec_mod_no_mem_default_module_iden_firm_ver1(self, firm_ver1: int):
        self.smarttec_mod_no_mem_default_module_iden_firm_ver1 = firm_ver1
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_firm_ver1

    def set_smarttec_mod_no_mem_default_module_iden_hard_ver1(self, hard_ver1: int):
        self.smarttec_mod_no_mem_default_module_iden_hard_ver1 = hard_ver1
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_hard_ver1

    def set_smarttec_mod_no_mem_default_module_iden_name1(self, name1: str):
        self.smarttec_mod_no_mem_default_module_iden_name1 = name1
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_name1

    def set_smarttec_mod_no_mem_default_module_iden_type2(self, type2: int):
        self.smarttec_mod_no_mem_default_module_iden_type2 = type2
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_type2

    def set_smarttec_mod_no_mem_default_module_iden_firm_ver2(self, firm_ver2: int):
        self.smarttec_mod_no_mem_default_module_iden_firm_ver2 = firm_ver2
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_firm_ver2

    def set_smarttec_mod_no_mem_default_module_iden_hard_ver2(self, hard_ver2: int):
        self.smarttec_mod_no_mem_default_module_iden_hard_ver2 = hard_ver2
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_hard_ver2

    def set_smarttec_mod_no_mem_default_module_iden_name2(self, name2: str):
        self.smarttec_mod_no_mem_default_module_iden_name2 = name2
        self._set_smarttec_mod_no_mem_default()
        return self.smarttec_mod_no_mem_default_module_iden_name2

    def _set_smarttec_mod_no_mem_default(self):
        # packages:
        type1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_1,
                           data=self.smarttec_mod_no_mem_default_module_iden_type1, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_1,
                               data=self.smarttec_mod_no_mem_default_module_iden_firm_ver1, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_1,
                               data=self.smarttec_mod_no_mem_default_module_iden_hard_ver1, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_1,
                           data=self.smarttec_mod_no_mem_default_module_iden_name1, dtype=DTYPE_CSTR)

        type2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_2,
                           data=self.smarttec_mod_no_mem_default_module_iden_type2, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_2,
                               data=self.smarttec_mod_no_mem_default_module_iden_firm_ver2, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_2,
                               data=self.smarttec_mod_no_mem_default_module_iden_hard_ver2, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_2,
                           data=self.smarttec_mod_no_mem_default_module_iden_name2, dtype=DTYPE_CSTR)

        container2 = SetMessage(
            obj_id=NO_MEM_DEFAULT_MODULE_IDEN,
            dtype=DTYPE_CONTAINER,
            data=(type1,
                  firm_ver1,
                  hard_ver1,
                  name1,
                  type2,
                  firm_ver2,
                  hard_ver2,
                  name2
                  )
        )

        container1 = SetMessage(obj_id=SET_SMARTTEC_MOD_NO_MEM_IDEN, data=container2, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(container1))
        self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
            self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
            self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def set_smarttec_mod_no_mem_user_set_module_iden_type1(self, type1: int):
        self.smarttec_mod_no_mem_user_set_module_iden_type1 = type1
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_type1

    def set_smarttec_mod_no_mem_user_set_module_iden_firm_ver1(self, firm_ver1: int):
        self.smarttec_mod_no_mem_user_set_module_iden_firm_ver1 = firm_ver1
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_firm_ver1

    def set_smarttec_mod_no_mem_user_set_module_iden_hard_ver1(self, hard_ver1: int):
        self.smarttec_mod_no_mem_user_set_module_iden_hard_ver1 = hard_ver1
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_hard_ver1

    def set_smarttec_mod_no_mem_user_set_module_iden_name1(self, name1: str):
        self.smarttec_mod_no_mem_user_set_module_iden_name1 = name1
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_name1

    def set_smarttec_mod_no_mem_user_set_module_iden_type2(self, type2: int):
        self.smarttec_mod_no_mem_user_set_module_iden_type2 = type2
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_type2

    def set_smarttec_mod_no_mem_user_set_module_iden_firm_ver2(self, firm_ver2: int):
        self.smarttec_mod_no_mem_user_set_module_iden_firm_ver2 = firm_ver2
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_firm_ver2

    def set_smarttec_mod_no_mem_user_set_module_iden_hard_ver2(self, hard_ver2: int):
        self.smarttec_mod_no_mem_user_set_module_iden_hard_ver2 = hard_ver2
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_hard_ver2

    def set_smarttec_mod_no_mem_user_set_module_iden_name2(self, name2: str):
        self.smarttec_mod_no_mem_user_set_module_iden_name2 = name2
        self._set_smarttec_mod_no_mem_user_set()
        return self.smarttec_mod_no_mem_user_set_module_iden_name2

    def _set_smarttec_mod_no_mem_user_set(self):
        # packages
        type1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_1,
                           data=self.smarttec_mod_no_mem_user_set_module_iden_type1, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_1,
                               data=self.smarttec_mod_no_mem_user_set_module_iden_firm_ver1, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_1,
                               data=self.smarttec_mod_no_mem_user_set_module_iden_hard_ver1, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_1,
                           data=self.smarttec_mod_no_mem_user_set_module_iden_name1, dtype=DTYPE_CSTR)

        type2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_2,
                           data=self.smarttec_mod_no_mem_user_set_module_iden_type2, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_2,
                               data=self.smarttec_mod_no_mem_user_set_module_iden_firm_ver2, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_2,
                               data=self.smarttec_mod_no_mem_user_set_module_iden_hard_ver2, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_2,
                           data=self.smarttec_mod_no_mem_user_set_module_iden_name2, dtype=DTYPE_CSTR)

        container2 = SetMessage(
            obj_id=NO_MEM_DEFAULT_MODULE_IDEN,
            dtype=DTYPE_CONTAINER,
            data=(type1,
                  firm_ver1,
                  hard_ver1,
                  name1,
                  type2,
                  firm_ver2,
                  hard_ver2,
                  name2
                  )
        )

        container1 = SetMessage(obj_id=SET_SMARTTEC_MOD_NO_MEM_USER_SET, data=container2, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(container1))
        self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
            self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
            self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def set_smarttec_mod_no_mem_user_min_module_iden_type1(self, type1: int):
        self.smarttec_mod_no_mem_user_min_module_iden_type1 = type1
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_type1

    def set_smarttec_mod_no_mem_user_min_module_iden_firm_ver1(self, firm_ver1: int):
        self.smarttec_mod_no_mem_user_min_module_iden_firm_ver1 = firm_ver1
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_firm_ver1

    def set_smarttec_mod_no_mem_user_min_module_iden_hard_ver1(self, hard_ver1: int):
        self.smarttec_mod_no_mem_user_min_module_iden_hard_ver1 = hard_ver1
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_hard_ver1

    def set_smarttec_mod_no_mem_user_min_module_iden_name1(self, name1: str):
        self.smarttec_mod_no_mem_user_min_module_iden_name1 = name1
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_name1

    def set_smarttec_mod_no_mem_user_min_module_iden_type2(self, type2: int):
        self.smarttec_mod_no_mem_user_min_module_iden_type2 = type2
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_type2

    def set_smarttec_mod_no_mem_user_min_module_iden_firm_ver2(self, firm_ver2: int):
        self.smarttec_mod_no_mem_user_min_module_iden_firm_ver2 = firm_ver2
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_firm_ver2

    def set_smarttec_mod_no_mem_user_min_module_iden_hard_ver2(self, hard_ver2: int):
        self.smarttec_mod_no_mem_user_min_module_iden_hard_ver2 = hard_ver2
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_hard_ver2

    def set_smarttec_mod_no_mem_user_min_module_iden_name2(self, name2: str):
        self.smarttec_mod_no_mem_user_min_module_iden_name2 = name2
        self._set_smarttec_mod_no_mem_user_min()
        return self.smarttec_mod_no_mem_user_min_module_iden_name2

    def _set_smarttec_mod_no_mem_user_min(self):
        # packages
        type1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_1,
                           data=self.smarttec_mod_no_mem_user_min_module_iden_type1, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_1,
                               data=self.smarttec_mod_no_mem_user_min_module_iden_firm_ver1, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_1,
                               data=self.smarttec_mod_no_mem_user_min_module_iden_hard_ver1, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_1,
                           data=self.smarttec_mod_no_mem_user_min_module_iden_name1, dtype=DTYPE_CSTR)

        type2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_2,
                           data=self.smarttec_mod_no_mem_user_min_module_iden_type2, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_2,
                               data=self.smarttec_mod_no_mem_user_min_module_iden_firm_ver2, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_2,
                               data=self.smarttec_mod_no_mem_user_min_module_iden_hard_ver2, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_2,
                           data=self.smarttec_mod_no_mem_user_min_module_iden_name2, dtype=DTYPE_CSTR)

        container2 = SetMessage(
            obj_id=NO_MEM_DEFAULT_MODULE_IDEN,
            dtype=DTYPE_CONTAINER,
            data=(type1,
                  firm_ver1,
                  hard_ver1,
                  name1,
                  type2,
                  firm_ver2,
                  hard_ver2,
                  name2
                  )
        )

        container1 = SetMessage(obj_id=SET_SMARTTEC_MOD_NO_MEM_USER_MIN, data=container2, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(container1))
        self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
            self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
            self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def set_smarttec_mod_no_mem_user_max_module_iden_type1(self, type1: int):
        self.smarttec_mod_no_mem_user_max_module_iden_type1 = type1
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_type1

    def set_smarttec_mod_no_mem_user_max_module_iden_firm_ver1(self, firm_ver1: int):
        self.smarttec_mod_no_mem_user_max_module_iden_firm_ver1 = firm_ver1
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_firm_ver1

    def set_smarttec_mod_no_mem_user_max_module_iden_hard_ver1(self, hard_ver1: int):
        self.smarttec_mod_no_mem_user_max_module_iden_hard_ver1 = hard_ver1
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_hard_ver1

    def set_smarttec_mod_no_mem_user_max_module_iden_name1(self, name1: str):
        self.smarttec_mod_no_mem_user_max_module_iden_name1 = name1
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_name1

    def set_smarttec_mod_no_mem_user_max_module_iden_type2(self, type2: int):
        self.smarttec_mod_no_mem_user_max_module_iden_type2 = type2
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_type2

    def set_smarttec_mod_no_mem_user_max_module_iden_firm_ver2(self, firm_ver2: int):
        self.smarttec_mod_no_mem_user_max_module_iden_firm_ver2 = firm_ver2
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_firm_ver2

    def set_smarttec_mod_no_mem_user_max_module_iden_hard_ver2(self, hard_ver2: int):
        self.smarttec_mod_no_mem_user_max_module_iden_hard_ver2 = hard_ver2
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_hard_ver2

    def set_smarttec_mod_no_mem_user_max_module_iden_name2(self, name2: str):
        self.smarttec_mod_no_mem_user_max_module_iden_name2 = name2
        self._set_smarttec_mod_no_mem_user_max()
        return self.smarttec_mod_no_mem_user_max_module_iden_name2

    def _set_smarttec_mod_no_mem_user_max(self):
        # packages
        type1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_1,
                           data=self.smarttec_mod_no_mem_user_max_module_iden_type1, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_1,
                               data=self.smarttec_mod_no_mem_user_max_module_iden_firm_ver1, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_1,
                               data=self.smarttec_mod_no_mem_user_max_module_iden_hard_ver1, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_1,
                           data=self.smarttec_mod_no_mem_user_max_module_iden_name1, dtype=DTYPE_CSTR)

        type2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_TYPE_2,
                           data=self.smarttec_mod_no_mem_user_max_module_iden_type2, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_FIRM_VER_2,
                               data=self.smarttec_mod_no_mem_user_max_module_iden_firm_ver2, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_HARD_VER_2,
                               data=self.smarttec_mod_no_mem_user_max_module_iden_hard_ver2, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=NO_MEM_DEFAULT_MODULE_IDEN_NAME_2,
                           data=self.smarttec_mod_no_mem_user_max_module_iden_name2, dtype=DTYPE_CSTR)

        container2 = SetMessage(
            obj_id=NO_MEM_DEFAULT_MODULE_IDEN,
            dtype=DTYPE_CONTAINER,
            data=(type1,
                  firm_ver1,
                  hard_ver1,
                  name1,
                  type2,
                  firm_ver2,
                  hard_ver2,
                  name2
                  )
        )

        container1 = SetMessage(obj_id=SET_SMARTTEC_MOD_NO_MEM_USER_MAX, data=container2, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(container1))
        self.module_basic_params_sup_ctrl, self.module_basic_params_u_sup_plus, self.module_basic_params_u_sup_minus, \
            self.module_basic_params_fan_ctrl, self.module_basic_params_tec_ctrl, self.module_basic_params_pwm, \
            self.module_basic_params_i_tec_max, self.module_basic_params_t_det = rm.parse_data()

    def set_module_iden_type(self, mtype: int):
        self.module_iden_type = mtype
        self._set_module_iden()
        return self.module_iden_type

    def set_module_iden_firm_ver(self, firm_ver: int):
        self.module_iden_firm_ver = firm_ver
        self._set_module_iden()
        return self.module_iden_firm_ver

    def set_module_iden_hard_ver(self, hard_ver: int):
        self.module_iden_hard_ver = hard_ver
        self._set_module_iden()
        return self.module_iden_hard_ver

    def set_module_iden_name(self, name: str):
        self.module_iden_name = name
        self._set_module_iden()
        return self.module_iden_name

    def set_module_iden_serial(self, mserial: DTYPE_SERIAL):
        self.module_iden_serial = mserial
        self._set_module_iden()
        return self.module_iden_serial

    def set_module_iden_det_name(self, det_name: str):
        self.module_iden_det_name = det_name
        self._set_module_iden()
        return self.module_iden_det_name

    def set_module_iden_det_serial(self, det_serial: DTYPE_SERIAL):
        self.module_iden_det_serial = det_serial
        self._set_module_iden()
        return self.module_iden_det_serial

    def set_module_iden_prod_date(self, prod_date: DTYPE_DATE_TIME):
        self.module_iden_prod_date = prod_date
        self._set_module_iden()
        return self.module_iden_prod_date

    def set_module_iden_tec_type(self, tec_type: int):
        self.module_iden_tec_type = tec_type
        self._set_module_iden()
        return self.module_iden_tec_type

    def set_module_iden_th_type(self, th_type: int):
        self.module_iden_th_type = th_type
        self._set_module_iden()
        return self.module_iden_th_type

    def set_module_iden_tec_param1(self, param1: float):
        self.module_iden_tec_param1 = param1
        self._set_module_iden()
        return self.module_iden_tec_param1

    def set_module_iden_tec_param2(self, param2: float):
        self.module_iden_tec_param2 = param2
        self._set_module_iden()
        return self.module_iden_tec_param2

    def set_module_iden_tec_param3(self, param3: float):
        self.module_iden_tec_param3 = param3
        self._set_module_iden()
        return self.module_iden_tec_param3

    def set_module_iden_tec_param4(self, param4: float):
        self.module_iden_tec_param4 = param4
        self._set_module_iden()
        return self.module_iden_tec_param4

    def set_module_iden_th_param1(self, param1: float):
        self.module_iden_th_param1 = param1
        self._set_module_iden()
        return self.module_iden_th_param1

    def set_module_iden_th_param2(self, param2: float):
        self.module_iden_th_param2 = param2
        self._set_module_iden()
        return self.module_iden_th_param2

    def set_module_iden_th_param3(self, param3: float):
        self.module_iden_th_param3 = param3
        self._set_module_iden()
        return self.module_iden_th_param3

    def set_module_iden_th_param4(self, param4: float):
        self.module_iden_th_param4 = param4
        self._set_module_iden()
        return self.module_iden_th_param4

    def set_module_iden_cool_time(self, cool_time: int):
        self.module_iden_cool_time = cool_time
        self._set_module_iden()
        return self.module_iden_cool_time

    def _set_module_iden(self):
        # packages
        mtype = SetMessage(obj_id=MODULE_IDEN_TYPE, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver = SetMessage(obj_id=MODULE_IDEN_FIRM_VER, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver = SetMessage(obj_id=MODULE_IDEN_HARD_VER, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name = SetMessage(obj_id=MODULE_IDEN_NAME, data=self.module_iden_name, dtype=DTYPE_CSTR)
        mserial = SetMessage(obj_id=MODULE_IDEN_SERIAL, data=self.module_iden_serial, dtype=DTYPE_SERIAL)

        det_name = SetMessage(obj_id=MODULE_IDEN_DET_NAME, data=self.module_iden_det_name, dtype=DTYPE_CSTR)
        det_serial = SetMessage(obj_id=MODULE_IDEN_DET_SERIAL, data=self.module_iden_det_serial, dtype=DTYPE_SERIAL)
        prod_date = SetMessage(obj_id=MODULE_IDEN_PROD_DATE, data=self.module_iden_prod_date, dtype=DTYPE_DATE_TIME)
        tec_type = SetMessage(obj_id=MODULE_IDEN_TEC_TYPE, data=self.module_iden_tec_type, dtype=DTYPE_UINT8)
        th_type = SetMessage(obj_id=MODULE_IDEN_TH_TYPE, data=self.module_iden_th_type, dtype=DTYPE_UINT8)

        tec_param1 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM1, data=self.module_iden_tec_param1, dtype=DTYPE_FLOAT)
        tec_param2 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM2, data=self.module_iden_tec_param2, dtype=DTYPE_FLOAT)
        tec_param3 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM3, data=self.module_iden_tec_param3, dtype=DTYPE_FLOAT)
        tec_param4 = SetMessage(obj_id=MODULE_IDEN_TEC_PARAM4, data=self.module_iden_tec_param4, dtype=DTYPE_FLOAT)
        th_param1 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM1, data=self.module_iden_th_param1, dtype=DTYPE_FLOAT)

        th_param2 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM2, data=self.module_iden_th_param2, dtype=DTYPE_FLOAT)
        th_param3 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM3, data=self.module_iden_th_param3, dtype=DTYPE_FLOAT)
        th_param4 = SetMessage(obj_id=MODULE_IDEN_TH_PARAM4, data=self.module_iden_th_param4, dtype=DTYPE_FLOAT)
        cool_time = SetMessage(obj_id=MODULE_IDEN_COOL_TIME, data=self.module_iden_cool_time, dtype=DTYPE_UINT16)

        module_iden = SetMessage(obj_id=MODULE_IDEN, data=(mtype, firm_ver,
                                                           hard_ver, name,
                                                           mserial, det_name,
                                                           det_serial, prod_date,
                                                           tec_type, th_type,
                                                           tec_param1, tec_param2,
                                                           tec_param3, tec_param4,
                                                           th_param1, th_param2,
                                                           th_param3, th_param4,
                                                           cool_time), dtype=DTYPE_CONTAINER)

        set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_SMARTTEC_MOD_NO_MEM_IDEN_2, data=module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_IDEN, data=self.write_and_read(set_smarttec_mod_no_mem_iden))

        self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
            self.module_iden_serial, self.module_iden_det_name, self.module_iden_det_serial, self.module_iden_prod_date, \
            self.module_iden_tec_type, self.module_iden_th_type, self.module_iden_tec_param1, self.module_iden_tec_param2, \
            self.module_iden_tec_param3, self.module_iden_tec_param4, self.module_iden_th_param1, self.module_iden_th_param2, \
            self.module_iden_th_param3, self.module_iden_th_param4, self.module_iden_cool_time = rm.parse_data()

    def set_module_default(self):
        # packages:
        i_type1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_SUP_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_PLUS, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_MINUS, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_FAN_CTRL, data=self.module_iden_name, dtype=DTYPE_CSTR)

        i_type2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_TEC_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_PWM, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_I_TEC_MAX, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_T_DET, data=self.module_iden_name, dtype=DTYPE_CSTR)

        head_module_iden = SetMessage(obj_id=HEAD_MODULE_IDEN, data=(i_type1, firm_ver1,
                                                                     hard_ver1, name1,
                                                                     i_type2, firm_ver2,
                                                                     hard_ver2, name2), dtype=DTYPE_CONTAINER)

        head_set_smarttec_mod_no_mem_iden = SetMessage(obj_id=HEAD_SET_SMARTTEC_MOD_NO_MEM_IDEN, data=head_module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(head_set_smarttec_mod_no_mem_iden))

        self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
            self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name = rm.parse_data()

    def set_module_user_set(self):
        # packages:
        i_type1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_SUP_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_PLUS, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_MINUS, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_FAN_CTRL, data=self.module_iden_name, dtype=DTYPE_CSTR)

        i_type2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_TEC_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_PWM, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_I_TEC_MAX, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_T_DET, data=self.module_iden_name, dtype=DTYPE_CSTR)

        head_module_iden = SetMessage(obj_id=HEAD_MODULE_IDEN, data=(i_type1, firm_ver1,
                                                                     hard_ver1, name1,
                                                                     i_type2, firm_ver2,
                                                                     hard_ver2, name2), dtype=DTYPE_CONTAINER)

        head_set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_USER_SET, data=head_module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(head_set_smarttec_mod_no_mem_iden))

        self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
            self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name = rm.parse_data()

    def set_module_user_min(self):
        # packages:
        i_type1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_SUP_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_PLUS, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_MINUS, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_FAN_CTRL, data=self.module_iden_name, dtype=DTYPE_CSTR)

        i_type2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_TEC_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_PWM, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_I_TEC_MAX, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_T_DET, data=self.module_iden_name, dtype=DTYPE_CSTR)

        head_module_iden = SetMessage(obj_id=HEAD_MODULE_IDEN, data=(i_type1, firm_ver1,
                                                                     hard_ver1, name1,
                                                                     i_type2, firm_ver2,
                                                                     hard_ver2, name2), dtype=DTYPE_CONTAINER)

        head_set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_USER_MIN, data=head_module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(head_set_smarttec_mod_no_mem_iden))

        self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
            self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name = rm.parse_data()

    def set_module_user_max(self):
        # packages:
        i_type1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_SUP_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_PLUS, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_MINUS, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name1 = SetMessage(obj_id=MODULE_BASIC_PARAMS_FAN_CTRL, data=self.module_iden_name, dtype=DTYPE_CSTR)

        i_type2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_TEC_CTRL, data=self.module_iden_type, dtype=DTYPE_UINT8)
        firm_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_PWM, data=self.module_iden_firm_ver, dtype=DTYPE_UINT16)
        hard_ver2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_I_TEC_MAX, data=self.module_iden_hard_ver, dtype=DTYPE_UINT16)
        name2 = SetMessage(obj_id=MODULE_BASIC_PARAMS_T_DET, data=self.module_iden_name, dtype=DTYPE_CSTR)

        head_module_iden = SetMessage(obj_id=HEAD_MODULE_IDEN, data=(i_type1, firm_ver1,
                                                                     hard_ver1, name1,
                                                                     i_type2, firm_ver2,
                                                                     hard_ver2, name2), dtype=DTYPE_CONTAINER)

        head_set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_USER_MAX, data=head_module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_BASIC_PARAMS, data=self.write_and_read(head_set_smarttec_mod_no_mem_iden))

        self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name, \
            self.module_iden_type, self.module_iden_firm_ver, self.module_iden_hard_ver, self.module_iden_name = rm.parse_data()

    def set_module_smipdc_default(self):
        # packages:
        det_u = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_U, data=self.module_smipdc_params_det_u, dtype=DTYPE_UINT16)
        det_i = SetMessage(obj_id=MODULE_BASIC_PARAMS_DET_1, data=self.module_smipdc_params_det_i, dtype=DTYPE_UINT16)
        gain = SetMessage(obj_id=MODULE_BASIC_PARAMS_U_SUP_MINUS, data=self.module_smipdc_params_gain, dtype=DTYPE_UINT16)
        offset = SetMessage(obj_id=MODULE_BASIC_PARAMS_FAN_CTRL, data=self.module_smipdc_params_offset, dtype=DTYPE_UINT16)

        varactor = SetMessage(obj_id=MODULE_BASIC_PARAMS_TEC_CTRL, data=self.module_smipdc_params_varactor, dtype=DTYPE_UINT16)
        trans = SetMessage(obj_id=MODULE_BASIC_PARAMS_PWM, data=self.module_smipdc_params_trans, dtype=DTYPE_UINT8)
        acdc = SetMessage(obj_id=MODULE_BASIC_PARAMS_I_TEC_MAX, data=self.module_smipdc_params_acdc, dtype=DTYPE_UINT8)
        bw = SetMessage(obj_id=MODULE_BASIC_PARAMS_T_DET, data=self.module_smipdc_params_bw, dtype=DTYPE_UINT8)

        module_iden = SetMessage(obj_id=MODULE_IDEN_SMIPDC_DEFAULT, data=(det_u, det_i,
                                                                    gain, offset,
                                                                    varactor, trans,
                                                                    acdc, bw), dtype=DTYPE_CONTAINER)

        set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_SMIPDC_DEFAULT, data=module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(set_smarttec_mod_no_mem_iden))

        self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
            self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
            self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()

    def set_module_smipdc_user_set(self):
        # packages:
        det_u = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_U_SET, data=self.module_smipdc_params_det_u, dtype=DTYPE_UINT16)
        det_i = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_I_SET, data=self.module_smipdc_params_det_i, dtype=DTYPE_UINT16)
        gain = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_GAIN_SET, data=self.module_smipdc_params_gain, dtype=DTYPE_UINT16)
        offset = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_OFFSET_SET, data=self.module_smipdc_params_offset, dtype=DTYPE_UINT16)

        varactor = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_VARACTOR_SET, data=self.module_smipdc_params_varactor, dtype=DTYPE_UINT16)
        trans = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_TRANS_SET, data=self.module_smipdc_params_trans, dtype=DTYPE_UINT8)
        acdc = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_ACDC_SET, data=self.module_smipdc_params_acdc, dtype=DTYPE_UINT8)
        bw = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_BW_SET, data=self.module_smipdc_params_bw, dtype=DTYPE_UINT8)

        module_iden = SetMessage(obj_id=MODULE_SMIPDC_PARAMS, data=(det_u, det_i,
                                                                    gain, offset,
                                                                    varactor, trans,
                                                                    acdc, bw), dtype=DTYPE_CONTAINER)

        set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_SMIPDC_USER_SET, data=module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(set_smarttec_mod_no_mem_iden))

        self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
            self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
            self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()

    def set_module_smipdc_user_min(self):
        # packages:
        det_u = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_U_SET, data=self.module_smipdc_params_det_u, dtype=DTYPE_UINT16)
        det_i = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_I_SET, data=self.module_smipdc_params_det_i, dtype=DTYPE_UINT16)
        gain = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_GAIN_SET, data=self.module_smipdc_params_gain, dtype=DTYPE_UINT16)
        offset = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_OFFSET_SET, data=self.module_smipdc_params_offset, dtype=DTYPE_UINT16)

        varactor = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_VARACTOR_SET, data=self.module_smipdc_params_varactor, dtype=DTYPE_UINT16)
        trans = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_TRANS_SET, data=self.module_smipdc_params_trans, dtype=DTYPE_UINT8)
        acdc = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_ACDC_SET, data=self.module_smipdc_params_acdc, dtype=DTYPE_UINT8)
        bw = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_BW_SET, data=self.module_smipdc_params_bw, dtype=DTYPE_UINT8)

        module_iden = SetMessage(obj_id=MODULE_SMIPDC_PARAMS, data=(det_u, det_i,
                                                                    gain, offset,
                                                                    varactor, trans,
                                                                    acdc, bw), dtype=DTYPE_CONTAINER)

        set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_SMIPDC_USER_MIN, data=module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(set_smarttec_mod_no_mem_iden))

        self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
            self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
            self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()

    def set_module_smipdc_user_max(self):
        # packages:
        det_u = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_U_SET, data=self.module_smipdc_params_det_u, dtype=DTYPE_UINT16)
        det_i = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_DET_I_SET, data=self.module_smipdc_params_det_i, dtype=DTYPE_UINT16)
        gain = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_GAIN_SET, data=self.module_smipdc_params_gain, dtype=DTYPE_UINT16)
        offset = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_OFFSET_SET, data=self.module_smipdc_params_offset, dtype=DTYPE_UINT16)

        varactor = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_VARACTOR_SET, data=self.module_smipdc_params_varactor, dtype=DTYPE_UINT16)
        trans = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_TRANS_SET, data=self.module_smipdc_params_trans, dtype=DTYPE_UINT8)
        acdc = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_ACDC_SET, data=self.module_smipdc_params_acdc, dtype=DTYPE_UINT8)
        bw = SetMessage(obj_id=MODULE_SMIPDC_PARAMS_BW_SET, data=self.module_smipdc_params_bw, dtype=DTYPE_UINT8)

        module_iden = SetMessage(obj_id=MODULE_SMIPDC_PARAMS, data=(det_u, det_i,
                                                                    gain, offset,
                                                                    varactor, trans,
                                                                    acdc, bw), dtype=DTYPE_CONTAINER)

        set_smarttec_mod_no_mem_iden = SetMessage(obj_id=SET_MODULE_SMIPDC_USER_MAX, data=module_iden, dtype=DTYPE_CONTAINER)

        rm = ResponseMessage(obj_id=MODULE_SMIPDC_PARAMS, data=self.write_and_read(set_smarttec_mod_no_mem_iden))

        self.module_smipdc_params_det_u, self.module_smipdc_params_det_i, self.module_smipdc_params_gain, \
            self.module_smipdc_params_offset, self.module_smipdc_params_varactor, self.module_smipdc_params_trans, \
            self.module_smipdc_params_acdc, self.module_smipdc_params_bw = rm.parse_data()


if __name__ == '__main__':
    with Detector(port_name='COM7') as x:
        x.get_device_iden()
        x.get_module_user_set()
        x.get_module_smipdc_default()
        print('1')
        print(x.module_smipdc_params_gain)
        x.module_smipdc_params_gain = 20
        print('2')
        print(x.module_smipdc_params_gain)
        print('3')
        x.set_module_smipdc_default()
        print(x.module_smipdc_params_gain)
