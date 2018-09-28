import json
import re


def import_role_files(role_files):
    """
    Import Gossamer role files to generate a goss-gen config file

    :param list role_files: List of role file paths
    :return: Generated configuration
    :rtype: dict
    """

    account_roles = set()
    accounts = []

    for filename in role_files:
        with open(filename, 'r') as f:
            file_data = json.loads(f.read())

        for item in file_data['Roles']:
            matches = re.match(r'arn:aws:iam::(?P<account>\d+):role/(?P<role>.+)', item['RoleArn'])

            account = matches.group('account')
            role = matches.group('role')

            if (account, role) in account_roles:
                continue

            accounts.append({
                'Id': account,
                'Name': item['AccountName'],
                'Region': item['Region'],
                'Role': role
            })

            account_roles.add((account, role))

    return {'Accounts': accounts}
