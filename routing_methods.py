from flask import request
import json

from helper import response, ip_to_int, int_to_ip, is_ip_valied, cidr_to_netmask, get_ip_detail
from database import DataBase
from models import VLAN, Subnets


database = DataBase()

def index():
    return "Welcome to IP Address Management API"

def api_add_vlan():
    data = json.loads(request.data)
    result = database.insert_data(VLAN, name=data['name'], descrition=data['descrition'])
    if type(result) is str:
        return response('error', result)
    else:
        return response('success', 'VLAN ' + data['name'] + ' succesfully added')

def api_add_subnet():
    data = json.loads(request.data)
    ip, mask = data["address"].split("/")
    if (not is_ip_valied(ip)): # check the ip format should be in this format x.x.x.x where 0 <= x <= 255
        return response('error address not valied')
    ip = ip_to_int(ip)  # convert ip address to integer like 192.168.0.1 > 3232235521
    result = database.insert_data(Subnets, name=data['name'], ip=ip, mask=int(mask), vlan_id=data['vlan_id'], descrition=data['descrition'])
    if type(result) is str:
        return response('error', result)
    else:
        return response('success', 'Subnet ' + data['name'] + ' succesfully added')

def api_reserve_ip(name):
    subnet = database.select_by_id(Subnets, name=name)
    
    broadcast_ip = subnet['ip'] + pow(2, (32 - subnet['mask'])) - 1  # calculate the broadcast ip (last ip on network)

    reserved_ips_count = subnet["reserved_ips_count"]
    first_free_ip = subnet['ip'] + reserved_ips_count + 1  # calculate the first free ip. will be the subnet ip + count of reserved ips  

    if (first_free_ip >= broadcast_ip):
        return response("no free IPs on this VlAN")
    database.update_by_id(tablename=Subnets, id=subnet["id"], reserved_ips_count=reserved_ips_count + 1)  # update count of reserved ips  
    return response('success', 'your ip is '+ int_to_ip(first_free_ip),)



def api_get_vlans():
    return response(result=database.select_all(VLAN))

def api_get_vlan(id):
    return response(result=database.select_by_id(VLAN, id=id))

def api_get_subnets():
    return response(result=database.select_all(Subnets))

def api_get_subnet(id):
    result = database.select_by_id(Subnets, id=id)
    data_list = dict()
    data_list["vlan_id"] = result["vlan_id"]
    data_list["network_IP"] = int_to_ip(result["ip"])
    data_list["subnet_mask"] = cidr_to_netmask(result["mask"])
    data_list["utilization_percentage"] = "{:.1f} %".format(result["reserved_ips_count"] / ( pow(2, (32 - result['mask'])) - 2) * 100)
    data_list["subnet_name"] = result["name"]

    return response(data_list)

def api_get_ip_details(ip):
    if(not is_ip_valied(ip)):
        return response({"error": "ip not in valied format"})

    int_ip = ip_to_int(ip)
    subnets = database.select_all(Subnets)
    ip_details = dict()
    for s in subnets:  #  loop through all subnets and get the subnet that contain this ip
        network_IP, mask = s["ip"].split("/")  #  get the network ip (first ip) and mask for subnet
        network_IP = ip_to_int(network_IP)  # convert the ip from string to int like 192.168.0.1 > 3232235521
        mask = int(mask)
        
        broadcast_ip = network_IP + pow(2, (32 - mask))  #  calculate broadcast ip (last ip in network) for subnet 

        if (int_ip >= network_IP and int_ip <= broadcast_ip):  #  if this ip in this subnet get ip detail
            ip_details = get_ip_detail(s, int_ip)

    if (ip_details):
        return response(result= ip_details)

    return response({"error": "cant find the ip"})
    
def api_delete_vlan(id):
    result = database.delete_data(VLAN, id=id)
    if type(result) is str:
        return response('error', result)
    else:
        return response('success', 'successfully deleted')

def api_delete_subnet(id):
    result = database.delete_data(Subnets, id=id)
    if type(result) is str:
        return response('error', result)
    else:
        return response('success', 'successfully deleted')

def api_update_vlan(id):
    data = json.loads(request.data)
    database.update_by_id(tablename=VLAN, id=id, **data)
    return response('success', 'successfully deleted')

def api_update_subnet(id):
    data = json.loads(request.data)
    database.update_by_id(tablename=Subnets, id=id, **data)
    return response('success', 'successfully deleted')

route_config = [
    
    { "endpoint" : "/", "endpoint_name" : "index", "handler" : index, "methods" : ['GET']},
    
    #               >>>>>>>>>>> POST Requests <<<<<<<<<<< 
    { "endpoint" : "/api/vlan", "endpoint_name" : "api_add_vlan", "handler" : api_add_vlan, "methods" : ['POST']},
    { "endpoint" : "/api/subnet", "endpoint_name" : "api_add_subnet", "handler" : api_add_subnet, "methods" : ['POST']},
    { "endpoint" : "/api/reserve_ip/<string:name>", "endpoint_name" : "api_reserve_ip", "handler" : api_reserve_ip, "methods" : ['POST']},
    
    #               >>>>>>>>>>> GET Requests <<<<<<<<<<< 
    { "endpoint" : "/api/vlan/", "endpoint_name" : "api_get_vlans", "handler" : api_get_vlans, "methods" : ['GET']},
    { "endpoint" : "/api/vlan/<int:id>", "endpoint_name" : "api_get_vlan", "handler" : api_get_vlan, "methods" : ['GET']},
    { "endpoint" : "/api/subnet/", "endpoint_name" : "api_get_subnets", "handler" : api_get_subnets, "methods" : ['GET']},
    { "endpoint" : "/api/subnet/<int:id>", "endpoint_name" : "api_get_subnet", "handler" : api_get_subnet, "methods" : ['GET']},
    { "endpoint" : "/api/ip/<string:ip>", "endpoint_name" : "api_get_ip_details", "handler" : api_get_ip_details, "methods" : ['GET']},
    
    #               >>>>>>>>>>> DELETE Requests <<<<<<<<<<< 
    { "endpoint" : "/api/vlan/<int:id>", "endpoint_name" : "api_delete_vlan", "handler" : api_delete_vlan, "methods" : ['DELETE']},
    { "endpoint" : "/api/subnet/<int:id>", "endpoint_name" : "api_delete_subnet", "handler" : api_delete_subnet, "methods" : ['DELETE']},
    
    #               >>>>>>>>>>> PUT Requests <<<<<<<<<<< 
    { "endpoint" : "/api/vlan/<int:id>", "endpoint_name" : "api_update_vlan", "handler" : api_update_vlan, "methods" : ['PUT']},
    { "endpoint" : "/api/subnet/<int:id>", "endpoint_name" : "api_update_subnet", "handler" : api_update_subnet, "methods" : ['PUT']},
]
