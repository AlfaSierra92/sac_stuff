[General]
ned-path = .;../queueinglib
network = server_2
#cpu-time-limit = 60s
cmdenv-config-name = server_2Base
#tkenv-default-config = server_2Base
qtenv-default-config = server_2Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config server_2Base]
description = "Global scenario"
**.net.queueLength.result-recording-modes = +histogram
**.cpu.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for Lambda in [6, 7, 7.1, 7.7, 7.9, 8, 8.5, 10, 12, 12.1, 12.2, 12.3, 12.4, 12.5, 13, 13.5, 14, 15, 15.5, 16]:

[Config server_2_1_lambda${"%03d" % int(Lambda*100)}]
extends=server_2Base
**.lambda=${Lambda}
**.mu_n=20
**.mu_c=10
**.mu_d=15
%endfor