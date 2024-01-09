import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network lognormal
{
    parameters:
        double mu = default(100);
        double rho = default(0.7);
        double cv = default(0.5);
        double lambda = rho * mu; // qui devi usare mu, non 1/mu
        src.interArrivalTime = 1s * exponential(1/lambda);
        fog.serviceTime = 1s * lognormal(log(1.0/(mu * sqrt(1 + cv^2))), sqrt(log(1 + cv^2)));
        // NOTA BENE BENE BENE
        // La lognormal vuole i parametri della distribuzione normale sottostante,
        // quindi devo usare i generatori dei momenti della lognormal per calcolare tali parametri
        // (vengono dati quelli della lognormal ma servono quelli della normal)

    submodules:
        src: Source;
        fog: Queue;
        sink: Sink;
    connections:
        src.out --> fog.in++;
        fog.out --> sink.in++;
}