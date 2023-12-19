#!/usr/bin/env python3
import cgi
import os
import shutil
import subprocess
from datetime import datetime

from setting import find_last_license, vendor_data

print("Content-type: text/html\n")

print("""<!DOCTYPE html>
<html>
<head>
    <title>Update License</title>
    <link rel="icon" href="/license_manager/imgs/add.ico" type="image/x-icon">
    <link rel="shortcut icon" href="/license_manager/imgs/add.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="/license_manager/style.css">
    <div class='header'>
    <h1>Update License</h1>
    <a href='https://license/license_manager/Main_Page.html'>
               <img src="imgs/logo.PNG" alt="SysAid Technologies Ltd." title="license_manager">
    </a>
</div>
</head>
<body>

<div class='text-body'>
""")

form = cgi.FieldStorage()

# backup and call to update
# last_lic => path to the current license #use find_last_license(vendor) function
# new_lic => new license data #use form["license_file"].file.read().decode("utf-8")


if "new_license_file_path" in form and "current_vendor" in form:
    # Extract parameters
    new_license_file = form.getvalue('new_license_file_path')
    current_vendor = form.getvalue('current_vendor')


    # Your make_update function
    def make_update(new_lic_path, vendor):

        # find backup path
        global bkp_path
        _vendor_data = vendor_data(vendor)
        for line in _vendor_data:
            key, value = line.strip().split(": ")
            if key == 'LOCAL_BCKP':
                bkp_path = value

        last_license_path = find_last_license(vendor)

        date_now = datetime.utcnow().strftime('%d.%m.%Y.%H.%M.%S')
        # Create BCKP
        filename = os.path.basename(last_license_path)
        new_license_backup_path = bkp_path + '/' + filename + '.' + date_now
        copy_backup = ["sudo", "-u", "root", "rsync", "-avl", last_license_path, new_license_backup_path]
        try:
            pass
        # subprocess.run(copy_backup, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            print("command failed with error:", e)
            pass

        if vendor == 'synopsys':
            # call to update function
            update(vendor, new_lic_path)
        else:
            switch(vendor, new_lic_path)


    # make the update functionality
    # use current and new as a licenses data
    # make_update() use this function by himself
    def update(vendor, new_lic_path):
        last_lic = find_last_license(vendor)

        # TESTING
        last_lic = "/var/www/html/license_manager/license_update_test/license.dat"

        with open(new_lic_path, 'r') as n:
            new_data_lines = n.readlines()

        use_server_index = next((i for i, line in enumerate(new_data_lines) if line.startswith("USE_SERVER")), None)

        if use_server_index is not None:
            start_index = use_server_index + 1
            end_index = len(new_data_lines)
        else:
            start_index = 0
            end_index = len(new_data_lines)

        # Extract desired lines from new_data while preserving the original formatting
        # required_data = "".join(new_data_lines[start_index:end_index + 1])
        required_data = []
        for line_number in range(start_index, end_index):
            required_data.append(new_data_lines[line_number])

        # Append data to another file
        try:
            # Use subprocess to run a bash command with sudo
            append = ['sudo', 'bash', '-c',
                      f'echo "\n############################################{datetime.now()}" >> {last_lic}']
            subprocess.run(append, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for line in required_data:
                line = line.replace('\n','')
                append = ['sudo', 'bash', '-c', f"echo '{line}' >> {last_lic}"]
                subprocess.run(append, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess execution: {e}")
        except Exception as e:
            print(f"Other error: {e}")

        print("9")


    def switch(vendor, new_lic_path):
        pass


    # Call make_update function
    make_update(new_license_file, current_vendor)
    print("10")

    # Print success message or redirect the user
    print("<html><body>")
    print("<h2>Update Successful!</h2>")
    print("</body></html>")
else:
    # Print error message or redirect the user
    print("<html><body>")
    print("<h2>Error: Form data missing or incorrect submission</h2>")
    print("</body></html>")
