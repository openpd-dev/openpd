import os, wget, requests, urllib
import threading as th
import multiprocessing as mp

class PDBDownloader:
    def __init__(self, save_dir='./') -> None:
        self.save_dir = save_dir
        self.pdb_ids = []
        self.target_urls = []
        self.target_files = []

    def _addPDBId(self, pdb_id):
        self.pdb_ids.append(pdb_id.upper())
        self.target_urls.append(self.getUrl(self.pdb_ids[-1]))
        self.target_files.append(os.path.join(self.save_dir, self.pdb_ids[-1] + '.pdb'))

    def addPDBIds(self, *pdb_ids):
        for pdb_id in pdb_ids:
            self._addPDBId(pdb_id)

    @staticmethod
    def getUrl(pdb_id):
        return ('https://files.rcsb.org/download/' + pdb_id + '.pdb')

    def download(self):
        for url, file_name in zip(self.target_urls, self.target_files):
            try:
                _ = urllib.request.urlopen(url)
            except:
                raise ValueError(
                    'Can not open %s, check PDB id'
                    %(url)
                )
            if os.path.exists(file_name):
                os.remove(file_name)
            # wget.download(url, file_name, bar=None)
            os.system('wget ' + url + ' -O ' + file_name)