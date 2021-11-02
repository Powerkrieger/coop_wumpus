from tkinter import *

def statusNull():
	print("reset")
	global boardCount
	boardCount = 0
	buttonConfig()

def forwardStep():
	global boardCount
	global boardEnt

	if boardCount+1 < boardEnt:
		boardCount = boardCount + 1
		buttonConfig()
	else:
		print("Positive IndexStop reached!")

def backwardStep():
	global boardCount
	global boardEnt

	if boardCount-1 >= 0:
		boardCount = boardCount - 1
		buttonConfig()
	else:
		print("Negative IndexStop reached!")

def buttonConfig():

	global board
	board = boards[boardCount]
	#boardX,boardY,
	#AgentX,AgentY,AgentLook-> 0=UP, 1=RIGHT, 2=DOWN, 3 = LEFT,
	#WumpusX,WumpusY,WumpusStatus -> 1=Alive, 0=Dead,
	#GoldX,GoldY,AHasGold -> 0=No, 1=Yes,
	#NumberOfPits,P1X,P1Y,...

	bx = [0] * board[0]
	global buttons
	buttons = [bx] * board[1]

	global bMap
	bMap = [ [""]*board[0] for i in range(board[1])]

	status['text'] = str(boardCount) + "." + " Zug"

	backwardB = Button(controlPanel, text="<", font=("consolas", 15), bg="#465777", command=backwardStep)
	backwardB.grid(row = 0, column = 0)
	resetB = Button(controlPanel, text="Reset", font=("consolas", 15), bg="#AC5A21", command=statusNull)
	resetB.grid(row = 0, column = 1)
	forwardB = Button(controlPanel, text=">", font=("consolas", 15), bg="#465777", command=forwardStep)
	forwardB.grid(row = 0, column = 2)

	global aLabel
	global wLabel

	if board[4] == 0:
		aLabel = "🧍⮝"
	elif board[4] == 1:
		aLabel = "🧍⮞"
	elif board[4] == 2:
		aLabel = "🧍⮟"
	elif board[4] == 3:
		aLabel = "🧍⮜"

	if board[7] == 1:
		wLabel = "👾"
	else:
		wLabel = "❌"

	if board[10] == 0:
		gLabel = "🥇"
	else:
		gLabel = ""

	for r in range(board[1]):
		for c in range(board[0]):
			#Agent
			if r == board[2] and c == board[3]:
				buttons[r][c] = Button(frame, text=aLabel, font=('consolas', 40), width=4, height=1)
				buttons[r][c].grid(row = r, column = c)
				bMap[r][c] = "A"
			
			#Wumpus
			elif r == board[5] and c == board[6]:
				buttons[r][c] = Button(frame, text=wLabel, font=('consolas', 40), width=4, height=1)
				buttons[r][c].grid(row = r, column = c)
				bMap[r][c] = "W"

			#Gold
			elif r == board[8] and c == board[9]:
				buttons[r][c] = Button(frame, text =gLabel, font=('consolas', 40), width=4, height=1)
				buttons[r][c].grid(row = r, column = c)
				bMap[r][c] = "G"
		
			#Empty
			else:
				buttons[r][c] = Button(frame, text="", font=('consolas', 40), width=4, height=1)
				buttons[r][c].grid(row = r, column = c)

	np = board[11]
	pi = 1

	#SetPits
	for i in range(np):
		px = board[11+pi]
		py = board[(11+pi+1)]

		buttons[px][py] = buttons[r][c] = Button(frame, text=pLabel, font=('consolas', 40), width=4, height=1)
		buttons[px][py].grid(row = px, column = py)
		bMap[px][py] = "P"
		pi = pi + 2

	#Breeze/Smell - Logic

	for li in range(board[1]):
		for lj in range(board[0]):
			if bMap[li][lj] == "P":
				place(breezeS, "b", li, lj)
			elif bMap[li][lj] == "W":
				place(smellS, "s", li, lj)

