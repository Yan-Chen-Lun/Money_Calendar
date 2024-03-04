import json

"""
该模块由江鹏祥编写
"""


class MysqlDatabases:
    def __init__(self):
        # 读取记录文件并将其转化为元组
        with open("records_daily_details.JSON", mode="r", encoding="utf-8") as f:
            self.records_daily: tuple = eval(str(json.load(f)).strip("[]"))

        # 读取设置文件并将其转化为字典
        with open("setting_details.JSON", mode="r", encoding="utf-8") as f:
            self.settings: dict = eval(str(json.load(f)).strip("[]"))

        with open("records_monthly_details.JSON", mode="r", encoding="utf-8") as f:
            self.records_monthly: dict = eval(str(json.load(f)).strip("[]"))

    def check_limit(self, add_up):
        if self.settings["down_limit"] <= abs(add_up) <= self.settings["up_limit"]:
            return "近期您的消费情况良好,请继续保持"
        elif abs(add_up) < self.settings["down_limit"]:
            return "近期您的消费水平过低,请不要因为节省而做出少餐或不餐等影响身体健康的行为"
        elif abs(add_up) > self.settings["up_limit"]:
            return "近期您的消费超标,请合理指定消费计划"

    def refresh(self):
        # 重新读取数据实现刷新
        with open("records_daily_details.JSON", mode="r", encoding="utf-8") as f:
            self.records_daily: tuple = eval(str(json.load(f)).strip("[]"))
        with open("setting_details.JSON", mode="r", encoding="utf-8") as f:
            self.settings: dict = eval(str(json.load(f)).strip("[]"))
        with open("records_monthly_details.JSON", mode="r", encoding="utf-8") as f:
            self.records_monthly: dict = eval(str(json.load(f)).strip("[]"))


# 创建db实例
db = MysqlDatabases()

if __name__ == '__main__':
    for t in db.records_daily:
        row_lst = [t["day"], t["income"], t["expenditure"], t["add_up"]]
        print(row_lst)
    print(db.check_limit(1))


