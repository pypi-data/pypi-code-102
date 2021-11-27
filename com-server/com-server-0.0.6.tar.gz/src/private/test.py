import serial
from serial.serialutil import SerialException
import time
import threading

import com_server

# a = com_server.Connection(115200, "/dev/ttyUSB0", send_interval=1)
# a.connect()

# a.send(beninignign, ending='\n')

# if (True):
#     b = com_server.Connection(115200, "/dev/ttyUSB0")
#     b.connect()
#     print("here")
#     b.disconnect()

# time.sleep(5)
# for t in threading.enumerate():
#     print(t.getName())
# exit(0)

conn = com_server.Connection(115200, "/dev/ttyACM0", "/dev/ttyUSB0", timeout=1) 

# @conn.custom_io_thread
# def asdf(a, b: com_server.ReceiveQueue, c):
#     if (a.in_waiting):
#         by = a.read_all()
#         print(by)
#         b.pushitems(by)

#     a.write(b"badsjlfal\n")
#     a.flush()
#     time.sleep(0.4)


with conn as a:
    beninignign = time.time()
    while True:
        a.send("asdfasdf", "abcasdf", time.time(),  concatenate=';', ending='\n')
        # print(a.receive_str(read_until=None))
        r = a.receive_str(read_until=None)
        # r = a.get_first_response("asdkfkaldsfklj", time.time(), concatenate=';', ending='\n', is_bytes = False)
        print(a.port)

        # sending = f"send time: {time.time()}"
        # success = a.send(sending, ending='\n')
        # if (not success): 
        #     time.sleep(0.05)
        #     continue
        # print(sending, a.get(bytes))
        # print(a.get_all_rcv_str())
        # # print(a.receive())

        time.sleep(0.05)

        # ask = input("> ")
        # a.send(ask, ending='\n')

        # print(a.get(str))
        # while (a.connected):
        #     # a.send("a b", "b", "c", 1, 2, 3, concatenate=';', ending='\n')
        #     # print(a.lock)
        #     sending = time.time()
        #     a.send(sending, ending='\n')
        #     print("sending", sending)

        #     if (int(time.time()) % 3 == 0):
        #         a.receive()
        #     # print("got:", a.receive())
        #     print("queue size", len(a._rcv_queue), a.get_all_rcv_str())
        #     print("lastrcv:", a.available, len(a._rcv_queue))
        #     # print("sending")
        #     # print(a)
        #     # print(a.conn_obj)
        #     time.sleep(1)

            # if (time.time() - beninignign > 5):
            #     break 

        # res = a.reconnect()

        # print(res) 
time.sleep(2)
print([i.name for i in threading.enumerate()])
