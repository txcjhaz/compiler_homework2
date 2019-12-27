import load_data

grammar = []                # 文法
lang = ''                   # 语言
itemSet = []                # 项目集
itemfamily = []             # 项目规范族

terminalSymbols = set()     # 终结符
unterminalSymbols = set()   # 非终结符
first = {}                  # FIRST集
follow = {}                 # FOLLOW集
goMap = []                  # Go函数
log = ''                    # 日志
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
                

# 开始分析
def analyse():
    global grammar

    # 读入CFGs
    grammar = load_data.load_CFG()

    # 添加S'
    grammar.insert(0, {'S\'': 'S'})

    collectSign()        # 收集所有的终结符和非终结符
    handleFirst()        # FIRST函数
    handleFollow()       # FOLLOW函数


analyse()

    
    

