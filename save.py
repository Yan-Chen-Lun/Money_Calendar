import json

"""
    该部分由江鹏祥编写
"""


def records_daily_save(details):
    with open("records_daily_details.JSON", mode="w", encoding="utf-8") as f:
        f.write(json.dumps(details, ensure_ascii=False))


def records_monthly_save():
    with open("records_daily_details.JSON", mode="r", encoding="utf-8") as f:
        records_daily: tuple = eval(str(json.load(f)).strip("[]"))

        # 重新创建容器,利用判断实现从收支日数据转向收支月数据
        day_lst = [d["day"] for d in records_daily]
        month_lst = []
        # print(day_lst)
        add_up_monthly_lst = []

        # day[:7]正好是月份数据
        # 填充月容器
        for day in day_lst:
            if day[:7] not in month_lst:
                month_lst.append(day[:7])
        # 计算月收支数据
        for month in month_lst:
            add_up_monthly = 0
            for d in records_daily:
                if d["day"][:7] == month:
                    add_up_monthly += d["add_up"]
            add_up_monthly_lst.append(add_up_monthly)
        # print(month_lst)
        # print(add_up_monthly_lst)

    # 储存数据
    with open("records_monthly_details.JSON", mode="w", encoding="utf-8") as f:
        records_monthly = {}
        for i in range(len(month_lst)):
            records_monthly[month_lst[i]] = add_up_monthly_lst[i]
        # print(records_monthly)
        f.write(json.dumps(records_monthly, ensure_ascii=False))


def setting_save(details):
    with open("setting_details.JSON", mode="w", encoding="utf-8") as f:
        f.write(json.dumps(details, ensure_ascii=False))


"""
    所有保存模式采用重写操作
"""


if __name__ == '__main__':
    records_monthly_save()
