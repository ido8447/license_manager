#!/usr/bin/env python3
import cgi

print("Content-type: text/html\n")
print("<html><body><h1>Site Added</h1></body></html>")

form = cgi.FieldStorage()

if "site_name" in form and "mac_address" in form and "backup_path" in form and "current_location" in form:
    site_name = form["site_name"].value
    mac_address = form["mac_address"].value
    backup_path = form["backup_path"].value
    current_location = form["current_location"].value
    password = form["password"].value

    # Save the site information and implement your logic
    # This is a placeholder for your site information processing logic

else:
    print("<html><body><h1>Invalid Request</h1></body></html>")
