import json

# 打开源文件
with open('source.json', 'r',encoding='utf-8') as source_file:
    # 读取源文件的内容
    source_data = json.load(source_file)

# 提取需要的部分数据到列表
result = [[sublist[0], sublist[1]] for sublist in source_data['data']['city']]
# 打开目标文件
with open('destination.json', 'w',encoding='utf-8') as destination_file:
    # 将部分数据写入目标文件
    json.dump(result, destination_file,indent=4)

print("部分数据已成功写入目标文件")
