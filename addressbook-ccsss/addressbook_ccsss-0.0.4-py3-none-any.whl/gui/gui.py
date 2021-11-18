from addressbook.AddressBook import FakeAddressBook
from PySimpleGUI import *

def gui_add(table, address_book):
    layout = [[Text('이름:', size=(8, 1)), Input(key="name")],
              [Text('전화번호:', size=(8, 1)), Input(key="phone_number")],
              [Text('주소:', size=(8, 1)), Input(key="address")],
              [Text('직업:', size=(8, 1)), Input(key="job")],
              [Text('생년월일:', size=(8, 1)), Input(key="birth")],
              [OK()]]

    window = Window('프로필 추가', layout)
    event, values = window.read()

    profile = (values['name'], values['phone_number'], values['address'], 
               values['job'], values['birth'])
    if None in profile or '' in profile:
        Popup("주의! 모든 필드를 입력하세요")
    else:
        address_book.add(*profile)
        table.update(values=address_book.address_book)
    window.close()

def gui_add_fake(table, address_book):
    layout = [[Text('가짜 프로필 개수:'), Input(key="fake_address", size=(8, 1)), OK()] ]

    window = Window('가짜 추가', layout)
    event, values = window.read()

    try:
        num = int(values['fake_address'])
    except ValueError:
        Popup("주의! 숫자만 입력하세요") 
    else:
        address_book.add_fake(num)
        table.update(values=address_book.address_book)
    window.close()

def gui_modify(table, address_book, selected):
    layout = [[Text('이름:', size=(8, 1)), Input(key="name")],
              [Text('전화번호:', size=(8, 1)), Input(key="phone_number")],
              [Text('주소:', size=(8, 1)), Input(key="address")],
              [Text('직업:', size=(8, 1)), Input(key="job")],
              [Text('생년월일:', size=(8, 1)), Input(key="birth")],
              [OK()]]

    window = Window('프로필 수정', layout)
    event, values = window.read()

    profile = (values['name'], values['phone_number'], values['address'], 
               values['job'], values['birth'])
    address_book.modify(selected, *profile)
    table.update(values=address_book.address_book)
    window.close()

def gui_remove(table, address_book, selected):
    address_book.remove(selected)
    table.update(values=address_book.address_book)

def gui_save(address_book):
    layout = [[Text('파일 이름:'), Input(key="filename"), Combo(['csv', 'xlsx'], key="type"), OK()]]

    window = Window('주소록 저장', layout)

    event, values = window.read()
    address_book.save(values['filename'], values['type'])
    window.close()

def gui_load(table, address_book):
    layout = [[Text('파일 이름:'), Input(), FileBrowse(key="filename")],
              [OK(), Cancel()]]

    window = Window('주소록 불러오기', layout)
    event, values = window.read()

    address_book.load(values['filename'])
    addr_book = [list(addr) for addr in address_book.address_book]
    table.update(values=addr_book)
    window.close()

def gui_sort(table, address_book):
    layout = [[Text("정렬방법:"), 
               Radio('이름', "RADIO1", default=True, key="name"), 
               Radio('생년월일', "RADIO1", key="birth"), Ok()]]

    window = Window('프로필 정렬', layout)
    event, values = window.read()

    if values['name']:
        address_book.sort('1')
    elif values['birth']:
        address_book.sort('2')
    table.update(values=address_book.address_book)
    window.close()

def gui_main():
    theme('Reddit')
    address_book = FakeAddressBook()
    layout = [[Table(values=address_book.address_book,
                     headings=address_book.headers,
                     justification='left',
                     auto_size_columns=False,
                     display_row_numbers=True,
                     row_height=25,
                     num_rows=25,
                     col_widths=[5,10,30,20,10,15],
                     alternating_row_color='lightyellow',
                     key='-TABLE-')],
              [Button("추가", key="add"), Button("가짜 추가", key='add_fake'),
               Button("수정", key="modify"), Button("삭제", key="remove"),
               Button("저장", key="save"), Button("불러오기", key="load"),
               Button("정렬", key="sort"), Button("종료", key="exit")]]

    window = Window('내가 만든 주소록 프로그램', layout)

    while True:
        event, values = window.read()
        if event in ("exit", WIN_CLOSED):
            break
        elif event == "add":
            gui_add(window['-TABLE-'], address_book)
        elif event == "add_fake":
            gui_add_fake(window['-TABLE-'], address_book)
        elif event == "modify":
            selected = values['-TABLE-'][0]
            gui_modify(window['-TABLE-'], address_book, selected)
        elif event == "remove":
            selected = values['-TABLE-'][0]
            gui_remove(window['-TABLE-'], address_book, selected)
        elif event == "save":
            gui_save(address_book)
        elif event == "load":
            gui_load(window['-TABLE-'], address_book)
        elif event == "sort":
            gui_sort(window['-TABLE-'], address_book)
    window.close()

if __name__ == '__main__':
    gui_main()