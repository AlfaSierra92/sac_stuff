import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Classifier;

network truncated
{
    parameters:
        double lambda = default(6); // tasso di arrivo
        double mu = default(10); // tasso di partenza rete
        double rho = default(0.01);

        LowLoadSrc.interArrivalTime = 1s * exponential(1/lambda);
        LowLoadSrv.serviceTime = 1s * truncnormal(1/mu, rho);
        //LowLoadSrc.jobType = default(0);
        
    submodules:
        LowLoadSrc: Source;
        LowLoadSrv: Queue;
        sink: Sink;
    connections:
        LowLoadSrc.out --> LowLoadSrv.in++;
        LowLoadSrv.out --> sink.in++;
}