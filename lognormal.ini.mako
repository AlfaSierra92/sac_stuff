[General]
ned-path = .;../queueinglib
network = lognormal
#cpu-time-limit = 60s
cmdenv-config-name = lognormalBase
#tkenv-default-config = lognormalBase
qtenv-default-config = lognormalBase
repeat = 3
sim-time-limit = 300s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config lognormalBase]
description = "Global scenario"
**.net.queueLength.result-recording-modes = +histogram
**.cpu.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for rho in [0.7, 0.9]:
%for cv in [0.5, 1, 1.5]:

[Config lognormal_rho${"%03d" % int(rho*100)}_cv${"%03d" % int(cv*100)}]
extends=lognormalBase
**.rho=${rho}
**.cv=${cv}
%endfor
%endfor