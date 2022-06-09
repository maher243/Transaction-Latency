from Distribution.DistFit import DistFit
import random
import numpy as np
import operator
import pandas as pd
from statistics import mean, median, stdev 

class Sim(object):


######################################################## Set configurable input parameters #####################################################################
        Binterval = 13.48  # Average block interval time (in seconds). The time between two consecutive blocks
        Blimit = 30000000 #The block gas limit
        Tn = 2000 # The arrival rate for transactions (i.e., the number of transactions to be created per second)
        Butilization= 1 # The block utilization level (it ranges from 0.0 to 1.0), where 0.0 indicates empty blocks and 1.0 indicates all blocks are full
        simTime = 1350 # The length of the simulation time in seconds, corresponding to the real blockchain time
        timer=0 # It indicates the current simulation time, where 0 indicates the simulator has not yet started
        runs=2 # Number of simulation runs
     
        network_pending_tx=[] # List of unconfirmed transactions
	transactionsPool=[] # Transaction memory-pool
        blockchain=[] # The blockchain ledger
        

######################################################## Transaction Classess #####################################################################

class Transaction(object):
    """ Define Ethereum Transaction

    :param int id: the uinque id or the hash of the transaction
    :param int timestamp: the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
    :param int sender: the id of the node that created and sent the transaction
    :param int to: the id of the recipint node
    :param int value: the amount of cryptocurrencies to be sent to the recipint node
    :param int size: the transaction size in MB
    :param int gasLimit: the maximum amount of gas units the transaction can use. It is specified by the submitter of the transaction
    :param int usedGas: the amount of gas used by the transaction after its execution on the EVM
    :param int gasPrice: the amount of cryptocurrencies (in Gwei) the submitter of the transaction is willing to pay per gas unit
    :param float fee: the fee of the transaction (usedGas * gasPrice)
    """

    def __init__(self,
	 id=random.randrange(100000000000),
	 timestamp=0,
	 sender=0,
       to=0,
       value=0,
	 size=0.000546,
         gasLimit= 30000000,
         usedGas=0,
         gasPrice=0,
         fee=0,
         inclusion_time=0,
         latency= 0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to= to
        self.value=value
        self.size = size
        self.gasLimit=gasLimit
        self.usedGas = usedGas
        self.gasPrice=gasPrice
        self.fee= usedGas * gasPrice
        self.inclusion_time=inclusion_time
        self.latency= inclusion_time - timestamp



class FullTransaction():
    #x=0 # counter to only fit distributions once during the simulation
    counter=0 # counter for tx created per second
    

    def create_transactions():
        j=1
        Psize= 100* Sim.Tn  #int(Sim.Tn * Sim.simTime)

        usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            FullTransaction.counter = FullTransaction.counter +1
            if FullTransaction.counter > Sim.Tn:
            	j = j +1 
            	FullTransaction.counter = 0

            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()
            tx.id = random.randrange(100000000000)
            tx.timestamp= j
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice
            Sim.transactionsPool.append(tx)


    def execute_transactions():
        Sim.timer = Sim.timer + random.expovariate(1/Sim.Binterval) 
        currentTime= Sim.timer 
        Sim.transactionsPool.sort(key=operator.attrgetter('gasPrice'), reverse=True)

        #while currentTime <= Sim.simTime:
        while len(Sim.transactionsPool) > 0:
            blocklimit = (Sim.Blimit * Sim.Butilization)
            tx_x=0
            for i in range (len(Sim.transactionsPool)):
                    if Sim.transactionsPool[i].timestamp <= currentTime:
                         tx_x += 1
            
            Sim.network_pending_tx += [tx_x]
            block = Block()
            block.depth = len(Sim.blockchain)
            block.timestamp = currentTime
            limit = 0 # calculate the total block gaslimit
            count=0

            while count < len(Sim.transactionsPool):

                    if  (blocklimit >= Sim.transactionsPool[count].usedGas and Sim.transactionsPool[count].timestamp <= currentTime):
                            blocklimit -= Sim.transactionsPool[count].usedGas
                            Sim.transactionsPool[count].inclusion_time = currentTime
                            Sim.transactionsPool[count].latency = Sim.transactionsPool[count].inclusion_time - Sim.transactionsPool[count].timestamp
                            block.transactions += [Sim.transactionsPool[count]]
                            limit += Sim.transactionsPool[count].usedGas
                            del Sim.transactionsPool[count]
                            count = count -1
                    count+=1

            block.usedgas= limit


            Sim.blockchain.append(block)
            #return transactions, limit
            currentTime += Sim.Binterval 

######################################################## Block Class #####################################################################

class Block():

    """ Defines the Ethereum Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    :param list uncles: a list of uncle blocks to be referenced in the block
    :param int gaslimit: the block gas limit (e.g., current block gas limit = 8,000,000 units of gas)
    :param int usedgas: the block used gas
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0,
	 uncles=[],
     gaslimit= 30000000,
     usedgas=0):

        self.depth = depth
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions or []
        self.size = size
        self.uncles= uncles
        self.gaslimit= gaslimit
        self.usedgas= usedgas


######################################################## Main Method #####################################################################

def main():

    #if Sim.xxx<1:
    #print("distriburions are fitted to data")
    DistFit.fit() # fit distributions
    latency=[[0 for x in range(5)] for y in range(Sim.runs)] # min,max,mean,mdeiam,SD

    for i in range(Sim.runs):
            FullTransaction.create_transactions()  # generate pending transactions
            FullTransaction.execute_transactions()

            txList=[]
            blocks= [[0 for x in range(5)] for y in range(len(Sim.blockchain))] 
            late=[]

            #*"" Define configurable input parameters
            for k in Sim.blockchain:
                    for j in range (len(k.transactions)):
                        txList.append(k.transactions[j])
                        late.append(k.transactions[j].latency)
                
            #avglate= avglate / len(txList)
            latency[i][0]= min(late)
            latency[i][1]= max(late)
            latency[i][2]= mean(late)
            latency[i][3]= median(late)
            latency[i][4]= stdev(late)
            
            #Sim.latency.append(late)

            transactionsList= [[0 for x in range(7)] for y in range(len(txList))] # rows number of int(Sim.Tn * Sim.simTime), columns =6
            for i in range (len(txList)):
                    transactionsList[i][0]= txList[i].id
                    transactionsList[i][1]= txList[i].timestamp
                    transactionsList[i][2]= txList[i].usedGas
                    transactionsList[i][3]= txList[i].gasPrice
                    transactionsList[i][4]= txList[i].fee
                    transactionsList[i][5]= txList[i].inclusion_time
                    transactionsList[i][6]= txList[i].latency

            for i in range (len(Sim.blockchain)):
                    blocks[i][0]= Sim.blockchain[i].depth
                    blocks[i][1]= Sim.blockchain[i].timestamp
                    blocks[i][2]= Sim.blockchain[i].gaslimit
                    blocks[i][3]= Sim.blockchain[i].usedgas
                    blocks[i][4]= len(Sim.blockchain[i].transactions)

            Sim.blockchain=[]
            Sim.transactionsPool=[]
            Sim.timer=0
######################################################## Saving Simulation Results in Excel files #####################################################################

    df = pd.DataFrame(transactionsList)
    df.columns = ['ID','Timestamp', 'Used Gas','Gas Price', 'Fee','Inclusion Time','Latency']
    df1 = pd.DataFrame(Sim.network_pending_tx)
    #df1.columns = ['Number of pending TX']
    df2 = pd.DataFrame(blocks)
    df2.columns = ['ID','Timestamp', 'Gas Limit','Used Gas', '# tx']
    df3 = pd.DataFrame(latency)
    df3.columns = ['Min','Max', 'Mean','Median', 'SD']

    #df.to_csv('TX.csv',index=False)
    #df1.to_csv('Pending.csv',index=False)
    #df2.to_csv('Blocks.csv',index=False)
    writer = pd.ExcelWriter('Results_2000Arrival_7Interval.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Transactions')
    df1.to_excel(writer, sheet_name='Network_Pending')
    df2.to_excel(writer, sheet_name='Blocks')
    df3.to_excel(writer,sheet_name='Latency')
    writer.save()


  
######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
