# Manual of ga-continuous-distrib.py

### TL;DR
As i am mindful of your available time, you can run directly the following command to minimise sumOfOnes with sensible defaults
```shell script
python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r
```
### Pre-programmed defaults
Before we start, here is the table with the pre-programmed desired behaviour. Everything is configurable through the command line(see below)

| Parameter                   | Default           |
|-----------------------------|-------------------|
| Mutation Rate               | 0.2               |
| Crossover Rate              | 0.8               |
| Population Size             | 10                |
| N (Dimensions)              | 20                |
| Simulations                 | 1                 |
| Extended Information(Debug) | No                |
| Present Results             | No                |
| Optimisation Subject        | Sum of ones-min   |

### Command line arguments
The following command line parameters are supported


| Option | Description          | Purpose                                                | Valid Arguments | Default  | Example                                                                                                 |
|--------|----------------------|--------------------------------------------------------|-----------------|----------|---------------------------------------------------------------------------------------------------------|
| -d     | Debug mode           | Provides useful information per generation             | -               | No       | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r                       |
| -r     | Present mode         | Presents the results at the end of every simulation    | -               | No       | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r                       |
| -mr    | Mutation Rate        | Alters the default mutation rate                       | 0<=float<=1     | 0.2      | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r                       |
| -cr    | Crossover Rate       | Alters the default crossover rate                      | 0<=float<=1     | 0.8      | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r                       |
| -po    | Population Size      | Alters the default population size                     | int>10          | 1000     | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -po 30 -dim 20  -d -r                |
| -fn    | Optimisation Subject | Alters the default optimisation function               | see below       | mse      | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1min -dim 20  -d -r                       |
| -dim   | Dimensions (N)       | Alters the default N (Genes per individual)            | int>0           | 4        | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r                       |
| -rt    | Simulations Number   | Alters the simulation number (returns averaged result) | int>0           | 1        | python2.7 ga-combinatorial-distrib.py  -mr 0.2 -cr 0.8 -fn sum1max -dim 20  -d -r -rt 20                |


### Functions supported
The following functions are supported and accepted in -fn parameter

| -fn parameter | Name                 |
|---------------|----------------------|
| sum1max       | Sum of ones (max)    |
| sum1min       | Sum of ones (min)    |