import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm
#sett

def dot_t(x,beta):
	return round(np.dot(x,beta))

def vector_sum(vector):
	assert vector,'Вектор пуст'

	num_elem=len(vector[0])
	assert all(len(vec)==num_elem for vec in vector)

	return [sum(ve[i] for ve in vector) for i in range(num_elem)]

def scalar_multiply(c,v):
	v=np.array(v)
	return v*c

def vector_mean(vector):
	n=len(vector)
	return scalar_multiply(1/n,vector_sum(vector))

def gradient_step(vector,gradient,step_size):
	assert len(vector)==len(gradient)
	step=scalar_multiply(step_size,gradient)
	return vector+step

def error(ans,x,beta):
	return ans-dot_t(x,beta)

def sqr_error(ans,x,beta):
	return error(ans,x,beta)**2

def squared_error(ans,x,beta):
	err=error(ans,x,beta)
	return [err*x_i for x_i in x]

def least_squares_fit(
	xs,
	ys,
	alpha=0.001,
	num_step=1000,
	batch_size=1):
	
	guess=np.random.random(len(xs[0]))

	for _ in tqdm.trange(num_step,desc='learn'):
		for start in range(0,len(xs),batch_size):
			batch_xs=xs[start:(start+batch_size)]
			batch_ys=ys[start:(start+batch_size)]

			gradient=vector_mean([squared_error(ans, x, guess) for x, ans in zip(batch_xs,batch_ys)])
			guess=gradient_step(guess, gradient, alpha)

	return guess

def drob(x):
	while x>1:
		x/=10
	return x

def beyts(Ptd,Pd,Ptnotd,Pnotd):
	return (Ptd*Pd)/((Ptd*Pd)+(Ptnotd*Pnotd))

def mean(x):
	return sum(x)/len(x)

def corelation(x,y):
	x_mean=mean(x)
	y_mean=mean(y)

	summ_x_y=0
	for i in range(len(x)):
		summ_x_y+= ((x[i]-x_mean)*(y[i]-y_mean))

	summ_x_sqrt=0
	summ_y_sqrt=0
	for i in range(len(x)):
		summ_x_sqrt+=(x[i]-x_mean)**2
		summ_y_sqrt+=(y[i]-y_mean)**2

	down=np.sqrt((summ_x_sqrt*summ_y_sqrt))
	return summ_x_y/down

data=pd.read_csv(r'C:\Users\Rom\Downloads\titanic\test.csv')

sett=[]
for i in range(len(data['PassengerId'])):
	sett.append([1,data['Sex'][i],data['Pclass'][i],data['Fare'][i]])

#if __name__=='__main__':
np.random.seed(0)
i=[ 0.38579743,  0.30827652,  -0.02129545,   0.00040962]
ch=0
test=np.array(sett)
g=[]
for ch,j in enumerate(data['PassengerId']):
	print(j,'-', round(np.dot(test[ch],i)))
	print(ch)
	g.append([int(j),int(round(np.dot(test[ch],i)))])

np.savetxt(r"C:\Users\Rom\Downloads\titanic\Test_answer2.csv", np.array(g,int),fmt='%.0f', delimiter=",")

#78.37837837837837-true
#21.6216216216216-false

##38.38383838383838-alive
##61.61616161616161-dead
