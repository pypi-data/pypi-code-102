import subprocess, os, re
import tkinter as tk
from tkinter import ttk
from tkinter.constants import END
import tkinter.messagebox as msg
from subprocess import getstatusoutput as sysget

 
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

        self.notebook.add(self.setup_page, text='Button')
        
        self.create_setup_page()

    # 页面1 布局
    def create_setup_page(self):

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
        ttk.Button(self.setup_page, text="Reload", command=self.setup_load_adb, style='Z.TButton').grid(column=1, row=3, pady=5, padx=5)

        # combo box 随着加载按钮的按下 刷新
        self.setup_load_adb()

        ttk.Button(self.setup_page, text="Select", command=self.setup_select_adb, style='Z.TButton').grid(column=3, row=3, pady=5, padx=5)

        # 全局默认设备名
        self.current_device = None
        # 如果只有一个设备直接选为默认设备
        if len(self.connectable_device) == 1:
            self.current_device = self.connectable_device[0]
            ttk.Label(self.setup_page, text=self.current_device).grid(column=2, row=4, pady=5, padx=5)


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
        self.current_device = value + " " + name
        ttk.Label(self.setup_page, text=self.current_device).grid(column=2, row=4, pady=5, padx=5)

    def setup_load_adb(self):
        self.setup_text3 = tk.StringVar()
        info = os.popen("adb devices -l").read().strip()
        able_device = re.findall(r"(\w{16}|192.168.\S*)", info)
        self.connectable_device = tuple(able_device)
        
        self.setup_text_entry3 = ttk.Combobox(self.setup_page, textvariable=self.setup_text3)
        self.setup_text_entry3['values'] = self.connectable_device
        self.setup_text_entry3.grid(column=2, row=3, pady=5, padx=5)


    @classmethod
    def sayTry(cls):
        msg.showinfo("Message", "手机连接失败,请尝试重新连接")  # 弹出消息窗口

    @classmethod
    def sayFail(cls):
        msg.showinfo("Message", "操作失败")  # 弹出消息窗口



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
