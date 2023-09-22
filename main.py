# Imports
import matplotlib.pyplot as plt
import numpy as np
from typing import NamedTuple, Union

# Simulation Parameters & Material Properties

class electron_properties:
    mass: float = 1
    charge: float = 1

class anode_properties:
    deltaX: float = 1.0
    deltaV: float = 1.0
    E_Field: float = deltaV/deltaX

class plate_properties:
    deltaY: float = 1.0
    deltaV: float = 1.0
    E_Field: float = (3/4) * deltaV/deltaY

electron    = electron_properties()
anode       = anode_properties()
plates      = plate_properties()

# Vector Functions 
vector = np.array

zeroVector  = vector([0.0,0.0])
xHat        = vector([1.0,0.0])
yHat        = vector([0.0,1.0])

# Simulation Records for Systematic Variables

class simulation:
    class recordStructure(NamedTuple):
        # This subclass exists to be the infrustructure of all records and data
        # collected during the simulation's runtime.
        position:       vector
        velocity:       vector
        acceleration:   vector
        simulationTime: float
        
        def __str__(self) -> str:
            # This built-in method is used for nice and clean presentation of
            # the data collected in each record
            time = self.simulationTime
            pos = self.position
            vel = self.velocity
            acc = self.acceleration

            return f"@ Time: {time}\nPosition:     [{pos[0]},{pos[1]}]\nVelocity:     [{vel[0]},{vel[1]}]\nAcceleration: [{acc[0]},{acc[1]}]"

    records: list[recordStructure] = list()
    dt:float = None

    def getRecords(self, *args: Union[str, tuple[str, int]]) -> Union[list[Union[float, vector]],None]:
        # *args will only recieve two types of arguments. Strings like: "position", "time", etc.
        # or  tuples such as the following: ("position", 0), ("velocity", 1).
        # The inteded purpose is to allow for reccords to be collected, but if the user
        # wishes to collected only the x or y values of a particular vector property,
        # then the method of tuple submission is avaliable.
        
        # The returned data is collectedRecords, which is a multidimentional list of all records.
        # For example:
        # If the arguments passed were ("position", 0), "velocity", "simulationTime",
        # Then collectedRecords[0] would contain all the x values (floats) of the position;
        # collectedRecords[1] would contain all the vectors (x and y) for the velocity;
        # and collectedRecords[2] would contain all the times for the simulation time.

        recordCollectionArray: list[Union[float, vector]] = []

        className = self.__class__.__name__
        
        for arg in args:
            try:
                if isinstance(arg, str):
                    properyStringName: str = arg
                    getRecordByName = lambda recordObj: getattr(recordObj,properyStringName) 
                elif isinstance(arg, tuple):
                    properyStringName: str = arg[0]
                    dimention: int = arg[1]
                    if dimention < 0: raise IndexError("Sorry, no numbers below zero")
                    getRecordByName = lambda recordObj: getattr(recordObj,properyStringName)[dimention]
                else:
                    print(f'Error(TypeError): Function argument type {type(arg)} not supported in function {self.__class__.__name__()}.getRecords()')
                    return None
            
                recordCollectionArray.append(list(map(getRecordByName, self.records)))
            except AttributeError:
                print(f"Error(AttributeError): Function \"{className}.getRecords()\" unable to fetch record propery named \"{properyStringName}\". Does not exist in simulation records.")
            except TypeError:
                print(f"Error(TypeError): Function \"{className}.getRecords()\"; unsupported operation done on record propery named \"{properyStringName}\".")
            except IndexError:
                print(f"Error(IndexError): Function \"{className}.getRecords()\"; record propery named \"{properyStringName}\" does no have index/dimension \"{dimention}\".")
        return recordCollectionArray
            
    def makeRecord(self, pos: vector, vel: vector, acc: vector, simTime: float) -> None:
        self.records.append(self.recordStructure(position = pos, velocity = vel, acceleration = acc, simulationTime = simTime))

    def latestRecord(self) -> recordStructure:
        return self.records[-1]
    
    def kinematicStep(self, acc: vector, returnResults = False) -> Union[None, list[vector]]:
        [oldPos,oldVel,lastTime] = [self.latestRecord().position, self.latestRecord().velocity, self.latestRecord().simulationTime]
        
        velNew = oldVel + acc * self.dt
        posNew = oldPos + velNew * self.dt + (.5) * acc * self.dt * self.dt

        self.makeRecord(posNew, velNew, acc, lastTime + self.dt)

        return returnResults if {"position": posNew, "velocity": velNew, "acceleration": acc} else None
    
    def start(self, dt):
        simulationComplete = False
        self.dt = dt

        #sim.makeRecord(xHat * (-anode.deltaX), zeroVector, yHat, 0.0)
        self.makeRecord(yHat*1, zeroVector, zeroVector, 0.0)
        print(yHat*1)

        while not simulationComplete:        
            '''
            if (xPos < 0):
                # Anode Acceleration Phase
                self.kinematicStep(yHat)
            elif (xPos > 0):
                # Plate Acceleration Phase
                self.kinematicStep(-self.latestRecord().position[1] * yHat)

            if (yPos >= (.5 * deltaY_plates)):
                # Simulation Complete
                simulationComplete = True
                print('Simulation Complete')
                '''
            
            if (self.latestRecord().simulationTime >= 100):
                simulationComplete = True
        
        #fig, ax = plt.subplots()
        #ax.plot(x, y)
        #plt.show()

# Runtime
sim = simulation()
sim.start(.001)
[yPosition, time] = sim.getRecords(("position", 1), "simulationTime")


fig, ax = plt.subplots()
ax.plot(time, yPosition)
plt.show()

