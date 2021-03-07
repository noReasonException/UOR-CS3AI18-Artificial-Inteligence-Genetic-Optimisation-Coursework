# Manual of ga-continuous-distrib.py

### TL;DR
As i am mindful of your available time, you can run directly the following command to optimise the Mean Square error with sensible defaults
```shell script
python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100  -fn mse
```
### Pre-programmed defaults
Before we start, here is the table with the pre-programmed desired behaviour. Everything is configurable through the command line(see below)

| Parameter                   | Default           |
|-----------------------------|-------------------|
| Mutation Rate               | 0.2               |
| Crossover Rate              | 0.8               |
| Population Size             | 1000              |
| Lower Bound(lb)             | 0                 |
| Upper Bound(lb)             | 10                |
| N (Dimensions)              | 4                 |
| Simulations                 | 1                 |
| Extended Information(Debug) | No                |
| Present Results             | No                |
| Optimisation Subject        | Mean Square Error |

### Command line arguments
The following command line parameters are supported


| Option | Description          | Purpose                                                | Valid Arguments | Default  | Example                                                                                             |
|--------|----------------------|--------------------------------------------------------|-----------------|----------|-----------------------------------------------------------------------------------------------------|
| -d     | Debug mode           | Provides useful information per generation             | -               | No       | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100  -fn mse                           |
| -r     | Present mode         | Presents the results at the end of every simulation    | -               | No       | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100  -fn mse                           |
| -mr    | Mutation Rate        | Alters the default mutation rate                       | 0<=float<=1     | 0.2      | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100  -fn mse                           |
| -cr    | Crossover Rate       | Alters the default crossover rate                      | 0<=float<=1     | 0.8      | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100  -fn mse                           |
| -po    | Population Size      | Alters the default population size                     | int>10          | 1000     | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 1000  -fn mse                          |
| -ub    | Upper Bound          | Alters the default upper bound                         | int>Lower bound | 10       | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100 -ub 20  -fn mse                    |
| -lb    | Lower Bound          | Alters the default lower bound                         | int<Upper bound | 0        | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100 -ub 20 -lb -5 -fn mse              |
| -fn    | Optimisation Subject | Alters the default optimisation function               | see below       | mse      | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100 -ub 20 -lb -5 -fn sph              |
| -dim   | Dimensions (N)       | Alters the default N (Genes per individual)            | int>0           | 4        | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100 -ub 20 -lb -5 -fn sph -dim 8       |
| -rt    | Simulations Number   | Alters the simulation number (returns averaged result) | int>0           | 1        | python2.7 ga-continuous-distrib.py -r -d -mr 0.2 -cr 0.8 -po 100 -ub 20 -lb -5 -fn mse -dim 8 -rt 3 |

Important notice: Make sure that the function can be minimized in the given LB, UB. Otherwise, unavoidably, this program will stuck in an endless loop

### Functions supported
The following functions are supported and accepted in -fn parameter

| -fn parameter | Name                 |
|---------------|----------------------|
| mse           | Mean Square Error    |
| sph           | Sphere               |
| ras           | Rastrigin's function |
| lin           | Linear Function      |
| sin           | Sinusoidal           |
| abs           | Absolute Function    |