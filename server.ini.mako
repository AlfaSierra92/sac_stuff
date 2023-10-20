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

[Config server1]
extends=serverBase
**.lambda=6
**.mu_n=20
**.mu_c=10
**.mu_d=15