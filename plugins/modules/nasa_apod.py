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
module: nasa_apod 

short_description: Interact with NASA APOD. More information available at https://api.nasa.gov

version_added: "2.9"

description:
    - "This module uses the NASA APOD service to pull a URL that provides thumbnail imagine, and meta data about that image. The resulting image is saved as a png on the target host(s). This module REQUIRES the requests module be installed on all hosts that it executes on."

options:
    date:
        description:
            - The date of the APOD image to retrieve. Default to todays date. Formatted YYYY-MM-DD
        required: false
    hd:
        description:
            - This controls if the user wants to download the HD image or standard image. Default true.
        required: true
    apikey:
        description:
            - This is the NASA API key to send to the module. Default to DEMO_KEY
        required: false
    dest:
        description:
            - This is the location and name to save the APOD image (PNG format). Defaults to /tmp/example.png directory.
        required: false

author:
    - Russell Zachary Feeser (@rzfeeser)
'''

EXAMPLES = '''
# Obtain TODAY's APOD
- name: Lookup the NASA APOD API entry for TODAY
  nasa_apod:
    apikey: DEMO_KEY   # this defaults to DEMO_KEY, but you should always supply your own key
                       # API keys are available at https://api.nasa.gov/

# Obtain APOD from January 01, 2020 in low res.
- name: Lookup the NASA APOD API for 2019-01-01 in std def
  nasa_apod:
    apikey: DEMO_KEY
    date: 2019-01-01
    hd: false
    dest: /home/student/example.png
'''

RETURN = '''
apodjson:
    description: The JSON returned by performing a lookup to https://api.nasa.gov/planetary/apod
    type: dict
    returned: always
apodurl:
    description: The link to the standard APOD image
    type: str
    returned: always
apodhdurl:
    description: The link to the HD APOD image
    type: str
    returned: always
'''

import requests

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        date=dict(type='str', required=False),
        hd=dict(type='bool', required=False, default=True),
        apikey=dict(type='str', required=False, default="DEMO_KEY"),
        dest=dict(type='str', required=False, default="/tmp/example.png")
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        apodjson='',
        apodurl='',
        apodhdurl=''
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

    # make the call to NASA APOD API service
    if module.params.get('date'):
        nasaresp = requests.get(f"https://api.nasa.gov/planetary/apod?hd={module.params['hd']}&api_key={module.params['apikey']}&date={module.params['date']}")
    else:
        nasaresp = requests.get(f"https://api.nasa.gov/planetary/apod?hd={module.params['hd']}&api_key={module.params['apikey']}")

    # if nasaresp returns a non-200, exit not
    if nasaresp.status_code != 200:
        module.fail_json(msg=f'A {nasaresp.status_code} response was returned from NASA. Huston, we have a problem!', **result)

    # pull JSON out of nasaresp object and rewrite as a dictionary
    nasaresp = nasaresp.json()

    # assign our data to the JSON response to send back to Ansible
    result['apodjson'] = nasaresp

    result['apodurl'] = nasaresp.get('url')

    result['apodhdurl'] = nasaresp.get('hdurl')

    # perform an HD download or a standard res download depending on the value the user passed in to our module
    if module.params['hd']:
        apodimage = requests.get(nasaresp['hdurl'])
    else:
        apodimage = requests.get(nasaresp['url'])

    # if nasaresp returns a non-200, exit not
    if apodimage.status_code != 200:
        module.fail_json(msg=f'A {nasaresp.status_code} response was returned as we tried to download APOD image from NASA. Huston, we have a problem!', **result)

    # download the image to the location provided by the user
    with open(module.params['dest'], 'wb') as f:
        f.write(apodimage.content)

    # a photo being written out is a state change
    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
