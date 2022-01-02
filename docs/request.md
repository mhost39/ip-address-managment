## this docs explain the format for every request

- Add a VLAN
```
/api/vlan POST

body:
{
	"name": "vlan_name",
	"descrition": "describe vlan"
}
```

- Add a Subnet
```
/api/subnet POST

body:
{
	"name": "subnet_name",
	"descrition": "describe subnet",
	"address": "subnet address in format x.x.x.x/mask",
	"vlan_id": 1
}
```

- Reserve IP with Specific Subnet Name
```
/api/reserve_ip/<string:name> POST

you will get your Reserve ip iin response 
```

- Get All VLANs
```
/api/vlan GET
```

- Get VLAN With Specific ID
```
/api/vlan/<int:id> GET
```

- Get All Subnets
```
/api/subnet GET
```

- Get Subnet With Specific ID
```
/api/subnet/<int:id> GET
```

- Get details regarding an IP (parent Subnet, is it free or used)
```
/api/ip/<string:ip> GET

well get parent Subnet and IP status (if used if free)
```

- Delete VLAN
```
/api/vlan/<int:id> DELETE
```

- Delete Subnet
```
/api/subnet/<int:id> DELETE
```

- Update a VLAN
```
/api/vlan/<int:id> PUT

body:
{
	"name": "new_vlan_name",
	"descrition": "describe vlan"
}
```

- Update a Subnet
```
/api/subnet/<int:id> PUT

body:
{
	"name": "subnet_name",
	"descrition": "describe subnet",
	"address": "subnet address in format x.x.x.x/mask",
	"vlan_id": 1
}
```
