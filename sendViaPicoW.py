
def PassItOn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    try:
        while True:
            conn, addr = s.accept()
            print('Connection: %s' % str(addr))
            req = conn.recv(1024)
            req = str(req)
            print('Connect = %s' % req)
            client.publish(TOPIC, req)
