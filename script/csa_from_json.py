import csa
import nest
import json
import sys
import time

class Population:
    """Represents a population of neurons"""
    def __init__(self, name, size, neuronModel):
        """
        :param name: The name of the population
        :param size: The size of the population (number of neurons)
        :param neuronModel: The NEST neuron model to use
        """
        self.name = name
        assert(size > 0)
        self.size = size
        self.neuronModel = neuronModel

        self.interval = self._createPopulation(self.neuronModel, self.size)

    def _createPopulation(self, neuronModel, size):
        """Creates the GIDs for this population
        In this instance, the GIDs are created in NEST for later use in the simulation"""
        nestIDs = nest.Create(neuronModel, size)
        interval = csa.ival(nestIDs[0], nestIDs[-1])
        return interval

    def getConnectionSet(self, target):
        """Returns a connection set of possible connections between this population 
        and a target population in terms of global IDs.
        The returned csa object is a rectangular mask that can be used to intersect other csets."""
        return csa.cross(self.getInterval(), target.getInterval())

    def getInterval(self):
        """Returns the global interval of this population as a csa interval"""
        return self.interval

inputNameDict = {
    'poisson': 'poisson_generator'
}

def buildNetwork(modelDict):
    """Builds the network from a given model dictionary
    :param modelDict: The model dict that is read from a JSON file"""
    # First read the populations
    print("Creating populations")
    populationDicts = modelDict['populations']
    populations = {}
    for populationDict in populationDicts:
        populations[populationDict['name']] = readPopulation(populationDict)

    globalInterval = reduce(lambda x, y: x+y, [p.getInterval() for p in populations.values()])
    print(globalInterval)

    # Second, connect the populations
    print("Connecting populations")
    connectionDicts = modelDict['connections']
    globalCSet = csa.empty
    for connectionDict in connectionDicts:
        cset, sourceName, targetName = readConnection(connectionDict)
        
        source = populations[sourceName]
        target = populations[targetName]

        globalConnections = source.getConnectionSet(target)
        
        csetCut = globalConnections * cset

        
        globalCSet = globalCSet + csetCut


        # csa.show(globalCSet, 2000,2000)

    # print("Drawing")
    # csa.show(globalCSet, 7000, 7000)
    
    print("Connecting using NEST")
    globalIDs = [gid for gid in globalInterval]
    t1 = time.time()
    connect(globalIDs, globalIDs, globalCSet)
    t2 = time.time()
    print("Created connections in " + str(t2-t1) + " seconds")
    
    print(len(nest.GetConnections()))
    return

    # Third, create the inputs
    inputDicts = modelDict['inputs']



    # Determine input types
    print("Creating inputs")
    inputTypes = {}
    for inputDict in inputDicts:
        inputType = inputDict['inputType']
        if inputType not in inputTypes:
            inputTypes[inputType] = createInputType(inputType)

    print("Connecting inputs")
    for inputDict in inputDicts:
        targetPopulation = populations[inputDict['target']]
        inputPopulation = inputTypes[inputDict['inputType']]
        connectInput(inputDict, targetPopulation, inputPopulation)


def readConnection(connDict):
    """Reads a connection from the JSON dict.
    :return: (connSet, sourcePopulationName, targetPopulationName) """
    connectivityModel = connDict['connectivityModel']
    if connectivityModel == 'random':
        connectivity = connDict['connectivity']
        connSet = csa.random(connectivity)
    else:
        connSet = csa.oneToOne

    csaDict = {'source': connDict['source'], 'target': connDict['target'], 'connectionSet': connSet}
    return connSet, connDict['source'], connDict['target']

def readPopulation(popDict):
    """Reads a population form the JSON dict"""
    n = popDict['size'] // 10
    neuronModel = popDict['neuronModel']
    name = popDict['name']

    population = Population(name, n, neuronModel)
    return population

def connectInput(inputDict, targetPopulation, inputPopulation):
    n = inputDict['n']
    nest.Connect(inputPopulation, targetPopulation, {'rule': 'fixed_outdegree', 'outdegree': n})

def connect(source, target, cset):
    nest.CGConnect(source, target, cset)

def createInputType(inputType):
    return nest.Create(inputNameDict[inputType], params={'rate': 8.0})

def main():
    if len(sys.argv) < 2:
        print("No file to work on")
        sys.exit()

    try:
        with open(sys.argv[1]) as fp:
            modelDict = json.load(fp)
    except IOError:
        print("Could not load file")
        sys.exit()

    buildNetwork(modelDict)
    # nest.GetConnections()

if __name__ == '__main__':
    main()