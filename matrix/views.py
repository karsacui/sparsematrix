from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import numberForm
import copy


import numpy as np
import fractions

# start of sparsecli
class spartrix:
	smlist = []
	height = 0
	length = 0

	def __init__(self, matrix=[], height=0, length=0):
		# self.smlist.append([len(matrix),len(matrix[0]),0])
		# 判断列表是否为空
		self.smlist = []
		if matrix == []:
			self.height = height
			self.length = length
		# 如果给的矩阵不为空则按照矩阵来初始化
		else:
			self.height = len(matrix)
			self.length = len(matrix[0])
			for i in range(len(matrix)):
				for j in range(len(matrix[i])):
					if (matrix[i][j]) != 0:
						self.smlist.append([i, j, matrix[i][j]])
				# self.smlist[0][2] += 1
				# self.row.append(i)
				# self.col.append(j)
				# self.data.append(matrix[i][j])

	def __str__(self):
		return f"height={self.height}, length={self.length}, {self.smlist}"

	# 拷贝方法
	def copy(self):
		copied = copy.deepcopy(self)
		copied.smlist = copy.deepcopy(self.smlist)
		return copied

	# 单目运算符取反"-"重载
	def __neg__(self):
		output = self.copy()
		a = 0
		while a < len(output.smlist):
			output.smlist[a][2] = -output.smlist[a][2]
			# print(output.smlist[a][2])
			a += 1
		return output

	# 双目运算符 “+” 重载
	def __add__(self, other):
		if other.length == self.length and other.height == self.height:
			sumtrix = spartrix(height=self.height, length=self.length)
			a = 0
			b = 0
			while a < len(self.smlist) and b < len(other.smlist):
				if self.smlist[a][0] == other.smlist[b][0] and self.smlist[a][1] == other.smlist[b][1]:
					sumtrix.smlist.append(
						[self.smlist[a][0], self.smlist[a][1], self.smlist[a][2] + other.smlist[b][2]])
					a += 1
					b += 1
				elif self.smlist[a][0] < other.smlist[b][0] or (
						self.smlist[a][0] == other.smlist[b][0] and self.smlist[a][1] < other.smlist[b][1]):
					sumtrix.smlist.append([self.smlist[a][0], self.smlist[a][1], self.smlist[a][2]])
					a += 1
				elif self.smlist[a][0] > other.smlist[b][0] or (
						self.smlist[a][0] == other.smlist[b][0] and self.smlist[a][1] > other.smlist[b][1]):
					sumtrix.smlist.append([other.smlist[b][0], other.smlist[b][1], other.smlist[b][2]])
					b += 1
			while a < len(self.smlist):
				sumtrix.smlist.append([self.smlist[a][0], self.smlist[a][1], self.smlist[a][2]])
				a += 1
			while b < len(other.smlist):
				sumtrix.smlist.append([other.smlist[b][0], other.smlist[b][1], other.smlist[b][2]])
				b += 1
			return sumtrix

	# 双目运算符"-"重载，直接先对减数取反然后与被减数相加
	def __sub__(self, other):
		return self + (-other)

	def trans(self):
		for i in self.smlist:
			i[1], i[0] = i[0], i[1]
		res = spartrix()
		res.length, res.height, res.smlist = self.height, self.length, sorted(self.smlist,
																			  key=lambda x: x[0] * self.length + x[1])
		return res

	def __mul__(self, other):
		if self.length != other.height:
			print("Multipy not applicable")
			return
		l = self.length
		m1 = self.decompress()
		m2 = other.decompress()
		mout = [[0 for i in range(other.length)] for i in range(self.height)]
		for i in range(self.height):
			for j in range(other.length):
				mout[i][j] = 0
				for a in range(l):
					mout[i][j] += m1[i][a] * m2[a][j]
		return spartrix(matrix=mout)

	# 展开
	def decompress(self):
		row = []
		trix = [[0 for k in range(self.length)] for k in range(self.height)]
		# for k in range(self.length):
		#     row.append(0)
		# for k in range(self.height):
		#     trix.append(row[:])

		for tup in self.smlist:
			trix[tup[0]][tup[1]] = tup[2]

		return trix
# end of sparsecli




np.set_printoptions(formatter={'all':lambda x: str(fractions.Fraction(x).limit_denominator())})

page_name = 'Matrix Calculator '
section = ''



def get_digits(request):

	if request.method == 'POST':
		form = numberForm(request.POST)


		if form.is_valid():

			try:
				numbers = form.cleaned_data['numbers']
				m = form.cleaned_data['rows']
				n = form.cleaned_data['cols']
				print(numbers)

				print(m,n)
				trix = [[numbers[i*n+v] for v in range(n)] for i in range(m)]
				print(trix)

				orism = spartrix(matrix=trix)
				outsm = orism.trans()
				outrix = outsm.decompress()

				nbs =[]
				for ro in outrix:
					for i in ro:
						nbs.append(i)
				print(nbs)





				num_array = list(numbers)


				A = np.matrix(num_array)
				A = A.reshape(int(m),int(n))

				#Calculate projection matrix step by step, plan to add show-work feature.
				At = A.getT()
				# AtA = np.matmul(At,A)
				# AtAi = AtA.getI()
				# AAtAI = np.matmul(A, AtAi)
				# AAtAIAt = np.matmul(AAtAI, At)

				#Matrix specifications

				#P = AAtAIAt
				P = At
				P_rows = P.shape[0]
				P_cols = outsm.length
				print("P_cols")
				print(P_cols)
				# P_cols = P.shape[1]


				#Parallel arrays hold numerator and denominators
				P_list = [None]*(P_rows * P_cols)
				P_numr = [None]*(P_rows * P_cols)
				P_dnmr = [None]*(P_rows * P_cols)

				counter = 0
				for i in range(P_rows):
					for j in range(P_cols):
						P_list[counter] = (fractions.Fraction(P[i,j]).limit_denominator())
						P_numr[counter] = P_list[counter].numerator
						P_dnmr[counter] = P_list[counter].denominator
						counter += 1
				P_list = None

				# #Zip arrays for template rendering
				# P_zip = zip(P_numr, P_dnmr)


				#Valid output response
				valid_output = True
				return render(request, 'matrix/orthproj_output.html', {
				'nbs': nbs,
				#'P_rows': P_rows,
				'P_cols': P_cols,
				#'P_numr': P_numr,
				#'P_dnmr': P_dnmr,
				#'P_zip': P_zip,
				#'table': P,
				'page_name': page_name,
				'section': section,
				'valid_output': valid_output,
				})

			#Invalid output response: something went wrong within the calculation
			except:

				# out = ' Perhaps your matrix rows are linearly dependent?'
				out = ' Something wrong?'
				valid_output = False
				return render(request, 'matrix/orthproj_output.html', {
				'page_name': page_name,
				'section': section,
				'out': out,
				'valid_output': valid_output,
				})
		#Invalid output: something went wrong before the calculation
		else:
			valid_output = False
			out = ' Check your matrix input values.'

			return render(request, 'matrix/orthproj_output.html', {
				'page_name': page_name,
				'section': section,
				'out': out,
				'valid_output': valid_output,
				})

	#Render form
	else:
		form = numberForm()

		return render(request, 'matrix/orthproj.html', {
		'page_name': page_name,
		'section': section,
		'form': form,





		})
