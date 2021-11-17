"""
Converter from Bancolombia to YNAB.
"""

import csv
import json
import pathlib

import arrow
import xdg
import click
import bullet


class PayeeCache:
    def __init__(self, filename):
        self.filename = pathlib.Path(filename)
        self._data = {}

    def _ensure(self):
        if self.filename.parent.exists():
            return
        self.filename.parent.mkdir()

    def _read(self):
        if not self.filename.is_file():
            self._data = {}
            return
        try:
            self._data = json.load(self.filename.open())
        except json.JSONDecodeError:
            self._data = {}

    def _write(self):
        self._ensure()
        json.dump(self._data, self.filename.open("w"), indent=2)

    def get(self, name, **context):
        self._read()
        if name not in self._data:
            # get the name
            cli = bullet.Bullet(
                prompt=f"{name} | {context}",
                choices=["Other"] + ["None"] + [w.title() for w in name.split()],
            )
            result = cli.launch()
            if result == "Other":
                result = input("Which: ")
            if result == "":
                return result
            if result == "None":
                result = ""
            self._data[name] = result
            self._write()
        return self._data[name]

    def clear(self):
        self._data = {}
        self._write()


@click.command()
@click.option("--input", "-i", type=click.File("r", encoding="latin-1"), default="-")
@click.option("--output", "-o", type=click.File("w"), default="-")
@click.option("--clear-cache", is_flag=True)
@click.option("--credit-card", "-c", is_flag=True)
def main(input, output, clear_cache, credit_card):
    reader = csv.reader(input, delimiter="\t")
    writer = csv.writer(output)
    next(reader)  # skip headers
    cache = PayeeCache(xdg.xdg_cache_home().joinpath("converter/cache.json"))
    if clear_cache:
        cache.clear()
    writer.writerow(["Date", "Payee", "Memo", "Amount"])
    for row in reader:
        if credit_card:
            date, memo, _, ref, value, _, _ = row
        else:
            date, _, _, memo, ref, value, _ = row
        writer.writerow(
            [
                arrow.get(date).format("MM/DD/YYYY"),
                cache.get(f"{memo} - {ref}", value=value),
                memo,
                float(value.replace(",", "")),
            ]
        )


if __name__ == "__main__":
    main()
