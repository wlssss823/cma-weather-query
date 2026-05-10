import tkinter as tk
from datetime import datetime

import matplotlib.pyplot as plt
import requests
from tkinter import messagebox, ttk
import json
from lxml import etree
from matplotlib import ticker

#从中国气象局天气预报爬取
#destination.json保存城市代码，query.json保存历史查询记录
url = "https://weather.cma.cn/api/now/"#获取当前温度请求的网址
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36 Edg/125.0.0.0"
}#模拟浏览器头部信息
with open('query.json', 'r', encoding='utf-8') as history_file:#读取历史查询记录
    history = json.load(history_file)
def nowtime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")#格式化现在时间

def query_today():#爬取当前温度，发出请求接收数据
    b = entry.get()
    with open('destination.json', 'r', encoding='utf-8') as destination_file:
        city1 = json.load(destination_file)#读取出为列表
        city = {item[0]: item[1] for item in city1}#字典表达式将列表转成字典
    for key, value in city.items():#遍历字典，判断是否存在查询城市
        if b == value:
            result = key
            history.append([b, nowtime()])#加入查询记录
            break
        else:
            result = 0
    if result == 0:#输入城市错误退出
        messagebox.showinfo("查询结果", "未查到该城市")
    else:
        url1 = url + result
        r = requests.get(url1, headers=headers)
        a = json.loads(r.text)

        url2 = "https://weather.cma.cn/web/weather/{}.html".format(result)#将城市代码加入到网址
        r1 = requests.get(url2, headers=headers)
        r1.encoding = "utf-8"#设置编码utf-8
        html = etree.HTML(r1.text)
        #通过xpath获取数据
        b = html.xpath('//*[@id="dayList"]/div[1]/div[3]/text()')#获取天气情况
        c = b[0].split()#去除两端换行符和空格
        high = html.xpath('//*[@id="dayList"]/div[1]/div[6]/div/div[1]/text()')#获取最高温度
        low = html.xpath('//*[@id="dayList"]/div[1]/div[6]/div/div[2]/text()')#获取最低温度
        high1 = high[0].split()#去除两端换行符和空格
        low1 = low[0].split()#去除两端换行符和空格
        #a['data']['now']['temperature']为获取数据json数据中的当前温度
        messagebox.showinfo("查询结果", f"当前温度为: {a['data']['now']['temperature']}\n当前天气为: {c[0]}\n最高温度: {high1[0]}\n最低温度: {low1[0]}")

def query_seven_days():#显示七日内天气情况，通过爬取静态html获取
    b = entry.get()
    with open('destination.json', 'r', encoding='utf-8') as destination_file:
        city1 = json.load(destination_file)
        city = {item[0]: item[1] for item in city1}
    for key, value in city.items():
        if b == value:
            result = key
            history.append([b,nowtime()])#加入查询记录
            break
        else:
            result = 0
    if result == 0:
        messagebox.showinfo("查询结果", "未查到该城市")
    else:
        url2 = "https://weather.cma.cn/web/weather/{}.html".format(result)#将城市代码加入到网址
        r1 = requests.get(url2, headers=headers)
        r1.encoding = "utf-8"
        html = etree.HTML(r1.text)
        days = []
        for i in range(1, 8):
            day = {}
            day['date'] = html.xpath(f'//*[@id="dayList"]/div[{i}]/div[1]/text()')[0].strip()
            day['weather'] = html.xpath(f'//*[@id="dayList"]/div[{i}]/div[3]/text()')[0].strip()
            day['high'] = html.xpath(f'//*[@id="dayList"]/div[{i}]/div[6]/div/div[1]/text()')[0].strip()
            day['low'] = html.xpath(f'//*[@id="dayList"]/div[{i}]/div[6]/div/div[2]/text()')[0].strip()
            days.append(day)

        # 创建一个新的窗口来显示七天天气
        weather_window = tk.Toplevel(root)
        weather_window.title("七天内天气情况")
        weather_window.geometry("800x400")

        # 创建 Treeview 组件
        tree = ttk.Treeview(weather_window, columns=("日期", "天气", "最高温度", "最低温度"), show="headings")
        tree.heading("日期", text="日期")
        tree.heading("天气", text="天气")
        tree.heading("最高温度", text="最高温度")
        tree.heading("最低温度", text="最低温度")
        tree.pack(fill=tk.BOTH, expand=True)

        # 填充 Treeview 组件
        for day in days:
            tree.insert("", tk.END, values=(day['date'], day['weather'], day['high'], day['low']))

