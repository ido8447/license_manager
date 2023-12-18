#!/usr/bin/env python3
import cgi
import os

print("Content-type: text/html\n")
print("<html><body><h1>Settings Updated</h1></body></html>")

form = cgi.FieldStorage()
upload_directory = "/var/www/html/license_manager/imgs"
# Debugging output to inspect form data
for field in form.keys():
    print(f"Field: {field}, Value: {form[field].value}")

if "logo" in form:
    logo = form["logo"]
    # Check if the logo field is not empty
    if logo.filename:
        # Normalize the filename to lowercase
        logo_filename = os.path.join(upload_directory, "logo.PNG")

        with open(logo_filename, "wb") as logo_file:
            logo_file.write(logo.file.read())


else:
    print("<html><body><h1>Invalid Request</h1></body></html>")
