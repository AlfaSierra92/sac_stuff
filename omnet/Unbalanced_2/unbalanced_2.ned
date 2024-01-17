import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Classifier;

network unbalanced_2
{
    parameters:
        double lambda = default(6); // tasso di arrivo
        double mu = default(10); // tasso di partenza rete
        double delta = default(0);

        LowLoadSrc.interArrivalTime = 1s * exponential(1/(lambda-delta));
        HighLoadSrc.interArrivalTime = 1s * exponential(1/(lambda+delta));
        LowLoadSrv.serviceTime = 1s * exponential(1/mu); 
        HighLoadSrv.serviceTime = 1s * exponential(1/mu); 
        class.dispatchField = "type";
        LowLoadSrc.jobType = default(0);
        HighLoadSrc.jobType = default(1);
    submodules:
        LowLoadSrc: Source;
        HighLoadSrc: Source;
        LowLoadSrv: Queue;
        HighLoadSrv: Queue;
        sink: Sink;
        sink2: Sink;
        sink3: Sink;
        class: Classifier {
            gates:
                in[2];
                out[2];
        }
    connections:
        LowLoadSrc.out --> LowLoadSrv.in++;
        HighLoadSrc.out --> HighLoadSrv.in++;
        LowLoadSrv.out --> class.in[0];
        HighLoadSrv.out --> class.in[1];
        class.out[0] --> sink.in++;
        class.out[1] --> sink2.in++;
        class.rest --> sink3.in++;
}
