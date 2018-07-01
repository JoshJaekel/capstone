import cv2
from matplotlib import pyplot as plt
import numpy as np
import functions as fun
import chess
import chess.uci
import time


def find_move(opponent_location,current_board,color):
	change=False
	from_square_found=False
	to_square_found=False
	current_locations=[]
	for piece_type in range(6):
		for x in board.pieces(piece_type+1,not color):
			current_locations.append(x)
	for x in current_locations:
		if (x not in opponent_location):
			change=True

			if from_square_found:
				if ((((fromsq==0 and x== 4) or (fromsq==4 and (x==0 or x==7)) or (fromsq==7 and x==4)) and (color==0)) or ((color==1) and ((fromsq==56 and x==60) or (fromsq==60 and (x==56 or x==63)) or (fromsq==63 and x==60)))):
					break
				else:
					return (False,"_")

			else:
				#print(x)
				fromsq=x
				move_found=True
				from_square_found=True

	if (change):


		for x in opponent_location:
			if (x not in current_locations):
				tosq=x
				if (to_square_found):
					if (((colour==0) and ((tosq==1 and x==2) or (tosq==2 and x==1)) or (tosq==5 and x==6) or (tosq==6 and x==5)) or ((colour==1) and ((tosq==57 and x==58) or (tosq==58 and x==57) or (tosq==61 and x== 62) or (tosq==62 and x==63)))):
						break
					else:
						return (False, "_")
				else:
					to_square_found=True

		return (True, fun.number_to_square(fromsq)+fun.number_to_square(tosq))
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
counter=0

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



				print "Computer move:", move[0],"\n"
				print board
				if(board.result()!='*'): #Check again if game is over
					break
				
				while(True):
					# time.sleep(15)
					try:
						opp_loc=fun.findPieces(colour)
						(found,move)=find_move(opp_loc,board,colour)
					except Exception as excpt:
						#print excpt
						found=False
					if(found):
						player_move=move
						break

				##Figure out what the move was
				print "Player move:", player_move,"\n"
				board.push_uci(player_move)
		else:
			board = chess.Board()
			while (board.result()=='*'):

				while(True):
					try:
						opp_loc=fun.findPieces(colour)
						(found,move)=find_move(opp_loc,board,colour)
					except Exception as excpt:
						#print excpt
						found=False
					if(found):
						player_move=move
						break

				##Figure out what the move was
				print "Player move:", player_move,"\n"
				board.push_uci(player_move)
				 #Checks if game is over
				engine.position(board)
				move=engine.go(movetime=100) #Engine makes first move
				board.push_uci(str(move[0]))


				print "Computer move:", move[0],"\n"
				print board
				if(board.result()!='*'): #Check again if game is over
					break
				


# player_move=raw_input("\nMove?")
