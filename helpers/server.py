import logging
from threading import Thread
from wsgiref.simple_server import make_server

APP_HOST = '127.0.0.1'

def print_service_running(host, port):
    msg = f"Service running at http://{host}:{port}"
    logging.info(msg)
    print(f"Service SOAP is listeining on {msg}/")
    print(f"WSDL disponible sur {msg}/?wsdl")
    
    
def runService(service_name, host, port, application):
    logging.info(f"Starting {service_name} SOAP server...")
    server = make_server(host, port, application)
    print_service_running(host, port)
    server.serve_forever()
    
def runServiceInThread(service_name, host, port, application):
    def target():
        logging.info(f"Starting {service_name} SOAP server...")
        server = make_server(host, port, application)
        print_service_running(host, port)
        server.serve_forever()
    Thread(target=target, daemon=True).start()