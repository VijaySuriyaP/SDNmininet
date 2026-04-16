# SDN Mininet Simulation - Packet Drop Simulator (Orange Problem)

**Author:** Vijay Suriya P  
**SRN:** PES1UG24AM320  
**Course:** UE24CS252B - Computer Networks  

## 1. Problem Statement
The goal of this assignment is to implement an SDN-based solution using Mininet and an OpenFlow controller (POX) that demonstrates controller-switch interaction and flow rule design (match-action). 

The specific objective is to create a custom network topology and program the POX controller to act as a Level 2 learning switch for all regular traffic, while functioning as an access control filter to explicitly block (DROP) packets between a specific source and destination (Host 1 to Host 3).

## 2. Network Topology
* **Controller:** POX (Remote, IP: 127.0.0.1, Port: 6633)
* **Switch:** 1 Open vSwitch (s1)
* **Hosts:** 4 Hosts connected to s1 (h1, h2, h3, h4)
* **Target Rule:** `h1 (10.0.0.1)` cannot communicate with `h3 (10.0.0.3)`. All other network communication is allowed.

## 3. Setup and Execution Steps
This project utilizes a `run.sh` script to automate the execution environment.

### Step 1: Initial Setup (One-time only)
Installs POX and moves the custom controller script to the correct directory.
```bash
chmod +x run.sh
./run.sh setup
```

### Step 2: Start the POX Controller
Open Terminal 1 and start the controller (Leave this terminal open):
```bash
./run.sh controller
```

### Step 3: Start the Mininet Topology
Open Terminal 2 and start the custom topology:
```bash
./run.sh topology
```

### Step 4: View Flow Tables
Open Terminal 3 to view the OpenFlow rules actively installed on switch `s1`:
```bash
./run.sh flowtable
```

### Step 5: Cleanup
After exiting Mininet, clean up the environment:
```bash
./run.sh clean
```

## 4. Expected Output
Inside the Mininet CLI (`mininet>`), run the following commands to verify the functional behavior:

* `h1 ping -c 4 h2`: Should succeed (0% packet loss).
* `h1 ping -c 4 h3`: Should fail (100% packet loss) due to the DROP flow rule.
* `pingall`: Shows an `X` specifically between h1 and h3, while all other host pairs show successful pings.
* `iperf h1 h2`: Displays the TCP bandwidth/throughput between allowed hosts.

## 5. Proof of Execution

### A. Allowed vs Blocked Testing
Demonstrating functional correctness where h1 can reach h2, but h1 is explicitly blocked from reaching h3.  

<img width="1280" height="800" alt="Screenshot from 2026-04-16 11-07-25" src="https://github.com/user-attachments/assets/8f9c7bb1-eb2b-4922-92e3-decf725a751a" />

<img width="1280" height="800" alt="image" src="https://github.com/user-attachments/assets/08da161d-3d2d-4559-a399-91b0583d32fb" />



### B. Pingall Results
Complete network sweep verifying isolated packet drop behavior.  

<img width="1280" height="800" alt="image" src="https://github.com/user-attachments/assets/bb4ed650-4c99-4f33-b4cc-a10144b9c7a5" />


### C. Throughput Observation (iperf)
Measurement of TCP bandwidth between h1 and h2.  

<img width="1280" height="800" alt="image" src="https://github.com/user-attachments/assets/5d1b56d6-99c2-4ce9-86ef-551a51d4027a" />

### D. OpenFlow Flow Tables
Verification of the match-action DROP rule installed on switch s1 (showing `nw_src=10.0.0.1, nw_dst=10.0.0.3 actions=drop` with intercepted packet counts).  

<img width="1280" height="800" alt="image" src="https://github.com/user-attachments/assets/4a04560c-8981-4812-855f-9ede32bb22c6" />
