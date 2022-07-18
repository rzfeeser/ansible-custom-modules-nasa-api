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
module: nasa_neow

short_description: Interact with NASA NEOW. More information available at https://api.nasa.gov.

version_added: "2.9"

description:
    - "This module gets data from NASA NEOW service and converts this data to YAML format, saving it on the local system. The outputted file is saved in the format neow-YYYY-MM-DDtoYYY-MM-DD.yml. By default the file is saved to the local folder, however, the user can control the path as to where the output file is placed. This module will only show CHANGED if the module creates a YAML output file. If the module FAILS it will display the HTTP code associated with the failed response."

options:
    startdate:
        description:
            - YYYY-MM-DD string format of the start date
        required: true
    enddate:
        description:
            - YYYY-MM-DD string format of the end date
        required: true
    apikey:
        description:
            - Users API key issued from NASA, defaults to DEMO_KEY
        required: false
    savepath:
        description:
           - Path a save the converted YAML file to, defaults to current directory



author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = '''
# Grab NEOW data from NASA and convert to YAML suppling an API key (DEMO_KEY) and saving to the current directory
- name: Is the Earth at risk of a NEO event
  nasa_neow:
    startdate: 2020-06-15
    enddate: 2020-06-17
    apikey: DEMO_KEY 

# Grab NEOW data from NASA and convert to YAML using DEMO_KEY and saving to current directory
- name: Is the Earth at risk of a NEO event (use DEMO_KEY)
  nasa_neow:
    startdate: 2020-06-15
    enddate: 2020-06-17

# Grab NEOW data from NASA and convert to YAML using an API key (DEMO_KEY) and saving to /home/student/
-name: Get astroid data
   startdate: 2020-01-01
   enddate: 2020-01-02
   apikey: DEMO_KEY
   savepath: /home/student/

'''

RETURN = '''
original_nasa_json:
    description: This is the JSON as returned by NASA by their NEOW API
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
    description: The start date supplied to the NASA NEOW API
    type: str
    returned: always
end_date:
    description: The end date supplied to the NASA NEOW API
    tye: str
    returned: always
'''
NASANEOW = "https://api.nasa.gov/neo/rest/v1/feed?"

import os

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
        startdate=dict(type='str', required=True),
        enddate=dict(type='str', required=True),
        apikey=dict(type='str', required=False, default="DEMO_KEY"),
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
    ## https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY
    ## https://api.nasa.gov/neo/rest/v1/feed?start_date=START_DATE&end_date=END_DATE&api_key=API_KEY
    sd = module.params['startdate']
    ed = module.params['enddate']
    ak = module.params['apikey']
    sp = module.params['savepath']

    lookMeUp = f"{NASANEOW}start_date={sd}&end_date={ed}&api_key={ak}"

    ## Send an HTTP GET - API call to nasa based on compelted URI+queryparams
    resp = requests.get(lookMeUp)

    ## if the response was NOT a 200, ansible module should FAIL
    if resp.status_code != 200:
        module.fail_json(msg=f"The NASA API lookup was not successful. STATUS CODE - {resp.status_code}", **result)

    ## strip JSON off HTTP 200 response
    nasaJson = resp.json()

    ## convvert JSON to YAML
    nasaYaml = yaml.dump(nasaJson)

    ## check to see if file already exists
    ## if file does not exist then create it
    if not os.path.isfile(f"{sp}neow-{sd}to{ed}.yml"):
        ## save YAML as file locally
        with open(f"{sp}neow-{sd}to{ed}.yml", "w") as myfile:
            myfile.write(nasaYaml)
        result['changed'] = True

    # set results that will be returned via JSON to the ansible module
    result['original_nasa_json'] = nasaJson # the JSON gathered from NASA
    result['status_code'] = resp.status_code # the HTTP response code
    result['file_loc'] = sp # the path to the save filed
    result['yaml_output_file'] = f"neow-{sd}to{ed}.yml" # name of the YAML output file created
    result['start_date'] = sd # the start search date
    result['end_date'] = ed # the end search date

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
