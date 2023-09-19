# Imports
import matplotlib.pyplot as plt
import numpy as np
from typing import NamedTuple, Union

print('Test')

vector = np.ndarray

# Simulation Resolution
dt: float = 1 # Seconds

# Simulation Parameters & Material Properties
electronMass: float = 1 # in kg

anode   = {'deltaX': 1.0, 'deltaV': 1.0}

plates  = {'deltaY': 1.0, 'deltaV': 1.0, 'E_Field_Magnitude': float}

plates['E_Field_Magnitude'] = (3/4) * plates['deltaV'] / plates['deltaY']

# Elementary Vectors
zeroVector  = np.array([0.0,0,0])
xHat        = np.array([1.0,0.0])
yHat        = np.array([0.0,1.0])

# Simulation Records for Systematic Variables

class simulation:
    class recordStructure(NamedTuple):
        position:       vector
        velocity:       vector
        acceleration:   vector
        simulationTime: float
    
    raw = list[recordStructure]

    def makeRecord(self, pos: vector, vel: vector, acc: vector, simTime: float) -> None:
        self.raw.append(self.recordStructure(position = pos, velocity = vel, acceleration = acc, simulationTime = simTime))

    def latestRecord(self) -> recordStructure:
        return self.raw[-1]
    
    def kinematicStep(self, acc: vector, returnResults = False) -> Union(None,list[vector]):
        [oldPos,oldVel] = [self.latestRecord().position,self.latestRecord().velocity]

        velNew = oldVel + acc * dt
        posNew = oldPos + acc * dt + (.5) * acc * dt * dt
        return [posNew,velNew]


sim = simulation()

# Runtime
def launchSimulationRuntime():
    simulationComplete = False

    sim.makeRecord(xHat * (-anode['deltaX']), zeroVector, yHat, 0.0)

    while not simulationComplete:
        latestRecord = sim.latestRecord()

        sim.kinematicStep(yHat)

        if (sim.latestRecord().position[0] >= 10):
            simulationComplete = True


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