import pytest

test_order = [
     'test_judgement',
     'test_locate',
     'test_geometry',
     'test_unique',
     'test_atom',
     'test_peptide',
     'test_chain',
     'test_topology',
     'test_system',
     'test_pdbLoader',
     'test_sequenceLoader',
     'test_pdffNonBondedForce',
     'test_forceEncoder'
]

def pytest_collection_modifyitems(session, items):
     current_index = 0
     for test in test_order:
          indexes = []
          for id, item in enumerate(items):
               if test in item.nodeid:
                    indexes.append(id)  
          for id, index in enumerate(indexes):
               items[current_index+id], items[index] = items[index], items[current_index+id]
          current_index += len(indexes)
