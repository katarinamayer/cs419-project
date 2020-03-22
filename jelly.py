from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

import os
import sys
import argparse
import random
import networkx
# need to import a bunch of mininet shit


'''
Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }
'''

class Jellyfish(Topo):

	#initialize nums
	def __init__(self, numNodes, numPorts, numServerPorts, numSwitches):
        self.numNodes = numNodes
        self.numPorts = numPorts
        self.numServerPorts = numServerPorts
        self.numSwitches = numSwitches

        # Initialize graph of switch topology using networkx
        self.graph = nx.Graph()
        g.add_nodes_from(['s'+str(i) for i in range(numSwitches)])

    '''
    see https://github.com/mininet/mininet/wiki/Introduction-to-Mininet
    class SingleSwitchTopo(Topo):
        "Single switch connected to n hosts."
        def build(self, n=2):
            switch = self.addSwitch('s1')
            # Python's range(N) generates 0..N-1
            for h in range(n):
                host = self.addHost('h%s' % (h + 1))
                self.addLink(host, switch)
    '''

	#algo to create graph
	def build(self):
        hosts = []
        for i in range(numNodes):
            hosts.append(self.addHost('h' + str(i)))

        switches = []
        ports = []
        for i in range(numSwitches):
            switches.append(self.addHost('s' + str(i))
            ports.append(numPorts)
            # each switch has all open ports at this point

        #connect each host to a switch?

        #randomly pick a pair of (non-neighboring) switches with free ports, Join them with a link, Repeat until no further links can be added.

        adjacent = set()
        checked_switch1 = []

        while len(checked_switch1) < numSwitches: # loop through all switches
            index1 = randrange(numSwitches)

            while index1 not in checked_switch1 and ports[index1] > 0:
                checked_switch2 = []
                index2 = randrange(numSwitches)

                while index2 not in checked_switch2 and index2 != index1 and ports[index2] > 0:

                    while (index1, index2) not in adjacent:

                        # Form new link
                        self.addLink(switch[index1], switch[index2])

                        # Add new link to set to track adjacency
                        adjacent.add((index1, index2))
                        adjacent.add((index2, index1))

                        checked_switch2.append(index2)

            checked_switch1.append(index1)

        #get switch at index1 (switch1)
        # while switch1 has open ports:

            #randomly pick switch2 (and track it - add it to some other checked array)
            #if switch2 not adjacent to switch1:
                #If switch2 has open port:
                    #Join switch 1 and switch 2
                    #decrement open port count for each

            #if all switches accounted for, break

        #checked.append(switch1)

        '''
        For sampling non-neighbors, just shuffle a list of non-neighbors, iterate through,
        and check whether each node is in a set of closed ports
        '''

#TODO
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numNodes', help="Number of hosts", required=True)
    parser.add_argument('--numPorts', help="Number of total ports per switch", required=True)
    parser.add_argument('--numServerPorts', help="Number of ports per switch to reserve to servers", required=True)
    parser.add_argument('--numSwitches', help="Number of Switches", required=True)
    return parser.parse_args()


# initalize the actual mininet
def main():
    '''
    args = get_args()
    numNodes = args.numNodes
    numPorts = args.numPorts
    numServerPorts = arsg.numServerPorts
    numSwitches = args.numSwitches
    '''
    numNodes = 10
    numPorts = 10
    numServerPorts = 5
    numSwitches = 10


    topo = Jellyfish(numNodes, numPorts, numServerPorts, numSwitches)
    network = Mininet(topo)

    network.start()
    network.pingAll()
    network.stop()

if __name__ == '__main__':
    main()
