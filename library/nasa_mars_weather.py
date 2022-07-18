#!/usr/bin/python

# Copyright: (c) 2020, Russell Zachary Feeser <RZfeeser@alta3.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nasa_mars_weather

short_description: Pull weather data from mars

version_added: "1.0.0"

description: See https://api.nasa.gov InSight: Mars Weather Service API https://api.nasa.gov/insight_weather/

options:
    name:
        description: This is the name of the FILE that we want to produce. The name will be given a *.txt extension
        required: true
        type: str
    file_loc:
        description: This is the location that the FILE will be saved to. If not provided, /tmp/ will be used.
        requred: false
        type: str
    version:
        description: This is the version of the API to use. Default to 1
        required: false
        type: int
    feedtype:
        description: The format of what is returned. Currently the default is JSON and only JSON works.
        required: false
        type: str
    apikey:
        description: This is the NASA API key to send to the module. Default to DEMO_KEY.
        required: false
        type: str

author:
    - RZFeeser (@rzfeeser)
'''

EXAMPLES = r'''
# Most elementary usage of the module
- name: Pull Mars weather
  nasa_mars_weather:
    name: 2021-04-27-marsweather   # the module adds *.txt to the file name

# Typical usage of the module
- name: Pull Mars weather, with cust API key
  nasa_mars_weather:
    name: todaysweather   # the module adds *.txt to the file name
    apikey: a1b2c3d4e5f6g   # api key avail from api.nasa.gov

# Write file to a directory
- name: Pull Mars weather and save into /tmp
  nasa_mars_weather:
    name: weatherreport         # the module add *.txt to the file name
    apikey: just1234example     # api key avail from api.nasa.gov
    file_loc: /tmp/
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
mars_weather:
    description: The weather report returned by https://api.nasa.gov/insight_weather/
    type: dict
    returned: always
    sample: {... ...}
savelocation:
    description: path and file name where weather report was saved to
    type: str
    returned: always
    sample: /home/student/todaysweather.txt
status_code:
    description: The status code returned to the lookup to https://api.nasa.gov/insight_weather/
    type: int
    returned: always
    sample: 200
apisearched:
    description: This is the API that the HTTP GET was sent to.
    type: str
    returned: always
    sample: https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1
'''

NASAAPI = "https://api.nasa.gov/insight_weather/?api_key="

# std library imports are first

# 3rd party libraries are next
# python3 -m pip install requests
import requests

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        file_loc=dict(type='str', required=False, default="/tmp"),
        version=dict(type='int', required=False, default=1),
        feedtype=dict(type='str', required=False, default="json"),
        apikey=dict(type='str', required=False, default="DEMO_KEY"),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        mars_weather={},
        savelocation='',
        status_code=0,
        apisearched="",
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # what is the save location going to be
    saveloc = f"{module.params['file_loc']}/{module.params['name']}"
    result["savelocation"] = saveloc

    # put together the api we will lookup
    api = f"{NASAAPI}{module.params['apikey']}&feedtype={module.params['feedtype']}&ver={module.params['version']}"
    result["apisearched"]= api

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    r = requests.get(api)

    result['status_code'] = r.status_code

    # pull the JSON response off the 200 code
    weather = r.json()
    result['mars_weather'] = weather

    # save out the file
    with open(f"{saveloc}.txt", "w") as mw:
        mw.write(r.text)

    # state has been modified
    result['changed'] = True
    
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
