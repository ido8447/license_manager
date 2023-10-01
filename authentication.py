#!/usr/local/install/python-3.7.2/bin/python3
import cgi
import cgitb
import subprocess
from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SUBTREE, ServerPool

import ldap.configure
from ldap import configure

# Enable detailed error reporting for CGI scripts
cgitb.enable()

print("Content-type: text/html")
print()

print("<html><head><title>Authentication</title>")
print("""    <link rel="icon" href="/license_manager/imgs/add.ico" type="image/x-icon">
    <link rel="shortcut icon" href="/license_manager/imgs/add.ico" type="image/x-icon">""")
print('<link rel="stylesheet" type="text/css" href="/useradd/style.css">')
print("<div class='header'>")
print("<h1>Authentication</h1>")
print("<a href='http://license/license_manager/Main_Page.html'>")
print(
    '<img src="/license_manager/imgs/logo.png" alt="SysAid Technologies Ltd." title="license_manager">')
print("</a>")
print("</div")
print("</head><body>")

print("<div class='text-body'>")

form = cgi.FieldStorage()

AD_SERVER = configure.AD_SERVER
AD_BASE_DN = configure.AD_BASE_DN
LDAP_USER_DN = configure.LDAP_USER_DN
LDAP_USER_PASSWORD = configure.LDAP_USER_PASSWORD

userName = form.getvalue("userName")
password = form.getvalue("password")

if userName and password:

    def authentication(_username, _password):
        ldap_conn = ldap.configure.ldap_connection()
        user_filter = f'(&(objectClass=user)(sAMAccountName={_username}))'
        ldap_conn.search(AD_BASE_DN, user_filter, attributes=['distinguishedName', 'memberOf'])
        if len(ldap_conn.entries) == 1:
            user_entry = ldap_conn.entries[0]
            user_dn = user_entry.entry_dn
            try:
                user_conn = Connection(AD_SERVER, user=user_dn, password=_password, auto_bind=True)
            except:
                return False
            if user_conn.bind():
                # Check group membership
                for group in user_entry.memberOf:
                    if "Linux users creation group" in group:
                        return True
        return False


    def ldapusername(username):
        user = ldap.configure.get_user_details(username)
        return user['fullName']

    if authentication(userName, password):
        print(
            '<script>document.cookie = `authenticated=1q2wadghffdgrthdryhd5f4145455y45645ghhfghg#E$R5t6y&U*I9o0p; expires=${new Date(Date.now() + 10 * 60 * '
            '1000).toUTCString()}`;</script>')
        print(
            f'<script>document.cookie = `current_user={ldapusername(userName)}; expires=${{new Date(Date.now() + 60 * 60 * 1000).toUTCString()}}`;</script>')
        print("Content-Type: text/html")
        print()

        print('<script>window.location.href = "https://license/license_manager/Main_Page.html";</script>')
    else:
        print("<div style='padding-top: 30px'><label>Authentication failed</label></div>")



else:

    print("<div style='padding-top: 30px'><label>Please fill out all the required fields.</label></div>")

html_code = '<button onclick="window.location.href = \'/license_manager/\';">Back</button>'
print(html_code)
print("</div>")
print("</body></html>")
