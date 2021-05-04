#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nasa_genelab

short_description: API interaction with GeneLab Public API https://api.nasa.gov/. The host that executes this module will require the 'requests' library.

version_added: "1.0.0"

description: API interaction with GeneLab Public API https://api.nasa.gov/. No APIKEY appears to be required to access the service. This module produces a file with completed https URLs. The host that executes this module will require the 'requests' library.

options:
    name:
        description: Name of the output file. Defaults to gene-results.txt
        required: false
        type: str
    path:
        description: Absolute (full) path to output file. Defaults to /tmp/.
        required: false
        type: str
    glds_study_ids:
        description: Comma separated list with mixture of single GLDS accession numbers and ranges. ex. 87-95,137
        required: true
        type: str
    page_number:
        description: Page number in pagination to return. Defaults starts from 0 and works through all pages.
        required: false
        type: int
    results_per_page:
        description: Number of results returned per page in pagination. Defaults to 25. Use in conjunction with page_number to limit the number of results writtin into output file.
        required: false
        type: int

author:
    - RZFeeser (@RZFeeser)
'''

EXAMPLES = r'''
# Simpliest use case
- name: Return results from NASA Genelab API into gene-results.txt
  nasa_genelab:
    glds_study_ids: 87-95,137

- name: Return just 10 results from NASA Genelab API into onepage.txt
  nasa_genelab:
    glds_study_ids: 100
    name: onepage.txt
    results_per_page: 10

- name: Return all results from NASA Genelab API to /tmp/
  nasa_genelab:
    path: /tmp/
    glds_study_ids: 102,104
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
api_lookedup:
    description: The API that the module sent an HTTP GET to.
    type: str
    returned: always
    sample: "https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/87"
status_code:
    description: The status code returned by genelab-data.ndc.nasa.gov. Typically a 200. If returned as 0, no API lookup was performed. Useful for troubleshooting.
    type: int
    returned: always
    sample: 200
filemade:
    description: Full path to the file created.
    type: str
    returned: always
    sample: '/home/student/ans/gene-results.txt'
'''

import requests

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=False, default="gene-results.txt"),
        path=dict(type='str', required=False, default="/tmp/"),
        glds_study_ids=dict(type='str', required=True),
        page_number=dict(type='int', required=False, default=0),
        results_per_page=dict(type='int', required=False, default=25),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        api_lookedup='',
        status_code=0,
        filemade='',
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/{GLDS_STUDY_IDs}/?page={CURRENT_PAGE_NUMBER}&size={RESULTS_PER_PAGE}
    # what is the API we are going to lookup
    x = module.params.get('glds_study_ids')
    y = module.params.get('page_number')
    z = module.params.get('results_per_page')
    nasa_api = f"https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/{x}/?page={y}&size={z}"

    result["api_lookedup"] = nasa_api  # determined the API to lookup

    # return the file we are going to create
    fp = module.params.get('path')  # pull in path as described by user
    fp = fp.rstrip('/')             # strip a possible trailing slash
    filetocreate = f"{fp}/{module.params.get('name')}"

    result["filemade"] = filetocreate
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    apilookup = requests.get(nasa_api)

    # write the status code into our results
    result["status_code"] = apilookup.status_code

    # if a 200 was not returned, fail
    if apilookup.status_code != 200:
        module.fail_json(**result)

    # strip json off of HTTP 200+json and convert to pythonic data
    rjson = apilookup.json()

    # prepend url to lookup with nasa API authority
    nasaroot =  "https://genelab-data.ndc.nasa.gov"

    with open(filetocreate, "a") as myfile:
        # loop through the data starting by grabbing a study name
        for study in rjson.get("studies"):
            myfile.write(f"{study}"+ "\n")
            for studydata in rjson.get("studies").get(study).get("study_files"):
                myfile.write(f"{nasaroot}{studydata.get('remote_url')}" + "\n")

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    
    result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
