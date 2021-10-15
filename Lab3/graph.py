#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:38:57 2021

@author: michaelmitschjr
"""
import pandas

df = pandas.read_csv("P_1-30__I_1-0__D_2.25.csv",skipinitialspace=True)
plot = df.plot('time','error',title="P D").get_figure().savefig("Graphs/PI.png")

df = pandas.read_csv("P_1-45__I_1-0__D_0.csv",skipinitialspace=True)
df.plot('time','error',xlim=(0,10**7), title="P").get_figure().savefig("Graphs/P.png")

df = pandas.read_csv("P_1-30__I_1-9000__D_2.5.csv",skipinitialspace=True)
df.plot('time','error',title="P I D").get_figure().savefig("Graphs/PID.png")