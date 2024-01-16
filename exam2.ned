import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Delay;

network exam2
{
    parameters:
        double lambda=default(10);
        double lambda_l = lambda * f_l;
        double lambda_c = lambda * (1-f_l);
        double delta = default(0.1);
        double f_l = default(0.7);
        double mu = default(10);
        local_src.interArrivalTime = 1s * exponential(1/lambda_l);
        cloud_src.interArrivalTime = 1s * exponential(1/lambda_c);
        delay1.delay=1.0s*truncnormal(1/mu, 0.1*delta);
        //delay2.delay=1.0s*truncnormal(delta, 0.1*delta);
        local_proc.serviceTime = 1s * exponential(1/mu); 
        local_proc.capacity = -1;
        cloud_proc.delay=1.0s*truncnormal(1/mu, 0.1*delta); 
    submodules:
        local_src: Source;
        cloud_src: Source;
        local_proc: Queue;
        //cloud_proc: Queue;
        delay1: Delay;
        cloud_proc: Delay;
        sink: Sink;
    connections:
        local_src.out --> local_proc.in++;
        local_proc.out --> sink.in++;
        cloud_src.out --> delay1.in++;
        delay1.out --> cloud_proc.in++;
        cloud_proc.out --> sink.in++;
}