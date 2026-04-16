# SDN Mininet Simulation - Packet Drop Simulator (Orange Problem)

**Author:** Vijay Suriya P
**SRN:** PES1UG24AM320
**Course:** UE24CS252B - Computer Networks

## 1. Problem Statement
[cite_start]The goal of this assignment is to implement an SDN-based solution using Mininet and an OpenFlow controller (POX) that demonstrates controller-switch interaction and flow rule design (match-action)[cite: 3, 4, 5]. 

The specific objective is to create a custom network topology and program the POX controller to act as a Level 2 learning switch for all regular traffic, while functioning as an access control filter to explicitly block (DROP) packets between a specific source and destination (Host 1 to Host 3).

## 2. Network Topology
* **Controller:** POX (Remote, IP: 127.0.0.1, Port: 6633)
* **Switch:** 1 Open vSwitch (s1)
* **Hosts:** 4 Hosts connected to s1 (h1, h2, h3, h4)
* **Target Rule:** `h1 (10.0.0.1)` cannot communicate with `h3 (10.0.0.3)`. All other network communication is allowed.

## [cite_start]3. Setup and Execution Steps [cite: 32]
This project utilizes a `run.sh` script to automate the execution environment.

**Step 1: Initial Setup (One-time only)**
Installs POX and moves the custom controller script to the correct directory.
```bash
chmod +x run.sh
./run.sh setup
