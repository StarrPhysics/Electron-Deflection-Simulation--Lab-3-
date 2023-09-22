# Imports
import matplotlib.pyplot as plt
import numpy as np
from typing import NamedTuple, Union

# Simulation Parameters & Material Properties

class electron_properties:
    mass: float = 9.1093837e-31
    charge: float = 1.60217663E-19

class anode_properties:
    deltaX: float = .01
    deltaV: float = 3000 # Volts
    E_Field: float = deltaV/deltaX

class plate_properties:
    deltaY: float = .05 # cm
    deltaV: float = 3000 # Volts
    E_Field: float = (3/4) * deltaV/deltaY

electron    = electron_properties()
anode       = anode_properties()
plates      = plate_properties()

# Vector Functions and Elementary Vectors
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
    dt:float = None # dt (to be assigned upon calling start method)

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
            
    def makeRecord(self, pos: vector, vel: vector, acc: vector, simTime: float) -> None: # Produce new record for calculated simulation data
        self.records.append(self.recordStructure(position = pos, velocity = vel, acceleration = acc, simulationTime = simTime))

    def latestRecord(self) -> recordStructure: # Return latest kinematic data calculated during simulation
        return self.records[-1]
    
    def kinematicStep(self, acc: vector, displayResults = False) -> Union[None, list[vector]]: # To vector math for kinematics
        [oldPos,oldVel,lastTime] = [self.latestRecord().position, self.latestRecord().velocity, self.latestRecord().simulationTime]
        
        velNew = oldVel + acc * self.dt
        posNew = oldPos + velNew * self.dt + (.5) * acc * self.dt * self.dt
        self.makeRecord(posNew, velNew, acc, lastTime + self.dt)

        if displayResults:
            clear = '\r' + " " * 100 + '\r'
            output = f"\rTime:      {'%.4f' % (lastTime + self.dt)}\nPosition: ({'%.4f' % posNew[0]},{'%.4f' % posNew[1]})\nVelocity: ({'%.4f' % velNew[0]},{'%.4f' % velNew[1]})\nAccel:    ({'%.4f' % acc[0]},{'%.4f' % acc[1]})"
            print(output, end= '', flush=True)
            print(clear +'\033[F' + clear + '\033[F' + clear + '\033[F' + clear, end='')
            #print('\r'+'%.4f' % (lastTime + self.dt), end="", flush=True)
            #print("\r", end="", flush=True)
        
    
    def start(self, dt, displayLive = False):
        simulationComplete = False
        self.dt = dt

        self.makeRecord(-xHat*(anode.deltaX), zeroVector, zeroVector, 0.0) # Inital Conditions

        while not simulationComplete: # RUNTIME!!!!
            [xPosition, yPosition] = self.latestRecord().position

            if (xPosition < 0):   # Anode Acceleration Phase
                self.kinematicStep(xHat * anode.E_Field * electron.charge / electron.mass)
            elif (xPosition > 0): # Plate Acceleration Phase
                self.kinematicStep(yHat * plates.E_Field * electron.charge / electron.mass)

            if (yPosition >= (.5 * plates.deltaY)):
                simulationComplete = True
                print('Simulation Complete')
    


sim = simulation() # Instanciate simulation Class
sim.start(1E-10, False) # Choose dt, choose live display of data in console (broken)
[positionX, positionY, time, acceleration] = sim.getRecords(("position", 0),("position", 1), "simulationTime", "acceleration") # Retrieve data

fig, ax = plt.subplots(3)
plt.suptitle('Simulation Results')
fig.tight_layout()
ax[0].plot(time, positionX)
ax[0].set_title('x-position vs. time')
ax[0].set_xticks(time)

ax[1].plot(time, positionY)
ax[1].set_title('y-position vs. time')
ax[1].set_xticks(time)

ax[2].plot(positionX, positionY)
ax[2].set_title('y-position vs. x-position')
ax[2].set_xticks(positionX[::3])

plt.show()


