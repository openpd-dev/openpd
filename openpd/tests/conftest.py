import pytest

test_order = [
     'test_atom.py',
     'test_peptide.py',
     'test_chain.py',
     'test_topology.py',
     'test_system.py',
     'test_pdbLoader.py',
     'test_sequenceLoader.py'
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
