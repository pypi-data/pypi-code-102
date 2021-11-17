"""
This module contains the Database class.

It is used to create new databases, and add or drop tables.
"""
import datetime
import json
import os
import threading
from .table import Table
from .utils import log_transaction
from .constants import initialize_constants, \
    get_db_dir, \
    get_data_file_path, \
    get_log_file_path


class Database():
    """Class to create db, and create or drop tables."""

    _db = {}

    def __init__(self, db_directory):
        """
        Initialize a new db.

        :param db_directory: directory to store db data and logs.
        """
        self.name = 'db'
        initialize_constants(db_directory, True)
        if not os.path.exists(get_db_dir()):
            os.makedirs(get_db_dir())
        if not os.path.exists('{}/db'.format(get_db_dir())):
            os.makedirs('{}/db'.format(get_db_dir()))
        if not os.path.exists('{}/log'.format(get_db_dir())):
            os.makedirs('{}/log'.format(get_db_dir()))

        self.data_filepath = get_data_file_path()
        self.log_filepath = get_log_file_path()
        self._load_db()

        # self._periodically_save()

    def _load_db(self):
        if os.path.exists(self.data_filepath):
            data = json.load(open(self.data_filepath))
            for key in data.keys():
                self._db[key] = Table(key, data[key])
        if os.path.exists(self.log_filepath):

            time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            archived_log = '{}/log/{}.txt'.format(get_db_dir(), time_str)
            os.rename(self.log_filepath, '{}/log/{}.txt'.format(get_db_dir(), time_str))

            with open(archived_log) as f:
                for index, line in enumerate(f):
                    self._replay(json.loads(line))

    def _replay(self, transaction):
        if transaction['class_name'] == Database.__name__:
            method = getattr(self, transaction['method'])
            method(transaction['params'][0])

        elif transaction['class_name'] == Table.__name__:
            table = self.add_table(transaction['object_name'])
            method = getattr(table, transaction['method'])
            method(transaction['params'][0])

    def _periodically_save(self):
        threading.Timer(3600, self._periodically_save).start()
        self._save_to_disk()

    def _save_to_disk(self):
        with open(self.data_filepath, 'w') as outfile:
            res = {k: v.records for (k, v) in self._db.items()}
            json.dump(res, outfile)
        if os.path.exists(self.log_filepath):
            os.remove(self.log_filepath)

    @log_transaction
    def add_table(self, table_name):
        """
        Add a new table. If table name exists, returns existing table.

        :param table_name: name of table
        :return: new :class:`Table`, or existing :class:`Table` matching table_name
        """
        if table_name in self._db:
            print('{} already exists'.format(table_name))
            return self._db[table_name]
        else:
            table = Table(table_name, {})
            self._db[table_name] = table
            return table

    @log_transaction
    def drop_table(self, table_name):
        """
        Drop a table from db.

        :param table_name: name of table to drop
        :return: True if drop successful, False otherwise.

        """
        if table_name in self._db:
            del self._db[table_name]
            return True
        else:
            print('{} does not exist'.format(table_name))
            return False

    def show_tables(self):
        """
        Return list of tables.

        :return: List of tables in db.

        """
        return list(self._db.keys())


if __name__ == '__main__':
    print("hello, world.")
