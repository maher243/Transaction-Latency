# Transaction Latency Simulator
Discrete-event simulator for estimating transaction latency within permissionless blockchains. 

## Installation and Requirements

Before you can use BlockSim  simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- sklearn 
>pip install sklearn
- xlsxwriter
>pip install xlsxwriter

## Running the simulator

Before you run the simulator, you can access the configuration file *InputsConfig.py* to choose the model of interest (Base Model 0, Bitcoin Model 1 and Ethereum Model 2) and to set up the related parameters.
The parameters include the number of nodes (and their fraction of hash power), the block interval time, the block propagation delays, the block and transaction sizes, the block rewards, the tranaction fees etc.
Each model has a slightly different (or additional) parameters to capture it.

To run the simulator, one needs to trigger the main class *Main.py* either from the command line
> python Main.py

or using any Python editor such as Spyder.

## Statistics and Results

The results of the simulator is printed in an excel file at the end of the simulation. The results include the blockchain ledger, number of blocks mined, number of stale (uncles) blocks and the rewards gained by each miner etc. 

## Contact

For any query about how to use or even extend the simulator, feel free to contact me **alharbi.maher@gmail.com**
