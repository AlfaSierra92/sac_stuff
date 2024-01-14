import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network mg1trunc
{
    parameters:
        double mu = default(100);
        double rho = default(0.7);
        double cv = default(1.0); // coefficente di variazione della gaussiana
        double lambda = rho * mu; // qui devi usare mu, non 1/mu
        double sigma = cv * (1.0 / mu);

        src.interArrivalTime = 1.0s * exponential(1.0/lambda);
        fog.serviceTime = 1.0s * truncnormal(1.0/mu, sigma); // ATTENTO!!!!
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