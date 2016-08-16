import numpy as np
from scipy.sparse import csr_matrix
import math as mt
import csv
from sparsesvd import sparsesvd
from scipy.sparse.linalg import * #used for matrix multiplication


# read the dataset
#constants defining the dimensions of our User Rating Matrix (URM)
MAX_PID = 37143
MAX_UID = 15375

def readUrm():
	urm = np.zeros(shape=(MAX_UID,MAX_PID), dtype=np.float32)
	with open('/PathToTrainFile.csv', 'rb') as trainFile:
		urmReader = csv.reader(trainFile, delimiter=',')
		for row in urmReader:
			urm[int(row[0]), int(row[1])] = float(row[2])
	return csr_matrix(urm, dtype=np.float32)

# retrieve the test users
def readUsersTest():
	uTest = dict()
	with open("./testSample.csv", 'rb') as testFile:
		testReader = csv.reader(testFile, delimiter=',')
		for row in testReader:
			uTest[int(row[0])] = list()
	return uTest

def getMoviesSeen():
	moviesSeen = dict()
	with open("./trainSample.csv", 'rb') as trainFile:
		urmReader = csv.reader(trainFile, delimiter=',')
		for row in urmReader:
			try:
				moviesSeen[int(row[0])].append(int(row[1]))
			except:
				moviesSeen[int(row[0])] = list()
				moviesSeen[int(row[0])].append(int(row[1]))
	return moviesSeen

# compute the svd of our user matrix
def computeSVD(urm, K):
	U, s, Vt = sparsesvd(urm, K)

	dim = (len(s), len(s))
	S = np.zeros(dim, dtype=np.float32)
	for i in range(0, len(s)):
		S[i,i] = mt.sqrt(s[i])

	U = csr_matrix(np.transpose(U), dtype=np.float32)
	S = csr_matrix(S, dtype=np.float32)
	Vt = csr_matrix(Vt, dtype=np.float32)
	return U, S, Vt

# predict the movies for our test users
def computeEstimatedRatings(urm, U, S, Vt, uTest, moviesSeen, K, test):
	rightTerm = S*Vt

	estimatedRatings = np.zeros(shape=(MAX_UID, MAX_PID), dtype=np.float16)
	for userTest in uTest:
		prod = U[userTest, :]*rightTerm

		#we convert the vector to dense format in order to get the indices of the movies with the best estimated ratings
		estimatedRatings[userTest, :] = prod.todense()
		recom = (-estimatedRatings[userTest, :]).argsort()[:250]
		for r in recom:
			if r not in moviesSeen[userTest]:
				uTest[userTest].append(r)

				if len(uTest[userTest]) == 5:
					break
	return uTest

# main of program
def main():
	K = 90
	urm = readUrm()
	U, S, Vt = computeSVD(urm, K)
	uTest = readUsersTest()
	moviesSeen = getMoviesSeen()
	uTest = computeEstimatedRatings(urm, U, S, Vt, uTest, moviesSeen, K, True)

if __name__=='__main__':
	main()
