import cv2
from matplotlib import pyplot as plt
import numpy as np
import functions as fun
import chess
import chess.uci
import time
import serial

ser = serial.Serial('/dev/ttyACM1', 9600)
castle_check=True
partial_castle=False


row_dict_lower_0={'a':390,'b':412,'c':432,'d':451,'e':470,'f':491,'g':511,'h':529,'A':390,'B':412,'C':432,'D':451,'e':470,'F':491,'G':511,'H':529}
row_dict_higher_0={'a':390,'b':409,'c':430,'d':450,'e':469,'f':490,'g':511,'h':530,'A':390,'B':409,'C':430,'D':450,'E':469,'F':490,'G':511,'H':530}
column_dict_lower_0={'1':356,'2':382,'3':404,'4':425,'5':445,'6':467,'7':487,'8':508,'x':575}
column_dict_higher_0={'1':356,'2':376,'3':398,'4':418,'5':438,'6':459,'7':481,'8':502,'x':575}

row_dict_lower_1={'h':390,'g':412,'f':432,'e':451,'d':470,'c':491,'b':511,'a':529,'H':390,'G':412,'F':432,'E':451,'D':470,'C':491,'B':511,'A':529}
row_dict_higher_1={'h':390,'g':409,'f':430,'e':450,'d':469,'c':490,'b':511,'a':530,'H':390,'G':409,'F':430,'E':450,'D':469,'C':490,'B':511,'A':530}
column_dict_lower_1={'8':356,'7':382,'6':404,'5':425,'4':445,'3':467,'2':487,'1':508,'x':575}
column_dict_higher_1={'8':356,'7':376,'6':398,'5':418,'4':438,'3':459,'2':481,'1':502,'x':575}

def find_move(opponent_location,current_board,color):
	time.sleep(1)
	global castle_check, partial_castle
	change=False
	from_square_found=False
	to_square_found=False
	partial_castle=False
	current_locations=[]
	

	for piece_type in range(6):
		for x in board.pieces(piece_type+1,not color):
			current_locations.append(x)

	for x in current_locations:
		if (x not in opponent_location):
			change=True

			if from_square_found:
				if ((((fromsq==0 and x== 4) or (fromsq==4 and (x==0 or x==7)) or (fromsq==7 and x==4))) and (color==0)):
					fromsq=4
					partial_castle=True
					break
				elif (((color==1) and ((fromsq==56 and x==60) or (fromsq==60 and (x==56 or x==63)) or (fromsq==63 and x==60)))):
					fromsq=60
					partial_castle=True
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
				
				if (to_square_found):
					if ((colour==0) and ((tosq==3 and x==2) or (tosq==2 and x==3))):
						partial_castle=False
						tosq=2
						break

					elif (((tosq==5 and x==6) or (tosq==6 and x==5)) and (colour==0)):
						tosq=6
						partial_castle=False
						break

					elif ((colour==1) and ((tosq==59 and x==58) or (tosq==58 and x==59))):
						tosq=58
						partial_castle=False
						break

					elif (((tosq==61 and x== 62) or (tosq==62 and x==61)) and (colour==1)):
						tosq=62
						partial_castle=False
						break
					
					else:
						return (False, "_")
				else:
					to_square_found=True
					tosq=x

		if (castle_check and (((colour==0) and (fun.number_to_square(fromsq)+fun.number_to_square(tosq)=="h1f1" or fun.number_to_square(fromsq)+fun.number_to_square(tosq)=="a1d1")) or ((colour==1) and (fun.number_to_square(fromsq)+fun.number_to_square(tosq)=="a8d8" or fun.number_to_square(fromsq)+fun.number_to_square(tosq)=="h8f8")))):
			print "found rook move"
			time.sleep(5)
			print "checking again"
			castle_check=False
			return (False, "_")


		castle_check=True

		if (not partial_castle):
			return (True, fun.number_to_square(fromsq)+fun.number_to_square(tosq))
		else:
			return (False,"_")
	else:
		return (False, "_")

