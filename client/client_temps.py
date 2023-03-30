from client_funcs import find_server, my_ip, request
from constants import PORT

HOST = find_server()

print('STARTING')
print(HOST)

print(f"Received {request({'event': 'get uuid'}, HOST, PORT)!r}")

request({'event': 'set temp', 'inside': 10, 'outside': 100}, HOST, PORT)

# print(f"Received {request({'event': 'get inside temp'}, HOST, PORT)!r}")