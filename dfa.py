class DFA():
    def __init__(self):
        #状态集
        self.listEdge = []
        #初态
        self.S = []
        #终态
        self.Z = []

    #判断是否是终态集
    def isZ(self,ch):
        for i in range(0,len(self.Z)) :
            if self.Z[0] == ch or self.Z[1] == ch:
                return True
            else:
                return False

    #输入
    def input(self):
        self.S = input("请输入开始符：")
        self.Z = input("请输入终态集(终集符组成的一个字符串)：")
        self.Z = self.Z.split(",")
        print("请输入正规文法以exit结尾：")
        print("example:S,aZ")
        while(True):
            list = []
            inStr = input()
            if inStr=='exit':
                break
            inStr = inStr.split(',')
            # 读取第一个状态集
            s = inStr[0]
            for i in range(0,len(inStr[1])):
                #ch,ns
                if len(inStr[1])==2:
                    c = inStr[1][0]
                    n = inStr[1][1]
                    list = [s,c,n]
                    self.listEdge.append(list)
                elif len(inStr[1])==1:
                    c = inStr[1][0]
                    list = [s, c, self.Z[0]]
                    self.listEdge.append(list)

    #转换函数
    def isNextState(self,s,ch):
        for i in range(0,len(self.listEdge)):
            if s == self.listEdge[i][0] and ch == self.listEdge[i][1]:
                return self.listEdge[i][2]
        return

    def judgeDFA(self):
        print("请输入要判断的字符串:")
        while(True):
            #获取字母表
            str = input()
            if '#' in str :
                print("程序已退出，欢迎下次使用!")
                return
            temp = self.S[0]
            for i in range(0,len(str)):
                if str[i] is 'a':
                    temp = self.isNextState(temp,'a')
                elif str[i] is 'b':
                    temp = self.isNextState(temp, 'b')
                else:
                    break
            if self.isZ(temp):
                print("此字符串“属于”该文法！")
            else:
                print("此字符串“不属于”该文法！")
            print("再次判断请输入字符串(退出程序输入#):")

if __name__ == '__main__':
    DFA = DFA()
    DFA.input()
    DFA.judgeDFA()