[General]
ned-path = .;../queueinglib
network = MM1_3
#cpu-time-limit = 60s
cmdenv-config-name = MM1Base
#tkenv-default-config = MM1Base
qtenv-default-config = MM1Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config MM1Base]
description = "Global scenario"
**.srv1.queueLength.result-recording-modes = +histogram
**.srv2.queueLength.result-recording-modes = +histogram
**.srv3.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for lambda1 in [1.5, 3, 5]:
%for lambda2 in [1.5, 3, 5]:
%for lambda3 in [1.5, 3, 5]:
[Config MM1_3_l1_${"%03d" % int(lambda1)}_l2_${"%03d" % int(lambda2)}_l3_${"%03d" % int(lambda3)}]
extends=MM1Base
**.lambda1 = ${lambda1}
**.lambda2 = ${lambda2}
**.lambda3 = ${lambda3}
%endfor
%endfor
%endfor