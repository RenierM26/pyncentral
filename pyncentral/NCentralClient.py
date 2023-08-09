"""pyncentral main module."""
from __future__ import annotations

from re import search
from typing import Any

import requests
import zeep

from .exceptions import HTTPError, InvalidURL, NCentralError


class NCentralClient:
    """NCentralClient class."""

    def __init__(self, username: str, password: str, url: str) -> None:
        """NCentralClient constructor."""
        self.username = username
        self.password = password
        self.api_soap = "/dms2/services2/ServerEI2?wsdl"
        self.api_base_url = "https://" + url

        try:
            self.client = zeep.CachingClient(wsdl=self.api_base_url + self.api_soap)

        except requests.exceptions.ConnectionError as err:
            raise InvalidURL("A Invalid URL or Proxy error occurred") from err
        except requests.exceptions.HTTPError as err:
            raise HTTPError from err

    def customerList(self, filter_customer_name: str | None = None) -> list:
        """Return list of customers. Each customer is an array upon itself with multiple identifiers."""

        try:
            req = self.client.service.customerList(
                username=self.username, password=self.password
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        result_entities = []
        for _idx, customer in enumerate(req):
            result_entities_sub = {}
            for item in customer.items:
                result_entities_sub[item.key] = item.value
            result_entities.append(result_entities_sub)

        if filter_customer_name:
            filter_result = []
            for items in result_entities:
                if search(filter_customer_name, items["customer.customername"]):
                    filter_result.append(items)
            if not filter_result:
                raise NCentralError(
                    "A customer named:", filter_customer_name, "was not found"
                )
            return filter_result

        return result_entities

    def activeissueslist(
        self, customerid: int, filter_device_name: str | None = None
    ) -> list:
        """Return list of active issues per customer id. Each issue is an array upon itself with multiple identifiers."""
        settings = {"key": "customerId", "value": customerid}

        try:
            req = self.client.service.activeIssuesList(
                username=self.username, password=self.password, settings=settings
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        result_entities = []
        for _idx, devices in enumerate(req):
            result_entities_sub = {}
            for device in devices.items:
                result_entities_sub[device.key] = device.value
            result_entities.append(result_entities_sub)

        if filter_device_name:
            filter_result = []
            for items in result_entities:
                if search(filter_device_name, items["activeissue.devicename"]):
                    filter_result.append(items)
            if not filter_result:
                raise NCentralError(
                    "A device named:", filter_device_name, "was not found"
                )

            return filter_result

        return result_entities

    def deviceList(
        self, customerid: int, filter_device_name: str | None = None
    ) -> list:
        """Return list of devices per customer id. Each device is an array upon itself with multiple identifiers."""
        settings = {"key": "customerId", "value": customerid}

        try:
            req = self.client.service.deviceList(
                username=self.username, password=self.password, settings=settings
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        result_entities = []
        for _idx, devices in enumerate(req):
            result_entities_sub = {}
            for device in devices.items:
                result_entities_sub[device.key] = device.value
            result_entities.append(result_entities_sub)

        if filter_device_name:
            filter_result = []
            for items in result_entities:
                if search(filter_device_name, items["device.longname"]):
                    filter_result.append(items)
            if not filter_result:
                raise NCentralError(
                    "A device named:", filter_device_name, "was not found"
                )

            return filter_result

        return result_entities

    def deviceGetStatus(
        self, deviceid: int | None = None, filter_device_name: str | None = None
    ) -> list:
        """Return tasks per device id. Each task is an array with multiple identifiers."""
        settings = {"key": "deviceID", "value": deviceid}

        try:
            req = self.client.service.deviceGetStatus(
                username=self.username, password=self.password, settings=settings
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        if deviceid:
            result_entities = []
            for _idx, entities in enumerate(req):
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
                if search(filter_device_name, items["devicestatus.modulename"]):
                    filter_result.append(items)
            if not filter_result:
                raise NCentralError(
                    "A task named:", filter_device_name, "was not found"
                )

            return filter_result

        return []

    def deviceGet(self, deviceid: int | None = None) -> list:
        """Retrieve the data for a user-specified list of devices."""
        settings = {"key": "deviceID", "value": deviceid}

        if deviceid is None:
            raise NCentralError("Please specify device id")

        try:
            req = self.client.service.deviceGet(
                username=self.username, password=self.password, settings=settings
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        result_entities = []
        for _idx, entities in enumerate(req):
            result_entities_sub = {}
            for devicestatus in entities.info:
                result_entities_sub[devicestatus.key] = devicestatus.value
            result_entities.append(result_entities_sub)

        return result_entities

    def deviceAssetInfoExportDeviceWithSettings(
        self, deviceid: int | None = None
    ) -> list:
        """Retrieve the data for a user-specified list of devices."""
        settings = {"key": "TargetByDeviceID", "value": [deviceid]}

        if deviceid is None:
            raise NCentralError("Please specify device id")

        try:
            req = self.client.service.deviceAssetInfoExportDeviceWithSettings(
                version="0.0",
                username=self.username,
                password=self.password,
                settings=settings,
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        result_entities = []
        for _idx, entities in enumerate(req):
            result_entities_sub = {}
            for device in entities.items:
                result_entities_sub[device.key] = device.value
            result_entities.append(result_entities_sub)

        return result_entities

    # Set values.

    def taskPauseMonitoring(self, taskid: int | None = None) -> Any:
        """Paused monitor task. Can accept taskid as list."""
        task_id_list = [taskid]

        try:
            req = self.client.service.taskPauseMonitoring(
                username=self.username, password=self.password, taskIDList=task_id_list
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        return req

    def taskResumeMonitoring(self, taskid: int | None = None) -> Any:
        """Resume paused monitor task. Can accept taskid as list."""
        task_id_list = [taskid]

        try:
            req = self.client.service.taskResumeMonitoring(
                username=self.username, password=self.password, taskIDList=task_id_list
            )

        except zeep.exceptions.Fault as err:
            raise NCentralError("Incorrect username or password combo") from err

        return req

    # End set values.
