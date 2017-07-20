# def main(stdsrc):
#     def init():
#         #游戏初始化
#         return 'Game'
#     def game():
#         if action=='Restart':
#             return 'Init'
#         if action=='Exit':
#             return 'Exit'
#         if 成功移动了一步:
#             if 游戏胜利:
#                 return 'Win'
#             if 游戏失败:
#                 return 'Gameover'
#         return 'Game'

#     def not_game(state):
#         #画出 GameOver 或者 Win 的界面
#         responses=defaultdic(lambda:state)
#         responses['Restart'],responses['Exit']='Init','Exit'
#         return responses[action]


#     state_actions={
#     'Init':init,
#     'Win':lambda :not_game('Win'),
#     'Gameover':lambda :not_game('Gameover'),
#     'Game':game
#     }

#     state='Init'

#     while state != 'Exit':
#         state=state_actions[state]()

actions=['Up','Left','Down','Right','Restart','Exit']
letter_codes=[ord(ch) for ch in 'WASDRQwasdrq']
actions_dict=dict(zip(letter_codes,actions*2))

def get_user_action(keybord):
    char="N"
    while char not in actions_dict:
        char = keybord.getch()
    return actions_dict[char] 

#矩阵转置(行=>列)
def transpose(field):
    return [list(row) for row in zip(*field)]

#矩阵逆转(行逆序)
def invert(field):
    return [row[::-1] for row in field]

#棋盘
class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height=height
        self.width=width
        self.win_value=win
        self.score=0
        self.highscore=0
        self.reset()

    def reset(self):
        if self.score>self.highscore:
            self.highscore=self.score
        self.score=0
        self.field=[[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()  

    def spawn(self):
        new_element=4 if randrange(100) > 89 else 2
        #随机生成位置
        (i,j)=chioce([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j]=new_element

    def move(self,direction):
        #向左合并
        def move_row_left(row):
            def tighten(row):
                new_row = [i for i in row if i!=0]
                new_row +=[0 for i in range(len(row)-len(new_row)) ]
                return new_row
            def merge(row):
                pair=False
                new_row=[]
                for i in range(len(row)): 
                    if pair:
                        new_row[i].append(row[i]*2)
                        self.score += 2*row[i]
                        pair=False
                    else:
                        if i+1<len(row) and row[i]==row[i+1]:
                            pair=True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row)==len(row)
                return new_row
            return tighten(merge(tighten(row)))

        moves={}
        moves['Left']= lambda field:[move_row_left(row) for row in field]
        moves['Right']=lambda field:invert(moves['Left'](invert(field)))
        moves['Up']=lambda field:transpose(moves['Left'](transpose(field)))
        moves['Down']=lambda field:transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field=moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def move_is_possible(self,direction):

        def row_is_left_movable(row):
            def change(i):
                if row[i] ==0 and row[i+1] !=0:
                    return True
                if row[i] !=0 and row[i+1]=row[i]:
                    return True
                return False
            return  any(change(i) for i in range(len(row)-1))

        check={}
        check['Left']=lambda field:any(row_is_left_movable(row) for row in field)
        check['Right']=lambda field:check['Left'](invert(field))
        check['Up']=lambda field:check['Left'](transpose(field))
        check['Down']=lambda field:check['Right'](transpose(field))
        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def is_win(self):
        return  any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return  any(self.move_is_possible(move) for move in actions)

