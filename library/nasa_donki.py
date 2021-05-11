#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nasa_donki

short_description: interaction with nasa api service @ https://api.nasa.gov/ and https://ccmc.gsfc.nasa.gov/donki/ 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: interaction with nasa donki notification service. The structure of this api is

https://api.nasa.gov/DONKI/notifications?startDate=2014-05-01&endDate=2014-05-08&type=all&api_key=DEMO_KEY

Interaction with this API requires an API keys. Keys are avail @ https://api.nasa.gov/.

requirements: The requests library (python) is required on the host that executes this module. https://docs.python-requests.org/en/master/

options:
    name:
        description: This is the name of the file to save. No need to provide a file extension (.txt will be appended to the name provided). Default: results.txt
        required: false
        type: str
    dest:
        description: Full path to where output file should be saved. (default output file name is results.json). Include trailing. Default: /tmp/
        required: false
        type: str
    apikey:
        description: This is the NASA API key to send to the module. Default to DEMO_KEY
        required: false
        type: str
    startdate:
        description: in format 'yyyy-MM-dd'. Default: if left out would default to 7 days prior to the current UT date.
        required: false
        type: str
    enddate:
        description: in format 'yyyy-MM-dd'. Default: if left out would default to current UT date
        required: false
        type: str
    datatype:
        description: 'type' could be: all, FLR, SEP, CME, IPS, MPC, GST, RBE, or report. Default: 'all'
        required: false
        type: str


# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = r'''
# basic usage of the module does not require any params
# however, in the example below, the api key DEMO_KEY is being used
# this has limitations. See api.nasa.gov for more info on apikey.
- name: Basic usage of our module
  nasa_donki:

# Below example provides custom api key value
# as well as a custom save file
- name: Save output from API lookup of last seven days to output_message.txt
  nasa_donki:
    name: output_message
    apikey: 24601 #avail @ api.nasa.gov

# Lookup data from across a span of dates
# using the format yyyy-MM-dd
- name: Return data from 2021-01-01 to 2021-01-04
  nasa_donki:
    name: jan_data
    apikey: qwerty
    startdate: 2021-01-01
    enddate: 2021-01-04
    datatype: all   # could be: all, FLR, SEP, CME, IPS, MPC, GST, RBE, or report
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
api_lookedup:
    description: The API that the module sent an HTTP GET to.
    type: str
    returned: always
    sample: "https://api.nasa.gov/DONKI/notifications?startDate=2014-05-01&endDate=2014-05-08&type=all&api_key=DEMO_KEY"
status_code:
    description: The status code returned by api.nasa.gov/DONKI/notifications. Typically a 200. If returned as 0, no API lookup was performed. Useful for troubleshooting.
    type: int
    returned: always
    sample: 200
filemade:
    description: Full path to the file created.
    type: str
    returned: always
    sample: '/tmp/results.txt'
donkijson:
    description: The entire block of json as returned by the API lookup.
    type: json
    returned: always
    sample: {"iam": "json"}
'''

# you will typically always bring in this toolkit when creating an ansible module
# other helpful tools are avail aswell
from ansible.module_utils.basic import AnsibleModule

# python3 -m pip install requests
import requests

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=False, default="results"),
        dest=dict(type='str', required=False, default="/tmp"),
        apikey=dict(type='str', required=False, default="DEMO_KEY"),
        startdate=dict(type='str', required=False),
        enddate=dict(type='str', required=False),
        datatype=dict(type='str', required=False, default="all")
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        api_lookedup='',
        changed=False,
        status_code=0,
        filemade='',
        donkijson=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ## put together the API we want to lookup
    apikey = module.params['apikey']   # grab the value of apikey passed by the user or defaulting to DEMO_KEY
    datatype = module.params['datatype'] # grab the value of datatype passed by the user or default to "all"
    sd = module.params['startdate']
    ed = module.params['enddate']
    
    api = f"https://api.nasa.gov/DONKI/notifications?api_key={apikey}&type={datatype}&startDate={sd}&endDate={ed}"
    result['api_lookedup'] = api # this allows the user to run check mode and see what API would be sent an HTTP GET

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    nasaresponse = requests.get(api) # the api we created with our fstring we now send an HTTP GET
    
    # allow our consumer to know what response code was returned
    result['status_code'] = nasaresponse.status_code

    if nasaresponse.status_code != 200:
        module.fail_json(msg='Huston we have a problem. HTTP status code returned was not the expected 200.', **result)

    fl = module.params['dest'].rstrip("/")  # strip off any trailing slash that may or may not be there
    fn = module.params['name']
    savloc = f"{fl}/{fn}.txt"

    if nasaresponse.json():
        nj = nasaresponse.json()
    else:
        module.exit_json(**result)  # lookup was given 200, but there was no JSON attached to it :(
                                    # no file produced (no state change)

    result['donkijson'] = nj  # return ALL of the json within our results
                              # thought is a consumer might want data beyond "just" the messageBody key

    # open our file we want to write out our data to
    with open(savloc, "w") as nasaf:
        for entry in nj:
            nasaf.write(entry.get("messageBody"))
            nasaf.write("\n------\n")

    result['filemade'] = savloc  # this is the location of the file we just created
    # if we made it this far, a file was created on the host executing the module
    # change our state to True
    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()
