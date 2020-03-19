# ansible-custom-modules-nasa-api
By day, I'm a trainer and consultant for private industry. Many of my students are interested in how to architect custom modules for Ansible, so this repo is dedicated to some of the custom modules I've written.

Like most tech nerds, it's always been a dream to work for NASA, so in lieu of actually working for NASA, I did the next best thing and began writing custom Ansible modules around the NASA APIs available on https://api.nasa.gov

So far (2) custom modules have been created:

  - nasa_apod
  - nasa_earth

Most of these custom modules require a *very* popular Python library called **requests** in order to function. See the **Getting Started** section for more help with installing **requests**.

### Goals

  - Write and maintain Ansible modules for all of the NASA APIs
  - Help other learn about automation and APIs
  - Get a shout out on NASA's social media feeds
  - Hired to consult or teach cool NASA cats about automation with Ansible and Python 
  - Work on a project with renowned driller Bruce Willis, after agreeing to consult on a dangerous space mission to save earth


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

    `ansible-playbook playbook-example-nasa_apod.yml`

#### Using Ansible to access the Astronomical Picture of the Day (APOD) API with nasa_apod

Too sleepy.

#### Using Ansible to access NASA Earth API with nasa_earth

zzzzzz.
