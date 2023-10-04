import os
import subprocess
from datetime import datetime
import shutil

SITE_PATH = "/var/www/html/license_manager/SITES"
LICENSES_PATH = '/var/www/html/license_manager/LICENSES'
LMSTAT = '/tools/linux/flexlm/latest/lmstat'


# return all sites
def sites():
    dirs = os.listdir(SITE_PATH)
    return [item for item in dirs if os.path.isfile(os.path.join(SITE_PATH, item))]


# return site data as a dictionary
def site_data(site):
    site_path = os.path.join(SITE_PATH, site)
    if not os.path.exists(site_path):
        return False
    else:
        with open(site_path, 'r') as file:
            lines = file.readlines()
        return lines


# find the current license of specific site
# return the path of him
def find_last_license(site):
    global location
    lines = site_data(site)
    data = {}
    for line in lines:
        key, value = line.strip().split(": ")
        if key == 'LOCATION':
            location = value
        data[key] = value
    return subprocess.check_output([LMSTAT, '-c', location]).decode('utf-8').split(':')[3].strip()


# return license data by a path
def get_license_data(_license):
    with open(_license, 'r') as file:
        data = file.readlines()
    output = []
    for line in data:
        line = line.replace('\\n', '\n')
        line = line.replace('\\t', '\t')
        output.append(line)
    return ' '.join(output)


# backup and call to update
# last_lic => path to the current license #use find_last_license(site) function
# new_lic => new license data #use form["license_file"].file.read().decode("utf-8")
def make_update(last_lic, new_lic, site):
    # find backup path
    global bkp_path
    _site_data = site_data(site)
    for line in _site_data:
        key, value = line.strip().split(": ")
        if key == 'BCKP':
            bkp_path = value

    # create backup
    now = datetime.utcnow().strftime('%d.%m.%Y:%H:%M:%S')
    shutil.copy(last_lic, bkp_path + '/license_lic-srv3.dat.' + now)

    # read last license data
    with open(last_lic, 'r') as file:
        last_lic_data = file.readlines()

    # call to update function
    update(last_lic_data, new_lic)


# make the update functionality
# use current and new as a licenses data
# make_update() use this function by himself
def update(current, new):
    pass


# return the site name from license data
def get_site_from_license(license_data):
    license_data = license_data.split(':')
    for line in license_data:
        for site in sites():
            if site.lower() in line.lower():
                return site
            else:
                continue


# show only features
def show_license_feature(license_data):
    grep_command = ['egrep', '-i', 'FEATURE|PACKAGE|INCREMENT', license_data]
    output = subprocess.check_output(grep_command).decode('utf-8')
    return output


# input: show_license_feature(license_data) => for old and new
# output: return only different
def different_changes(current_features, new_features):
    current_same_features = []
    new_same_features = []
    all_same_feature = []

    current = current_features.split("\n")
    new = new_features.split("\n")
    for nfeature in range(1, len(new) - 1):
        for cfeature in range(1, len(current) - 1):

            if new[cfeature] == '':
                break
            else:
                pass

            if '#' in new[cfeature]:
                continue

            if len(current[nfeature]) > 1 and len(new[cfeature]) > 1 or current[nfeature] == '':
                nsplit = new[nfeature].split(' ')
                csplit = current[cfeature].split(' ')
                if csplit[1] == nsplit[1]:
                    new_same_features.append(new[nfeature])
                    current_same_features.append((current[cfeature])+'\r')
                    break
            else:
                break

    all_same_feature.append(new_same_features)
    all_same_feature.append(current_same_features)
    return all_same_feature





