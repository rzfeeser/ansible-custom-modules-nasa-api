#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nasa_mars_rover_photos

short_description: Looking up rover photo data from nasa. Pass opportunity, spirit, or curiosity 

version_added: "1.0.0"

description: This is my longer description explaining my test info module.

options:
    apikey:
        description: This is the message to send to the test module.
        required: true
        type: str
    rover_name:
        description: This is opportunity, spirit, or curiosity
        required: true
        type: str
    sol:
        description: This is a int
        required: false
        type: int || str

author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  nasa_mars_rover_photos:
    apikey: DEMO_KEY
    rover_name: opportunity
    sol: 1000
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
rover_name:
    description: The rover name that was looked up
    type: str
    returned: always
    sample: 'spirit'
nasa_url:
    description: This is the API that was called. Useful for debugging or validating
    type: str
    returned: always
    sample: 'https://api.nasa.gov/mars-photos/api/v1/rovers/Opportunity/photos?sol=100&api_key=DEMO_KEY'
json:
    description: The is the json attached to the 200 response to the API we call
    type: dict
    sample: {"photos":[{"id":119096,"sol":1,"camera": ... ... ...
'''

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        rover_name=dict(type='str', required=True),
        sol=dict(type='str', required=False, default="1000"),
        apikey=dict(type='str', required=False, default="DEMO_KEY"),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        nasa_url='',
        rover_name='',
        json='',
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # we can now set our rover name in our resutls we would return
    result['rover_name'] = module.params['rover_name']

    # put together URL we are about to lookup
    nasaurl2lookup = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ module.params['rover_name'] }/photos?sol={ module.params['sol'] }&api_key={ module.params['apikey'] }"

    result['nasa_url'] = nasaurl2lookup

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    r = requests.get(nasaurl2lookup)
    
    result['json'] = r.json()
    
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
