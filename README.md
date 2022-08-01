# Transaction Latency Simulator
Discrete-event simulator for estimating transaction latency within permissionless blockchains. 

## Installation and Requirements

Before you can use the simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- sklearn 
>pip install sklearn
- xlsxwriter
>pip install xlsxwriter

## Running the simulator

Before you run the simulator, you need to configure the input parameter for the simulator by accessing the *Sim.py* class. The paramters that need to be set the end user are:

        Binterval -> Average block interval time (in seconds). The time between two consecutive blocks
        Blimit -> The block gas limit
        Tn ->  The arrival rate for transactions (i.e., the number of transactions to be created per second)
        Butilization -> The block utilization level (it ranges from 0.0 to 1.0), where 0.0 indicates empty blocks and 1.0 indicates all blocks are full
        simTime -> The length of the simulation time in seconds, corresponding to the real blockchain time
        runs -> Number of simulation runs
        
To run the simulator, one needs to trigger the *Sim.py* class either from the command line
> python Sim.py

or using any Python editor such as Spyder.

## Statistics and Results

The results of the simulator is printed in an excel file at the end of the simulation. The results include the blockchain ledger, number of blocks mined and details of transactions confirmed in the network. For every transaction, we record it gas related attributes, fees, creation time, time when it was recorded in the blockchain ledger and etc.

## Contact

For any query about how to use or even extend the simulator, feel free to contact me **alharbi.maher@gmail.com**
