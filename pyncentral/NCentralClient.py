import json
import logging
import time
from re import search
import zeep
from zeep import helpers

class NCentralError(Exception):
    pass

class NCentralClient(object):
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.api_soap = "/dms2/services2/ServerEI2?wsdl"
        self.api_base_url = "https://" + url
        self.client = zeep.CachingClient(wsdl=self.api_base_url + self.api_soap)

    def customerList(self, filter_customer_name = None):
        #Returns list of customers

        req = self.client.service.customerList(username=self.username, password=self.password)

        result_entities = []
        for idx, customer in enumerate(req):
            result_entities_sub = {}
            for item in customer.items:
                result_entities_sub[item.key] = item.value
            result_entities.append(result_entities_sub)

        if filter_customer_name:
            filter_result = []
            for items in result_entities:
                if search(filter_customer_name, items['customer.customername']):
                    filter_result.append(items)
            if not filter_result:
                print("A customer named:", filter_customer_name, "was not found" )
            else:
                print (filter_result)
        else:
            print (result_entities)

        return

    def activeissueslist(self, customerid):

        settings = {'key' : 'customerId', 'value' : customerid}

        devices = self.client.service.activeIssuesList(username=self.username, password=self.password, settings=settings)

        for device in devices:
            print(device)

        return

    def deviceList(self, customerid, filter_device_name = None):
        #Returns list of devices per customer id. Each device is an array upon itself with multiple identifiers.)
        settings = {'key' : 'customerId', 'value' : customerid}

        req = self.client.service.deviceList(username=self.username, password=self.password, settings=settings)

        result_entities = []
        for idx, devices in enumerate(req):
            result_entities_sub = {}
            for device in devices.items:
                result_entities_sub[device.key] = device.value
            result_entities.append(result_entities_sub)

        if filter_device_name:
            filter_result = []
            for items in result_entities:
                if search(filter_device_name, items['device.longname']):
                    filter_result.append(items)
            if not filter_result:
                print("A device named:", filter_device_name, "was not found" )
            else:
                print (filter_result)
        else:
            print (result_entities)

        return

    def deviceGetStatus(self, deviceid = None, filter_task_name = None):
        #returns tasks per device id. Each task is and array with multiple identifiers.
        settings = {'key' : 'deviceID', 'value' : deviceid}

        req = self.client.service.deviceGetStatus(username=self.username, password=self.password, settings=settings)

        if deviceid:
            result_entities = []
            for idx, entities in enumerate(req):
                result_entities_sub = {}
                for devicestatus in entities.items:
                    result_entities_sub[devicestatus.key] = devicestatus.value
                result_entities.append(result_entities_sub)

        if deviceid and not filter_task_name:
            print(result_entities)

        if not deviceid:
            print("Please supply device id")

        if filter_task_name and deviceid:
            filter_result = []
            for items in result_entities:
                if search(filter_task_name, items['devicestatus.modulename']):
                    filter_result.append(items)
            if not filter_result:
                print("A task named:", filter_task_name, "was not found" )
            else:
                print (filter_result)

        return

########################Set values#####################################################

    def taskPauseMonitoring(self, taskid = None):
        #Paused monitor task. Can accept taskid as list
        task_id_list = [taskid]

        req = self.client.service.taskPauseMonitoring(username=self.username, password=self.password, taskIDList=task_id_list)

        print(req)
        
        return

    def taskResumeMonitoring(self, taskid = None):
        #Resume paused monitor task. Can accept taskid as list
        task_id_list = [taskid]

        req = self.client.service.taskResumeMonitoring(username=self.username, password=self.password, taskIDList=task_id_list)

        print(req)
        
        return


########################End set values#################################################