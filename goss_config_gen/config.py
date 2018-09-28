import json
import os
import six

from .exceptions import InvalidConfigException, MissingEnvironmentVariableException


def set_config_defaults(config):
    """
    Set default values

    :param dict config: Configuration
    :return:
    """
    config.setdefault('OutputDirectory', '$HOME/gossamer')
    config.setdefault('OutputFile', 'goss-generated-aliases.sh')
    config.setdefault('GossamerPath', '/usr/local/bin/gossamer')
    config.setdefault('AWSCLIPath', '/usr/local/bin/aws')
    config.setdefault('AWSCredentialsPath', '$HOME/.aws/credentials')
    config.setdefault('BaseProfile', 'default')


def validate_config(config):
    """
    Validate the config file

    :param dict config: Config
    :raises InvalidConfigException
    """
    required_fields = {
        'Accounts': list
    }

    if six.PY2:
        str_types = (unicode, str)
    else:
        str_types = str

    optional_fields = {
        'OutputDirectory': str_types,
        'OutputFile': str_types,
        'GossamerPath': str_types,
        'AWSCredentialsPath': str_types,
        'BaseProfile': str_types,
        'RoleAliases': dict
    }

    # Validate required fields
    for field, field_type in required_fields.items():
        if field not in config:
            raise InvalidConfigException('Missing key "%s" in configuration file.' % field)
        elif not isinstance(config[field], field_type):
            raise InvalidConfigException('Key "%s" should be type %s' % (field, field_type))

    # Validate optional fields
    for field, field_type in optional_fields.items():
        if field in config and not isinstance(config[field], field_type):
            raise InvalidConfigException('Key "%s" should be type %s' % (field, field_type))

    # Make sure user has $MFA in their profile
    if 'MFA' not in os.environ:
        raise MissingEnvironmentVariableException(
            'The environment variable $MFA is missing. '
            'This should be configured with your multi-factor device serial number.'
        )


def get_config(config_file):
    """
    Read and validate configuration file

    :param str config_file: Config file path
    :return: Configuration
    :rtype: dict
    """
    # Check if file exists
    if not os.path.exists(config_file):
        raise InvalidConfigException('The configuration file "%s" does not exist' % config_file)

    # Read config file
    with open(config_file, 'r') as f:
        config = json.loads(f.read())

    # Configure default values
    set_config_defaults(config)

    # Validate configuration
    validate_config(config)

    return config
