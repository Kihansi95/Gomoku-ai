from easyAI import AI_Player, Negamax, Human_Player

# run in terminal
from easyai.Gomoku import Gomoku

if __name__ == '__main__':
	ai_algo = Negamax(6)
	Gomoku(Human_Player(),
	              AI_Player(ai_algo),
	              (3,3)).play()

