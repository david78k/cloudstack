cloudstack
===

Triple Elements Model (TEM) with CloudStack Python Client (descriptino)

Python client library for the CloudStack User API v3.0.0. For older versions,
see the [tags](https://github.com/jasonhancock/cloudstack-python-client/tags).

- list-simple: simple VM list with number, name, and state 
- list: detailed VM list including KVM display name, ping result, IP address, memory, and HA-enabled (high availability)
- tem-client: 
- tem-server:

```
No VM Name                        State     Ping Network       Memory HA
--------------------------------------------------------------------------------
 1 centos6-1 (i-2-14-VM)          Running    OK  192.244.34.112  2048   1
 2 centos6-2 (i-2-13-VM)          Running    OK  192.244.34.118  2048   1
 3 centos6 (i-2-11-VM)            Running    OK  192.244.34.116  2048   1
 4 centos5-ha (i-2-10-VM)         Stopped    -   192.244.34.128   512   1
 5 hadoop4 (i-2-9-VM)             Stopped    -   192.244.34.115  2048   0
```

Examples
--------

List all virtual machines

```python
#!/usr/bin/python

import CloudStack

api = 'http://example.com:8080/client/api'
apikey = 'API KEY'
secret = 'API SECRET'

cloudstack = CloudStack.Client(api, apikey, secret)

vms = cloudstack.listVirtualMachines()

for vm in vms:
    print "%s %s %s" % (vm['id'], vm['name'], vm['state'])
```


   
Asynchronous tasks

```python
#!/usr/bin/python

import CloudStack

api = 'http://example.com:8080/client/api'
apikey = 'API KEY'
secret = 'API SECRET'

cloudstack = CloudStack.Client(api, apikey, secret)

job = cloudstack.deployVirtualMachine({
    'serviceofferingid': '2',
    'templateid':        '214',
    'zoneid':            '2'
})

print "VM being deployed. Job id = %s" % job['jobid']

print "All Jobs:"
jobs = cloudstack.listAsyncJobs({})
for job in jobs:
    print  "%s : %s, status = %s" % (job['jobid'], job['cmd'], job['jobstatus'])

```

TODO:
-----
There is a lot to do to clean up the code and make it worthy of production. This
was just a rough first pass.
