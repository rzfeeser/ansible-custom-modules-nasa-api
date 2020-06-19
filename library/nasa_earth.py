#!/usr/bin/python3
# Copyright: (c) 2020, Zach Feeser <rzfeeser@users.noreply.github.com>
# https://alta3.com || https://rzfeeser.com 
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: nasaimagery

short_description: This module pulls images from google earth via the NASA earth api

version_added: "2.9"

description:
    - "This module uses the NASA imagery service to pull a URL that provides a thumbnail image of a lat and lon. The resulting image is saved as a png on the target hosts. This module REQUIRES the requests module be installed on all hosts that it executes on."

options:
    lon:
        description:
            - This is the longitude to send to the module
        required: true
    lat:
        description:
            - This is the latitude to send to the module
        required: true
    apikey:
        description:
            - This is the NASA API key to send to the module. Default to DEMO_KEY.
        required: false
    dest:
        description:
            - This is the location and name to save the PNG to. Defaults to /tmp/example.png
        required: false

author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  nasaimagery:
    apikey: DEMO_KEY
    lon:
    lat:
    dest: /tmp/
'''

RETURN = '''
url:
    description: URL to NASA imagery api that was an HTTP GET was sent to
    type: str
    returned: always
urlearth:
    description: URL to Google Earth thumbnail that was used to download PNG
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        apikey=dict(type='str', required=False, default="DEMO_KEY"),
        lon=dict(type='float', required=True),
        lat=dict(type='float', required=True),
        dest=dict(type='str', required=False, default="/tmp/example.png")
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        url='',
        urlearth=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # https://api.nasa.gov/planetary/earth/imagery/?lon=77.593675&lat=12.972172&date=2016-03-09&api_key=DEMO_KEY

    nasaurl = f"https://api.nasa.gov/planetary/earth/imagery/?lon={ module.params['lon'] }&lat={ module.params['lat'] }&date=2017-01-01&api_key={ module.params['apikey'] }"

    result['url'] = nasaurl

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)


    # begin NASA lookup
    nasaresp = requests.get(nasaurl)
    # if a non-200 response, then FAIL
    if nasaresp.status_code != 200:
        module.fail_json(msg='A non-200 response was returned from NASA', **result)        
    # strip off json response and reassign to nasaresp
    nasaresp = nasaresp.json()

    # begin Google Earth lookup (url taken from NASA lookup)
    googleearth = requests.get( nasaresp["url"] )
    # if a non-200 response, then FAIL
    if googleearth.status_code != 200:
        module.fail_json(msg='A non-200 response was returned from Google Earth', **result)
    # save the picture to the dest provided
    with open( module.params['dest'], 'wb') as f:
        f.write(googleearth.content)

    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
