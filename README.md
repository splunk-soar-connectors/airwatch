# AirWatch

Publisher: Splunk Community <br>
Connector Version: 1.0.2 <br>
Product Vendor: Mhike <br>
Product Name: AirWatch <br>
Minimum Product Version: 4.9.39220

This app interacts with Airwatch

### Configuration variables

This table lists the configuration variables required to operate AirWatch. These variables are specified when configuring a AirWatch asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**tenant** | required | password | AirWatch Tenant Code |
**username** | required | string | Basic Auth Username for AirWatch API |
**password** | required | password | Basic Auth Password for AirWatch API |
**base_url** | required | string | Base URL for AirWatch API |
**verify_server_cert** | optional | boolean | Verify server certificate |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied credentials <br>
[add to group](#action-add-to-group) - Add device UUID to AirWatch Group

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied credentials

Type: **test** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'add to group'

Add device UUID to AirWatch Group

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**smartgroup_uuid** | required | AirWatch Smartgroup UUID | string | |
**device_uuid** | required | Device UUID | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.smartgroup_uuid | string | | |
action_result.parameter.device_uuid | string | | |
action_result.data | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
