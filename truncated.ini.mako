[General]
ned-path = .;../queueinglib
network = truncated
#cpu-time-limit = 60s
cmdenv-config-name = truncated
#tkenv-default-config = truncated
qtenv-default-config = truncated
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config truncated]
description = "Global scenario"
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for rho in [0.01, 0.05, 0.10, 0.50, 1.00]:

[Config truncated_rho${"%03d" % int(rho*100)}]
extends=truncated
**.rho=${rho}
%endfor