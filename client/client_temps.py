from client_funcs import find_server, request
from constants import PORT

HOST = find_server()

print('STARTING')
print(HOST)

print(f"Received {request({'event': 'get uuid'}, HOST, PORT)!r}")

request({'event': 'set temp', 'inside': 100, 'outside': 0}, HOST, PORT)

# print(f"Received {request({'event': 'get inside temp'}, HOST, PORT)!r}")
