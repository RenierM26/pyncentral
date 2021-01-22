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

        try:
            req = self.client.service.customerList(username=self.username, password=self.password)

        except:
            raise NCentralError("Incorrect username or password combo")

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
                raise NCentralError("A customer named:", filter_customer_name, "was not found" )
            else:
                return filter_result
        else:
            return result_entities

        return

    def activeissueslist(self, customerid, filter_device_name = None):

        settings = {'key' : 'customerId', 'value' : customerid}

        try:
            req = self.client.service.activeIssuesList(username=self.username, password=self.password, settings=settings)

        except:
            raise NCentralError("Incorrect username or password combo")

        result_entities = []
        for idx, devices in enumerate(req):
            result_entities_sub = {}
            for device in devices.items:
                result_entities_sub[device.key] = device.value
            result_entities.append(result_entities_sub)

        if filter_device_name:
            filter_result = []
            for items in result_entities:
                if search(filter_device_name, items['activeissue.devicename']):
                    filter_result.append(items)
            if not filter_result:
                raise NCentralError("A device named:", filter_device_name, "was not found" )
            else:
                return filter_result
        else:
            return result_entities

    def deviceList(self, customerid, filter_device_name = None):
        #Returns list of devices per customer id. Each device is an array upon itself with multiple identifiers.)
        settings = {'key' : 'customerId', 'value' : customerid}

        try:
            req = self.client.service.deviceList(username=self.username, password=self.password, settings=settings)

        except:
            raise NCentralError("Incorrect username or password combo")

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
                raise NCentralError("A device named:", filter_device_name, "was not found" )
            else:
                return filter_result
        else:
            return result_entities

    def deviceGetStatus(self, deviceid = None, filter_device_name = None):
        #returns tasks per device id. Each task is an array with multiple identifiers.
        settings = {'key' : 'deviceID', 'value' : deviceid}

        try:
            req = self.client.service.deviceGetStatus(username=self.username, password=self.password, settings=settings)

        except:
            raise NCentralError("Incorrect username or password combo")

        if deviceid:
            result_entities = []
            for idx, entities in enumerate(req):
                result_entities_sub = {}
                for devicestatus in entities.items:
                    result_entities_sub[devicestatus.key] = devicestatus.value
                result_entities.append(result_entities_sub)

        if deviceid and not filter_device_name:
            return result_entities

        if not deviceid:
            raise NCentralError("Please supply device id")

        if filter_device_name and deviceid:
            filter_result = []
            for items in result_entities:
                if search(filter_device_name, items['devicestatus.modulename']):
                    filter_result.append(items)
            if not filter_result:
                raise NCentralError("A task named:", filter_device_name, "was not found" )
            else:
                return filter_result

    def deviceGet(self, deviceid = None):
        #retrieves the data for a user-specified list of devices.
        settings = {'key' : 'deviceID', 'value' : deviceid}

        if deviceid == None:
            raise NCentralError("Please specify device id")

        try:
            req = self.client.service.deviceGet(username=self.username, password=self.password, settings=settings)

        except:
            raise NCentralError("Incorrect username or password combo")

        result_entities = []
        for idx, entities in enumerate(req):
            result_entities_sub = {}
            for devicestatus in entities.info:
                result_entities_sub[devicestatus.key] = devicestatus.value
            result_entities.append(result_entities_sub)

        return result_entities


########################Set values#####################################################

    def taskPauseMonitoring(self, taskid = None):
        #Paused monitor task. Can accept taskid as list
        task_id_list = [taskid]

        try:
            req = self.client.service.taskPauseMonitoring(username=self.username, password=self.password, taskIDList=task_id_list)

        except:
            raise NCentralError("Incorrect username or password combo")

        return req

    def taskResumeMonitoring(self, taskid = None):
        #Resume paused monitor task. Can accept taskid as list
        task_id_list = [taskid]

        try:
            req = self.client.service.taskResumeMonitoring(username=self.username, password=self.password, taskIDList=task_id_list)

        except:
            raise NCentralError("Incorrect username or password combo")

        return req

########################End set values#################################################