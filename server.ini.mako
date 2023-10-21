[General]
ned-path = .;../queueinglib
network = server
#cpu-time-limit = 60s
cmdenv-config-name = serverBase
#tkenv-default-config = serverBase
qtenv-default-config = serverBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config serverBase]
description = "Global scenario"
**.net.queueLength.result-recording-modes = +histogram
**.cpu.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for Lambda in [6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8, 8.5, 10, 12, 15]:

[Config server1_lambda${"%03d" % int(Lambda*100)}]
extends=serverBase
**.lambda=${Lambda}
**.mu_n=20
**.mu_c=10
**.mu_d=15
%endfor