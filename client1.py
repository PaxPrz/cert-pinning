import ssl, socket, pprint, os, sys

if not os.path.isfile('server_cert.pem'):
    cert = ssl.get_server_certificate(('127.0.0.1',9000))

    if cert:
        with open('server_cert.pem', 'w') as f:
            f.write(cert)
    else:
        print("No certificate from server")
        sys.exit()
    
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False
context.load_verify_locations(cafile='server_cert.pem')
cnx = context.wrap_socket(socket.socket(socket.AF_INET))

cnx.connect(('127.0.0.1', 9000))
print(cnx.recv(1024))
# import ipdb; ipdb.set_trace();
cnx.send(b'Hello server')
cnx.send(b'\n')