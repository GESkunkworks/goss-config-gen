# Gossamer/AWS Alias Generator

Generates [Gossamer](https://github.com/GESkunkworks/gossamer) and AWS aliases
based on a single configuration file.

## Requirements
- Python 2.7 or 3.6

  It is recommended that you use [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.io/en/latest/) to separate
  your Python environments.
  
- [Gossamer](https://github.com/GESkunkworks/gossamer)

## Installation

1. Install the latest release of [Gossamer](https://github.com/GESkunkworks/gossamer#installation)

2. Make sure the path that you saved Gossamer to is in your `$PATH`.

    **Linux/Mac:**

    Add to your `.bashrc` (Linux) or `.bash_profile` (Mac):

    ```
    export PATH=$PATH:<add the path to the folder containing the Gossamer binary>
    ```

    **Windows:**

    https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/

3. Install goss-config-gen

    ```
    pip install goss-config-gen
    ```

4. Add the following to the bottom of your `.bash_profile`:

    ```
    # Generated aliases
    if [ -f $HOME/gossamer/goss-generated-aliases.sh ]; then
        . $HOME/gossamer/goss-generated-aliases.sh
    fi
    ```

## Configuration

The configuration file can be specified manually as an argument `--config-file` or `-c`, or it can be set using the
`GOSS_GEN_CONFIG` environment variable. It defaults to `$HOME/goss-config.json`. This is where `goss-config-gen` by
default expects the configuration file to be stored. A [sample configuration file](goss-config.json) is available
to get you started. Customize the values as appropriate.

### `OutputDirectory`
Output directory that files will be written to.

This argument is optional and defaults to `$HOME/gossamer`.

### `OutputFile`
Output file that will contain all the generated aliases

This argument is optional and defaults to `goss-generated-aliases.sh`.

### `RoleAliases`
Mapping of aliases to roles.

This argument is optional and allows for the creation of an alias that maps to one or more roles.

```json
"RoleAliases": {
    "all": [
        "path/role1",
        "path/role2
    ]
}
```

For instance, if you are trying to assume roles `path/role1` and `path/role2` in all accounts using the above
configuration, the generated alias would be `goss-all`. In addition to these aliases, by default, an alias for each
normalized version (`/`'s are replaced with `-`'s) of a role name will be created.

### `GossamerPath`

Path to the Gossamer executable. Defaults to `/usr/local/bin/gossamer`

### `AWSCredentialsPath`

Path to the AWS credentials file. Defaults to `$HOME/.aws/credentials`

### `AWSCLIPath`

Path to the AWS CLI executable. Defaults to `/usr/local/bin/aws`

### `BaseProfile`

Base profile that has credentials from which roles can be assumed. This profile should already be configured in your
AWS credentials file. Defaults to "default".

### `Accounts`
List of objects contining information about accounts. This argument is **required**.

Below is an overview of the fields supported by each object.

| Field  | Description                                                                                        | Required | Defaults                  |
|--------|----------------------------------------------------------------------------------------------------|----------|---------------------------|
| Id     | Account ID                                                                                         | Yes      |                           |
| Name   | Account Name                                                                                       | Yes      |                           |
| Alias  | String to use in the generated alias (i.e. if this is `r1`, the generated alias will be `goss-r1`) | No       | Value of the "Name" field |
| Region | AWS region                                                                                         | Yes      |                           |
| Role   | Role name, including path, to assume                                                               | Yes      |                           |

## Usage

1. Run `goss-config-gen`:
    ```
    goss-config-gen
    ```

2. Restart your terminal

3. Use one of the generated aliases. For example, if one of your `Alias`'s is set to `a`, an alias named `goss-a` would be generated. The alias can be used as follows:

    ```
    goss-a [enter your MFA code here]
    ```

## Importing existing role files

If you already have a number of gossamer role files, you can generated a `goss-config-gen` configuration file by
passing those role files into `goss-config-gen`.

For example, if you have the following role files:

`role-file-1`

```json
{
    "Roles": [
        {
            "AccountName": "acct-a",
            "Region": "us-east-1",
            "RoleArn": "arn:aws:iam::123456789012:role/path/role1"
        },
        {
            "AccountName": "acct-b",
            "Region": "us-east-1",
            "Role": "arn:aws:iam::987654321098:role/path/role1"
        }
    ]
}
```

`role-file-2`

```json
{
    "Roles": [
        {
            "AccountName": "acct-c",
            "Region": "us-east-1",
            "Role": "arn:aws:iam::123456789012:role/cs/role2"
        },
        {
            "AccountName": "acct-d",
            "Region": "us-east-1",
            "Role": "arn:aws:iam::111111111111:role/cs/role2"
        }
    ]
}
```

Run the following command to generate the config file:
```
goss-config-gen \
    --config-file <path-where-config-file-will-be-saved> \
    --import-file <path-to-role-file-1> \
    --import-file <path-to-role-file-2>
```

Note: The `--config-file` argument is optional and only needed if the config file should be saved to a custom location.


It will generate the following configuration file that can be used for subsequent
```json
{
    "Accounts": [
        {
            "Id": "123456789012",
            "Name": "acct-a",
            "Region": "us-east-1",
            "Role": "path/role1"
        },
        {
            "Id": "987654321098",
            "Name": "acct-b",
            "Region": "us-east-1",
            "Role": "path/role1"
        },
        {
            "Id": "123456789012",
            "Name": "acct-c",
            "Region": "us-east-1",
            "Role": "path/role2"
        },
        {
            "Id": "111111111111",
            "Name": "acct-d",
            "Region": "us-east-1",
            "Role": "path/role2"
        }
    ]
}
```

Now to generate the aliases with the new configuration file, simply run `goss-config-gen` as normal:
```
goss-config-gen --config-file <path-to-config-file>
```

Note: Again, the `--config-file` argument is optional and only needed if the config file is stored in a custom location.

### Sample

The [sample configuration file](goss-config.json) will generate the following aliases:

```bash
goss-a
goss-b
goss-c
goss-d
goss-e
goss-acct-f

aws-a
aws-b
aws-c
aws-d
aws-e
aws-acct-f

awsi-a
awsi-b
awsi-c
awsi-d
awsi-e
awsi-acct-f
```
