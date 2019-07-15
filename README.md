# BigTrustScheduling

Big data task scheduling in cloud computing environments has gained considerable attention in the past few years, due to the
exponential growth in the number of businesses that are relying on cloud-based infrastructure as a backbone for big data storage
and analytics. The main challenge in scheduling big data services in cloud-based environments is to guarantee minimal makespan 
while minimizing at the same time the amount of utilized resources. Several approaches have been proposed in an attempt to 
overcome this challenge. The main limitation of these approaches stems from the fact that they overlook the trust levels of the 
Virtual Machines (VMs), thus risking to endanger the overall Quality of Service (QoS) of the big data analytics process. 
To overcome this limitation, we propose in this work a trust-aware scheduling solution called BigTrustScheduling that consists 
of three stages: VMs' trust level computation, tasks priority level determination, and trust-aware scheduling. Experiments conducted
using real-world datasets collected from Google Cloud Platform pricing and Bitbrains tasks resource requirements show that our solution
minimizes the makespan by 59% compared to the Shortest Job First (SJF), by 48% compared to the Round Robin (RR), and by 40% compared to
the improved Particle Swarm Optimization (PSO) approaches in the presence of untrusted VMs. Moreover, our solution decreases the monetary
cost by 58% compared to the SJF, by 47% compared to the RR, and by 38% compared to the improved PSO in the presence of untrusted VMs.

## Getting started

## Requirements

* python 
* java 

## Implementation
There are two files for the code
* We use cloudsim to calculate the trust value for the VMs.
* 
* We employ a datset collected by Bitbrains, a service provider that is specialized in managed hosting and business computation for enterprises. 
