from easyAI import TwoPlayerGame
import numpy as np
from scipy.ndimage import convolve


class Gomoku(TwoPlayerGame):
	
	def __init__(self, player1, player2, board_dim: tuple = (9, 9)):
		
		assert len(board_dim) == 2, f"2 dimensions for board dim (width, height). Actual: board_dim={board_dim}"
		assert 0 < board_dim[0] and 0 < board_dim[1], f"Positive dimension. Actual: board_dim={board_dim}"
		
		self.players = [player1, player2]
		self.nplayer = 1 # Player 1 go first
		self.board = np.array([[0 for i in range(board_dim[0])] for j in range(board_dim[1])])
		self.is_win = GomokuWinDetector()
	
	def possible_moves(self):
		"""
		return a list of couple (x,y) as possible move
		"""
		x, y = np.where(self.board == 0)
		return list(zip(x,y))
	
	def make_move(self, move):
		x, y = move
		self.board[x, y] = -2 * self.current_player + 3 # -2x+3 map (1,2) -> (1,-1)
	
	def is_over(self):
		return self.is_win(self.board)
	
	def show(self):
		if hasattr(self, 'current_player'):
			print(f'Player {self.current_player}\'s turn')
		print(self.board)
	
	def unmake_move(self, move):
		"""
		How to unmake a move. Help speed up the AI.
		"""
		self.board[int(move)-1] = 0
	
	def scoring(self):
		return 100 if self.is_win(self.board) else 0
	
	
class GomokuWinDetector:
	def __init__(self):
		kernels = dict()
		kernels['5_horizontal'] = np.array([[0]*5, [0]*5, [1/5]*5, [0]*5, [0]*5])
		kernels['5_vertical'] = kernels['5_horizontal'].transpose()
		kernels['5_diagonal_l'] = np.eye(5)/5
		kernels['5_diagonal_r'] = kernels['5_diagonal_l'][:,::-1] # flip the previous diagonal
		self.kernels = kernels
	
		
	def __call__(self, board):
		"""
		Detect if a pattern of winning is found
		"""
		kernels = self.kernels
		
		# If activated by any of the kernel == win
		return any([convolve(board, k, mode='constant', cval=0).sum() for k in kernels])
	