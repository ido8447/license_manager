from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SUBTREE, ServerPool

AD_SERVER = 'hrzdc10'
AD_BASE_DN = 'DC=corp,DC=local'
LDAP_USER_DN = 'CN=adquery,OU=_Special,OU=Users,OU=Israel,OU=Asia,DC=corp,DC=local'
LDAP_USER_PASSWORD = 'Wh0D0UTh!nkUr?'


def get_user_details(username):
    connection = Connection(AD_SERVER, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, auto_bind=True)
    search_base = AD_BASE_DN
    search_filter = f"(sAMAccountName={username})"
    attributes = ['cn', 'givenName', 'sn', 'mail', 'c', 'memberOf', 'sAMAccountName']  # Add more attributes as needed
    connection.search(search_base, search_filter, attributes=attributes, search_scope=SUBTREE)
    if len(connection.entries) == 1:
        user_entry = connection.entries[0]
        main_group_dn = user_entry.entry_dn
        groups = []
        if 'memberOf' in user_entry:
            groups = [group.split(',')[0].split('=')[1] for group in user_entry['memberOf']]
        user_details = {
            'fullName': user_entry.cn.value if 'cn' in user_entry else '',
            'firstName': user_entry.givenName.value if 'givenName' in user_entry else '',
            'lastName': user_entry.sn.value if 'sn' in user_entry else '',
            'mail': user_entry.mail.value if 'mail' in user_entry else '',
            'country': user_entry.c.value if 'c' in user_entry else '',
            'mainGroup': main_group_dn.split(',')[0].split('=')[1],
            'mainGroupId': main_group_dn.split(',')[1].split('=')[1],
            'groups': groups,
            'userName': user_entry.sAMAccountName.value if 'sAMAccountName' in user_entry else ''
        }
        return user_details
    else:
        return None


def ldap_connection():
    return Connection(AD_SERVER, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, auto_bind=True)
