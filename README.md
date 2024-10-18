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
