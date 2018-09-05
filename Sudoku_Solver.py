from satispy import Variable, Cnf
from satispy.solver import Minisat
import numpy as np

class Empty:
	def __init__(self, i,j):
        	self.i = i
		self.j = j
		self.p = []
		self.f = Cnf()	
		self.s = Cnf()	
		for d in range(9):
			temp = 'p' + str(i) + str(j) + str(d+1)
			#print temp
			self.p.append(Variable(temp))
			#create first case -- it must be filled
			self.f |= self.p[d]
			#print type(self.p[i])
			
		
sudoku = np.zeros((9,9))
sudoku[0,0] = 0
sudoku[0,1] = 2
sudoku[1,3] = 6
sudoku[1,8] = 3
sudoku[2,1] = 7
sudoku[2,2] = 4
sudoku[2,4] = 8
sudoku[3,5] = 3
sudoku[3,8] = 2
sudoku[4,1] = 8
sudoku[4,4] = 4
sudoku[4,7] = 1
sudoku[5,0] = 6
sudoku[5,3] = 5
sudoku[6,4] = 1
sudoku[6,6] = 7
sudoku[6,7] = 8
sudoku[7,0] = 5
sudoku[7,5] = 9
sudoku[8,7] = 4
#sudoku[7,5] = 9
#sudoku[6,6] = 2
#sudoku[2,7] = 6
#sudoku[6,7] = 8
#sudoku[8,7] = 7
#sudoku[3,8] = 3
#sudoku[4,8] = 1
#sudoku[5,8] = 6
#sudoku[7,8] = 5
#sudoku[8,8] = 9




# inds hold the indexes of nonzero/zero sudoku entries
inds_nonzero= np.column_stack((np.nonzero(sudoku)[0][:],np.nonzero(sudoku)[1][:])) 
inds_zero = np.column_stack((np.where(sudoku == 0)[0][:],np.where(sudoku == 0)[1][:]))

# create a list that holds the p variables for every empty cell
var = [None]*len(inds_zero)
for i,ind in enumerate(inds_zero):
	var[i] = Empty(ind[0],ind[1])

#print inds_zero[0,0]
complete = Cnf()
#checking Sudoku entries
for i in range(9):
	empty_box = [None]*2
	
	#row i 
	second = Cnf()
	placed_d = sudoku[i,np.nonzero(sudoku[i,:])][0]
	empty_inds = np.where(inds_zero[:,0] == i )[0]
	temp = ""
	for d in range(9):
	# if d exists
		if d+1 in placed_d:
			for k in empty_inds:
				#print type(var[k].p[0])
				second &= -var[k].p[d]
				temp += "-v" + str(k) + "_" + str(d) + "  &  "
		else:
			for ik,k in enumerate(empty_inds[:-1]):
				for kk in empty_inds[ik+1:]:
					#print str(k) + "_" + str(kk)
					#print type(var[k].p[0])
					second &= -var[k].p[d] | (-var[kk].p[d])
					temp += "(-v" + str(k) + "_" + str(d) + " | -v" + str(kk) + "_" + str(d) + ")  &  "		
	
	# col i 
	third = Cnf()
	placed_d = sudoku[np.nonzero(sudoku[:,i]),i][0]
	empty_inds = np.where(inds_zero[:,1] == i )[0]
	temp = ""
	for d in range(9):
	# if d exists
		#print d
		if d+1 in placed_d:
			for k in empty_inds:
				#print type(var[k].p[0])
				third &= -var[k].p[d]
				temp += "-v" + str(k) + "_" + str(d) + "  &  "
		else:
			for ik,k in enumerate(empty_inds[:-1]):
				for kk in empty_inds[ik+1:]:
					#print str(k) + "_" + str(kk)
					#print type(var[k].p[0])
					third &= -var[k].p[d] | (-var[kk].p[d])
					temp += "(-v" + str(k) + "_" + str(d) + " | -v" + str(kk) + "_" + str(d) + ")  &  "
	# box i
	fourth = Cnf()
	xmin = ((3*i) % 9)
	ymin = (3*(i / 3))
	xmax = ((3*i) % 9) +2
	ymax = ymin + 2
	l1 = np.nonzero(sudoku[xmin:xmax+1,ymin:ymax+1])[0]
	l2 = np.nonzero(sudoku[xmin:xmax+1,ymin:ymax+1])[1]
	placed_d = sudoku[l1+xmin,l2+ymin]
	#print i,l1 + xmin,l2 +ymin
	# ta empty inds tou box	
	empty_inds = np.where(np.logical_and(np.logical_and(inds_zero[:,1] >= ymin, inds_zero[:,1] <= ymax),np.logical_and(inds_zero[:,0] >= xmin, inds_zero[:,0] <= xmax)) )[0]
	#print empty_inds
	temp = ""
	for d in range(9):
		if d+1 in placed_d:
			for k in empty_inds:
				#print type(var[k].p[0])
				fourth &= -var[k].p[d]
				temp += "-v" + str(k) + "_" + str(d) + "  &  "
		else:
			for ik,k in enumerate(empty_inds[:-1]):
				for kk in empty_inds[ik+1:]:
					#print str(k) + "_" + str(kk)
					#print type(var[k].p[0])
					fourth &= -var[k].p[d] | (-var[kk].p[d])
					temp += "(-v" + str(k) + "_" + str(d) + " | -v" + str(kk) + "_" + str(d) + ")  &  "
		
	
	complete &= second & third & fourth
	#complete &= third  


for i,cell in enumerate(var):
	complete &= cell.f







#exp = ( v1 | -v3) & (v2 & v3) 




solver = Minisat()




solution = solver.solve(complete)



if solution.success:
    print "Found a solution:"
    for j,var in enumerate(var):	
    	for i in range(9):
		if solution[var.p[i]] == True:
			#print "(" + str(var.i+1) + "," + str(var.j+1) + ")  ==>  " + str(i+1) 
			sudoku[var.i,var.j]= i+1
    #print v2, solution[v2]
    #print v3, solution[v3]
    print sudoku
else:
    print "The expression cannot be satisfied"
