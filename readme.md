# 🚦 SmartFlow: Adaptive Traffic Signal Control System

SmartFlow is an **intelligent, decentralized traffic signal control system** developed using the **SPADE (Smart Python Agent Development Environment)** framework. It transforms conventional fixed-time traffic lights into **autonomous, cooperative agents** capable of real-time decision-making, coordination, and emergency prioritization.

---

## 📖 Project Overview

Traditional traffic signal systems operate on static schedules, often causing **“ghost waiting”**—vehicles stopped at red lights despite no cross-traffic. This leads to unnecessary delays, increased fuel consumption, and higher emissions.

**SmartFlow** addresses these issues by modeling each intersection as an **Intelligent Utility-Based Agent** that dynamically adapts to traffic conditions using FSM-based logic and inter-agent communication.

By leveraging **Finite State Machines (FSM)** and **XMPP-based communication**, SmartFlow improves traffic throughput, reduces congestion, and ensures efficient urban mobility.

---

## 🧠 Agent Architecture

SmartFlow agents follow a **Sense–Think–Act** cycle implemented through a **Finite State Machine (FSM)**.

### 1️⃣ PEAS Framework

- **Performance Measure**
  - Maximize vehicle throughput
  - Minimize average waiting time
  - Ensure successful emergency vehicle preemption

- **Environment**
  - Dynamic and stochastic urban **4-way intersection**

- **Actuators**
  - Traffic signal controllers (Red, Yellow, Green)

- **Sensors**
  - Simulated induction loops
  - Traffic cameras
  - Emergency broadcast signals

---

### 2️⃣ Finite State Machine (FSM) Control Logic

| State | Description |
|------|------------|
| `STATE_GREEN` | Acting phase – clears traffic based on clockwise order or traffic density |
| `STATE_YELLOW` | Safety transition – warns drivers before stopping |
| `STATE_RED` | Clearance phase – all-red interval ensures intersection is empty |

---

## ✨ Key Features

- **Decentralized Coordination**  
  Each traffic intersection operates as an independent SPADE agent and communicates with neighboring agents using **XMPP**.

- **Emergency Preemption**  
  Detects emergency vehicles (ambulance/police) and immediately overrides normal signal cycles.

- **Clockwise Signal Handover**  
  Fair and predictable rotation:
  **North → East → South → West**

- **Quality of Service (QoS) Tracking**  
  - Total vehicle throughput
  - Average waiting time per vehicle

---

## 🛠️ Technology Stack

- **Language:** Python 3.10+
- **Framework:** SPADE (Smart Python Agent Development Environment)
- **Protocol:** XMPP (Extensible Messaging and Presence Protocol)
- **Server:** Openfire (Local XMPP Server)
- **Libraries:** `asyncio`, `threading`, `flask` (optional)

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites

- Install **Python 3.x**
- Install **Openfire XMPP Server**


---

### 2️⃣ Install Dependencies

pip install spade


### 3️⃣ Run the System

python traffic_agent.py

⚠️ Ensure the Openfire server is running before executing the agent.
