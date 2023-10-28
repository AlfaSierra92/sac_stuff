[General]
ned-path = .;../queueinglib
network = unbalanced_duale
#cpu-time-limit = 60s
cmdenv-config-name = unbalanced_dualeBase
#tkenv-default-config = unbalanced_dualeBase
qtenv-default-config = unbalanced_dualeBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config unbalanced_dualeBase]
description = "Global scenario"
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.HighLoadSrv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:

[Config unbalanced_dualeBase1_delta${"%03d" % int(delta*100)}]
extends=unbalanced_dualeBase
**.delta=${delta}
%endfor