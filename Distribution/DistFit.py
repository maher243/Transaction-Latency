"""
Created on Mon Aug 26 19:11:48 2019

@author: b6068199
"""
import random
import numpy as np
from sklearn.mixture import GaussianMixture
#from sklearn.ensemble import RandomForestRegressor
#from InputsConfig import InputsConfig as p
import pandas as pd





""" A class to fit distribution to Ethereum transaction attributes, which are 
    Gas Limit, Used Gas, Gas Price as well as CPU Time
"""
class DistFit():

    txGas=None
    txGasPrice=None
    utlization=None
    x=0

    
    df2= pd.read_excel('/Users/LENOVO/Desktop/Maher/Research/Latency_study/Distribution/Data.xlsx',sheet_name="tx")
    df3= pd.read_excel('/Users/LENOVO/Desktop/Maher/Research/Latency_study/Distribution/Data.xlsx',sheet_name="tx2")
    
    def fit():

              	#df= pd.read_excel (r'Data.xlsx',sheet_name="tx")
                #df2= pd.read_excel(r'Data.xlsx',sheet_name="tx")

                txUsedGas2=np.log(DistFit.df2['txUsedGas']).values.reshape(-1,1)
                txPrice=np.log(DistFit.df3['txGasPrice']+0.001).values.reshape(-1,1)
                #txPrice=txPrice.values.reshape(-1,1)
                
          	    #DistFit.cgas,DistFit.cprice,DistFit.ctime= DistFit.creation_fit(df) # fitted models (u:used gas, p: gas price, t: cpu time)
                DistFit.txGas, DistFit.txGasPrice = DistFit.creation_fit(txUsedGas2,txPrice)
                #DistFit.txGasPrice= DistFit.creation_fit(txPrice)



    def creation_fit(df,df1):
            """
                Define distribution of log(used gas) as Mixure Normal distribution with K components
            """
            
            K=5
            g = GaussianMixture(n_components = K)
            gmm= g.fit(df)# fit model
            

            """
                Estimate parameters of log(gas price) as normal distribution
            """
            eps= 0.001 # correction param
            K=65
            gg = GaussianMixture(n_components = K)
            ggmm= gg.fit(df1)# fit model


            return gmm, ggmm


    def sample_transactions(n):
        gastx= DistFit.txGas.sample(n)[0]
        gastx= np.exp(gastx).flatten().round()
        gastx[gastx<21000]= 21000
        gastx[gastx>30000000]= 30000000

        gasprice= DistFit.txGasPrice.sample(n)[0]
        gasprice= np.exp(gasprice).flatten().round()

        #gastx=gastx.reshape(-1,1)
        #gastx=gastx.flatten().round()
        
        #gastx= gastx[0]
        #gasprice= gasprice[0]
        UT = random.uniform(0,100)


        if (UT <= 6.57):
            utlization = 0
        elif (UT <=27.07):
            utlization = random.uniform(0.1,20)
        elif (UT <=34.75):
            utlization = random.uniform(20.1,40)
        elif (UT <=40.34):
            utlization = random.uniform(40.1,60)
        elif (UT <=44.97):
            utlization = random.uniform(60.1,80)
        elif (UT <=48.91):
            utlization = random.uniform(80.1,95)
        elif (UT <=100):
            utlization = random.uniform(95.1,100)     
            

        ######### preparing samples #######
        #gasLimit= np.concatenate((a_s,a_e),axis=None)
        #usedGas= np.concatenate((b_s,b_e),axis=None)
        #gasPrice= np.concatenate((c_s,c_e),axis=None)
        #CPUTime= np.concatenate((d_s,d_e),axis=None)

        return gastx, gasprice, utlization
