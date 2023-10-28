[General]
ned-path = .;../queueinglib
network = unbalanced
#cpu-time-limit = 60s
cmdenv-config-name = unbalancedBase
#tkenv-default-config = unbalancedBase
qtenv-default-config = unbalancedBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config unbalancedBase]
description = "Global scenario"
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.HighLoadSrv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:

[Config unbalancedBase1_lambda${"%03d" % int(delta*100)}]
extends=unbalancedBase
**.delta=${delta}
%endfor