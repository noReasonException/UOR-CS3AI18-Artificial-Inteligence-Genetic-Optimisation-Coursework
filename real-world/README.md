# Manual of ga-continuous-distrib.py

### TL;DR
As i am mindful of your available time, you can run directly the following command to to solve the bin packing problem
```shell script
python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r
```
With the following parameters
| Parameter                   | Default            |
|-----------------------------|--------------------|
| Weights                     | 4, 8, 1, 4, 2, 1   |
| Max Bin Capacity            | 10                 |

### Pre-programmed defaults
Before we start, here is the table with the pre-programmed desired behaviour. Everything is configurable through the command line(see below)

| Parameter                   | Default            |
|-----------------------------|--------------------|
| Mutation Rate               | 0.2                |
| Population Size             | 10                 |
| Weights                     | 4, 8, 1, 4, 2, 1   |
| Max Bin Capacity            | 10                 |
| Simulations                 | 1                  |
| Extended Information(Debug) | No                 |
| Present Results             | No                 |
| Optimisation Subject        | Bin packing problem|


### Command line arguments
The following command line parameters are supported


| Option | Description          | Purpose                                                | Valid Arguments | Default                    | Example                                                                                                 |
|--------|----------------------|--------------------------------------------------------|-----------------|----------------------------|---------------------------------------------------------------------------------------------------------|
| -d     | Debug mode           | Provides useful information per generation             | -               | No                         | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                       |
| -r     | Present mode         | Presents the results at the end of every simulation    | -               | No                         | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                       |
| -mr    | Mutation Rate        | Alters the default mutation rate                       | 0<=float<=1     | 0.2                        | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                       |
| -po    | Population Size      | Alters the default population size                     | int>10          | 1000                       | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                |
| -rt    | Simulations Number   | Alters the simulation number (returns averaged result) | int>0           | 1                          | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                |
| -we    | Weights              | Alters the default weights parameter                   | list            | 4, 8, 1, 4, 2, 1           | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                |
| -bc    | Bin Capacity         | Alters the default bin capacity parameter              | int>0           | 10                         | python2.7 ga-bin-packing.py  -mr 0.2 -po 10  -d -r -we 4,8,1,4,2,1 -bc 10                |



