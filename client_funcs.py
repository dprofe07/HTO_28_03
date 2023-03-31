import json
import random
import socket

from constants import SERVER_UUID, PORT

count = 0


def request(data, host, port):
    text = json.dumps(data) + "\1"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except OSError:
        return None
    s.send(text.encode('utf-8'))

    res = ""
    while True:
        data = s.recv(1024)
        if not data:
            break
        elif data.endswith(b"\1"):
            data = data[:-1]
            res += data.decode("utf-8")
            break
        res += data.decode("utf-8")
    s.close()
    return res


def check_address(address, saver):
    try:
        res = request({'event': 'get uuid'}, address, PORT)

    except socket.error:
        return False
    finally:
        global count
        count += 1

    if res == str(SERVER_UUID):
        saver[0] = address
        print(f'FOUND: {address}')


def find_server(moving=False, ip=None):
    data = {
        'event': 'finding_server',
        'moving': moving,
        'code': random.randint(100000, 999999)
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, 32, 1)
    s.bind(('', 0))
    for i in range(10):
        s.sendto(json.dumps(data).encode('utf-8'), ("255.255.255.255", 65432))
    print('Recving data')
    try:
        data, addr = s.recvfrom(1024)
    except OSError:
        raise ValueError('Server not found')
    s.close()
    data = json.loads(data)
    if data['role'] != 'server':
        print('TROUBLES!!!')
    else:
        return addr[0]

'''    saver = [None]
    for i in range(1, 255):
        serv_ip = '.'.join(my_ip.split(".")[:-1] + [str(i)])
        print(f'SERVER_IP: {serv_ip}')

        threading.Thread(target=lambda: check_address(serv_ip, saver)).start()

    while count < 254:
        time.sleep(1)
        print(f'WAITING: {count}/254')
    print('WAITING: 254/254')
    if saver[0] is None:
        raise ValueError('Server not found')
    return saver[0]'''