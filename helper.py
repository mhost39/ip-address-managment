
import struct, socket
from flask import request, jsonify


def ip_to_int(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]

def int_to_ip(i):
    return socket.inet_ntoa(struct.pack('!L', i))

def is_ip_valied(add):
    try:
        socket.inet_pton(socket.AF_INET, add)
    except AttributeError:
        try:
            socket.inet_aton(add)
        except socket.error:
            return False
        return add.count('.') == 3
    except socket.error:
        return False

    return True

def cidr_to_netmask(net_bits):
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask

def get_ip_detail(subnet, ip):
    result = dict()
    network_IP, mask = subnet["ip"].split("/")
    network_IP = ip_to_int(network_IP)
    mask = int(mask)

    result['parent_subnet'] = cidr_to_netmask(mask)
    first_free_ip = network_IP + subnet['reserved_ips_count']

    if ( ip <  first_free_ip):
        result['status'] = "used"
    elif ( ip >= first_free_ip ):
        result['status'] = "free"
    return result

def response(result="", notification="", request_info=None):
    return jsonify({'result': result, 'notification': notification, 'request_info': dict(request.view_args)})