#展示历史查询
def show_history():
    # 创建一个新的窗口来显示历史记录
    history_window = tk.Toplevel(root)
    history_window.title("历史查询")
    history_window.geometry("400x300")

    # 创建 Treeview 组件
    tree = ttk.Treeview(history_window, columns=("城市", "时间"), show="headings")
    tree.heading("城市", text="城市")
    tree.heading("时间", text="时间")
    tree.pack(fill=tk.BOTH, expand=True)#tree.pack(fill=tk.BOTH, expand=True)
    # 的作用是让 Treeview 小部件在水平和垂直方向上填充其父容器，并且会扩展以填充父容器中剩余的空间。

    # 填充 Treeview 组件
    for record in reversed(history):
        tree.insert("", tk.END, values=(record[0], record[1]))
#24小时温度变化折线图
def show_curve():
    b = entry.get()
    with open('destination.json', 'r', encoding='utf-8') as destination_file:
        city1 = json.load(destination_file)
        city = {item[0]: item[1] for item in city1}
    for key, value in city.items():
        if b == value:
            result = key
            history.append([b, nowtime()])  # 加入查询记录
            break
        else:
            result = 0
    if result == 0:
        messagebox.showinfo("查询结果", "未查到该城市")
    else:
        url3 = "https://weather.cma.cn/web/weather/{}.html".format(result)
        r4 = requests.get(url3, headers=headers)
        r4.encoding = "utf-8"
        html = etree.HTML(r4.text)
        time = []
        avg_temp = []
        for i in range(2, 10):
            a = html.xpath(f'//*[@id="hourTable_0"]/tbody/tr[1]/td[{i}]/text()')
            b = html.xpath(f'//*[@id="hourTable_0"]/tbody/tr[3]/td[{i}]/text()')
            time.append(a[0])
            temp_str = b[0].replace('℃', '')
            avg_temp.append(float(temp_str))

            # 设置 y 轴刻度为带一位小数
        plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
        # 增加方格背景
        plt.grid(which='both', linestyle='--', alpha=0.7)
        # 标注数据点
        for x, y in zip(time, avg_temp):
            plt.annotate(f'{y:.1f}℃', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
        # f'{y:.1f}'：格式化温度值，保留一位小数。
        # (x, y)：标注的位置。
        # textcoords="offset points"：文本坐标相对于标注点的偏移量。
        # xytext=(0,10)：文本相对于标注点的偏移量，这里设置为向上偏移10个点。
        # ha='center'：水平对齐方式为居中
        # 调整刻度和网格
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.gca().set_facecolor('#f0f0f0')  # 设置背景颜色
        plt.plot(time, avg_temp)
        plt.show()

# 创建主窗口
root = tk.Tk()
root.title("天气查询(请输入城市名称)")

# 设置窗口大小
root.geometry("300x200")

# 创建一个输入框
entry = tk.Entry(root, width=25)
entry.pack(pady=10)

# 创建查询今日天气按钮
button_today = tk.Button(root, text="查询今日温度", command=query_today)
button_today.pack(pady=5)

# 创建查询近七日天气按钮
button_seven_days = tk.Button(root, text="查询近七日天气", command=query_seven_days)
button_seven_days.pack(pady=5)

# 创建历史查询按钮
button_history = tk.Button(root, text="历史查询", command=show_history)
button_history.pack(pady=5)

# 创建展示气温曲线按钮
button_curve = tk.Button(root, text="展示24小时气温曲线", command=show_curve)
button_curve.pack(pady=5)

# 运行主循环
root.mainloop()
#写入查询记录
with open('query.json', 'w', encoding='utf-8') as history_file:
    json.dump(history,history_file ,indent=4)#indent缩进