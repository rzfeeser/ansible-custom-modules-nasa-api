#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nasa_tle.py

short_description: abstracting interacitons with nasa tle API https://api.nasa.gov/ and http://tle.ivanstanojevic.me

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: for a better understanding of how the nasa tle api works, see http://tle.ivanstanojevic.me
 and to use the api see http://tle.ivanstanojevic.me/api/tle. Home of the api is http://api.nasa.gov. This module allows the user to return all tle data, serach by satellite number, OR search by satellite name.

options:
    sat_name:
        description: This is the name of the satellite you wish to look up. Mutually exclusive with sat_name. Must choose to search by sat_name or sat_number.
        required: false
        type: str
    sat_num:
        description: This is the number of the satellite you wish to look up. Mutually exclusive with sat_name. Must choose to search by sat_name or sat_number.
        required: false
        type: int
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - rzfeeser.nasa.my_collection.my_doc_fragment_name

author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = r'''
# Return all satellite data
- name: return all TLE data
  rzfeeser.nasa.nasa_tle:
  register: results

# Search by satellite name
- name: return a search by name
  rzfeeser.nasa.nasa_tle:
       name: IHOPSAT-TD
  register: results

# Search by satellite number
- name: return a search by number
  rzfeeser.nasa.nasa_tle:
       name: 44859
  register: results
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
json:
    description: The json returned by the API.
    type: dict
    returned: always
url:
    description: The url that was used to look up the API
    type: str
    returned: always
    sample: 'https://tle.ivanstanojevic.me/api/tle/?search=ihopsat-td'
status:
    description: The HTTP status code returned by the API
    type: int
    returned: always
    sample: 200
'''

import requests

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        sat_name=dict(type='str', required=False),
        sat_num=dict(type='int', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,  # this controls GREEN / YELLOW results - FALSE means "green", TRUE means "yellow"
        json=dict(),
        url='',
        status=int()
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ('sat_name', 'sat_num'),],
        )

    api = "https://tle.ivanstanojevic.me/api/tle/"

    if module.params['sat_name']:   # if the user passed in sat_name
        api = f"{api}?search={module.params['sat_name']}"
    elif module.params['sat_num']:  # if the user passed in sat_num
        api = f"{api}{module.params['sat_num']}"

    result['url'] = api  # we have finished creating our api we want to lookup

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    #s = requests.Session()
    #r = s.get(api)

    # the TLE service will not respond unless you make it think you are a browser
    r = requests.get(api, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}) # send an HTTP get to our API

    # set the results with the returned status code
    result['status'] = r.status_code

    if r.status_code != 200:
        module.fail_json(msg=f'Huston, we have a problem. The status code returned was a non-200. Returned code was {r.status_code}. The HTTP interaction has the following history\n{r.history}', **result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    result['json'] = r.json() # strip JSON off the 200 that was returned
    

    # our code does NOT produce a state change
    # therefore to perserve idempotence we remain GREEN
    # however, if your code DID create a change-- you want to set
    # result['changed'] = True
    # in order to return YELLOw (changed) to Ansible

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