def place(symbol, mode, li, lj):
	#Down
	if li+1 <= board[1]-1:
		if bMap[li+1][lj] == "":
			buttons[li+1][lj] = Button(frame, text=symbol, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = mode

		elif bMap[li+1][lj] == "A":
			symb = symbol + aLabel
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			if mode == "s":
				bMap[li+1][lj] = "As"
			elif mode == "b":
				bMap[li+1][lj] = "Ab"

		elif bMap[li+1][lj] == "Ab" and mode == "s":
			symb = symbol + breezeS + aLabel
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = "Abs"
			
		elif bMap[li+1][lj] == "As" and mode == "b":
			symb = smellS + symbol + aLabel
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = "Abs"

		elif bMap[li+1][lj] == "G":
			symb = symbol + gLabel
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			if mode == "s":
				bMap[li+1][lj] = "Gs"
			elif mode == "b":
				bMap[li+1][lj] = "Gb"

		elif bMap[li+1][lj] == "Gb" and mode == "s":
			symb = symbol + breezeS + gLabel
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = "Gbs"
			
		elif bMap[li+1][lj] == "Gs" and mode == "b":
			symb = smellS + symbol + gLabel
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = "Gbs"

		elif bMap[li+1][lj] == "Gbs":
			pass

		elif bMap[li+1][lj] == "W":
			pass

		elif bMap[li+1][lj] == "P":
			pass

		elif bMap[li+1][lj] == "b" and mode == "s":
			symb = symbol + breezeS
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = "bs"

		elif bMap[li+1][lj] == "s" and mode == "b":
			symb = smellS + symbol
			buttons[li+1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li+1][lj].grid(row = li+1, column = lj)
			bMap[li+1][lj] = "bs"

		elif bMap[li+1][lj] == "bs":
			pass


	#UP
	if li-1 >= 0:
		if bMap[li-1][lj] == "":
			buttons[li-1][lj] = Button(frame, text=symbol, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = mode

		elif bMap[li-1][lj] == "A":
			symb = symbol + aLabel
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			if mode == "s":
				bMap[li-1][lj] = "As"
			elif mode == "b":
				bMap[li-1][lj] = "Ab"

		elif bMap[li-1][lj] == "Ab" and mode == "s":
			symb = symbol + breezeS + aLabel
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = "Abs"
			
		elif bMap[li-1][lj] == "As" and mode == "b":
			symb = smellS + symbol + aLabel
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = "Abs"

		elif bMap[li-1][lj] == "G":
			symb = symbol + gLabel
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			if mode == "s":
				bMap[li-1][lj] = "Gs"
			elif mode == "b":
				bMap[li-1][lj] = "Gb"

		elif bMap[li-1][lj] == "Gb" and mode == "s":
			symb = symbol + breezeS + gLabel
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = "Gbs"
			
		elif bMap[li-1][lj] == "Gs" and mode == "b":
			symb = smellS + symbol + gLabel
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = "Gbs"

		elif bMap[li-1][lj] == "Gbs":
			pass

		elif bMap[li-1][lj] == "W":
			pass

		elif bMap[li-1][lj] == "P":
			pass

		elif bMap[li-1][lj] == "b" and mode == "s":
			symb = symbol + breezeS
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = "bs"

		elif bMap[li-1][lj] == "s" and mode == "b":
			symb = smellS + symbol
			buttons[li-1][lj] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li-1][lj].grid(row = li-1, column = lj)
			bMap[li-1][lj] = "bs"

		elif bMap[li-1][lj] == "bs":
			pass


	#Right
	if lj+1 <= board[0]-1:
		if bMap[li][lj+1] == "":
			buttons[li][lj+1] = Button(frame, text=symbol, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = mode

		elif bMap[li][lj+1] == "A":
			symb = symbol + aLabel
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			if mode == "s":
				bMap[li][lj+1] = "As"
			elif mode == "b":
				bMap[li][lj+1] = "Ab"

		elif bMap[li][lj+1] == "Ab" and mode == "s":
			symb = symbol + breezeS + aLabel
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = "Abs"
			
		elif bMap[li][lj+1] == "As" and mode == "b":
			symb = smellS + symbol + aLabel
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = "Abs"

		elif bMap[li][lj+1] == "G":
			symb = symbol + gLabel
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			if mode == "s":
				bMap[li][lj+1] = "Gs"
			elif mode == "b":
				bMap[li][lj+1] = "Gb"

		elif bMap[li][lj+1] == "Gb" and mode == "s":
			symb = symbol + breezeS + gLabel
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = "Gbs"
			
		elif bMap[li][lj+1] == "Gs" and mode == "b":
			symb = smellS + symbol + gLabel
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = "Gbs"

		elif bMap[li][lj+1] == "Gbs":
			pass

		elif bMap[li][lj+1] == "W":
			pass

		elif bMap[li][lj+1] == "P":
			pass

		elif bMap[li][lj+1] == "b" and mode == "s":
			symb = symbol + breezeS
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = "bs"

		elif bMap[li][lj+1] == "s" and mode == "b":
			symb = smellS + symbol
			buttons[li][lj+1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj+1].grid(row = li, column = lj+1)
			bMap[li][lj+1] = "bs"

		elif bMap[li][lj+1] == "bs":
			pass

	#Left
	if lj-1 >= 0:
		if bMap[li][lj-1] == "":
			buttons[li][lj-1] = Button(frame, text=symbol, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = mode

		elif bMap[li][lj-1] == "A":
			symb = symbol + aLabel
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			if mode == "s":
				bMap[li][lj-1] = "As"
			elif mode == "b":
				bMap[li][lj-1] = "Ab"

		elif bMap[li][lj-1] == "Ab" and mode == "s":
			symb = symbol + breezeS + aLabel
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = "Abs"
			
		elif bMap[li][lj-1] == "As" and mode == "b":
			symb = smellS + symbol + aLabel
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = "Abs"

		elif bMap[li][lj-1] == "G":
			symb = symbol + gLabel
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			if mode == "s":
				bMap[li][lj-1] = "Gs"
			elif mode == "b":
				bMap[li][lj-1] = "Gb"

		elif bMap[li][lj-1] == "Gb" and mode == "s":
			symb = symbol + breezeS + gLabel
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = "Gbs"
			
		elif bMap[li][lj-1] == "Gs" and mode == "b":
			symb = smellS + symbol + gLabel
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = "Gbs"

		elif bMap[li][lj-1] == "Gbs":
			pass

		elif bMap[li][lj-1] == "W":
			pass

		elif bMap[li][lj-1] == "P":
			pass

		elif bMap[li][lj-1] == "b" and mode == "s":
			symb = symbol + breezeS
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = "bs"

		elif bMap[li][lj-1] == "s" and mode == "b":
			symb = smellS + symbol
			buttons[li][lj-1] = Button(frame, text=symb, font=('consolas', 40), width=4, height=1)
			buttons[li][lj-1].grid(row = li, column = lj-1)
			bMap[li][lj-1] = "bs"

		elif bMap[li][lj-1] == "bs":
			pass

#read board from file

boardFile = open("senf.txt", "r")

boardData = boardFile.readlines()
global boardEnt
boardEnt = int(boardData[0])
boardVLength = int(boardData[1])

boards = []

for bi in range(2, boardEnt + 2):

	bTemp = list(boardData[bi].rstrip())
	#bTemp.remove("\n")

	for bk in range(boardVLength):
		if bTemp[bk] == ",":
			del bTemp[bk]

	boards.append(list(map(int, bTemp)))


#--------------------
global boardCount
boardCount = 0

window = Tk()
window.title("Wumpus Vision v1.0")

pLabel = "🕳"

breezeS = "≈" 
smellS = "☁"

frame = Frame(window)
frame.pack()

controlPanel = Frame(window)
controlPanel.pack(side="top")

status = Label(text= str(boardCount) + "." + " Zug", font=("consolas", 15))
status.pack(side="top")

buttonConfig()

window.mainloop()