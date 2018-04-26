import cv2
from matplotlib import pyplot as plt
import numpy as np
import functions as fun
import chess
import chess.uci
import time


def find_move(opponent_location,current_board,color):
	change=False
	current_locations=[]
	for piece_type in range(6):
		for x in board.pieces(piece_type+1,not color):
			current_locations.append(x)
	for x in current_locations:
		if (x not in opponent_location):
			change=True
			fromsq=x
			print fromsq
			break
	if (change):
		print opponent_location

		for x in opponent_location:
			if (x not in current_locations):
				tosquare=x
		return (True, fun.number_to_square(fromsq)+fun.number_to_square(tosquare))
	else:
		return (False, "_")





colour=int(raw_input("White/Orange(0) or Black/Blue(1): "))

# def detect_moves(team,board,image):


# board_position=[]

# for x in range (64):
# 	if (x/8)<2:
# 		board_position.append('w')
# 	if (x/8)>5:
# 		board_position.append('b')

if __name__ == "__main__":
	engine=chess.uci.popen_engine("/home/austin/Downloads/komodo-9_9dd577/Linux/komodo-9.02-linux")
	engine.uci()

	while(True):
		if(colour==1): ##Player plays white
			board = chess.Board()
			while (board.result()=='*'): #Checks if game is over
				engine.position(board)
				move=engine.go(movetime=100) #Engine makes first move
				board.push_uci(str(move[0]))

				for piece_type in range(6):
					for x in board.pieces(piece_type+1,0):
						print x

				print "Computer move:", move[0],"\n"
				print board
				if(board.result()!='*'): #Check again if game is over
					break
				
				while(True):
					time.sleep(15)
					(found,move)=find_move(fun.findPieces(colour),board,colour)
					if(found):
						player_move=move
						break

				##Figure out what the move was
				print player_move
				board.push_uci(player_move)
		else:
			board = chess.Board()
			while (board.result()=='*'):

				while(True):
					time.sleep(15)
					(found,move)=find_move(fun.findPieces(colour),board,colour)
					if(found):
						player_move=move
						break

				##Figure out what the move was

				board.push_uci(player_move)
				 #Checks if game is over
				engine.position(board)
				move=engine.go(movetime=100) #Engine makes first move
				board.push_uci(str(move[0]))

				for piece_type in range(6):
					for x in board.pieces(piece_type+1,0):
						print x

				print "Computer move:", move[0],"\n"
				print board
				if(board.result()!='*'): #Check again if game is over
					break
				


				# player_move=raw_input("\nMove?")
				
				








