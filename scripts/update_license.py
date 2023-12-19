#!/usr/bin/env python3
import cgi
import shutil
from datetime import datetime

from setting import find_last_license, get_vendor_from_license, get_license_data, show_license_feature, LICENSES_PATH, \
    different_changes, vendor_data, show_features_lmstat

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




if "license_file" in form:
    # Read the attachment license
    new_license_file = form["license_file"].file.read().decode("utf-8")
    now = datetime.utcnow().strftime('%d.%m.%Y:%H:%M:%S')

    # Return vendor name, vendor path and vendor license
    current_vendor = get_vendor_from_license(new_license_file)
    current_vendor_path = find_last_license(current_vendor)
    current_vendor_license = get_license_data(current_vendor_path)


    # Create license backup
    new_license_file_path = LICENSES_PATH + '/' + current_vendor + '.' + now
    try:
        with open(new_license_file_path, 'w') as file:
            file.write(new_license_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Create a list of the features
    #######TESTING
   # diff = different_changes(show_license_feature(current_vendor_path), show_license_feature(new_license_file_path))
    diff = different_changes(show_license_feature("/var/www/html/license_manager/license_update_test/license.dat"), show_license_feature(new_license_file_path))
    current_same_features = ' '.join(diff[1])
    new_same_features = ' '.join(diff[0])

    if len(new_same_features) == 0:
        new_same_features = show_license_feature(new_license_file_path)
        current_same_features = 'The new features does not exist ======================>'

    #show_features_lmstat()
    #current_features_lm = show_features_lmstat(current_vendor)
    #new_features_lm  = show_features_lmstat()


    print(f'<p>LICENSE: {current_vendor}</p>')
    print("<div style='display: inline-block; margin-right: 10px;'>")
    print('<p>Current LICENSE</p>')
   # print(f"<textarea style='width: 730px; height: 850px; font-size: 16px;'>{show_features_lmstat(current_vendor_path)}</textarea>")
    print(f"<textarea style='width: 651px; height: 850px; font-size: 16px;'>{current_same_features}</textarea>")
    #print(f"<textarea style='width: 651px; height: 850px; font-size: 16px;'>{show_license_feature(current_vendor_path)}</textarea>")

    print("</div>")

    print("<div style='display: inline-block;'>")
    print('<p>New LICENSE</p>')
    print(f"<textarea style='width: 651px; height: 850px; font-size: 16px;'>{new_same_features}</textarea>")
    #print(f"<textarea style='width: 730px; height: 850px; font-size: 16px;'>{show_features_lmstat(new_license_file_path)}</textarea>")
    #print(f"<textarea style='width: 651px; height: 850px; font-size: 16px;'>{show_license_feature(new_license_file_path)}</textarea>")

    print("</div>")



else:
    print("<html><body><h1>Invalid Request</h1></body></html>")
html_code = '</br><button style="margin-left: 4px;margin-bottom: 0px;padding-top: 10px;margin-top: 0px;width: 400px;height: 50px;" onclick="window.location.href = \'/license_manager/adding.html\';">Back</button>'
print(html_code)
html_code=f"""
<form action="/license_manager/scripts/install_license.py" method="post">
    <input type="hidden" name="new_license_file_path" value="{new_license_file_path}">
    <input type="hidden" name="current_vendor" value="{current_vendor}">
    <button type="submit" name="install_button">Install</button>
</form>
"""
# html_code = '<button style="margin-left: 5px;margin-bottom: 0px;padding-top: 10px;margin-top: 0px;width: 400px;height: 50px;" onclick="window.location.href = \'/license_manager/apply_licenses.html\';">Install</button>'
print(html_code)

print('</body></html>')
