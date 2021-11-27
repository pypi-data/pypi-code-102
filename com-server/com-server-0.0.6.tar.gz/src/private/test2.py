from com_server import Connection, RestApiHandler, Builtins

with Connection(115200, "/dev/ttyUSB0", "/dev/ttyACM0") as conn:
    h = RestApiHandler(conn, add_cors=True, has_register_recall=False)
    Builtins(h) 

    h.run_dev(host="0.0.0.0", port=8080)
