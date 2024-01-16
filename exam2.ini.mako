[General]
ned-path = .;../queueinglib
network = exam2
#cpu-time-limit = 10000s
cmdenv-config-name = exam2Base
#tkenv-default-config = exam2Base
qtenv-default-config = exam2Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config exam2Base]
description = "Global scenario"
**.srv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
%for f_l in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:

[Config exam2_fl${"%03d" % int(f_l*100)}]
extends=exam2Base
**.f_l=${f_l}
%endfor

