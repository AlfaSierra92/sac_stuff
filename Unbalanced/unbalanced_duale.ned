import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network unbalanced_duale
{
    parameters:
        double lambda = default(6); // tasso di arrivo
        double mu = default(10); // tasso di partenza rete
        double delta = default(0);

        LowLoadSrc.interArrivalTime = 1s * exponential(1/lambda);
        HighLoadSrc.interArrivalTime = 1s * exponential(1/lambda+delta);
        LowLoadSrv.serviceTime = 1s * exponential(1/(mu+delta)); 
        HighLoadSrv.serviceTime = 1s * exponential(1/(mu-delta)); 
    submodules:
        LowLoadSrc: Source;
        HighLoadSrc: Source;
        LowLoadSrv: Queue;
        HighLoadSrv: Queue;
        sink: Sink;
    connections:
        LowLoadSrc.out --> LowLoadSrv.in++;
        HighLoadSrc.out --> HighLoadSrv.in++;
        LowLoadSrv.out --> sink.in++;
        HighLoadSrv.out --> sink.in++;
}
