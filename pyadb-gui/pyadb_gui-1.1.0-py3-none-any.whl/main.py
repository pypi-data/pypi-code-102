import subprocess, os, re
import tkinter as tk
from tkinter import ttk
from tkinter.constants import END
import tkinter.messagebox as msg
from subprocess import getstatusoutput as sysget

current_device = None

class HomePage1(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.resizable(0,0)
        self.root.title('pyadb_GUI')
        self.root.geometry('%dx%d' % (440, 380))  # 设置窗口大小

        self.style = ttk.Style()
        self.style.configure('W.TButton', font = ('calibri', 11, 'bold', 'underline'),foreground = 'Green')
        self.style.configure('X.TButton', font = ('calibri', 11, 'bold', 'underline'),foreground = 'Purple')
        self.style.configure('Y.TButton', font = ('calibri', 11, 'bold', 'underline'),foreground = 'Blue')
        self.style.configure('Z.TButton', font = ('calibri', 11, 'bold'))

        self.createNotebook()
 
    def createNotebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=5, expand=True)
        
        # 页面 1 
        self.setup_page = ttk.Frame(self.notebook, width=380, height=380)
        self.setup_page.pack(fill='both', expand=True)

        # 页面 2
        self.btn_page = ttk.Frame(self.notebook, width=380, height=380)
        self.btn_page.pack(fill='both', expand=True)

        # 页面 3
        self.info_page = ttk.Frame(self.notebook, width=380, height=380)
        self.info_page.pack(fill='both', expand=True)

        # 页面 4
        # self.about_page = ttk.Frame(self.notebook, width=380, height=380)
        # self.about_page.pack(fill='both', expand=True)

        self.notebook.add(self.setup_page, text='Setup')
        self.notebook.add(self.btn_page, text='Button')
        self.notebook.add(self.info_page, text='Information')
        # self.notebook.add(self.about_page, text='About')

        self.createPage_setup()
        self.createPage_btn()
        self.createPage_info()
        # self.createPage_about()


    # Setup 页面布局
    def createPage_setup(self):

        # 自动配置电脑静态 ip 功能

        ttk.Label(self.setup_page, text="Network devices").grid(column=1, row=1, pady=5, padx=5)

        self.setup_text1 = tk.StringVar()
        info = os.popen("nmcli d").read().strip()
        enx = re.findall(r"(enx\S*)", info)
        enx_devices = tuple(enx)
        self.setup_text_entry1 = ttk.Combobox(self.setup_page, textvariable=self.setup_text1)
        self.setup_text_entry1['values'] = enx_devices
        self.setup_text_entry1.grid(column=2, row=1, pady=5, padx=5)

        ttk.Button(self.setup_page, text="Config", command=self.setup_config_eth, style='Z.TButton').grid(column=3, row=1, pady=5, padx=5)


        # adb connect 功能
        ttk.Label(self.setup_page, text="ADB connect").grid(column=1, row=2, pady=5, padx=5)
        
        self.setup_text2 = tk.StringVar()
        adb_list = ('192.168.1.101')
        self.setup_text_entry2 = ttk.Combobox(self.setup_page, textvariable=self.setup_text2)
        self.setup_text_entry2['values'] = adb_list
        self.setup_text_entry2.grid(column=2, row=2, pady=5, padx=5)

        ttk.Button(self.setup_page, text="Connect", command=self.setup_connect_adb, style='Z.TButton').grid(column=3, row=2, pady=5, padx=5)


        # select adb 功能
        # ttk.Label(self.setup_page, text="Select ADB").grid(column=1, row=3, pady=5, padx=5)
        ttk.Button(self.setup_page, text="Reload adb", command=self.setup_load_adb, style='Z.TButton').grid(column=1, row=3, pady=5, padx=5)

        # combo box 随着加载按钮的按下 刷新
        self.setup_load_adb()

        ttk.Button(self.setup_page, text="Select", command=self.setup_select_adb, style='Z.TButton').grid(column=3, row=3, pady=5, padx=5)

        # 全局默认设备名
        global current_device

        # 如果只有一个设备直接选为默认设备
        if len(self.connectable_device) == 1:
            current_device = self.connectable_device[0]
            ttk.Label(self.setup_page, text=current_device).grid(column=2, row=4, pady=5, padx=5)


    # Button 页面布局
    def createPage_btn(self):

        # 实例化 ButtonPress 类
        bp = ButtonPress()

        btn_up = ttk.Button(self.btn_page, text='up', command=bp.ky_up, style = 'Z.TButton').grid(row=1, column=2, pady=5, padx=5)
        btn_down= ttk.Button(self.btn_page, text='down', command=bp.ky_down, style = 'Z.TButton').grid(row=3, column=2, pady=5, padx=5)
        btn_left = ttk.Button(self.btn_page, text='left', command=bp.ky_left, style = 'Z.TButton').grid(row=2, column=1, pady=5, padx=5)
        btn_right = ttk.Button(self.btn_page, text='right', command=bp.ky_right, style = 'Z.TButton').grid(row=2, column=3, pady=5, padx=5)
        btn_enter = ttk.Button(self.btn_page, text='Enter', command=bp.ky_select, style = 'Z.TButton').grid(row=2, column=2, pady=5, padx=5)

        ttk.Button(self.btn_page, text='Back', command=bp.ky_back, style = 'Z.TButton').grid(row=4, column=1, pady=5, padx=5)
        ttk.Button(self.btn_page, text='Home', command=bp.ky_home, style = 'Z.TButton').grid(row=4, column=2, pady=5, padx=5)
        ttk.Button(self.btn_page, text='Menu', command=bp.ky_menu, style = 'Z.TButton').grid(row=4, column=3, pady=5, padx=5)

        ttk.Button(self.btn_page, text='Play/Pause', command=bp.ky_play, style = 'Z.TButton').grid(row=5, column=2, pady=5, padx=5)
        ttk.Button(self.btn_page, text='Vol +', command=bp.ky_vol_up, style = 'Z.TButton').grid(row=5, column=1, pady=5, padx=5)
        ttk.Button(self.btn_page, text='Vol -', command=bp.ky_vol_down, style = 'Z.TButton').grid(row=5, column=3, pady=5, padx=5)

        short_ble = ttk.Button(self.btn_page, text='Bluetooth', command=bp.shortcut_bluetooth, style = 'W.TButton').grid(row=6, column=1, pady=5, padx=5)
        short_wifi = ttk.Button(self.btn_page, text='Wifi', command=bp.shortcut_wifi, style = 'W.TButton').grid(row=6, column=2, pady=5, padx=5)
        short_mirror = ttk.Button(self.btn_page, text='Mirror', command=bp.shortcut_mirror, style = 'W.TButton').grid(row=6, column=3, pady=5, padx=5)

        btn_reload = ttk.Button(self.btn_page, text='Reload', command=self.createPage_info, style='Y.TButton').grid(row=7, column=1, pady=5, padx=5)
        btn_reboot = ttk.Button(self.btn_page, text='Reboot', command=bp.ky_reboot, style='X.TButton').grid(row=7, column=2, pady=5, padx=5)
        btn_oobe = ttk.Button(self.btn_page, text='OOBE', command=bp.ky_OOBE, style='X.TButton').grid(row=7, column=3, pady=5, padx=5)

        input_guide = ttk.Label(self.btn_page, text="input your text:").grid(column=1, row=8, pady=5, padx=5)

        # 可输入文字 统一以 input 开头
        self.input_text = tk.StringVar()
        account = ('kpbhat@us.neusoft.com',
                    'BeyondTech21!',
                    'coex-prime@amazon.com',
                    'lab126@126',
                    'wang.yao_neu@neusoft.com',
                    'w@ngya0O')

        # 可输入文字对应的输入框 在文字变量后加 entry
        self.input_text_entry = ttk.Combobox(self.btn_page, textvariable=self.input_text)
        self.input_text_entry['values'] = account
        self.input_text_entry.grid(column=2, row=8, pady=5, padx=5)

        ttk.Button(self.btn_page, text="Input",  command=self.input, style='Z.TButton').grid(column=3, row=8, pady=5, padx=5)


    # Info 页面布局
    def createPage_info(self):
        self.device = DeviceInfo()

        # tree view 布局
        columns = ('#1', '#2')

        tree = ttk.Treeview(self.info_page, columns=columns, height=300, show='headings')

        # define headings
        tree.heading('#1', text='Name')
        tree.heading('#2', text='Value')

        all_device_info = []
        global current_device
        if current_device is not None:
            all_device_info.append((f'TV Name', f'{self.device.get_bluetooth_tv()[0]}'))
            all_device_info.append((f'Time', f'{self.device.get_time()}'))
            all_device_info.append((f'DSN', f'{self.device.get_dsn()}'))
            all_device_info.append((f'Version', f'{self.device.get_build_version()[0]}'))
            all_device_info.append((f'Version2', f'{self.device.get_build_version()[1]}'))
            all_device_info.append((f'Wifi Mac Address', f'{self.device.get_mac_addr()[0]}'))
            all_device_info.append((f'Eth Mac Address', f'{self.device.get_mac_addr()[1]}'))
            all_device_info.append((f'Wifi ip address', f'{self.device.get_ip_addr()[0]}'))
            all_device_info.append((f'Eth ip address', f'{self.device.get_ip_addr()[1]}'))

            # all_device_info.append((f'TV ble mac addr', f'{self.device.get_bluetooth_tv()[1]}'))

            ble_all = self.device.get_bluetooth_all()
            for i in range(len(ble_all[0])):
                    all_device_info.append((f'{ble_all[1][i]}', f'{ble_all[0][i]}'))

        # adding data to the treeview
        for item in all_device_info:
            tree.insert('', tk.END, values=item)

        # bind the select event
        def item_selected(event):
            for selected_item in tree.selection():
                # dictionary
                item = tree.item(selected_item)
                # list
                record = item['values']

                # copy selected text to clipboard
                # print(f"copied on {record[1]}")
                self.root.clipboard_clear()
                self.root.clipboard_append(record[1])

        tree.bind('<Double-1>', item_selected)

        tree.grid(row=0, column=0, padx=10,sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.info_page, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')


    # "关于" 页面布局

    # def createPage_about(self):
    #     from version import history
    #     results = history
    #     text = tk.Text(self.about_page)
    #     text.pack()
    #     text.insert('end',results)
    #     text['state'] = 'disabled'


    def setup_config_eth(self):
        value = str(self.setup_text1.get())
        answer = msg.showinfo(title='Confirmation', message='请在命令行输入密码')
        try: 
            info = os.popen("nmcli c").read().strip()
            search = 'ethernet-'+value
            if search in info:
                search_result = sysget(f'sudo nmcli con delete {search}')
                os.popen("wait")
            out = sysget(f'sudo nmcli con add type ethernet ifname {value}')
            os.popen("wait")

            os.popen(f'sudo nmcli con modify ethernet-{value} ipv4.method manual ip4 192.168.1.102/24 gw4 192.168.1.1')
            # os.popen("wait")
            # os.popen(f'sudo nmcli connection up ethernet-{value}')
    
        except Exception as e:
            print(e)

    def setup_connect_adb(self):
        value = str(self.setup_text2.get())
        try: 
            os.popen(f'adb connect {value}')
            os.popen("wait")
            result = os.popen(f'adb connect {value}').read()
            if "already connected" in result:
                msg.showinfo("Message", "Connect Successful!")
            else:
                msg.showerror("Message", "Failed! wait a sec and retry")
                
    
        except Exception as e:
            print(e)

    def setup_select_adb(self):
        value = str(self.setup_text3.get())
        info = os.popen("adb devices -l").read().strip()
        name = re.findall(r"%s.*device:(\w*)"%value, info)[0]
        global current_device
        current_device = value
        self.createPage_btn()
        self.createPage_info()
        ttk.Label(self.setup_page, text=current_device).grid(column=2, row=4, pady=5, padx=5)


    def setup_load_adb(self):
        self.setup_text3 = tk.StringVar()
        info = os.popen("adb devices -l").read().strip()
        able_device = re.findall(r"(\w{16}|192.168.\S*)", info)
        self.connectable_device = tuple(able_device)
        
        self.setup_text_entry3 = ttk.Combobox(self.setup_page, textvariable=self.setup_text3)
        self.setup_text_entry3['values'] = self.connectable_device
        self.setup_text_entry3.grid(column=2, row=3, pady=5, padx=5)

    def input(self):
        global current_device
        value = str(self.input_text.get())
        out = sysget(f'adb -s {current_device} shell input text {value}')
        self.input_text_entry.delete(0, END)
        if out[0]==0:
            pass
        else:
            self.sayTry()



    @classmethod
    def sayTry(cls):
        msg.showinfo("Message", "手机连接失败,请尝试重新连接")  # 弹出消息窗口

    @classmethod
    def sayFail(cls):
        msg.showerror("Message", "操作失败")  # 弹出消息窗口



class ButtonPress(object):
    def __init__(self):
        pass

    global current_device

    def ky_reboot(self):
        answer = msg.askyesno(title='Confirmation', message='Are you sure that you want to Reboot?')
        if answer:
            out = sysget(f'adb -s {current_device} shell reboot')
            if out[0]==0:
                pass
            else:
                HomePage1.sayTry()

    def ky_OOBE(self):
        answer = msg.askyesno(title='Confirmation', message='Are you sure that you want to OOBE?')
        if answer:
            out = sysget(f'adb -s {current_device} shell am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.FactoryResetActivity')
            if out[0]==0:
                pass
            else:
                HomePage1.sayTry()

    def ky_up(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 19')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()
 
    def ky_down(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 20')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_left(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 21')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_right(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 22')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_select(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 23')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_back(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 4')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_home(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 3')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_menu(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 82')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_play(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 85')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_vol_up(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 24')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def ky_vol_down(self):
        out = sysget(f'adb -s {current_device} shell input keyevent 25')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def shortcut_bluetooth(self):
        sysget(f'adb -s {current_device} shell input keyevent 4')
        out = sysget(f'adb -s {current_device} shell am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.controllers_bluetooth_devices.ControllersAndBluetoothActivity')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def shortcut_wifi(self):
        sysget(f'adb -s {current_device} shell input keyevent 4')
        out = sysget(f'adb -s {current_device} shell am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.network.NetworkActivity')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def shortcut_mirror(self):
        out = sysget(f'adb -s {current_device} shell am start -n com.amazon.cast.sink/.DisplayMirroringSinkActivity')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()



class DeviceInfo(object):
    def __init__(self, dsn = None):
        self.dsn = dsn

    global current_device

    def get_time(self):
        try:
            time = os.popen(f"adb -s {current_device} shell date").read().strip()
        except:
            time = None
        return time

    def get_build_version(self):
        try:
            info = os.popen(f"adb -s {current_device} shell cat /system/build.prop").read()
            info = info.strip()
        except:
            build_info1 = None
            build_info2 = None
        try:
            build_info1 = re.findall(r"ro.build.display.id=(.*)", info)[0].strip()
        except:
            build_info1 = None

        try:
            build_info2 = re.findall(r"ro.build.description=(.*)", info)[0].strip()
        except:
            build_info2 = None

        return build_info1, build_info2

    def get_dsn(self):
        try:
            info = os.popen(f"adb -s {current_device} shell idme print").read().strip()
            dsn = re.findall(r"serial:\s(\S*)", info)[0].strip()
        except UnicodeDecodeError:
            info = subprocess.check_output(['adb', 'shell', 'idme', 'print'])
            regex = rb"serial:\s(\w*)"
            dsn = re.findall(regex, info)
            dsn = str(dsn)[3:-2]
        except:
            dsn = None
        return dsn
        
    def get_mac_addr(self):
        try:
            info = os.popen(f"adb -s {current_device} shell ifconfig").read()
            info = info.strip()
        except:
            wifi_mac = None
            eth_mac = None
        try:
            wifi_mac = re.findall(r"wlan0.*HWaddr\s(\S*)", info)[0].strip()
        except:
            wifi_mac = None
        try:
            eth_mac = re.findall(r"eth0.*HWaddr\s(\S*)", info)[0].strip()
        except:
            eth_mac = None

        return wifi_mac, eth_mac

    def get_ip_addr(self):
        info = os.popen(f"adb -s {current_device} shell ifconfig").read()
        info = info.strip()
        try:
            wifi_ip = re.findall(r"wlan0.*\n.*addr:(\S*)", info)[0].strip()
        except:
            wifi_ip = None
        try:
            eth_ip = re.findall(r"eth0.*\n.*addr:(\S*)", info)[0].strip()
        except:
            eth_ip = None
        return wifi_ip, eth_ip

    def get_bluetooth_tv(self):
        try:
            info = os.popen(f"adb -s {current_device} shell cat /data/misc/bluedroid/bt_config.conf").read()
            info = info.strip()
        except:
            name = None
            addr = None
        try:
            name = re.findall(r"Name\s=\s(.*)", info)[0].strip()
        except:
            name = None
        try:
            addr = re.findall(r"\[Adapter\][\n]Address\s=\s(.*)", info)[0].strip()
        except:
            addr = None
        return name,addr

    def get_bluetooth_all(self):
        try:
            info = os.popen(f"adb -s {current_device} shell cat /data/misc/bluedroid/bt_config.conf").read()
            info = info.strip()
        except:
            device_mac_addr = None
            device_name = None
        try:
            device_mac_addr = re.findall(r"\[(\S{17})\]", info)
        except:
            device_mac_addr = None
        try:
            device_name = re.findall(r"Timestamp.*\nName\s=\s(.*)", info)[0:]
        except:
            device_name = None
        
        return device_mac_addr, device_name


if __name__ == '__main__':
    root = tk.Tk()
    root.title('pyadb_GUI')
    HomePage1(root)
    root.mainloop()

def main():
    root = tk.Tk()
    root.title('pyadb_GUI')
    HomePage1(root)
    root.mainloop()
