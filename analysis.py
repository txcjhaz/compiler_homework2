import load_data

import re

grammar = []                # 文法
lang = ''                   # 语言
itemSet = []                # 项目集
itemfamily = []             # 项目规范族

terminalSymbols = set()     # 终结符
unterminalSymbols = set()   # 非终结符
first = {}                  # FIRST集
follow = {}                 # FOLLOW集
goMap = []                  # Go函数
ACTION = []
GOTO = []

# 收集所有的终结符和非终结符
def collectSign():
    global grammar

    for g in grammar:
        for value in dict(g).values():
            for ch in value:
                if str(ch).isupper():
                    unterminalSymbols.add(ch)
                else:
                    terminalSymbols.add(ch)

# 是否是终结符
def isUpper(word):
    return word >= 'A' and word <= 'Z'

# FIRST
def handleFirst():
    global grammar
    global first
    # 初始化
    first['S\''] = []
    for sign in unterminalSymbols:
        first[sign] = []
        
    flag = True
    while(flag):
        flag = False
        for g in grammar:
            g = dict(g)
            pos = 0
            while pos < len(list(g.values())[0]):
                # 如果形如A->·BC, 把FIRST(B)加入FIRST(A)
                if str(list(g.values())[0][pos]).isupper():  
                    for ch in first[list(g.values())[0][pos]]:
                        if not ch in first[list(g.keys())[0]] and ch != 'e':
                            first[list(g.keys())[0]].append(ch)
                            flag = True
                    # 如果FIRST(B)包含epsilon(e)
                    if 'e' in first[list(g.values())[0][pos]]:
                        pos += 1
                    else:
                        break
                # 如果形如，A->a，则把a加入FIRST(A)
                else:
                    if not (list(g.values())[0][pos] in first[list(g.keys())[0]]):
                        first[list(g.keys())[0]].append(list(g.values())[0][pos])
                        flag = True
                    break

    print('-----FIRST函数-----')
    print(first)

# FOLLOW
def handleFollow():
    global grammar
    global follow
    global first

    # 初始化
    follow['S\''] = ['#']
    for sign in unterminalSymbols:
        follow[sign] = []

    flag = True
    while flag:
        flag = False
        for g in grammar:
            pos = 0     # 找到非终结符
            ppos = 0    # 找到非终结符后的其他终结符
            key = list(dict(g).keys())[0]
            value = list(dict(g).values())[0]
            while pos < len(value):
                if value[0].isupper():
                    ppos = pos + 1
                    if ppos == len(value):
                        for f in follow[key]:
                            if not f in follow[value[pos]]:
                                follow[value[pos]].append(f)
                                flag = True
                            
                        break
                    while ppos < len(value):
                        if value[ppos].isupper():
                            for f in first[value[ppos]]:
                                if not f in follow[value[pos]] and f != 'e':
                                    follow[value[pos]].append(f)
                                    flag = True
                            if 'e' in first[value[ppos]]:
                                ppos += 1
                            else:
                                pos += 1
                                break

                        else:
                            if not value[ppos] in follow[value[pos]]:
                                follow[value[pos]].append(value[ppos])
                                flag = True
                            pos += 1
                            break

                        if ppos == len(value):   # A->αB 或  A->αBβ 且 β=>e
                            for f in follow[key]:
                                if not f in follow[value[pos]]:
                                    follow[value[pos]].append(f)
                                    flag = True
                else:
                    pos += 1

    print('-----FOLLOW函数-----')
    print(follow)            

# 项目集中包含某个项目
def itemsInclude(items, item):
    for i in items:
        if item['key'] == i['key'] and item['value'] == i['value'] and item['dot'] == i['dot']:
            return True   
    return False

# 求闭包
def closure(item):
    global itemSet

    result = []      # 闭包结果集
    for i in item:
        result.append(i)   # 先把初始值放入集合
        

    # 对集合中的每一个添加新的元素
    # 如果有新元素加入，那么len(result)也增加，即可保证最后结果不再增加
    i = 0
    while(i < len(result)):
        item = result[i]
        if item['dot'] >= len(item['value']) or not isUpper(item['value'][item['dot']]):
            i += 1
            continue    # A->·ab，不管
        for j in range(len(itemSet)):
            if itemSet[j]['key'] == item['value'][item['dot']] and itemSet[j]['dot'] == 0 and not itemsInclude(result, itemSet[j]):
                result.append(itemSet[j])
        i += 1

    return result

# GO
def go(index, sign):
    global itemfamily

    if sign is None:
        return None
    items = itemfamily[index]
    from_  = [];   # 满足go函数的项目集合
    for item in items:
        if item['value'][item['dot']] == sign:
            from_.append({
                'key': item['key'],
                'value': item['value'],
                'dot': item['dot']+1
            })
    
    return closure(from_)

# 生成项目集         
def buildItemSet():
    global grammar
    global itemSet
    for g in grammar:
        for i in range(len(list(g.values())[0]) + 1):
            itemSet.append({
                'key': list(g.keys())[0],
                'value': list(g.values())[0],
                'dot': i})
    print('-----生成项目集-----')
    print(itemSet)

