"""
PROJECT: SmartFlow AI - Multi-Agent Adaptive Traffic Signal Control
COURSE: BAXI 3113 Intelligent Agent (Phase 3 Final Implementation)
"""

import random, time, asyncio, threading, json
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State, CyclicBehaviour
from spade.message import Message
from spade.template import Template

# ==========================================================
# Phase 1 : THE INTELLIGENT ENVIRONMENT
# ==========================================================
class SmartEnvironment:
    def __init__(self):
        self.lanes = {'NORTH': 0, 'EAST': 0, 'SOUTH': 0, 'WEST': 0}
        self.intersection_locked = False 
        self.emergency_target = None  
        self.total_passed = 0

        for lane in self.lanes:
            self.lanes[lane] = random.randint(15, 25)

    def spawn_traffic(self):
        lane = random.choice(['NORTH', 'EAST', 'SOUTH', 'WEST'])
        # Spawning 10-20 cars per arrival to maintain pressure in a fast cycle
        self.lanes[lane] += random.randint(10, 20) 

    def clear_traffic(self, lane, capacity):
        if self.lanes[lane] > 0:
            passed = min(self.lanes[lane], capacity)
            self.lanes[lane] -= passed
            self.total_passed += passed
            return passed
        return 0

env = SmartEnvironment()

# ==========================================================
# Phase 2 : THE DIRECTIONAL AGENT (Hybrid Architecture)
# ==========================================================
class SmartFlowAgent(Agent):
    def __init__(self, jid, password, direction, next_agent_jid):
        super().__init__(jid, password)
        self.direction = direction
        self.next_agent = next_agent_jid
        self.fsm_active = False 
        self.last_turn_efficiency = 0 

    class StateGreen(State):
        async def run(self):
            # Coordination: Wait for Safety Lock
            while env.intersection_locked:
                await asyncio.sleep(0.2)

            env.intersection_locked = True
            
            # --- SIMULATION TIMER TRAFFIC (10s) ---
            # The parameter can be adjusted everytime for simulation
            duration = 10 
            queue_at_start = env.lanes[self.agent.direction]
            
            print(f"\n[{self.agent.jid}] >>> GREEN: {self.agent.direction}")
            
            # Simulates realistic discharge rates (not all cars clear in one turn)
            friction_factor = random.uniform(0.65, 0.90)
            physical_capacity = int(queue_at_start * friction_factor)
            
            # Minimum clearance for very small queues
            if queue_at_start < 5: physical_capacity = queue_at_start

            passed = env.clear_traffic(self.agent.direction, physical_capacity)
            
            if queue_at_start > 0:
                self.agent.last_turn_efficiency = int((passed / queue_at_start) * 100)
            else:
                self.agent.last_turn_efficiency = 100
            
            print(f"[{self.agent.jid}] ACTION: Cleared {passed}/{queue_at_start} cars. (Wait: {duration}s)")
            
            # Preemption Check Loop (Runs for 10s unless interrupted)
            for _ in range(duration * 2):
                if env.emergency_target and env.emergency_target != self.agent.direction:
                    print(f"[{self.agent.jid}] !!! PREEMPTION: Ending Green early for Emergency !!!")
                    break
                await asyncio.sleep(0.5)
            
            self.set_next_state("STATE_YELLOW")

    class StateYellow(State):
        async def run(self):
            print(f"[{self.agent.jid}] TRANSITION: {self.agent.direction} YELLOW")
            await asyncio.sleep(2)
            self.set_next_state("STATE_RED")

    class StateRed(State):
        async def run(self):
            print(f"[{self.agent.jid}] SAFETY: {self.agent.direction} RED")
            
            # Emergency Reset
            if env.emergency_target == self.agent.direction:
                print(f"[{self.agent.jid}] EMERGENCY CLEARED. Resuming cycle.")
                env.emergency_target = None
            
            env.intersection_locked = False
            self.agent.fsm_active = False 

            # COORDINATION: Multi-agent Handover
            if not env.emergency_target:
                msg = Message(to=self.agent.next_agent)
                msg.set_metadata("performative", "inform")
                msg.body = "YOUR_TURN"
                await self.send(msg)
            
            # Performance Measure Report
            print(f"[{self.agent.jid}] THROUGHPUT: {env.total_passed} cars | CLEARANCE EFFICIENCY: {self.agent.last_turn_efficiency}%")

    def start_logic(self):
        if not self.fsm_active:
            self.fsm_active = True
            fsm = FSMBehaviour()
            fsm.add_state(name="STATE_GREEN", state=self.StateGreen(), initial=True)
            fsm.add_state(name="STATE_YELLOW", state=self.StateYellow())
            fsm.add_state(name="STATE_RED", state=self.StateRed())
            fsm.add_transition(source="STATE_GREEN", dest="STATE_YELLOW")
            fsm.add_transition(source="STATE_YELLOW", dest="STATE_RED")
            self.add_behaviour(fsm)

    class MainListener(CyclicBehaviour):
        async def run(self):
            # Listen for turn messages
            msg = await self.receive(timeout=0.5)
            if msg and "YOUR_TURN" in msg.body:
                if not env.emergency_target:
                    self.agent.start_logic()
            
            # Listen for siren sense
            if env.emergency_target == self.agent.direction:
                self.agent.start_logic()

    async def setup(self):
        self.add_behaviour(self.MainListener())

# ==========================================================
# Phase 3 : EXECUTION
# ==========================================================
def run_physics():
    while True:
        env.spawn_traffic()
        time.sleep(1.5) # Fast spawning for a fast simulation

async def main():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found!")
        return
    
    password = config["xmpp_password"]
    jids = config["agents"]

    print("--- SmartFlow AI - Multi-Agent Adaptive Traffic Signal Control ---")
    threading.Thread(target=run_physics, daemon=True).start()

    agents = {
        "NORTH": SmartFlowAgent(jids["NORTH"], password, "NORTH", jids["EAST"]),
        "EAST":  SmartFlowAgent(jids["EAST"],  password, "EAST",  jids["SOUTH"]),
        "SOUTH": SmartFlowAgent(jids["SOUTH"], password, "SOUTH", jids["WEST"]),
        "WEST":  SmartFlowAgent(jids["WEST"],  password, "WEST",  jids["NORTH"])
    }
    
    for a in agents.values(): await a.start()
    await asyncio.sleep(2)
    agents["NORTH"].start_logic()

    try:
        while True:
            # Siren triggers every 25 seconds for the demo
            await asyncio.sleep(25) 
            target = random.choice(['NORTH', 'EAST', 'SOUTH', 'WEST'])
            print(f"\n[SYSTEM] SIREN: EMERGENCY ON {target} ROAD!")
            env.emergency_target = target 
    except KeyboardInterrupt:
        for a in agents.values(): await a.stop()

if __name__ == "__main__":
    asyncio.run(main())