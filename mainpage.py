import tkinter as tk
from views import FirstFrame, ChartsFrame, RecordsFrame, SettingsFrame, AboutFrame

"""
该模块由江鹏祥编写
"""


class Mainpage:
    """管理所有的类"""

    def __init__(self, master: tk.Tk):
        """初始化并创建程序所创建首页"""

        # 设置初始资源
        self.root = master
        self.root.title("money_manager")
        self.root.geometry('550x400')
        self.create_page()
        self.show_first_frame()

    def create_page(self):
        # 创建所有页面的类对象
        self.first_frame = FirstFrame(self.root)
        self.charts_frame = ChartsFrame(self.root)
        self.records_frame = RecordsFrame(self.root)
        self.settings_frame = SettingsFrame(self.root)
        self.about_frame = AboutFrame(self.root)

        # 创建菜单栏
        menubar = tk.Menu(self.root)
        menubar.add_command(label='首页', command=self.show_first_frame)
        menubar.add_command(label='图表', command=self.show_charts_frame)
        menubar.add_command(label='记录', command=self.show_records_frame)
        menubar.add_command(label='设置', command=self.show_settings_frame)
        menubar.add_command(label='关于', command=self.show_about_frame)
        self.root['menu'] = menubar

    def show_first_frame(self):
        self.first_frame.pack()
        self.charts_frame.pack_forget()
        self.records_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.about_frame.pack_forget()
        self.root.geometry('550x400')

    def show_charts_frame(self):
        self.first_frame.pack_forget()
        self.charts_frame.pack()
        self.records_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.about_frame.pack_forget()
        # 改变页面大小,以便显示图表
        self.root.geometry("850x600")

    def show_records_frame(self):
        self.first_frame.pack_forget()
        self.charts_frame.pack_forget()
        self.records_frame.pack()
        self.settings_frame.pack_forget()
        self.about_frame.pack_forget()
        self.root.geometry('550x400')

    def show_settings_frame(self):
        self.first_frame.pack_forget()
        self.charts_frame.pack_forget()
        self.records_frame.pack_forget()
        self.settings_frame.pack()
        self.about_frame.pack_forget()
        self.root.geometry('550x400')

    def show_about_frame(self):
        self.first_frame.pack_forget()
        self.charts_frame.pack_forget()
        self.records_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.about_frame.pack()
        self.root.geometry('550x400')


if __name__ == '__main__':
    root = tk.Tk()
    mm = Mainpage(master=root)
    root.mainloop()
