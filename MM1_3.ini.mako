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
**.srv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

[Config MM1_3_Low]
extends=MM1Base
**.lambda1=1.5
**.lambda2=1.5
**.lambda3=1.5

[Config MM1_3_Balanced]
extends=MM1Base
**.lambda1=3.5
**.lambda2=3.5
**.lambda3=3.5

[Config MM1_3_Hi]
extends=MM1Base
**.lambda1=4.5
**.lambda2=4.5
**.lambda3=4.5

[Config MM1_3_Unbalanced]
extends=MM1Base
**.lambda1=3.5
**.lambda2=4.5
**.lambda3=1.5
