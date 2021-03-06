import numpy as n
import matplotlib.pyplot as plt
from matplotlib import gridspec
import argparse

def randomB(N):
	B = n.random.random_sample(size = (N, N))
	# print B
	return (B + B.T)/2


class MMSB():
	def __init__(self, K, N, alpha = None, B = None, rho = 0.):
		#K = number of groups
		#N = number of items
		self._K = K
		self._N = N
		self._rho = rho #sparsity parameter
		if alpha != None:
			self._alpha = n.repeat(alpha, self._K)
		else:
			self._alpha = n.random.random_sample(self._K)

		self._pi = n.zeros((self._N, self._K))

		if B != None:
			self._B = B
		else:
			self._B = randomB(self._K)

		self._model = n.zeros((N, N))

	def drawMemberships(self):
		self._pi = n.random.dirichlet(self._alpha, size = (self._N))
		self._pi = n.vstack(sorted(self._pi, key=n.argmax))
		# print n.sum(self._pi, axis = 1)
		# print n.sum(self._pi, axis = 0)

	def sampleInteractions(self):
		for i in range(self._N):
			for j in range(self._N):
				initiator = n.random.multinomial(1, self._pi[i])
				# print initiator
				receiver = n.random.multinomial(1, self._pi[j])
				# print receiver
				self._model[i, j] = n.random.binomial(1, (1-self._rho)*n.dot(n.dot(initiator.T, self._B), receiver))
		# print self._model

	def display(self):
		fig = plt.figure()
		gs = gridspec.GridSpec(2, 4)
		ax1 = plt.subplot(gs[1, 0])
		ax2 = plt.subplot(gs[:, 1:3])	
		ax3 = plt.subplot(gs[:, 3])	
		ax4 = plt.subplot(gs[0, 0])
		ax1.set_title('Random B')
		ax2.set_title('Generated Graph of Interactions,\n black is interaction')
		ax3.set_title('Generated Membership Vectors')
		ax4.set_title('Random Alpha')
		ax1.imshow(self._B, interpolation = 'nearest', cmap ="Greys")
		ax2.imshow(self._model, interpolation='nearest', cmap="Greys")
		ax3.imshow(self._pi, interpolation='nearest', cmap = 'OrRd')
		ax4.bar(n.arange(self._K), self._alpha, color = "black")
		plt.show()

def test():
	testmodel = MMSB(3, 15)
	testmodel.drawMemberships()
	testmodel.sampleInteractions()
	testmodel.display()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-K','--groups', help='number of groups',required=True)
	parser.add_argument('-N','--items', help='number of items/people',required=True)
	parser.add_argument('-a','--alpha', help='alpha', default = None, required=False)
	parser.add_argument('-r','--rho', help='rho, sparsity parameter', default = 0., required=False)

	args = parser.parse_args()


	K = int(args.groups)
	N = int(args.items)
	alpha = args.alpha
	if alpha != None:
		alpha = float(alpha)
	rho = float(args.rho)
	assert rho >= 0 and rho <= 1, "invalid rho, must be [0, 1]"
	model = MMSB(K, N, alpha = alpha, rho = rho)
	model.drawMemberships()
	model.sampleInteractions()
	model.display()



if __name__ == '__main__':
	main()




