import argparse
import csv
import logging
import logging.handlers
import sys
from pathlib import Path

import pandas

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Bookizer:

    arguments = None
    log = logging.getLogger('bookizer')
    extra_params = None
    _credentials = None
    files = None
    csv_streams = None

    def __init__(self):
        handler = logging.StreamHandler(sys.stdout)
        self.log.addHandler(handler)
        self.files = []
        self.csv_streams = {}
        self.log.setLevel(logging.INFO)
        parser = argparse.ArgumentParser(description='Bookizer allows to convert multiple csvs into a big one ods/xsl/xlslx/csv file.')
        parser.add_argument('--from', '-f', action='append', type=str, dest='filenames', help='List of csv files or folders.')
        parser.add_argument('--to', '-o', type=Path, dest='output', help='Output file, can be csv, xsl, xslx or ods.')
        self.args = parser.parse_args()

    def start(self):
        if not self.args.filenames:
            return 'No file provided.'

        if not self.args.output or not str(self.args.output).endswith(('.csv', '.xsl', '.xlsx', '.ods')):
            return 'No valid output provided'

        for file_name in self.args.filenames:
            file = Path(file_name).resolve()

            if file.is_file() and not file_name.endswith('.csv'):
                return f'{file_name} is not a valid csv'

            if file.is_dir():
                for item in file.glob('*.csv'):
                    self.files.append(item)
            else:
                self.files.append(file)

        temp_streams = {}
        for file in self.files:
            try:
                obj = csv.DictReader(open(str(file), 'r'))
                _fieldnames = obj.fieldnames
                csv_name = file.stem
                temp_streams.setdefault(csv_name, 0)
                temp_streams[csv_name] += 1
                num = temp_streams[csv_name]
                if num > 1:
                    csv_name = f'{csv_name} {num}'
                self.csv_streams[csv_name] = obj
            except BaseException:
                return f'{file_name} is not a valid csv.'

    def convert(self):
        if str(self.args.output).endswith(('.xls', '.xlsx', '.ods')):
            return self.convert_to_excel()
        else:
            return self.convert_to_csv()

    def convert_to_excel(self):
        file_name = str(self.args.output.resolve())

        try:
            writer = pandas.ExcelWriter(file_name)

            for csvfilename in self.files:
                df = pandas.read_csv(csvfilename)
                df.to_excel(writer, sheet_name=csvfilename.stem, index=False)
            writer.save()
        except BaseException as excp:
            self.log.exception(excp)
            return 1

    def convert_to_csv(self):

        fieldnames = []
        file_name = str(self.args.output.resolve())
        data = []

        try:
            with open(file_name, 'w') as output_file:
                for file_name, reader in self.csv_streams.items():
                    fieldnames.extend(reader.fieldnames)
                    for item in reader:
                        item['ORIGINAL_FILE'] = file_name
                        data.append(item)
                fieldnames = list(set(x for x in fieldnames))
                fieldnames.insert(0, 'ORIGINAL_FILE')
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except BaseException as excp:
            self.log.exception(excp)
            return 1

def main():
    try:
        bookizer = Bookizer()
        objection = bookizer.start()
        if objection:
            return objection
        return bookizer.convert()
    except KeyboardInterrupt:
        return 'Interrupted by the user. Exiting.'

if __name__ == '__main__':
    sys.exit(main())
