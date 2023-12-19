#!/usr/bin/env python3
import cgi
import shutil
from datetime import datetime

from setting import vendor_PATH
import os

print("Content-type: text/html\n")
print("<html><body><h1>vendor Added</h1></body></html>")

form = cgi.FieldStorage()

if "vendor_name" in form and "mac_address" in form and "backup_path" in form and "current_location" in form:
    vendor_name = form["vendor_name"].value
    mac_address = form["mac_address"].value
    backup_path = form["backup_path"].value
    current_location = form["current_location"].value
    file_location = form["file_location"].value
    vendor_file = vendor_PATH + '/' + vendor_name
    vendor = {
        "NAME": vendor_name,
        "MAC": mac_address,
        "LOCAL_BCKP": backup_path,
        "SOFTWARE_BCKP": vendor_PATH + '/backup' + '/' + vendor_name,
        "LOCATION": current_location,
        "PATH": file_location
    }
    try:
        if os.path.exists(vendor_file):
            now = datetime.utcnow().strftime('%d.%m.%Y:%H:%M:%S')
            dest = vendor_PATH + '/backup' + '/' + vendor_name + "." + now
            shutil.copy(vendor_file, dest)
            file = open(vendor_file, "w")
            for key, value in vendor.items():
                file.write(f"{key}: {value}\n")
            print(f"<p>vendor '{vendor_name}' overwritten successfully with backup on {dest}.</p>")
        else:
            file = open(vendor_file, "w")
            for key, value in vendor.items():
                file.write(f"{key}: {value}\n")
            print(f"<p>Vendor '{vendor_name}' created successfully.</p>")
            print('<meta http-equiv="refresh" content="5;url=/license_manager" />')

    except Exception as e:
        print(f"<p>{e}</p>")
else:
    print("<html><body><h1>Invalid Request</h1></body></html>")
