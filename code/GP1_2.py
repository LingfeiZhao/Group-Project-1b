import pylab
from scipy.optimize import curve_fit

class Diffusion_1D(object):
	def __init__(self,D,N=101,dx=1,dt=0.01):# N is the number of the grid sites, D is the diffusion constant
		self.N=N
		self.D=D
		self.dx=dx
		self.dt=dt
		self.t=0
		self.x=[-(self.N-1)/2*self.dx+i*dx for i in range(N)] #initialize the grid position
		self.rho=[pylab.exp(-1000*self.x[i]*self.x[i]) for i in range(N)] #initialize the distribution at t=0 
		self.rho_new=[0.0]*N #the distribution at t+dt

	def diffuse(self): #calculate the distribution at t+dt
		for i in range(self.N-2):
			#the diffusion equation
			self.rho_new[i+1]=self.rho[i+1] + self.D*self.dt/self.dx/self.dx* (self.rho[i+2]+self.rho[i]-2*self.rho[i+1])
		self.rho=self.rho_new[:] #update distribution
		self.t+=self.dt #update time t


def Normal_Distribution(x,sigma):#the normal distribution function
	return 1/pylab.sqrt(2*pylab.pi)/sigma*pylab.exp(-x*x/2/sigma/sigma)

#initialize the lists to store the fitting parameter
tfit=[] 
sigmafit=[] #fitted parameter sigma at time tfit

for i in [100,1000,5000,10000,15000]: #i is the steps of the diffusion which is proportional to time
	Dif=Diffusion_1D(2)
	for j in range(i):
		Dif.diffuse()
	popt,pcov=curve_fit(Normal_Distribution,Dif.x,Dif.rho) # fit out the parameter sigma
	tfit.append(Dif.t)
	sigmafit.append(popt)

	xfit=[i/10.0 for i in range(-500,500)]
	rhofit=[Normal_Distribution(x,popt) for x in xfit]
	# plot the fitting snapshot
	pylab.plot(Dif.x,Dif.rho,'o',label='t=%d'% Dif.t)
	pylab.plot(xfit,rhofit,'-')
	pylab.xlabel('x')
	pylab.ylabel('$\\rho(x)$')
	pylab.title('5 different time snapshots, the solid lines are the fitted curves')
	pylab.legend(loc=0,numpoints=1)
	pylab.savefig('snapshot.pdf')
pylab.show()
#theoretical sigma
t=[2*i for i in range(100)]
sigma=[pylab.sqrt(4*i) for i in t]

#plot figure
pylab.plot(t,sigma,'r-',linewidth=2,label='$\sigma (t)= \sqrt{2Dt} $')
pylab.plot(tfit,sigmafit,'ko')
pylab.xlabel('t')
pylab.ylabel('$\sigma(t)$')
pylab.title('Parameter $\sigma$ of the diffusion equation')
pylab.legend(loc=0)
pylab.savefig('sigma.pdf')
pylab.show() 