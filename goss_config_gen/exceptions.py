class InvalidConfigException(Exception):
    """Raised when the configuration is not valid."""


class MissingEnvironmentVariableException(Exception):
    """Raised when an environment variable is missing."""
