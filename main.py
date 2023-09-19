# Imports
import matplotlib.pyplot as plt
import numpy as np
from typing import NamedTuple, Union

# Simulation Resolution
dt: float = 1 # Seconds

# Simulation Parameters & Material Properties
electronMass: float = 1 # in kg

class anode_properties:
    deltaX: float = 1.0
    deltaV: float = 1.0
    E_Field: float = deltaV/deltaX

class plate_properties:
    deltaY: float = 1.0
    deltaV: float = 1.0
    E_Field: float = (3/4) * deltaV/deltaY

anode   = anode_properties()
plates  = plate_properties()

# Vector Functions 
vector = np.array

zeroVector  = vector([0.0,0.0])
xHat        = vector([1.0,0.0])
yHat        = vector([0.0,1.0])

# Simulation Records for Systematic Variables

class simulation:
    class recordStructure(NamedTuple):
        position:       vector
        velocity:       vector
        acceleration:   vector
        simulationTime: float
        
        def __str__(self) -> str:
            time = self.simulationTime
            pos = self.position
            vel = self.velocity
            acc = self.acceleration

            return f"@ Time: {time}\nPosition: [{pos[0]},{pos[1]}]\nVelocity: [{vel[0]},{vel[1]}]\nAcceleration: [{acc[0]},{acc[1]}]"
    
    
    records: list[recordStructure] = list()

    def makeRecord(self, pos: vector, vel: vector, acc: vector, simTime: float) -> None:
        self.records.append(self.recordStructure(position = pos, velocity = vel, acceleration = acc, simulationTime = simTime))

    def latestRecord(self) -> recordStructure:
        return self.records[-1]
    
    def kinematicStep(self, acc: vector, returnResults = False) -> Union[None, list[vector]]:
        [oldPos,oldVel,lastTime] = [self.latestRecord().position, self.latestRecord().velocity, self.latestRecord().simulationTime]
        
        velNew = oldVel + acc * dt
        posNew = oldPos + acc * dt + (.5) * acc * dt * dt

        self.makeRecord(posNew, velNew, acc, lastTime + dt)

        return returnResults if {"position": posNew, "velocity": velNew, "acceleration": acc} else None

# Runtime
def launchSimulationRuntime():
    sim = simulation()
    simulationComplete = False

    #sim.makeRecord(xHat * (-anode.deltaX), zeroVector, yHat, 0.0)
    sim.makeRecord(zeroVector, zeroVector, yHat, 0.0)

    while not simulationComplete:

        sim.kinematicStep(yHat)

        print(sim.latestRecord().position[1] >= 10.0)

        if (sim.latestRecord().position[1] >= 10):
            simulationComplete = True

    print(sim.records)

launchSimulationRuntime()

'''
if (xPos < 0):
    # Anode Acceleration Phase
    kinematicStep(pos, vel)
elif (xPos > 0):
    # Plate Acceleration Phase
    print('')

if (yPos >= (.5 * deltaY_plates)):
    # Simulation Complete
    simulationComplete = True
    print('Simulation Complete')
'''