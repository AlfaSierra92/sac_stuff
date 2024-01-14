[General]
ned-path = .;../queueinglib
network = mg1trunc
#cpu-time-limit = 60s
cmdenv-config-name = mg1truncBase
#tkenv-default-config = mg1truncBase
qtenv-default-config = mg1truncBase
repeat = 3
sim-time-limit = 300s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config mg1truncBase]
description = "Global scenario"
**.net.queueLength.result-recording-modes = +histogram
**.cpu.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for rho in [0.7, 0.9]:
%for cv in [0.5, 1, 1.5]:

[Config mg1trunc_rho${"%03d" % int(rho*100)}_cv${"%03d" % int(cv*100)}]
extends=mg1truncBase
**.rho=${rho}
**.cv=${cv}
%endfor
%endfor