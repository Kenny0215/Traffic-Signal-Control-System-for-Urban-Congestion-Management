import random, time, threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

class TrafficSimulation:
    def __init__(self):
        self.directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.phases = [
            {'green': 'NORTH_GREEN', 'yellow': 'NORTH_YELLOW'},
            {'green': 'EAST_GREEN', 'yellow': 'EAST_YELLOW'},
            {'green': 'SOUTH_GREEN', 'yellow': 'SOUTH_YELLOW'},
            {'green': 'WEST_GREEN', 'yellow': 'WEST_YELLOW'}
        ]
        self.current_phase_idx = 0
        self.kb = {
            "vehicles": [],
            "current_signal": "NORTH_GREEN",
            "timer": 30.0,
            "throughput": 0,
            "is_clearing_junction": False
        }
        self.last_time = time.time()

    def run(self):
        while True:
            now = time.time()
            dt = now - self.last_time
            self.last_time = now

            # 1. Spawning
            if random.random() < 0.15: 
                lane = random.choice(self.directions)
                if not any(v for v in self.kb['vehicles'] if v['lane'] == lane and v['progress'] < 0.25):
                    self.kb['vehicles'].append({
                        "id": str(random.randint(10000, 99999)),
                        "lane": lane,
                        "progress": 0.0,
                        "speed": 0.45 + random.random() * 0.1, 
                        "color": random.choice(['#6366f1', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6']),
                        "turn": random.choice(['straight', 'left']),
                        "moving": True
                    })

            # 2. Smart Signal Logic (Non-blocking)
            self.kb['timer'] -= dt
            
            # Check if any car is currently in the "Danger Zone" (the middle of the turn)
            junction_occupied = any(1.0 <= v['progress'] <= 1.35 for v in self.kb['vehicles'])

            if self.kb['timer'] <= 0:
                curr_p = self.phases[self.current_phase_idx]
                
                if self.kb['current_signal'] == curr_p['green']:
                    # Switch to Yellow
                    self.kb['current_signal'] = curr_p['yellow']
                    self.kb['timer'] = 3.0
                else:
                    # Switch to NEXT Green ONLY if junction is clear (The "Smart" part)
                    if not junction_occupied:
                        self.current_phase_idx = (self.current_phase_idx + 1) % 4
                        self.kb['current_signal'] = self.phases[self.current_phase_idx]['green']
                        self.kb['timer'] = 30.0
                    else:
                        # Hold Red for safety until the junction is clear
                        self.kb['current_signal'] = "ALL_RED"

            # 3. Physics & Realistic Queuing
            new_vehicles = []
            # Sort front to back
            sorted_vehs = sorted(self.kb['vehicles'], key=lambda x: x['progress'], reverse=True)
            
            for v in sorted_vehs:
                is_green = self.kb['current_signal'] == f"{v['lane']}_GREEN"
                can_move = True
                
                # A. Stop Line Check
                if 0.78 <= v['progress'] <= 0.81 and not is_green:
                    can_move = False
                
                # B. Advanced Car-Following (Gap depends on turn type)
                ahead = [o for o in sorted_vehs if o['lane'] == v['lane'] and o['progress'] > v['progress']]
                if ahead:
                    front_car = min(ahead, key=lambda x: x['progress'])
                    
                    # If car in front is turning left, it moves "slower" spatially. 
                    # We increase the required safety gap (0.22 instead of 0.18)
                    safe_gap = 0.22 if front_car['turn'] == 'left' else 0.18
                    
                    if front_car['progress'] - v['progress'] < safe_gap:
                        can_move = False

                v['moving'] = can_move
                if can_move or v['progress'] > 0.85:
                    v['progress'] += v['speed'] * dt
                
                if v['progress'] < 2.5:
                    new_vehicles.append(v)
                    if 1.49 < v['progress'] < 1.55: self.kb['throughput'] += 1

            self.kb['vehicles'] = new_vehicles
            time.sleep(0.01)

sim = TrafficSimulation()
@app.route('/')
def index(): return render_template('index.html')
@app.route('/data')
def data(): return jsonify(sim.kb)

if __name__ == '__main__':
    threading.Thread(target=sim.run, daemon=True).start()
    app.run(debug=True, port=5000, use_reloader=False)