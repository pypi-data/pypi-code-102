# coding: utf-8

import sys
from datetime import datetime
from random import randint

from faker import Faker
from tabulate import tabulate
import tablib


class AddressBook:
    headers = ["이름", "전화번호", "주소", "직업", "생년월일", "수정한 날짜"]

    def __init__(self):
        self.address_book = []

    def _now(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def table(self):
        return tabulate(self.address_book, headers=self.headers,
                        showindex=True, tablefmt="fancy_grid")

    def show(self):
        print(self.table())

    def add(self, name, phone_number, address, job, birth):
        self.address_book.append(
            [name, phone_number, address, job, birth, self._now()])

    def remove(self, index):
        del self.address_book[index]

    def modify(self, index, name, phone_number, address, job, birth):
        self.address_book[index] = [
            name, phone_number, address, job, birth, self._now()]

    def save(self, fname, type='csv'):
        if type not in ['csv', 'xlsx']:
            sys.stderr.write('파일 타입은 csv 또는 xlsx 이어야 합니다.\n')
            return

        address_book_data = tablib.Dataset()
        address_book_data.headers = self.headers
        for address in self.address_book:
            address_book_data.append(address)

        filepath = fname+'.'+type

        if type == 'xlsx':
            with open(filepath, 'wb') as f:
                f.write(address_book_data.export('xlsx'))
        elif type == 'csv':
            with open(filepath, 'w') as f:
                f.write(address_book_data.export('csv'))

    def load(self, filepath):
        type = filepath.split('.')[-1]
        if type not in ['csv', 'xlsx']:
            sys.stderr.write('파일 타입은 csv 또는 xlsx 이어야 합니다.\n')
            return

        address_book_data = tablib.Dataset()
        address_book_data.headers = self.headers

        try:
            if type == 'xlsx':
                with open(filepath, 'rb') as f:
                    address_book_data.load(f, 'xlsx')
            elif type == 'csv':
                with open(filepath, 'r') as f:
                    address_book_data.load(f, 'csv')
        except FileNotFoundError:
            sys.stderr.write('존재하지 않는 파일입니다.\n')
            return

        self.address_book = address_book_data
    
    def _sort(self, array, key = lambda x: x):
        if len(array) < 2:
            return array

        pivot = array[randint(0, len(array) - 1)]
        _pivot = key(pivot)

        low, same, high = [], [], []

        for item in array:
            _item = key(item)
            if _item < _pivot:
                low.append(item)
            elif _item == _pivot:
                same.append(item)
            elif _item > _pivot:
                high.append(item)

        return self._sort(low, key) + same + self._sort(high, key)

    def sort(self, method):
        if method == '1':
            self.address_book = self._sort(self.address_book, key=lambda x: x[0])
        elif method == '2':
            self.address_book = self._sort(self.address_book, key=lambda x: x[4])
        else:
            sys.stderr.write("1 또는 2 를 입력해주세요.\n")
            sys.stderr.write("정렬 방법은 1 이름 정렬, 2 생년월일 정렬입니다.\n")

class FakeAddressBook(AddressBook):
    def __init__(self):
        super().__init__()
        self.fake = Faker('ko_KR')

    def _fake_person(self):
        return [self.fake.name(), self.fake.phone_number(),
                self.fake.address(), self.fake.job(), self.fake.date(), self._now()]

    def add_fake(self, num):
        for _ in range(num):
            self.address_book.append(self._fake_person())
