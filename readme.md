# 🚦 SmartFlow: A Multi-Agent Adaptive Traffic Signal Control System

SmartFlow is an intelligent, decentralized traffic signal control system designed to address urban traffic congestion using multi-agent technology. Unlike traditional fixed-time traffic lights, SmartFlow allows each intersection to act as an autonomous agent that communicates with neighboring intersections to optimize traffic flow in real time.

---

## 🚀 Project Overview

Traditional traffic signal systems operate on static timing cycles, which often lead to inefficient traffic flow—green lights at empty intersections and long waiting times during peak hours.

SmartFlow replaces static cycles with a **Utility-Based Decision Engine** that dynamically adjusts traffic signals based on:
- Real-time vehicle density
- Waiting time
- Safety constraints
- Emergency vehicle priority

---

## ✨ Key Features

- **Utility-Based Decision Logic**  
  Calculates traffic urgency using queue length and waiting time.

- **Scalable Design**  
  Supports multiple connected intersections in a grid layout.

---

## 🏗️ Agent Architecture

Each intersection is modeled as an autonomous agent consisting of the following components:

- **Knowledge Base**  
  Stores dynamic information such as:
  - Vehicle queue density
  - Safety timers
  - Emergency flags

- **Decision Engine**  
  Applies utility-based logic to determine optimal signal phases.

- **Action Handler**  
  Executes decisions by controlling traffic lights (Red / Yellow / Green).

---

---

## 🛠️ Technology Stack

- **Programming Language:** Python 3.x  
- **Framework:** SPADE (Smart Python Agent Development Environment)
- **Agent Model:** Utility-Based Agent  
- **Control Logic:** Finite State Machine (FSM)

---

