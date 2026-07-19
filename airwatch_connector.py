# File: airwatch_connector.py
# Copyright (c) 2020-2026 Splunk Inc.
#
# Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)

import json
import sys
from urllib.parse import quote

import phantom.app as phantom
import requests
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from airwatch_consts import *


class AirWatchConnector(BaseConnector):
    def __init__(self):
        super().__init__()

        self._tenant = None
        self._username = None
        self._password = None
        self._python_version = None
        self._verify_server_cert = True

    def initialize(self):
        """Automatically called by the BaseConnector before the calls to the handle_action function"""

        config = self.get_config()

        # Fetching the Python major version
        try:
            self._python_version = int(sys.version_info[0])
        except:
            return self.set_status(phantom.APP_ERROR, "Error occurred while getting the Phantom server's Python major version.")

        # Fetching configuration parameters
        self._username = config["username"]
        self._password = config["password"]
        self._tenant = config["tenant"]
        self._base_url = config["base_url"].strip("/")
        self._verify_server_cert = config.get("verify_server_cert", True)

        return phantom.APP_SUCCESS

    def finalize(self):
        return phantom.APP_SUCCESS

    def _get_error_message_from_exception(self, e):
        """ This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        error_msg = AIRWATCH_ERR_MSG
        error_code = AIRWATCH_ERR_CODE_MSG
        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_code = AIRWATCH_ERR_CODE_MSG
                    error_msg = e.args[0]
            else:
                error_code = AIRWATCH_ERR_CODE_MSG
                error_msg = AIRWATCH_ERR_MSG
        except:
            error_code = AIRWATCH_ERR_CODE_MSG
            error_msg = AIRWATCH_ERR_MSG

        try:
            if error_code in AIRWATCH_ERR_CODE_MSG:
                error_text = "Error Message: {0}".format(error_msg)
            else:
                error_text = "Error Code: {0}. Error Message: {1}".format(error_code, error_msg)
        except:
            self.debug_print(AIRWATCH_PARSE_ERR_MSG)
            error_text = AIRWATCH_PARSE_ERR_MSG

        return error_text

    def _get_headers(self):
        self.save_progress("Trying to get headers")
        # Creating headers
        headers = dict()
        headers["aw-tenant-code"] = self._tenant
        headers["Accept"] = "application/json;version=2"
        headers["Content-Type"] = "application/json"
        return headers

    def _build_groupadd_body(self, param):
        self.save_progress("Trying to build body to add a device into the group")

        # Fetching the action parameters
        device_uuid = param.get("device_uuid")

        # Return the body
        return json.dumps(
            [
                {
                    "value": device_uuid,
                    "path": "/smartGroupsOperationV2/devices",
                    "op": "add",
                }
            ]
        )

    def _build_groupadd_url(self, param):
        self.save_progress("Trying to build URL to add a device into the group")

        # Fetching the action parameters
        smartgroup_uuid = quote(str(param.get("smartgroup_uuid")), safe="")

        # Return the URL
        return f"{self._base_url}/mdm/smartgroups/{smartgroup_uuid}"

    def _add_to_group(self, param):
        self.save_progress("Try to add a device into the group")
        action_result = self.add_action_result(ActionResult(dict(param)))

        try:
            # Try to create headesr based on the provided configuration parameters
            headers = self._get_headers()

            # Trying to build body to add a device into the group
            body = self._build_groupadd_body(param)
            self.save_progress(f"Body: {body}")

            # Trying to build URL to add a device into the group
            url = self._build_groupadd_url(param)
            self.save_progress(f"URL: {url}")

            # Fetching the action parameters
            device_id = param.get("device_uuid")
            smartgroup_uuid = param.get("smartgroup_uuid")

            # Try to make REST call
            try:
                response = requests.patch(
                    url,
                    data=body,
                    headers=headers,
                    auth=(self._username, self._password),
                    verify=self._verify_server_cert,
                )
            except requests.exceptions.InvalidSchema:
                error_message = f"Error connecting to server. No connection adapters were found for {url}"
                return action_result.set_status(phantom.APP_ERROR, error_message)
            except requests.exceptions.InvalidURL:
                error_message = f"Error connecting to server. Invalid URL {url}"
                return action_result.set_status(phantom.APP_ERROR, error_message)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, f"Error Connecting to server. {self._get_error_message_from_exception(e)}")

            # Parsing the response
            self.save_progress(f"Status code: {response.status_code}")
            json_response = json.loads(response.text)

            # Checking the response
            if response.status_code >= 200 and response.status_code < 300 and device_id in json_response.get("devices", []):
                self.save_progress(f"Device ({device_id}) successfully added to smartgroup ({smartgroup_uuid})")
                return action_result.set_status(phantom.APP_SUCCESS, "Successfully added device to group")
            else:
                error_msg = f"Failed to add device to group. Response status code: {response.status_code}"
                self.save_progress(error_msg)
                return action_result.set_status(phantom.APP_ERROR, error_msg)

        except Exception as e:
            error_msg = f"Error occurred while adding a device into the group. {self._get_error_message_from_exception(e)}"
            self.save_progress(error_msg)
            return action_result.set_status(phantom.APP_ERROR, error_msg)

    def _test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("The test connectivity action doesn't perform any validation for the asset configuration parameters")
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        action = self.get_action_identifier()
        ret_val = phantom.APP_SUCCESS
        if action == ACTION_ID_ADD:
            ret_val = self._add_to_group(param)
        elif action == ACTION_ID_TEST:
            ret_val = self._test_connectivity(param)
        return ret_val


if __name__ == '__main__':
    import pudb
    pudb.set_trace()
    if len(sys.argv) < 2:
        print('No test json specified as input')
        exit(0)
    with open(sys.argv[1]) as (f):
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))
        connector = AirWatchConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))
    exit(0)
