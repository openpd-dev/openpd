import pytest

test_order = [
     'unit',
     'quantity',
     'unitDefinition',
     'judgement',
     'locate',
     'geometry',
     'unique',
     'math',
     'baseDimension',
     'atom',
     'peptide',
     'chain',
     'topology',
     'system',
     'loader',
     'pdbLoader',
     'sequenceLoader',
     'force',
     'pdffNonBondedForceField',
     'pdffNonBondedForce',
     'pdffTorsionForceField',
     'pdffTorsionForce',
     'rigidBondForce',
     'ensemble',
     'forceEncoder',
     'integrator',
     'verletIntegrator',
     'simulation',
     'logDumper',
     'snapshotDumper',
     'snapshotVisualizer'
]

def pytest_collection_modifyitems(items):
     current_index = 0
     for test in test_order:
          indexes = []
          for id, item in enumerate(items):
               if 'test_'+test+'.py' in item.nodeid:
                    indexes.append(id)  
          for id, index in enumerate(indexes):
               items[current_index+id], items[index] = items[index], items[current_index+id]
          current_index += len(indexes)
