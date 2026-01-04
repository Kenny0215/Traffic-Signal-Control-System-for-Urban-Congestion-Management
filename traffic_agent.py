import random
import time
import asyncio
import threading
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

# ==========================================================
# 1: THE SIMULATION (The Environment)
# ==========================================================
class TrafficEnvironment:
    def __init__(self):
        self.lanes = {'NORTH': 0, 'EAST': 0, 'SOUTH': 0, 'WEST': 0}
        self.current_light = 'ALL_RED'
        self.emergency_flag = False
        self.total_throughput = 0

    def spawn_traffic(self):
        lane = random.choice(['NORTH', 'EAST', 'SOUTH', 'WEST'])
        self.lanes[lane] += random.randint(1, 3)

    def clear_traffic(self, lane):
        if self.lanes[lane] > 0:
            passed = min(self.lanes[lane], 5)
            self.lanes[lane] -= passed
            self.total_throughput += passed
            return passed
        return 0

env = TrafficEnvironment()

# ==========================================================
# 2: THE INTELLIGENT AGENT (SPADE Framework)
# ==========================================================
class SmartFlowAgent(Agent):
    
    class TrafficFSM(FSMBehaviour):
        async def on_start(self):
            print(f"[{self.agent.jid}] Starting Decision Engine ...")

    class StateGreen(State):
        async def run(self):
            print("\n--- NEW DECISION CYCLE ---")
            
            # 1. PERCEPTION
            if env.emergency_flag:
                print("[PERCEPTION] !! EMERGENCY VEHICLE DETECTED !!")
                target_lane = 'NORTH'
                env.emergency_flag = False
            else:
                # 2. SEQUENCE LOGIC
                target_lane = self.agent.order[self.agent.current_idx]
                # Save this as the 'active' lane so other states can see it
                self.agent.last_lane = target_lane 
                
                print(f"[DECISION] Fixed Sequence: Current turn is {target_lane}")
                
                # Update index for the NEXT lane
                self.agent.current_idx = (self.agent.current_idx + 1) % 4

            # 3. ACTION
            env.current_light = f"{target_lane}_GREEN"
            print(f"[ACTION] Signal switched to {env.current_light}")
            
            # 4. EXECUTION
            print(f"[STATUS] Cars waiting in {target_lane}: {env.lanes[target_lane]}")
            passed = env.clear_traffic(target_lane)
            print(f"[EXECUTION] {passed} cars passed. Total Throughput: {env.total_throughput}")

            await asyncio.sleep(3) 
            self.set_next_state("STATE_YELLOW")

    class StateYellow(State):
        async def run(self):
            current_lane = self.agent.last_lane # Get the lane that was just green
            env.current_light = f"{current_lane}_YELLOW"
            print(f"[SAFETY] Transitioning: {env.current_light} (Warning)")
            await asyncio.sleep(2)
            self.set_next_state("STATE_RED")

    class StateRed(State):
        async def run(self):
            # 1. Identify current vs next
            stopped_lane = self.agent.last_lane
            next_lane = self.agent.order[self.agent.current_idx]
            
            # 2. Update environment
            env.current_light = f"{stopped_lane}_RED"
            
            # 3. Print specific handover message as requested
            print(f"[STATUS] {stopped_lane} is now RED. Passing control to {next_lane}...")
            
            await asyncio.sleep(1) # Brief clearance interval
            self.set_next_state("STATE_GREEN")

    async def setup(self):
        self.order = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.current_idx = 0
        self.last_lane = 'NORTH' # Initial placeholder
        
        fsm = self.TrafficFSM()
        fsm.add_state(name="STATE_GREEN", state=self.StateGreen(), initial=True)
        fsm.add_state(name="STATE_YELLOW", state=self.StateYellow())
        fsm.add_state(name="STATE_RED", state=self.StateRed())
        
        fsm.add_transition(source="STATE_GREEN", dest="STATE_YELLOW")
        fsm.add_transition(source="STATE_YELLOW", dest="STATE_RED")
        fsm.add_transition(source="STATE_RED", dest="STATE_GREEN")
        
        self.add_behaviour(fsm)

# ==========================================================
# 3: EXECUTION
# ==========================================================

def run_background_sim():
    while True:
        env.spawn_traffic()
        if random.random() < 0.05:
            env.emergency_flag = True
        time.sleep(5)

async def main():
    sim_thread = threading.Thread(target=run_background_sim, daemon=True)
    sim_thread.start()

    agent = SmartFlowAgent("traffic_agent@127.0.0.1", "password123")
    await agent.start()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())