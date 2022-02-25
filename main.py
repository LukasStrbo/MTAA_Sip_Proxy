import logging
import socketserver
import socket
import time

import sipproxy


def select_interface():
    interfaces = socket.getaddrinfo(socket.gethostname(), None)
    for i, x in enumerate(interfaces):
        if x[0] is not socket.AF_INET6:
            print(f"{i + 1}: {x[4][0]}")
    interface_id = int(input("Select interface on which server should serve on:")) - 1

    return str(interfaces[interface_id][4][0])


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='proxy.log', level=logging.INFO,
                        datefmt='%H:%M:%S')
    logging.info(time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()))
    hostname = socket.gethostname()
    logging.info(hostname)

    sipproxy.HOST = select_interface()
    logging.info(sipproxy.HOST)

    sipproxy.recordroute = "Record-Route: <sip:%s:%d;lr>" % (sipproxy.HOST, sipproxy.PORT)
    sipproxy.topvia = "Via: SIP/2.0/UDP %s:%d" % (sipproxy.HOST, sipproxy.PORT)

    server = socketserver.UDPServer((sipproxy.HOST, sipproxy.PORT), sipproxy.UDPHandler)
    print("Server running...")
    server.serve_forever()
