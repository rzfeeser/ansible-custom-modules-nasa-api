# ansible-custom-modules-nasa-api

Author: Russell Zachary Feeser  
GitHub: @RZFeeser  
 Email: rzfeeser@users.noreply.github.com  
     
### Overview

Many of my students are interested in how to architect custom modules for Ansible, so this repo is dedicated to some of the custom modules I've written.

Like most tech nerds, it's always been a dream to work for NASA, so in lieu of actually working for NASA, I did the next best thing and began writing custom Ansible modules around the NASA APIs available on https://api.nasa.gov

So far (9) custom Ansible modules have been created:

  - nasa_apod
  - nasa_donki
  - nasa_earth
  - nasa_eonet_event
  - nasa_genelab
  - nasa_mars_rover_photos
  - nasa_mars_weather
  - nasa_neow
  - nasa_tle

Most of these custom modules require a *very* popular Python library called **requests** installed on the hosts they execute on in order to function. Additionally, the nasa_neow module requires the **pyyaml** library to perform the JSON to YAML conversion. See the **Getting Started** section for more help with installing these libraries.

### Ansible Collection - rzfeeser.nasa

This repository has recently been converted to a collection, `rzfeeser.nasa`. To install, use:

    ansible-galaxy collection install git@github.com:rzfeeser/ansible-custom-modules-nasa-api

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

0. You can validate the Python3.x install with one of the two following commands.

    `python3 --version` or `python --version`

0. It really doesn't matter which command displays a version of Python3.x, however, if the command `python --version` says something about Python2.x, you 100% do not want to use command. Python2.x is historic (dead). Don't try to get up and running with it.

0. After you install and validate you have installed Python3.x, you can install the latest version of Ansible with their package installer, `pip`.

    `python3 -m pip install ansible`

0. Most of these modules require the `requests` library, installed on the target hosts. If you run in 'localhost' mode, you need to install this package on the controller. You can install this with the pip tool.

    `python3 -m pip install requests`

0. Install the collection, `rzfeeser.nasa`

    `ansible-galaxy collection install git+https://github.com/rzfeeser/ansible-custom-modules-nasa-api`

0. Within this repo, pick one of the playbooks within `playbooks/` and try running it with:

    `ansible-playbook playbook-example-nasa_apod.yml`

0. *NOTE: If the Ansible playbook `playbook-example-nasa_neow.yml`, fails, it is likely because you do not have `pyyaml` installed. This is required to conver the NEOW data to a YAML format. To install this library, see notes on this module within this README file.*

#### Using Ansible to access NASA APIs

A key is common to all modules, which is `apikey`. Be sure to define it, or it will default to `DEMO_KEY`, although `DEMO_KEY` is legal, it has a very limited number of uses, at which time, your playbook will stop working. Getting an API key is easy. Just visit https://api.nasa.gov  

When you sign up for a key, be sure to comment that the reason you're signing up for a key is to interact with the Ansible code found in this repository (rzfeeser/ansible-custom-modules-nasa-api/). Thanks! 

#### Using Ansible to access the Astronomical Picture of the Day (APOD) API with nasa_apod

Start by reviewing the example playbook within this repostiory.

After the `nasa_apod` task runs, the Astronomical Picture of the Day will be saved on the target hosts as `apod.png` by default. The user is able to define the date of the photo they would like via the `date` paramater using YYYY-MM-DD format. By default, the current date will be returned. The `hd` parameter controls the return of HD image or standard image data, the default is HD. If a different name or path is desired, the `dest` parameter may be defined with a full path and name.
*Future Feature Request: module parameter dest <- default to current directory, allow relative path, full path, and provide a default name apod.png if no name is provided*

#### Using Ansible to access NASA Earth API with nasa_earth

Start by reviewing the example playbook within this repostiory.

#### Using Ansible to access NASA Near Earth Object Webservice (NEOW) API with nasa_neow

Start by reviewing the example playbook within this repository.  

After the `nasa_neow` task runs, the JSON data returned by the NEOW API service will be convered to YAML and saved in the format `neow-YYYY-MM-DDtoYYYY-MM-DD.yml`. By default this file will appear in the local folder. However, the save path can be controlled by the user. This module will only show **CHANGED** if the YAML output file is created.
*Future Feature Request: module parameter force:bool <- allow a user to force the creation of the YAML file ever time (overwrite it if it exists). Should default to False/no*

#### Using Ansible to access NASA Earth Observatory Natural Event Tracker (EONET) Event API with nasa_eonet_event

Start by reviewing the example playbook within this repository. *NOTE: There is no requirement to use an API KEY with this service*

After the `nasa_eonet_event` tasks runs, the JSON data returned by the EONET Event API service will be converted to YAML and saved in the format `eonet-YYYY-MM-DDtoYYYY-MM-DD.yml`. By default this file will appear in the local folder. However, the save path can be controlled by the user. This module will only show **CHANGED** if the YAML output file is created.

#### Using Ansible to access NASA GeneLab API with nasa_genelab

Start by reviewing the example playbook within this repository. *NOTE: There is not requirement to use an API KEY with this service*

#### Using Ansible to access NASA Mars Weather API with nasa_mars_weather

Start by reviewing the example playbook within this repository.

#### Using Ansible to access NASA Mars Rover Photos API with nasa_mars_rover_photos

Start by reviewing the example playbook within this repository.

#### Using Ansible to access NASA TLE API with nasa_tle

Start by reviewing the example playbook within this repository.

#### Using Ansible to access NASA DONKI API with nasa_donki

Start by reviewing the example playbook within this repository.
