#!/usr/bin/env python3
import cgi
import shutil
from datetime import datetime

from setting import SITE_PATH
import os

print("Content-type: text/html\n")
print("<html><body><h1>Site Added</h1></body></html>")

form = cgi.FieldStorage()

if "site_name" in form and "mac_address" in form and "backup_path" in form and "current_location" in form:
    site_name = form["site_name"].value
    mac_address = form["mac_address"].value
    backup_path = form["backup_path"].value
    current_location = form["current_location"].value
    file_location = form["file_location"].value
    site_file = SITE_PATH + '/' + site_name
    site = {
        "NAME": site_name,
        "MAC": mac_address,
        "LOCAL_BCKP": backup_path,
        "SOFTWARE_BCKP": SITE_PATH + '/backup' + '/' + site_name,
        "LOCATION": current_location,
        "PATH": file_location
    }
    try:
        if os.path.exists(site_file):
            now = datetime.utcnow().strftime('%d.%m.%Y:%H:%M:%S')
            dest = SITE_PATH + '/backup' + '/' + site_name + "." + now
            shutil.copy(site_file, dest)
            file = open(site_file, "w")
            for key, value in site.items():
                file.write(f"{key}: {value}\n")
            print(f"<p>Site '{site_name}' overwritten successfully with backup on {dest}.</p>")
        else:
            file = open(site_file, "w")
            for key, value in site.items():
                file.write(f"{key}: {value}\n")
            print(f"<p>Site '{site_name}' created successfully.</p>")
            print('<meta http-equiv="refresh" content="5;url=/license_manager" />')

    except Exception as e:
        print(f"<p>{e}</p>")
else:
    print("<html><body><h1>Invalid Request</h1></body></html>")
