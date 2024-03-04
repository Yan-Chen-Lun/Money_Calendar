import json
import time
import save
import tkinter as tk
import matplotlib.pyplot as plt

from database import db
from tkinter import ttk
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
FirstFrame, RecordsFrame, SettingsFrame, AboutFrame由江鹏祥编写 
ChartsFrame由申兆曦编写
"""


class FirstFrame(tk.Frame):

    def __init__(self, root):
        super().__init__(root)

        # 定义成员变量为整数,方便后台数据计算
        self.income = tk.IntVar()
        self.expenditure = tk.IntVar()

        # 显示页面
        self.create_page()

    def create_page(self):

        # 打印日期
        self.day = time.strftime('%Y-%m-%d', time.localtime())
        tk.Label(self, text="今天是" + " " + self.day).grid(row=0, column=1, pady=10)

        # 增加收入与支出的标签和输入框
        tk.Label(self, text="收入:").grid(row=1, column=0, pady=10)
        tk.Entry(self, textvariable=self.income).grid(row=1, column=1, pady=10)
        tk.Label(self, text="支出:").grid(row=2, column=0, pady=10)
        tk.Entry(self, textvariable=self.expenditure).grid(row=2, column=1, pady=10)

        # 创建完成按钮
        tk.Button(self, text="完成", command=self.done).grid(row=3, column=1)

        # 消费提醒,if语句防止月初报错
        if time.strftime('%Y-%m', time.localtime()) in db.records_monthly:
            self.notice = db.check_limit(db.records_monthly[time.strftime('%Y-%m', time.localtime())])
            self.notice_label = tk.Label(self, text=self.notice)
            self.notice_label.grid(row=4, column=1, pady=10)

    def done(self):
        # 获取记录信息
        with open("records_daily_details.JSON", mode="r+", encoding="utf-8") as f:
            details = eval(str(json.load(f)))

        # print(details)
        # print(type(details))

        # 获取输入框信息
        detail = {"day": self.day, "income": self.income.get(), "expenditure": self.expenditure.get(),
                  "add_up": self.income.get() - self.expenditure.get()}

        # print(detail["day"], details[-1]["day"])

        # 对本次完成操作进行记录
        # 判断是否存在相同日期只需要对details[-1]进行判断
        if detail["day"] == details[-1]["day"]:
            details[-1]["income"] += detail["income"]
            details[-1]["expenditure"] += detail["expenditure"]
            details[-1]["add_up"] = details[-1]["add_up"] + detail["income"] - detail["expenditure"]
            # print(details[-1])

        else:
            details.append(detail)
            details = sorted(details, key=lambda x: x["day"], reverse=False)
            # print(details)

        # 记录成功时刷新输入框数据
        self.income.set(0)
        self.expenditure.set(0)

        # 储存数据
        save.records_daily_save(details=details)
        save.records_monthly_save()

        # 刷新提醒
        self.refresh_notice()

    def refresh_notice(self):
        # 销毁提醒标签
        self.notice_label.destroy()
        # 更新后台数据
        db.refresh()
        # 重新创建提醒标签
        self.notice = db.check_limit(db.records_monthly[time.strftime('%Y-%m', time.localtime())])
        self.notice_label = tk.Label(self, text=self.notice)
        self.notice_label.grid(row=4, column=1, pady=10)


class ChartsFrame(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.create_page()

    def create_page(self):
        # 创建图表
        self.create_matplotlib()
        self.create_widget(self.figure)
        # 添加注释
        tk.Label(self, text="为使图表更加直观,正值表示支出,负值表示收入").grid(row=1, column=0, pady=10)
        # 添加刷新按钮
        tk.Button(self, text="刷新", command=self.refresh_charts).grid(row=2, column=0, pady=10)

    def create_matplotlib(self):
        # 创建plt图像的基本容器
        self.figure = plt.figure(num=2, figsize=(10, 6), dpi=80, frameon=True)
        # 从db中获取数据
        self.days = []
        self.money_daily = []
        # 防止逻辑错误
        # 不展示年份,只显示月份与日期
        if len(db.records_daily) <= 7:
            for d in db.records_daily:
                self.days.append(d["day"][5:10])
                self.money_daily.append(-d["add_up"])
        else:
            for d in db.records_daily[-8:]:
                self.days.append(d["day"][5:10])
                self.money_daily.append(-d["add_up"])

        # 只显示近三个月的数据,同时防止逻辑错误
        if len(db.records_monthly) <= 3:
            self.months = db.records_monthly.keys()
            self.money_monthly = db.records_monthly.values()
        else:
            self.months = db.records_monthly.keys()[-3:]
            self.money_monthly = db.records_monthly.values()[-3:]

        # 将数据转化为正值
        self.money_monthly = list(map(lambda x: abs(x), self.money_monthly))

        # 绘制图表
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
        mpl.rcParams['axes.unicode_minus'] = False  # 负号显示
        fig1 = plt.subplot(311)
        x1 = range(len(self.days))
        y1 = self.money_daily
        fig1.set_title("近七天收支数据")
        # 适用蓝色线条
        fig1.plot(x1, y1, "#0000FF")
        fig1.set_xticks(x1)
        fig1.set_xticklabels(self.days)
        fig1.grid()
        # 将第二张图放在第三行使得图表不重叠
        fig2 = plt.subplot(313)
        x2 = range(len(self.months))
        y2 = self.money_monthly
        fig2.set_title("近三个月收支数据")
        fig2.plot(x2, y2, "#0000FF")
        fig2.set_xticks(x2)
        fig2.set_xticklabels(self.months)
        fig2.grid()

    def create_widget(self, figure):
        """创建组件"""

        # 创建画布
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, pady=10)

    def refresh_charts(self):
        # 清楚容器,防止刷新后出现多线重叠
        self.figure.clear()
        # 删除原有组件,防止刷新后多组件重叠
        for widget in self.winfo_children():
            widget.destroy()
        # 刷新数据
        db.refresh()
        # 重新生成页面
        self.create_page()


class RecordsFrame(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        # 创建纵向滚轮
        self.yscroll = tk.Scrollbar(self, orient="vertical")
        # 创建按钮
        tk.Button(self, text="刷新", command=self.refresh_data).pack(side=tk.BOTTOM, pady=50)

        self.create_page()

    def create_page(self):
        self.columns = ['日期', '收入', '支出', '总计']
        # 创建表格对象
        self.table = ttk.Treeview(
            master=self,
            height=10,
            columns=self.columns,
            show='headings',
            yscrollcommand=self.yscroll.set
        )
        self.table.pack()

        # 定义表头
        for column in self.columns:
            self.table.heading(column=column, text=column, anchor="w")

        # 定义列
        for column in self.columns:
            self.table.column(column, width=100, minwidth=100, anchor="center")

        # 包装表格
        self.table.pack(fill=tk.BOTH, expand=False)

        # 排序数据
        db.records_daily = sorted(db.records_daily, key=lambda x: x["day"], reverse=True)

        # 添加数据
        for d in db.records_daily:
            row_lst = [d["day"], d["income"], d["expenditure"], d["add_up"]]
            self.table.insert(parent="", index="end", values=row_lst)

    def refresh_data(self):
        # 删除原有组件
        self.table.destroy()
        # 重新生成页面
        db.refresh()
        self.create_page()


class SettingsFrame(tk.Frame):
    """设置消费提醒"""

    def __init__(self, root):
        super().__init__(root)
        self.down_limit = tk.IntVar()
        self.up_limit = tk.IntVar()

        self.create_page()

    def create_page(self):
        # 各组件排版
        tk.Label(self, text="请根据您的习惯设置您的月消费预期:").grid(row=0, column=1, pady=10)
        tk.Label(self, text="~").grid(row=1, column=1, pady=10)
        # print(db.settings["down_limit"], db.settings["up_limit"])
        tk.Entry(self, textvariable=self.down_limit).grid(row=1, column=0, pady=10)
        tk.Entry(self, textvariable=self.up_limit).grid(row=1, column=2, pady=10)

        tk.Button(self, text="完成", command=self.done_setup).grid(row=2, column=1, pady=10, sticky="s")

    def done_setup(self):
        # 获取到输入框数据
        detail = {"down_limit": self.down_limit.get(), "up_limit": self.up_limit.get()}
        # 储存数据
        save.setting_save(detail)


class AboutFrame(tk.Frame):

    def __init__(self, root):
        super().__init__(root)

        self.create_page()

    def create_page(self):
        tk.Label(self, text='关于作品:本作品由tkinter制作').pack()
        tk.Label(self, text='关于作者:本作品由 江鹏祥 和 申兆曦 联合制作').pack()
        tk.Label(self, text='关于版权:版权归作者所有').pack()


if __name__ == '__main__':
    root = tk.Tk()
    chats = ChartsFrame(root=root)
    root.mainloop()
