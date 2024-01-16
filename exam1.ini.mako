[General]
ned-path = .;../queueinglib
network = exam1
#cpu-time-limit = 10000s
cmdenv-config-name = exam1Base
#tkenv-default-config = exam1Base
qtenv-default-config = exam1Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config exam1Base]
description = "Global scenario"
**.srv.queueLength.result-recording-modes = +histogram
**.sink1.lifeTime.result-recording-modes = +histogram
**.sink2.lifeTime.result-recording-modes = +histogram
%for f_l in [0.501, 0.502, 0.503, 0.504, 0.505, 0.506, 0.507, 0.508, 0.509]:

[Config exam1_fl${"%04d" % int(f_l*1000)}]
extends=exam1Base
**.f_l=${f_l}
%endfor

