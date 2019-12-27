import config

# 文法字符串转换，S->AB转换为{'S': 'AB'}
def genGrammar(str):
    # 去除空格
    str = str.replace(' ', '')
    temp = str.split('->')

    if len(temp) != 2 or len(temp[0]) != 1:
        print('文法有误：', str)
        return None

    subGrammar = []
    # 处理|的情况
    if '|' in temp[1] :
        right_side = temp[1].split('|')
        for right_str in right_side:
            subGrammar.append({temp[0]: right_str})
    else:
        subGrammar.append({temp[0]: temp[1]})

    return subGrammar

# 读入CFGs，将其转换为字典存储，{'S': 'AB'}
def load_CFG():
    content = ''
    with open(config.cfg_path) as f:
        content = f.read()
        print('-----读取CFGs成功-----')
        print(content)
    
    if content != '':
        lines = content.split('\n')

        grammar = []
        for i in range(len(lines)):
            tempGrammar = genGrammar(lines[i])
            grammar += tempGrammar

        return grammar
    

# print(load_CFG())