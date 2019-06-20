import numpy as np
from scipy.stats import norm
from scipy import optimize, special
import matplotlib.pyplot as plt
import csv
import pandas as pd
import pymc3 as pm
from pymc3 import summary

from pymc3 import NUTS, sample



def gaith (datagaith):
    # datagaith=pd.DataFrame(datagaith)
    data = datagaith.iloc[:-1, 0].values
    # print(data)
    # Fit a normal distribution to the data:
    mu, std = norm.fit(data)

    # Plot the histogram.
    plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    pdf = norm.pdf(x, mu, std)


    # plt.plot(x, pdf, 'k', linewidth=2)
    # title = "Fit results: mu = %.2f,  std = %.4f" % (mu, std)
    # plt.title(title)
    # plt.show()


    # prior


    prior=datagaith.iloc[-1,0]
    stdprior=0.002

    x = np.linspace(prior-.01, prior+.01, 100)

    p = norm.pdf(x, prior, stdprior)


    # plt.plot(x, p, 'k', linewidth=2)
    # title = "Fit results: mu = %.2f,  std = %.4f" % (prior, stdprior)
    # plt.title(title)
    # plt.show()

    # with pm.Model():
    #     mu1 =pdf
    #
    # niter = 20
    # with pm.Model():
    #     mu = mu
    #     sd = std
    #     y = pm.Normal('y', mu=mu, sd=sd, observed=data)
    #     start = pm.find_MAP(fmin=optimize.fmin_powell)
    #     print("************************")
    #     print(start)
    #     step = pm.NUTS(scaling=start)
    #     trace = pm.sample(niter, start=start, step=step)


    model = pm.Model()
    with model:
        mu1 = pm.Normal("mu1", mu=mu, sd=std, shape=10)
    with model:
        # step = pm.NUTS()
        # trace = pm.sample(2000, tune=1000, init=None, step=step, cores=2)

        # obtain starting values via MAP
        start = pm.find_MAP(fmin=optimize.fmin_powell)

        # instantiate sampler
        step = NUTS(scaling=start)

        # draw 2000 posterior samples
        trace = sample(10, step, start=start)

    # for i in summary(trace).iterrows():
    #     print(str(i))
        # if (i[1]) == (min(summary(trace)['mc_error'])):
        #     print(i)

    a = summary(trace).loc[summary(trace)['mc_error'] == min(summary(trace)['mc_error'])]
    return a,mu,prior

if __name__ == '__main__':
    path = "/Users/gaithrjoub/Desktop/gaith.csv"

    colnames = list('ABCDEFGHIJKLMNOPQR')
    datagaith = pd.read_csv(path, names=colnames)
    datagaith = pd.DataFrame(datagaith)
    # print(datagaith.iloc[0, :].values)
    vol = []

    # Generate some data for this demonstration.
    for index,i in datagaith.iterrows():

        # i = pd.DataFrame(list(i[0,1]),columns = list('ABCDEFGHIKLMNO'))
        # # print(i[0,1])
        s = pd.DataFrame(list(i))
        # print(s.iloc[:-1, 0].values)

        # print(i)
        # print(str(i[0]))

        # data = datagaith.iloc[i, :-1].values
        a,mu,prior=gaith(s)

        # # #
        # print("****************")
        #
        # print(a['mean'][0])
        # print("****************")
        #
        # print(mu)
        # print("****************")
        #
        # print(prior)
        # print("****************")
        # print(a['mean'][0]*mu/prior)
        # print("****************")
        #
      #  vol.append((a['mean'][0],mu,prior,a['mean'][0]*mu/prior))
        vol.append (( a['mean'][0] * mu / prior))
    vol=pd.DataFrame(vol)
    vol = vol.sort_values([0])
    vol.to_csv("/Users/gaithrjoub/Desktop/trustvms.csv")
    print(vol)


