# Cloud Computing Project: Load Balancing in Jellyfish Networks


### [Instructions for Peer Validators](https://docs.google.com/document/d/1gw0bQXfTPnE98h_51koCD04AAzTgu5nammc-pARR2Jw/edit?usp=sharing)

### Instructions to Run Basic Network
Start up the VM on GCP. In a terminal window, type:
``` code
 $ ssh [external IP]
 $ cd ../kat/cs419-project
 $ sudo python jellyfish_network.py
 ```
You should now be in the Mininet CLI and can perform some basic tests.

``` code
mininet> pingall
mininet> h0 iperf -s -e &
mininet> h1 iperf -c h0 -e
```
To exit the CLI, type:
``` code
mininet> exit

```
Clear the network after each run. To clear the network, type:
``` code
$ sudo mn -c
```

### Instructions to Run Remote Controller

Start up the VM on GCP. In two separate terminal windows, type:
``` code
 $ ssh [external IP]
 $ cd ../kat/cs419-project/jellyfish
 ```
In terminal window 1, run this command to generate a saved graph (adjaceny list), routing files, and iperf test files:
``` code
$ python generate.py
```
In terminal window 2, start the remote controller:
``` code
$ ~/pox/pox.py riplpox.riplpox --topo=jelly,20,20,5,graph_adjlist --routing=jelly,ecmp_8_test --mode=reactive
```
In terminal window 1, start the network:
``` code
$ sudo mn --custom ~/ripl/ripl/mn.py --topo=jelly,20,20,5,graph_adjlist --controller=remote --mac
```

You should now be in the Mininet CLI and can perform some iperf tests.

### Perform Tests in the Mininet CLI

Perform an initial pingall to ensure network connectivity. It is likely that packets are initially dropped. Wait approximately 30 seconds or until packets start to be recieved before retrying pingall.
``` code
mininet> pingall
```

After achieving successful connectivity, perform iperf tests by typing these commands into the CLI:
``` code
mininet> source ../perftest/tests/single_flow
mininet> source ../perftest/tests/eight_flow
```

To view the results, wait a few minutes and exit the Mininet CLI by typing ``` mininet> exit ```. View tests results under directory ``` perftest/results ``` After exiting the Mininet CLI in window 1, exit the pox controller in window 2 by hitting ctrl-D.



### Lingering Issues
- FIXED, pingall now reaches all hosts. ~~After some research and a lot of headache, I've discovered that Mininet does not work well with cycles in a graph, which is why it's dropping packets.~~ Manually specified 10.0.X.X IP addresses and added stp and failMode params to addSwitch() calls.
- FIXED, wrote a script with tests. Call script using ``` source ``` command in Mininet CLI. ~~Iperf tests with multiple hosts at a time (via script). Could add logic to Mininet startup in jellyfish_network.py script but this does not work with the remote controller since Mininet startup is handled by ripl.~~

### Progress Achieved
- Built and tested custom Jellyfish topo and network. Our network is based on topology described in [Jellyfish: Networking Data Centers Randomly](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf).
- Configured network to work with a remote controller. Added custom topology flag to ripl/ripl/mn.py (``` topo=jelly,[NHOSTS][NSWITCHES],[NPORTS],[ADJLIST_FILE] ```) which directs to our topo in jellyfish_network.py.
- Separated graph creation from network creation. Before this, we were generating the graph topology at Mininet startup time. Graph is now pre-generated and saved as an adjaceny list. This allows us to generate routing schemes for the saved graph. Jellyfish topo processes the adjacency list file to build the network.
- Added logic for ECMP and routing file output. Routing is "calculated" based on the saved graph and outputted in pickle format.
- Modified getRouting() in riplpox/riplpox/util.py and riplpox/riplpox/riplpox.py for custom routing flag (```--routing=jelly[ROUTING FILE]```) and argument parsing. Added the i/o to process the pkl routing file in JellyfishRouting class in ripl/ripl/routing.py.

### Next Steps
- More robust iperf testing
- K-shortest paths routing

### References
- Paper: [Jellyfish: Networking Data Centers Randomly, Singla et al](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final82.pdf)
- Paper: [A Heuristic Approach to Finding Diverse Short Paths, Voss et al](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7139774)
- Repository [mininet/mininet](https://github.com/mininet/mininet)
- Repository: [brandonheller/ripl](https://github.com/brandonheller/ripl)
- Repository: [brandonheller/riplpox](https://github.com/brandonheller/riplpox)
- Reporitory: [lechengfan](https://github.com/lechengfan/cs244-assignment2/tree/f4f0f06fbb939a8a3bb9a10bd3446363f53bf6b2)
