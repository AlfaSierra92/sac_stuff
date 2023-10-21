import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network server
{
    parameters:
        double lambda = default(6); // tasso di arrivo
        double mu_n = default(20); // tasso di partenza rete
        double mu_c = default(10); // tasso di partenza cpu
        double mu_d = default(15); // tasso di partenza disco

        src.interArrivalTime = 1s * exponential(1/lambda);
        net.serviceTime = 1s * exponential(1/mu_n); 
        cpu.serviceTime = 1s * exponential(1/mu_c); 
        disk.serviceTime = 1s * exponential(1/mu_d); 
    submodules:
        src: Source;
        net: Queue;
        cpu: Queue;
        disk: Queue;
        sink: Sink;
    connections:
        src.out --> net.in++;
        net.out --> cpu.in++;
        cpu.out --> disk.in++;
        disk.out --> sink.in++;
}

// Presumo che il tempo di risposta complessivo sia la sommatoria dei singoli
// tempi di risposta; quindi:
// tr_i = 1/(mu_i - lambda_i)
//
// 
