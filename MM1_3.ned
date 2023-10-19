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

// Senza la specifica di una capacita' massima, le code saranno teoricamente illimitate 
// e saranno in grado di gestire qualsiasi numero di clienti contemporaneamente, 
// a meno che ci siano altri meccanismi o limitazioni specifiche nel codice che 
// non sono visibili nel frammento che hai condiviso.

import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network MM1_3
{
	parameters:
	    int k1 = default(5);
	    int k2 = default(5);
	    int k3 = default(5);
		double mu = default(10); //RIMANE COSTANTE IN QUESTA SIM.
		double lambda1 = default(4); //tasso di arrivo 1
		double lambda2 = default(4); //tasso di arrivo 2
		double lambda3 = default(4); //tasso di arrivo 3
		src1.interArrivalTime = 1s * exponential(1/lambda1);
		src2.interArrivalTime = 1s * exponential(1/lambda2);
		src3.interArrivalTime = 1s * exponential(1/lambda3);
		srv1.serviceTime = 1s * exponential(1/mu);
		srv2.serviceTime = 1s * exponential(1/mu);
		srv3.serviceTime = 1s * exponential(1/mu);
		srv1.capacity = k1;
		srv2.capacity = k2;
		srv3.capacity = k3;
	submodules:
		src1: Source;
		src2: Source;
		src3: Source;
		srv1: Queue;
		srv2: Queue;
		srv3: Queue;
		sink: Sink;
	connections:
		src1.out --> srv1.in++;
		src2.out --> srv2.in++;
		src3.out --> srv3.in++;
		srv1.out --> sink.in++;
		srv2.out --> sink.in++;
		srv3.out --> sink.in++;
}