[comment]: # "Auto-generated SOAR connector documentation"
# AirWatch

Publisher: Splunk Community  
Connector Version: 1\.0\.3  
Product Vendor: Mhike  
Product Name: AirWatch  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app interacts with Airwatch

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a AirWatch asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**tenant** |  required  | password | AirWatch Tenant Code
**username** |  required  | string | Basic Auth Username for AirWatch API
**password** |  required  | password | Basic Auth Password for AirWatch API
**base\_url** |  required  | string | Base URL for AirWatch API

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied credentials  
[add to group](#action-add-to-group) - Add device UUID to AirWatch Group  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied credentials

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'add to group'
Add device UUID to AirWatch Group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**smartgroup\_uuid** |  required  | AirWatch Smartgroup UUID | string | 
**device\_uuid** |  required  | Device UUID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.smartgroup\_uuid | string | 
action\_result\.parameter\.device\_uuid | string | 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 