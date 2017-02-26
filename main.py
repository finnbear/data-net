# -*- coding: utf-8 -*-

'''
© 2017 Finn Bear All Rights Reserved
'''

import time
import random

def generate(minLength, maxLength):
	length = random.randint(minLength, maxLength)
	index = 0
	code = []

	for i in range(length):
		code.append(random.randint(0, 12))

	return code

def mutate(code, numMutations):
	for i in range(numMutations):
		type = random.random

		if type < 0.5:
			code[random.randint(0, len(code) - 1)] = random.randint(0, 12)
		elif type < 0.7:
			code.insert(random.randint(0, len(code)), random.randint(0, 12))
		else:
			if len(code) >= 2:
				code.remove(code[random.randint(0, len(code) - 1)])

	return code

def execute(code, matSize, maxTime):
	running = True
	pc = 0;
	ptrX = 0;
	ptrY = 0;
	mat = [[0 for x in range(matSize)] for y in range(matSize)]
	acc = 0;

	t0 = time.time()

	while (running and (ptrX >= 0 or ptrY >= 0) and pc < len(code)):
		inst = code[pc]

		if inst == 0:
			pc = 0
		elif inst == 1:
			pc += 1
		elif inst == 2:
			ptrX = 0
		elif inst == 3:
			ptrX += 1
			if ptrX >= matSize:
				ptrX = matSize - 1
		elif inst == 4:
			ptrY = 0
		elif inst == 5:
			ptrY += 1
			if ptrY >= matSize:
				ptrY = matSize - 1
		elif inst == 6:
			mat[ptrX][ptrY] = 0
		elif inst == 7:
			mat[ptrX][ptrY] += 1
		elif inst == 8:
			acc = 0
		elif inst == 9:
			acc = mat[ptrX][ptrY]
		elif inst == 10:
			mat[ptrX][ptrY] = acc
		elif inst == 11:
			acc += 1
		elif inst == 12:
			running = False

		if time.time() > t0 + maxTime:
			running = False

		pc += 1

	return mat

def printMat(mat):
	for y in range(len(mat)):
		line = ""
		for x in range(len(mat)):
			if mat[x][y] > 0:
				line += str(mat[x][y])
				line += " "
			else:
				line += "_ "
		print(line)

def scoreMat(mat):
	score = 0

	for x in range(len(mat)):
		for y in range(len(mat)):
			if not mat[x][y] == 0:
				score += 1

	return float(score) / (len(mat) * len(mat))

numCodes = 100
codes = []

for i in range(0, numCodes):
	codes.append(generate(25, 50))

while True:
	mats = []
	for i in range(0, numCodes):
		mats.append(execute(codes[i], 10, 0.001))

	scores = []
	for i in range(0, numCodes):
		scores.append(scoreMat(mats[i]))

	for i in range(0, numCodes):
		if scores[i] == 0:
			codes[i] = generate(25, 50)

	best = codes[scores.index(max(scores))]

	printMat(mats[scores.index(max(scores))])

	for i in range(0, numCodes / 5):
		codes[random.randint(0, numCodes -  1)] = mutate(best, random.randint(0, 3))

	for i in range(0, numCodes / 10):
		codes[random.randint(0, numCodes - 1)] = mutate(codes[random.randint(0, numCodes - 1)], random.randint(0, 2))

	print str(sum(scores) / len(scores))

printMat(mat)
print(str(scoreMat(mat)))