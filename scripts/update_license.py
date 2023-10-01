#!/usr/bin/env python3
import cgi

print("Content-type: text/html\n")
print("<html><body><h1>License Added</h1></body></html>")

form = cgi.FieldStorage()


if "license_file" in form:
    license_file = form["license_file"].file.read().decode("utf-8")
    print(f"<textarea style='width:651px; height:982px;'>{license_file}<textarea>")



else:
    print("<html><body><h1>Invalid Request</h1></body></html>")
