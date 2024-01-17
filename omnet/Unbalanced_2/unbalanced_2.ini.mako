[General]
ned-path = .;../queueinglib
network = unbalanced_2
#cpu-time-limit = 60s
cmdenv-config-name = unbalanced_2
#tkenv-default-config = unbalanced_2
qtenv-default-config = unbalanced_2
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config unbalanced_2]
description = "Global scenario"
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.HighLoadSrv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
**.sink2.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:

[Config unbalanced_2Base1_delta${"%03d" % int(delta*100)}]
extends=unbalanced_2
**.delta=${delta}
%endfor