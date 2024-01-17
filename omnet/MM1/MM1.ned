//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//
// Questo dice la rete che noi utilizziamo nella simulazione.


import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network MM1
{
	parameters: // definisco dei valori di default che poi posso cambiare "dinamicamente" via file *.ini
		int K = default(10); // numero massimo di clienti che puo' gestire il sistema (coda)
		double rho = default(0.8); // utilizzazione
		double mu = default(10); // tasso di partenza
		double lambda = mu * rho; // tasso di arrivo
		
		// def. della v.a. processo di arrivo (ovvero definisco lamb*e^(-lamb*x); lamb e' il parametro dell'esponenziale (qui uguale a 1/lambda)
		// exponential e' la distribuzione esponenziale, non l'esponenziale in se'
		// perche' 1/lambda? Lambda e' il tasso di arrivo, quindi il suo reciproco e' il tempo medio di arrivo
		src.interArrivalTime = 1s * exponential(1/lambda); 
		
		// def. della v.a. processo di servizio
		// perche' 1/mu? Mu e' il tasso di servizio quindi il suo reciproco e' il tempo di servizio (tempo impiegato ad espletare l'ordine)
		srv.serviceTime = 1s * exponential(1/mu); 
		
		srv.capacity = K; // capacita' coda (finita in questo caso)
	submodules:
		src: Source; // Rappresenta la sorgente dei clienti, che genera i clienti con intervalli di tempo casuali tra gli arrivi.
		srv: Queue; // Rappresenta la coda (o il server) in cui i clienti attendono il servizio.
		sink: Sink; // Rappresenta il destinatario dei clienti, che registra quando i clienti hanno completato il servizio.
	connections:
	    // Le connessioni tra i sottomoduli sono definite tramite l'operatore -->. 
	    // Ad esempio, src.out --> srv.in++ indica che i clienti generati dalla sorgente (src.out) vengono inviati alla coda (srv.in++), 
	    //e srv.out --> sink.in++ indica che i clienti completati nella coda vengono inviati al destinatario (sink.in++).
		src.out --> srv.in++;
		srv.out --> sink.in++;
}


