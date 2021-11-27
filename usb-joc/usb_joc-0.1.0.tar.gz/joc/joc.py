"""
Joc - JSON Across COM
Send JSON over USB_CDC lines.

Adapted from Adafruit's USB CDC Remote Procedure Call class
"""

import time
import json
try:
    import serial
    import adafruit_board_toolkit.circuitpython_serial
    json_decode_exception = json.decoder.JSONDecodeError
except ImportError:
    import usb_cdc as serial
    json_decode_exception = ValueError

RESPONSE_TIMEOUT=5
DATA_TIMEOUT=0.5

class JocError(Exception):
    """For SJS-specific errors"""
    pass

class Joc:
    def __init__(self):
        self._serial = None
        
    @staticmethod
    def create_response_packet(error=False, error_type="RPC", message=None, return_val=None):
        packet = {
            "error": error,
            "error_type": error_type if error else None,
            "message": message,
            "return_val": return_val
        }
        return packet

    @staticmethod
    def create_request_packet(info, args=[], kwargs={}):
        return {
            "name": info['text'],
            "cat": info['category'],
            "data": info['data']
        }

    def _wait_for_packet(self, timeout=None):
        incoming_packet = b""
        if timeout is not None:
            response_start_time = time.monotonic()
        while True:
            if incoming_packet:
                data_start_time = time.monotonic()
            while not self._serial.in_waiting:
                if incoming_packet and (time.monotonic() - data_start_time) >= DATA_TIMEOUT:
                    incoming_packet = b""
                if not incoming_packet and timeout is not None:
                    if (time.monotonic() - response_start_time) >= timeout:
                        return self.create_response_packet(error=True, message="Timed out waiting for response")
                time.sleep(0.001)
            data = self._serial.read(self._serial.in_waiting)
            if data:
                try:
                    incoming_packet += data
                    packet = json.loads(incoming_packet)
                    # json can try to be clever with missing braces, so make sure we have everything
                    if sorted(tuple(packet.keys())) == sorted(self._packet_format()):
                        return packet
                except json_decode_exception:
                    pass # Incomplete packet
                
class JocClient(Joc):
    def __init__(self, timeout = -1):
        super().__init__()
        self._serial = serial.data
        if timeout == -1:
            self._timeout = RESPONSE_TIMEOUT
        else:
            self._timeout = timeout
    
    def _packet_format(self):
        return self.create_response_packet().keys()

    def call(self, function):
        packet = self.create_request_packet(function)
        self._serial.write(bytes(json.dumps(packet), "utf-8"))
        # Wait for response packet to indicate success
        return self._wait_for_packet(self._timeout)

class JocServer(Joc):
    def __init__(self, handler, timeout = 5, baudrate=9600):
        super().__init__()
        self._serial = self.init_serial(baudrate)
        self._handler = handler
        self.timeout = timeout

    def _packet_format(self):
        return self.create_request_packet(None).keys()

    def init_serial(self, baudrate):
        port = self.detect_port()

        return serial.Serial(
            port,
            baudrate,
            parity='N',
            rtscts=False,
            xonxoff=False,
            exclusive=True,
        )

    def detect_port(self):
        """
        Detect the port automatically
        """
        comports = adafruit_board_toolkit.circuitpython_serial.data_comports()
        ports = [comport.device for comport in comports]
        if len(ports) >= 1:
            if len(ports) > 1:
                print("Multiple devices detected, using the first detected port.")
            return ports[0]
        raise RuntimeError("Unable to find any CircuitPython Devices with the CDC Data port enabled.")

    def loop(self):
        packet = self._wait_for_packet(self.timeout)
        if "error" not in packet:
            response_packet = self._handler(packet)
            self._serial.write(bytes(json.dumps(response_packet), "utf-8"))
    
    def close_serial(self):
        if self._serial is not None:
            self._serial.close()