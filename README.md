# pyncentral
Python API for Solarwinds NCentral using SOAP.

1) install using pi install pyncentral

Usage:

Actions are based on 4 tasks:

pyncentral -username "USERNAME" -p "PASSWORD" -url "www.myncentralserver.local" all -h
pyncentral -username "USERNAME" -p "PASSWORD" -url "www.myncentralserver.local" customer -h
pyncentral -username "USERNAME" -p "PASSWORD" -url "www.myncentralserver.local" device -h
pyncentral -username "USERNAME" -p "PASSWORD" -url "www.myncentralserver.local" task -h


Please use -h switch for more info 


Ncentral genral refereneces:

1) Each customer or site has a CustomerID
2) Each device has a unique id
3) Each monitored item on a device is called a task and also has a unique id (in API)


What is implemented:

1) You can pause/enable monitoring of spesific items ---- Yes, that means a website or service on a server for example.
2) You list customers.
3) You can list devices per customer.
4) You can list tasks per device.
5) Get active issue list per customer.
6) Get device info.

Output: All in Json format ;-)