def send_move(move,board,team):
	##type 0: normal move
	##type 1: capture
	##type 2: castle
	##type 3: promotion
	##type 4: en-passant
	if (board.is_capture(move[0])):
		move_type=1
	elif(board.is_castling(move[0])):
		move_type=2
	elif(board.is_en_passant(move[0])):
		move_type=3
	else:
		move_type=0
	
	while True:
		message = ser.readline()
		if (message[0:10]=='move_ready'):
			break
	

	##print len(message)


	user_in=str(move[0])
	if (team==0):
		if (move_type==0):

			move1=row_dict_lower_0[user_in[0]]+1000*column_dict_higher_0[user_in[1]]+move_type*1000000
			
			if (int(user_in[1])>int(user_in[3])):
				column2=column_dict_higher_0[user_in[3]]
			elif(int(user_in[1])<int(user_in[3])):
				column2=column_dict_lower_0[user_in[3]]
			else:
				column2=column_dict_higher_0[user_in[1]]
			
			if (row_dict_lower_0[user_in[0]]<row_dict_lower_0[user_in[2]]):
				row2=row_dict_lower_0[user_in[2]]
			elif(row_dict_lower_0[user_in[0]]>row_dict_lower_0[user_in[2]]):
				row2=row_dict_higher_0[user_in[2]]
			else:
				row2=row_dict_lower_0[user_in[0]]
			move2=row2+1000*column2
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))

		elif (move_type==1):

			move1=row_dict_lower_0[user_in[0]]+1000*column_dict_higher_0[user_in[1]]+move_type*1000000
			column2=column_dict_higher_0[user_in[3]]
			row2=row_dict_lower_0[user_in[2]]
			move2=row2+1000*column2

			if (int(user_in[1])>int(user_in[3])):
				column3=column_dict_higher_0[user_in[3]]
			elif(int(user_in[1])<int(user_in[3])):
				column3=column_dict_lower_0[user_in[3]]
			else:
				column3=column_dict_higher_0[user_in[1]]
			
			if (row_dict_lower_0[user_in[0]]<row_dict_lower_0[user_in[2]]):
				row3=row_dict_lower_0[user_in[2]]
			elif(row_dict_lower_0[user_in[0]]>row_dict_lower_0[user_in[2]]):
				row3=row_dict_higher_0[user_in[2]]
			else:
				row3=row_dict_lower_0[user_in[0]]
			move3=row3+1000*column3
			
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))
			_=ser.readline()
			ser.write(str(move3))

		elif(move_type==2):
			move1=row_dict_lower_0[user_in[0]]+1000*column_dict_higher_0[user_in[1]]+move_type*1000000
			column2=column_dict_higher_0[user_in[3]]

			if (board.is_queenside_castling(move[0])):
				move3=row_dict_higher_0['a']+1000*column2
				move4=row_dict_lower_0['d']+1000*column2
				row2=row_dict_higher_0[user_in[2]]
				move2=row2+1000*column2
			else:
				move3=row_dict_lower_0['h']+1000*column2
				move4=row_dict_higher_0['f']+1000*column2
				row2=row_dict_lower_0[user_in[2]]
				move2=row2+1000*column2

			
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))
			_=ser.readline()
			ser.write(str(move3))
			_=ser.readline()
			ser.write(str(move4))

		elif(move_type==3):
			move1=row_dict_lower_0[user_in[0]]+1000*column_dict_higher_0[user_in[1]]+move_type*1000000
			move2=row_dict_lower_0[user_in[2]]+1000*column_dict_higher_0[user_in[1]]

			if (int(user_in[1])>int(user_in[3])):
				column3=column_dict_higher_0[user_in[3]]
			elif(int(user_in[1])<int(user_in[3])):
				column3=column_dict_lower_0[user_in[3]]
			else:
				column3=column_dict_higher_0[user_in[1]]
			
			if (row_dict_lower_0[user_in[0]]<row_dict_lower_0[user_in[2]]):
				row3=row_dict_lower_0[user_in[2]]
			elif(row_dict_lower_0[user_in[0]]>row_dict_lower_0[user_in[2]]):
				row3=row_dict_higher_0[user_in[2]]
			else:
				row3=row_dict_lower_0[user_in[0]]
			move3=row3+1000*column3
			
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))
			_=ser.readline()
			ser.write(str(move3))

	
	elif(team==1):
		if (move_type==0):

			move1=row_dict_lower_1[user_in[0]]+1000*column_dict_higher_1[user_in[1]]+move_type*1000000
			
			if (int(user_in[1])<int(user_in[3])):
				column2=column_dict_higher_1[user_in[3]]
			elif(int(user_in[1])>int(user_in[3])):
				column2=column_dict_lower_1[user_in[3]]
			else:
				column2=column_dict_higher_1[user_in[1]]
			
			if (row_dict_lower_1[user_in[0]]<row_dict_lower_1[user_in[2]]):
				row2=row_dict_lower_1[user_in[2]]
			elif(row_dict_lower_1[user_in[0]]>row_dict_lower_1[user_in[2]]):
				row2=row_dict_higher_1[user_in[2]]
			else:
				row2=row_dict_lower_1[user_in[0]]
			move2=row2+1000*column2
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))

		elif (move_type==1):

			move1=row_dict_lower_1[user_in[0]]+1000*column_dict_higher_1[user_in[1]]+move_type*1000000
			column2=column_dict_higher_1[user_in[3]]
			row2=row_dict_lower_1[user_in[2]]
			move2=row2+1000*column2

			if (int(user_in[1])<int(user_in[3])):
				column3=column_dict_higher_1[user_in[3]]
			elif(int(user_in[1])>int(user_in[3])):
				column3=column_dict_lower_1[user_in[3]]
			else:
				column3=column_dict_higher_1[user_in[1]]
			
			if (row_dict_lower_1[user_in[0]]<row_dict_lower_1[user_in[2]]):
				row3=row_dict_lower_1[user_in[2]]
			elif(row_dict_lower_1[user_in[0]]>row_dict_lower_1[user_in[2]]):
				row3=row_dict_higher_1[user_in[2]]
			else:
				row3=row_dict_lower_1[user_in[0]]
			move3=row3+1000*column3
			
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))
			_=ser.readline()
			ser.write(str(move3))

		elif (move_type==2):

			move1=row_dict_lower_1[user_in[0]]+1000*column_dict_higher_1[user_in[1]]+move_type*1000000
			column2=column_dict_higher_1[user_in[3]]


			if (board.is_queenside_castling(move[0])):
				move3=row_dict_lower_1['a']+1000*column2
				move4=row_dict_higher_1['d']+1000*column2
				row2=row_dict_lower_1[user_in[2]]
				move2=row2+1000*column2
			else:
				move3=row_dict_higher_1['h']+1000*column2
				move4=row_dict_lower_1['f']+1000*column2
				row2=row_dict_higher_1[user_in[2]]
				move2=row2+1000*column2

			
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))
			_=ser.readline()
			ser.write(str(move3))
			_=ser.readline()
			ser.write(str(move4))

		elif (move_type==3):

			move1=row_dict_lower_1[user_in[0]]+1000*column_dict_higher_1[user_in[1]]+move_type*1000000
			move2=row_dict_lower_1[user_in[2]]+1000*column_dict_higher_1[user_in[1]]

			if (int(user_in[1])<int(user_in[3])):
				column3=column_dict_higher_1[user_in[3]]
			elif(int(user_in[1])>int(user_in[3])):
				column3=column_dict_lower_1[user_in[3]]
			else:
				column3=column_dict_higher_1[user_in[1]]
			
			if (row_dict_lower_1[user_in[0]]<row_dict_lower_1[user_in[2]]):
				row3=row_dict_lower_1[user_in[2]]
			elif(row_dict_lower_1[user_in[0]]>row_dict_lower_1[user_in[2]]):
				row3=row_dict_higher_1[user_in[2]]
			else:
				row3=row_dict_lower_1[user_in[0]]
			move3=row3+1000*column3
			
			ser.write(str(move1))
			_=ser.readline()
			ser.write(str(move2))
			_=ser.readline()
			ser.write(str(move3))







	
	while True:
		message = ser.readline()
		if (message[0:4]=='done'):
			break


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
		if(colour==1): ##Player plays black
			board = chess.Board()
			while (board.result()=='*'): #Checks if game is over
				engine.position(board)
				move=engine.go(movetime=100) #Engine makes first move
				send_move(move,board,colour)
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
						# print excpt
						found=False
					if(found):
						if (board.is_legal(chess.Move(fun.square_to_num(move[0:2]),fun.square_to_num(move[2:4])))):
							player_move=move
							break
						else:
							print "Detected illegal move: ", move

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
						# print excpt
						found=False
					if(found):
						if (board.is_legal(chess.Move(fun.square_to_num(move[0:2]),fun.square_to_num(move[2:4])))):
							player_move=move
							break
						else:
							print "Detected illegal move: ", move

				##Figure out what the move was
				
				print "Player move:", player_move,"\n"
				board.push_uci(player_move)
				engine.position(board)
				move=engine.go(movetime=100) #Engine makes first move
				send_move(move,board,colour)
				board.push_uci(str(move[0]))


				print "Computer move:", move[0],"\n"
				print board
				if(board.result()!='*'): #Check again if game is over
					break

				 #Checks if game is over

				
		break


# player_move=raw_input("\nMove?")
