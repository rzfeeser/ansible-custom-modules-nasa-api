# ansible-custom-modules-nasa-api
"Helpful" custom modules I've written to help my students understand programming Ansible with Python

It's always been my dream to work for NASA, so in lieu of actually working for NASA, I did the next best thing and began writing custom Ansible modules around the NASA APIs available on https://api.nasa.gov

So far (2) custom modules have been created:

    - nasa_apod
    - nasa_earth
    
### Getting Started

0. Access https://api.nasa.gov and sign up for a free API key (they are indeed free).

0. Install Python3.x on a Linux platform. On Debian / Ubuntu, you would type something like:

    `sudo apt install python3-pip`

0. After you install Python, you can install the latest version of Ansible with their package installer, `pip`.

    `python3 -m pip install ansible`

0. Most of these modules require the `requests` library, which you may also install with `pip`.

    `python3 -m pip install requests`

0. Clone this repo to a place where you can work.

    `git clone https://github.com/rzfeeser/ansible-custom-modules-nasa-api/ ~/ans/`

0. Check out the playbooks in the `~/ans/` directory. All of these should work. To try one out, simply type:

    `ansible-playbook name_of_playbook.yml`

### Using Ansible to access the Astronomical Picture of the Day (APOD) API with nasa_apod


### Using Ansible to access NASA Earth API with nasa_earth
