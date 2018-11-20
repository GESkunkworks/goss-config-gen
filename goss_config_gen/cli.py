import json
import os
import stat
from argparse import ArgumentParser

from .config import get_config
from .role_import import import_role_files
from .utils import expand_env


def main():
    parser = ArgumentParser(
        description='Generate Gossamer config files and aliases'
    )

    parser.add_argument(
        '--config-file',
        '-c',
        help='Configuration file to use. Defaults to $HOME/goss-config.json [$GOSS_GEN_CONFIG]',
        metavar='<path>'
    )
    
    parser.add_argument(
        '--import-file',
        '-i',
        help='Import an existing gossamer role file and output a configuration file. '
             'This argument can be specified multiple times for multiple gossamer role files.',
        action='append'
    )

    options = parser.parse_args()

    # Configuration file
    if options.config_file:
        config_file = options.config_file
    else:
        config_file = expand_env(os.environ.get('GOSS_GEN_CONFIG', os.path.join('$HOME', 'goss-config.json')))

    # Expand absolute path
    config_file = os.path.abspath(config_file)

    # Check for role file imports
    if options.import_file:
        config = import_role_files(options.import_file)

        with open(config_file, 'w') as f:
            f.write(json.dumps(config, indent=4))

        print('Configuration file written to "%s"' % config_file)
        return

    # Read in the config
    config = get_config(config_file)

    # Build output file path
    output_dir = expand_env(config['OutputDirectory'])
    output_path = os.path.join(
        output_dir,
        config['OutputFile']
    )

    # Create directory if needed
    try:
        os.makedirs(output_dir)
    except OSError:
        pass

    # Read in data
    roles = {}
    aliases = []
    account_data = config['Accounts']
    role_aliases = config.get('RoleAliases', {})

    # Loop through all accounts configured
    for item in account_data:
        # Initialize role dict
        roles.setdefault(item['Role'], [])

        # Create alias
        alias = item.get('Alias', '')
        if not alias:
            alias = item['Name']

        # Add role to the dict
        roles[item['Role']].append({
            "RoleArn": "arn:aws:iam::%(account_id)s:role/%(role)s" % {
                'account_id': item['Id'],
                'role': item['Role']
            },
            "AccountName": item['Name'],
            "Region": item['Region']
        })

        # Write AWS alias
        aliases.append(
            "alias aws-%(alias)s='%(aws_cli_path)s --profile %(account_name)s'\n" % {
                'alias': alias,
                'aws_cli_path': config['AWSCLIPath'],
                'account_name': item['Name']
            }
        )

        # Write AWS insecure alias
        aliases.append(
            "alias awsi-%(alias)s='%(aws_cli_path)s --profile %(account_name)s --no-verify-ssl'\n" % {
                'alias': alias,
                'aws_cli_path': config['AWSCLIPath'],
                'account_name': item['Name']
            }
        )

        # Write gossamer alias
        aliases.append(
            "alias goss-%(alias)s='%(gossamer_path)s -a arn:aws:iam::%(account_id)s:role/%(role)s -profile %(profile)s "
            "-serialnumber $MFA -o %(aws_creds_path)s -entryname %(account_name)s -force -tokencode'\n" % {
                'alias': alias,
                'gossamer_path': config['GossamerPath'],
                'role': item['Role'],
                'profile': config['BaseProfile'],
                'aws_creds_path': config['AWSCredentialsPath'],
                'account_id': item['Id'],
                'account_name': item['Name']
            }
        )

    # Write role alias files
    aliased_roles = set()
    for alias, role_names in role_aliases.items():
        role_file = os.path.join(
            output_dir,
            alias + '.json'
        )

        role_data = []
        for role in role_names:
            role_data += roles.get(role)
            aliased_roles.add(role)

        output_data = {'Roles': role_data}

        with open(role_file, 'w') as f:
            f.write(json.dumps(output_data, indent=4))

        # Write gossamer alias
        aliases.append(
            "alias goss-%(alias)s='%(gossamer_path)s -rolesfile %(role_file)s -profile %(profile)s -serialnumber $MFA "
            "-o %(aws_creds_path)s -force -tokencode'\n" % {
                'alias': alias,
                'gossamer_path': config['GossamerPath'],
                'role_file': role_file,
                'profile': config['BaseProfile'],
                'aws_creds_path': config['AWSCredentialsPath']
            }
        )

    # Write role files
    for role_name, role_data in roles.items():
        normalized_role_name = role_name.replace('/', '-')

        role_file = os.path.join(
            output_dir,
            normalized_role_name + '.json'
        )
        output_data = {'Roles': role_data}

        with open(role_file, 'w') as f:
            f.write(json.dumps(output_data, indent=4))

        # Write gossamer alias
        aliases.append(
            "alias goss-%(alias)s='%(gossamer_path)s -rolesfile %(role_file)s -profile %(profile)s -serialnumber $MFA "
            "-o %(aws_creds_path)s -force -tokencode'\n" % {
                'alias': normalized_role_name,
                'gossamer_path': config['GossamerPath'],
                'role_file': role_file,
                'profile': config['BaseProfile'],
                'aws_creds_path': config['AWSCredentialsPath']
            }
        )

    # Write alias file
    with open(output_path, 'w') as f:
        f.writelines(aliases)

    # Make the file executable
    os.chmod(output_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IROTH)

    print('Generated Gossamer aliases successfully.')
