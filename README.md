# law-example
A simple example of why `law` is nice

## Environment
First we need a nice new python environment where we run `law`. 
Let's start with a fresh `micromamba` installation, if you don't have one:
```bash
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
```
Go ahead and install the `environment.yml` with
```bash
micromamba env create -f environment.yml
```
and activate
```bash
micromamba activate law-example
```

## Analysis
In this example we want to calculate $\pi$ using Monte Carlo sampling (check [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_method)).
To do this, we construct a step-by-step analysis which does the following things:

1. Sample points from a unit square (Event generator)
2. Check how many points fall into a unit circle (Detector)
3. Calculate $\pi$
4. Visualize the detection method

## The un`law`ful solution

We create three python script in the `scripts` folder which we can execute after another to produce what
we want to achieve:

- scripts/events.py
- scripts/detector.py
- scripts/pi.py
- scripts/plot.py
