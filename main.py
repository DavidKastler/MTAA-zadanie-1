import sipFullProxyLib.sipfullproxy as sip_proxy
import time
import socket
import sys
import socketserver

HOST, PROXY_PORT = '0.0.0.0', 5060


# nastavenie vlastnych sprav
def set_custom_messages():
    sip_proxy.msg_200 = "VYBORNE"
    sip_proxy.msg_400 = "Zla poziadavka"
    sip_proxy.msg_406 = "Ne-ak-cep-to-va-tel-ne"
    sip_proxy.msg_480 = "Docasne nedostupne"
    sip_proxy.msg_488 = "Tuto to je neakcetpovatelne"
    sip_proxy.msg_500 = "Nieco sa pokazilo so serverom"


# Touto funkciou sa zapina program
if __name__ == "__main__":
    set_custom_messages()

    logger = sip_proxy.innit_logging()

    hostname = socket.gethostname()

    ipaddress = socket.gethostbyname(hostname)
    if ipaddress == "127.0.0.1":
        ipaddress = sys.argv[1]

    start_msg = 'NEW SESSION\n\t' + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + '\n\t' +\
                hostname + '\n\t' + ipaddress

    print(start_msg)
    logger.info('\n\t' + start_msg)

    sip_proxy.recordroute = "Record-Route: <sip:%s:%d;lr>" % (ipaddress, PROXY_PORT)
    sip_proxy.topvia = "Via: SIP/2.0/UDP %s:%d" % (ipaddress, PROXY_PORT)
    server = socketserver.UDPServer((HOST, PROXY_PORT), sip_proxy.UDPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server interrupted by user.\n Ending program.')
