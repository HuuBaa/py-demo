def main(stdsrc):
    def init():
        #游戏初始化
        return 'Game'
    def game():
        if action=='Restart':
            return 'Init'
        if action=='Exit':
            return 'Exit'
        if 成功移动了一步:
            if 游戏胜利:
                return 'Win'
            if 游戏失败:
                return 'Gameover'
        return 'Game'

    def not_game(state):
        #画出 GameOver 或者 Win 的界面
        responses=defaultdic(lambda:state)
        responses['Restart'],responses['Exit']='Init','Exit'
        return responses[action]


    state_actions={
    'Init':init,
    'Win':lambda :not_game('Win'),
    'Gameover':lambda :not_game('Gameover'),
    'Game':game
    }

    state='Init'

    while state != 'Exit':
        state=state_actions[state]()