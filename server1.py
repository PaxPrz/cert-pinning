import socket, ssl

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="selfsigned.crt", keyfile="selfsigned.key")

bindsocket = socket.socket()
bindsocket.bind(('127.0.0.1', 9000))
bindsocket.listen(5)

print("STARTING SERVER...")

while True:
    try:
        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        print('Got connection')
        connstream.send(b'Greetings to my server')
        # import ipdb; ipdb.set_trace();
        while 1:
            data = connstream.recv(1024)
            if not data or data == b'\n':
                break
            print('Data: ', data)
        print('Closing connection')
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
    except Exception as e:
        print("ERROR: ", e)