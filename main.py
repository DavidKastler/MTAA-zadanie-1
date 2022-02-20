import sipFullProxyLib.sipfullproxy as sip_proxy
import time
import logging
import socket
import sys
import socketserver

HOST, PROXY_PORT = '0.0.0.0', 5060


def set_custom_messages():
    sip_proxy.msg_200 = "VYBORNE"
    sip_proxy.msg_400 = "Oprav si poziadavku laskavo"
    sip_proxy.msg_406 = "Toto je ne-ak-cep-to-va-tel-ne"
    sip_proxy.msg_480 = "Neotravuj ma!"
    sip_proxy.msg_488 = "Tuto to je neakcetpovatelne"
    sip_proxy.msg_500 = "Nieco sa dojebalo"


def set_up_logging():
    sip_proxy.logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                                  filename='logs\\proxy.log', filemode='w',
                                  level=logging.INFO, datefmt='%H:%M:%S')
    logging.info('\n\tNEW SESSION\n\t' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + '\n')


if __name__ == "__main__":
    set_custom_messages()

    set_up_logging()

    hostname = socket.gethostname()
    logging.info(hostname)
    ipaddress = socket.gethostbyname(hostname)

    if ipaddress == "127.0.0.1":
        ipaddress = sys.argv[1]
    logging.info(ipaddress)
    sip_proxy.recordroute = "Record-Route: <sip:%s:%d;lr>" % (ipaddress, PROXY_PORT)
    sip_proxy.topvia = "Via: SIP/2.0/UDP %s:%d" % (ipaddress, PROXY_PORT)
    server = socketserver.UDPServer((HOST, PROXY_PORT), sip_proxy.UDPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server interrupted by user.\n Ending program.')
