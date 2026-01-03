SmartFlow: A Multi-Agent Adaptive Traffic Signal Control System

SmartFlow is an intelligent, decentralized traffic management system designed to solve urban congestion. Unlike traditional fixed-time traffic signals, SmartFlow uses a multi-agent approach where each intersection acts as an autonomous agent that communicates with its neighbors to optimize traffic flow in real-time, prioritize emergency vehicles, and reduce commute times.

This project was developed for the BAXI 3113 Intelligent Agent course at Universiti Teknikal Malaysia Melaka (UTeM).

🚀 Project Overview

Traditional traffic lights operate on static cycles, leading to wasted time at empty intersections and massive congestion during peak hours. SmartFlow replaces these static loops with a Utility-Based Decision Engine that calculates the optimal green-light duration based on real-time vehicle density and safety constraints.

Key Features

Decentralized Coordination: Uses the SPADE framework and XMPP protocol to eliminate single points of failure.

Emergency "Green Waves": Instant override mode to prioritize ambulances and emergency services.

Utility-Based Logic: Dynamically calculates traffic "urgency" by weighing queue lengths against waiting times.

Pedestrian Safety: Integrated safety timers to ensure minimum crossing times are always met.

Scalability: Designed to support a grid of multiple connected intersections.

🏗️ Agent Architecture

The SmartFlow agent operates as a continuous control loop consisting of the following modules:

Perception Module: Gathers raw data (vehicle counts) from sensors (cameras/induction loops).

Communication Layer (XMPP): Enables inter-agent messaging to coordinate traffic flow with neighboring intersections.

Knowledge Base: Stores dynamic variables like queue density, safety timers, and emergency flags.

Decision Engine: Employs utility-based logic to decide whether to maintain the current state or switch phases.

Action Handler: Translates high-level decisions into hardware commands (Red/Yellow/Green signals).

Decision Modes

Normal Operation: Sense → Analyze → Calculate Utility → Act

Emergency Override: Detects high-priority signals (Ambulance ID) and shortcuts directly to the Decision Engine to force a green light, ensuring zero-latency response.

🛠️ Technology Stack

Framework: SPADE (Smart Python Agent Development Environment)

Language: Python 3.x

Protocol: XMPP (Extensible Messaging and Presence Protocol)

Modeling: Utility-based Agent & Finite State Machine (FSM)

📋 Task Requirements (Phase 2 Design)

The agent utilizes specific SPADE behaviors:

CyclicBehaviour: For continuous sensor polling.

FSMBehaviour: To manage signal states and safety transitions.

Message Pattern Matching: To distinguish between routine traffic updates and high-priority emergency alerts.

👥 Contributors
Name	Matric No.
THIM WONG	B032310558
KENNY KHOW JIUN XIAN	B032310349
NG GUO HENG	B032310331
ANG WEI EN	B032310502
TAY SHER YANG	B032310363
🛠️ Setup & Installation (Coming Soon)

Note: This project is currently in the design phase (Phase 2). Implementation details will follow.

To prepare the environment:

code
Bash
download
content_copy
expand_less
pip install spade
🤖 Generative AI Usage

This project utilized Google AI Studio (Gemini) for technical reasoning, vetting multi-agent frameworks (selecting SPADE over Mesa), and refining the agent's decision-making hierarchy.

🏛️ Institution

Faculty of Artificial Intelligence and Cyber Security (FAIX)
Universiti Teknikal Malaysia Melaka (UTeM)