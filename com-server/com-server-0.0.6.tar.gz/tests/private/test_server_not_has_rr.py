from com_server import Connection, RestApiHandler, Builtins

conn = Connection(115200, "/dev/ttyACM0")
r = RestApiHandler(conn, False)
Builtins(r)

r.run_dev()
