import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Router;

network server_2
{
    parameters:
        double lambda = default(6); // tasso di arrivo
        double mu_n = default(20); // tasso di partenza rete
        double mu_c = default(10); // tasso di partenza cpu
        double mu_d = default(15); // tasso di partenza disco

        src.interArrivalTime = 1s * exponential(1/lambda);
        router.routingAlgorithm = "roundRobin";
        
        net.serviceTime = 1s * exponential(1/mu_n); 
        cpu.serviceTime = 1s * exponential(1/mu_c); 
        cpu2.serviceTime = 1s * exponential(1/mu_c); 
        disk.serviceTime = 1s * exponential(1/mu_d); 
    submodules:
        src: Source;
        net: Queue;
        router: Router {
            gates:
                in[1];
                out[2];
        }
        cpu: Queue;
        cpu2: Queue;
        disk: Queue;
        sink: Sink;
    connections:
        src.out --> net.in++;
        net.out --> router.in[0];
        router.out[0] --> cpu.in++;
        router.out[1] --> cpu2.in++;
        cpu.out --> disk.in++;
        cpu2.out --> disk.in++;
        disk.out --> sink.in++;
}

// Presumo che il tempo di risposta complessivo sia la sommatoria dei singoli
// tempi di risposta; quindi:
// tr_i = 1/(mu_i - lambda_i)
//
// 
