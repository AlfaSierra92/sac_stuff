[General]
ned-path = .;../queueinglib
network = exam
#cpu-time-limit = 10000s
cmdenv-config-name = examBase
#tkenv-default-config = examBase
qtenv-default-config = examBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config examBase]
description = "Global scenario"
**.srv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
%for f_l in [0.7]:

[Config exam_fl${"%03d" % int(f_l*100)}]
extends=examBase
**.f_l=${f_l}
%endfor