# 规范族去重
def itemfamilyEqual(item1):
    global itemfamily

    for j in range(len(itemfamily)):
        flag = True
        if len(itemfamily[j]) != len(item1):
            continue
        for i in range(len(item1)):
            if not itemsInclude(itemfamily[j], item1[i]):
                flag = False
        if flag:
            return j

    return -1

# 生成项目集规范族
def buildItemFamily():
    global itemfamily
    global itemSet
    global goMap
    
    # 初始化
    goMap = []
    itemfamily.append(closure([itemSet[0]]))
    for m in range(len(itemSet)):
        temp = []
        for n in range(len(itemSet)):
            temp.append(-1)
        goMap.append(temp)
    
    i = 0
    while i < len(itemfamily):
        front = []
        for item in itemfamily[i]:
            if item['dot'] < len(item['value']):
                front.append(item['value'][item['dot']])
        # goMap[i] = []
        for sign in front:      # 生成新的规范族
            newItem = go(i, sign)
            if newItem is None:
                i+=1
                continue
            same = itemfamilyEqual(newItem)
            if same == -1:      # 如果不存在相同的规范族
                itemfamily.append(newItem)
                goMap[i][len(itemfamily)-1] = sign
            else:               # 已经存在相同的规范族
                goMap[i][same] = sign

        i+=1

    print('-----项目集规范族-----')
    print(itemfamily)

# findgrammar
def findgrammar(key, value):
    global grammar
    for i, item in enumerate(grammar):
        if list(grammar[i].keys())[0] == key and list(grammar[i].values())[0] == value:
            return i

# 生成分析表
def buildACTIONGOTO():
    global ACTION
    global GOTO

    for index in range(len(itemfamily)):
        ACTION.append({})
        GOTO.append({})

        for item in itemfamily[index]:

            if item['dot'] == len(item['value']):
                if item['key'] == 'S\'':
                    ACTION[index]['#'] = 'acc'
                    continue
                for f in follow[item['key']]:
                    toIndex = findgrammar(item['key'], item['value'])
                    ACTION[index][f] = 'r' + str(toIndex)
            elif not isUpper(item['value'][item['dot']]):
                for toIndex, kk in enumerate(goMap[index]):
                    if goMap[index][toIndex] == item['value'][item['dot']]:
                        ACTION[index][item['value'][item['dot']]] = 's'+str(toIndex)
            elif isUpper(item['value'][item['dot']]):
                for toIndex, kk in enumerate(goMap[index]):
                    try:
                        if goMap[index][toIndex] == item['value'][item['dot']]:
                            GOTO[index][item['value'][item['dot']]] = toIndex;
                    except Exception as e:
                        print(e)
                        print(item)


    print('-----ACTION-----')
    print(ACTION)
    print('-----GOTO-----')
    print(GOTO)

# 分析语言
def process():
    global grammar
    global lang
    print('-----开始分析-----')
    if lang.replace(' ', '') == '':
        print('-----为空-----')
        return

    statusStack = []
    statusStack.append(0)
    signStack = []
    signStack.append('#')
    pos = 0
    flag = True
    step = 1
    lang += '#'

    while flag:
        try:
            temp = ACTION[int(statusStack[len(statusStack)-1])][lang[pos]]
        except:
            temp = False
        if not temp:              # 不存在
            flag = False
            print('Step ' + str(step) + ' ACTION(' + str(statusStack[len(statusStack)-1]) + ', ' + str(lang[pos]), end='')
            print(') == err，该语法不符合该文法')
        elif temp[0] == 's':      # 入栈
            print('Step ' + str(step) + ' ACTION(' + str(statusStack[len(statusStack)-1]) + ', ' + str(lang[pos]), end='')
            statusStack.append(temp[1])
            signStack.append(lang[pos])
            pos += 1
            print(')状态' + str(statusStack[len(statusStack)-1]) + '入栈')
        elif temp[0] == 'r':      # 规约 
            r = int(temp[1])
            print('Step ' + str(step) + ' ' + str(temp) + ':', end='')
            for i in range(len(list(grammar[r].values())[0])):      # 根据文法长度规约
                signStack.pop()
                statusStack.pop()
            print('用' + str(list(grammar[r].keys())[0]) + '->' + str(list(grammar[r].values())[0]) + '规约且GOTO(' + str(statusStack[len(statusStack) -1]) + ', ' + str(list(grammar[r].keys())[0]) + ')', end = '')

            signStack.append(list(grammar[r].keys())[0]);
            statusStack.append(GOTO[int(statusStack[len(statusStack)-1])][list(grammar[r].keys())[0]]);

            print('状态' + str(statusStack[len(statusStack) - 1]) + '入栈')
        else:
            flag = False;                                                       # 分析成功
            print('acc: 分析成功');

        step += 1

# 开始分析
def analyse():
    global grammar
    global lang
 

    # 读入CFGs
    grammar = load_data.load_CFG()

    # 添加S'
    grammar.insert(0, {'S\'': 'S'})

    collectSign()        # 收集所有的终结符和非终结符
    handleFirst()        # FIRST函数
    handleFollow()       # FOLLOW函数
    buildItemSet()       # 生成项目集
    buildItemFamily()    # 生成项目集规范族
    buildACTIONGOTO()    # 生成分析表

    # 读入语言
    lang = load_data.load_lang()
    process()            # 分析语言


analyse()

    
    

