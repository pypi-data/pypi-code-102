"""Initialize and get global variables."""


def initialize_constants(db_directory, log_enabled):
    """Set global variables.

    Parameters:
    db_directory (string): Path to directory to save db data and logs
    """
    global DB_DIRECTORY
    DB_DIRECTORY = db_directory
    global LOG_ENABLED
    LOG_ENABLED = log_enabled

    global DATA_FILEPATH
    DATA_FILEPATH = '{}/db/data.json'.format(DB_DIRECTORY)
    global LOG_FILEPATH
    LOG_FILEPATH = '{}/log/log.txt'.format(DB_DIRECTORY)


def get_log_file_path():
    """
    Get file path for log.

    :return: log file path
    """
    return LOG_FILEPATH


def get_data_file_path():
    """
    Get db path.

    :return: db path
    """
    return DATA_FILEPATH


def get_db_dir():
    """
    Get db directory.

    :return: db directory
    """
    return DB_DIRECTORY


def get_log_enabled():
    """
    Get log enabled.

    :return: is log enabled
    """
    return LOG_ENABLED
