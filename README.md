# djattendance

[![Build Status](https://travis-ci.org/attendanceproject/djattendance.svg?branch=dev)](https://travis-ci.org/attendanceproject/djattendance) [![Coverage Status](https://coveralls.io/repos/attendanceproject/djattendance/badge.png?branch=dev)](https://coveralls.io/r/attendanceproject/djattendance?branch=dev)

## Summary
Djattendance is a rewrite of the original FTTA attendance server in Python/Django. It supports many internal functions of the FTTA, for both trainees and administrators, such as:
* Attendance
* Service Scheduling
* Life-studies
* Class Syllabi
* etc.

## Architecture
The original attendance server was based on a traditional LAMPstack. The new version is written in Python on top of the Django web framework (djangoproject.com) using Postgres and Nginx.

### Backend
Python/Django
Postgres
Gunicorn
Nginx

### Frontend
HTML5 Boilerplate
Bootstrap

### Misc. Libraries
Celery (using Redis)
Memcached (deployment only)


## Running djattendance
A more detailed guide to running djattendance on your local machine can be found in the wiki (coming soon).

0. have Python and Postgres installed
1. `git clone` the djattendance repo
2. `pip install -r requirements.txt` from the `/requirements` (recommended that you use `virtualenv`)
3. using django: `manage.py syncdb` and `manage.py runserver` (be sure to use the local settings)


## Running djattendance with vagrant
NOTE: Folder that contains the vagrant file is synced as well, so all work is still done on the host.

(NOTE FOR WINDOWS USERS: You will need to issue this command in git, "git config --global core.autocrlf input". See this for a list of issues related to CRLF and LF, http://blog.xjtian.com/post/54399466362/vagrant-tips-for-windows-users.)

0. have VirtualBox and Vagrant installed
1. `git clone` the djattendance repo
2. Run 'vagrant up' within the project directory where the VagrantFile is located
3. Run 'vagrant ssh' to access the VM
4. 'cd ap'
5. 'python manage.py syncdb --settings=ap.settings.dev'
6. 'python manage.py runserver 0.0.0.0:8000 --settings=ap.settings.dev'
7. From your host (not the guest VM) you can access the site from localhost:8111. 
