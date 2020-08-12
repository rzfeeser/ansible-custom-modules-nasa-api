#!/usr/bin/python3

# Copyright: (c) 2020, Russell Zachary Feeser <rzfeeser@users.noreply.github.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: nasa_eonet

short_description: Interact with NASA Earth Observatory Natural Event Tracker (EONET). More information available at https://api.nasa.gov and https://eonet.sci.gsfc.nasa.gov/

version_added: "2.9"

description:
    - "This module gets data from NASA Earth Observatory Natural Event Tracker (EONET) service and converts this data to YAML format, saving it on the local system. The outputted file is saved in the format eonet-YYYY-MM-DDtoYYY-MM-DD.yml. By default the file is saved to the local folder, however, the user can control the path as to where the output file is placed. This module will only show CHANGED if the module creates a YAML output file. If the module FAILS it will display the HTTP code associated with the failed response."

options:
    source:
        description:
            - Filter the returned events by the Source. Multiple sources can be included in the parameter as a comma seperated list. For values within source, see https://eonet.sci.gsfc.nasa.gov/docs/v3#sourceFields
        required: false
    status:
        description:
            - May take the value of "open" or "closed". Events that have ended are assigned a closed date and the existence of that date will allow you to filter for only-open or only-closed events. Omitting the status parameter will return only the currently open events.
        required: false
    limit:
        description:
            - Limits the number of events returned
        required: false
    days:
        description:
            - Limit the number of prior days (including day) from which events will be returned.
        required: false
    start:
        description:
            - Takes the format YYYY-MM-DD to select a range of dates for the events to fall between.
        required: false
    end:
        description:
            - Takes the format YYYY-MM-DD to select a range of dates for the events to fall between.
    magID:
        description:
            - takes the format #.## to select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        required: false
    magMin:
        description:
            - takes the format #.## to select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        required: false
    magMax:
        description:
            - takes the format #.## to select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        required: false
    bbox:
        description:
            - takes the format (minLon,maxLon,minLat,maxLat) to Query using a bounding box for all events with datapoints that fall within. This uses two pairs of coordinates: the upper left hand corner (lon,lat) followed by the lower right hand corner (lon,lat).
    savepath:
        description:
           - Path a save the converted YAML file to, defaults to current directory. The outputted file is saved in the format eonet-YYYY-MM-DDtoYYY-MM-DD.yml
        required: false

author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = '''
# Grab EONET data from NASA and convert to YAML saved in local directory
- name: Grab EONET data and convert to YAML in local directory
  nasa_eonet_event:

# Grab EONET data from NASA and conver to YAML for the date 2020-06-15 then save in current directory
- name: Get EONET data and convert to YAML for start date 2020-06-15
  nasa_eonet_event:
    start: 2020-06-15

'''

RETURN = '''
original_nasa_json:
    description: This is the JSON as returned by NASA by their EONET Event API
    type: dict
    returned: always
status_code:
    description: The status code the JSON was returned on
    type: str
    returned: always
file_loc:
    description: The path to the file containing converted JSON to YAML.
    type: str
    returned: always
yaml_output_file:
    description: The name of the YAML output file
    type: str
    returned: always
start_date:
    description: The start date supplied to the NASA EONET Event API
    type: str
    returned: always
end_date:
    description: The end date supplied to the NASA EONET Event API
    tye: str
    returned: always
'''
NASAEONET = "https://eonet.sci.gsfc.nasa.gov/api/v3/events?"

import os

from datetime import datetime

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule

# https://requests.readthedocs.io/en/master/
# python3 -m pip install requests
import requests

# python3 -m pip install pyyaml
import yaml

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        source=dict(type='str', required=False),
        status=dict(type='str', required=False, choices=["open", "closed"]),
        limit=dict(type='str', required=False),
        days=dict(type='str', required=False),
        start=dict(type='str', required=False),
        end=dict(type='str', required=False),
        magID=dict(type='str', required=False),
        magMin=dict(type='str', required=False),
        magMax=dict(type='str', required=False),
        bbox=dict(type='str', required=False),
        savepath=dict(type='str', required=False, default=os.getcwd())
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_nasa_json='',
        status_code='',
        file_loc='',
        yaml_output_file='',
        start_date='',
        end_date=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    
    ## create a compelte URI to query (including params)
    ## https://eonet.sci.gsfc.nasa.gov/api/v3/events
    queryparams = []

    for mp in module.params:
        if module.params[mp] is not None and mp != "savepath":
            queryparams.append(f"{mp}={module.params[mp]}&")

    qp = "".join(queryparams).rstrip("&")

    lookMeUp = f"{NASAEONET}{qp}"

    ## Send an HTTP GET - API call to nasa based on compelted URI+queryparams
    resp = requests.get(lookMeUp)

    ## if the response was NOT a 200, ansible module should FAIL
    if resp.status_code != 200:
        module.fail_json(msg=f"The NASA EONET Event API lookup was not successful. STATUS CODE - {resp.status_code}", **result)

    ## strip JSON off HTTP 200 response
    nasaJson = resp.json()

    ## convvert JSON to YAML
    nasaYaml = yaml.dump(nasaJson)


    sp = module.params["savepath"]
    ## check to see if file already exists
    ## if file does not exist then create it
    savename = "eonet-"
    
    if module.params["start"] is not None:
        savename += module.params["start"]

    if module.params["end"] is not None:
        savename = f"{savename}to{module.params['end']}.yml"
    else:
        savename += datetime.today().strftime('%Y-%m-%d')


    if not os.path.isfile(f"{sp}{savename}"):
        ## save YAML as file locally
        with open(f"{sp}{savename}", "w") as myfile:
            myfile.write(nasaYaml)
        result['changed'] = True

    # set results that will be returned via JSON to the ansible module
    result['original_nasa_json'] = nasaJson # the JSON gathered from NASA
    result['status_code'] = resp.status_code # the HTTP response code
    result['file_loc'] = sp # the path to the save filed
    result['yaml_output_file'] = savename # name of the YAML output file created
    result['start_date'] = module.params["start"] # the start search date
    result['end_date'] = module.params["end"] # the end search date

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
