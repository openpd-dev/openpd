import pytest

test_order = [
     'judgement',
     'locate',
     'geometry',
     'unique',
     'baseDimension',
     'unit',
     'quantity',
     'unitDefinition',
     'atom',
     'peptide',
     'chain',
     'topology',
     'system',
     'loader',
     'pdbLoader',
     'sequenceLoader',
     'force',
     'pdffNonBondedForce',
     'pdffTorsionForce',
     'rigidBondForce',
     'ensemble',
     'forceEncoder'
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
