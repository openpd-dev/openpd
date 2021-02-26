import sys
from . import Dumper 
from .. import PDFFNonBondedForce, PDFFTorsionForce
from ..unit import *

class LogDumper(Dumper):
    def __init__(
        self, output_file, dump_interval,
        get_steps=False,
        get_elapsed_time=False,
        get_remain_time=False,
        get_simulation_time=False,
        get_temperature=False,
        get_potential_energy=False, get_kinetic_energy=False, 
        get_nonbonded_energy=False, get_torsion_energy=False,
        get_total_energy=False,
    ) -> None:
        super().__init__(output_file, dump_interval)
        self.flag_dict = {
            "Steps": [get_steps, 10, self._getSteps],
            "Elapsed Time": [get_elapsed_time, 20, self._getElapsedTime],
            "Remain Time": [get_remain_time, 20, self._getRemainTime],
            "Sim Time (ns)": [get_simulation_time, 15, self._getSimulationTime],
            "Temperature (K)": [get_temperature, 17, self._getTemperature],
            "Potential Energy (kj/mol)": [get_potential_energy, 27, self._getPotentialEnergy],
            "Kinetic Energy (kj/mol)": [get_kinetic_energy, 25, self._getKineticEnergy],
            "Nonbonded Energy (kj/mol)": [get_nonbonded_energy, 27, self._getNonBondedEnergy],
            "Torsion Energy (kj/mol)": [get_torsion_energy, 25, self._getTorsionEnergy],
            "Total Energy (kj/mol)": [get_total_energy, 23, self._getTotalEnergy]
        }
        
    def _getSteps(self):
        return(
            '{:<%d}' %self.flag_dict["Steps"][1]
        ).format(self._simulation.cur_step)
        
    def _getElapsedTime(self):
        return(
            '{:<%d}' %self.flag_dict["Elapsed Time"][1]
        ).format(str(self._simulation._elapsed_time))
        
    def _getRemainTime(self):
        return(
            '{:<%d}' %self.flag_dict["Remain Time"][1]
        ).format(str(self._simulation._remain_time))
        
    def _getSimulationTime(self):
        return(
            '{:<%d}' %self.flag_dict["Sim Time (ns)"][1]
        ).format(
            '%.6f' %(self._simulation.cur_step * self._simulation._integrator.sim_interval / nanosecond)
        )
        
    def _getTemperature(self):
        return(
            '{:<%d}' %self.flag_dict["Temperature (K)"][1]
        ).format(
            '%.2f' %(self._simulation._integrator.calculateTemperature()/kelvin)
        )
        
    def _getPotentialEnergy(self):
        return(
            '{:<%d}' %self.flag_dict["Potential Energy (kj/mol)"][1]
        ).format(
            '%.5f' %(
                self._simulation._ensemble.calculatePotentialEnergy() / 
                kilojoule_permol
            )
        )
    
    def _getKineticEnergy(self):
        return(
            '{:<%d}' %self.flag_dict["Kinetic Energy (kj/mol)"][1]
        ).format(
            '%.5f' %(
                self._simulation._integrator.calculateKineticEnergy() / 
                kilojoule_permol
            )
        )
        
    def _getNonBondedEnergy(self):
        nonbonded_force = 0
        for force in self._simulation._ensemble.forces:
            if isinstance(force, PDFFNonBondedForce):
                nonbonded_force = force
                break
        return(
            '{:<%d}' %self.flag_dict["Torsion Energy (kj/mol)"][1]
        ).format(
            '%.5f' %(
                nonbonded_force.calculatePotentialEnergy() / 
                kilojoule_permol
            )
        )
        
    def _getTorsionEnergy(self):
        torsion_force = 0
        for force in self._simulation._ensemble.forces:
            if isinstance(force, PDFFTorsionForce):
                torsion_force = force
                break
        return(
            '{:<%d}' %self.flag_dict["Nonbonded Energy (kj/mol)"][1]
        ).format(
            '%.5f' %(
                torsion_force.calculatePotentialEnergy() / 
                kilojoule_permol
            )
        )
        
    def _getTotalEnergy(self):
        return(
            '{:<%d}' %self.flag_dict["Potential Energy (kj/mol)"][1]
        ).format(
            '%.5f' %(
                (
                    self._simulation._ensemble.calculatePotentialEnergy() +
                    self._simulation._integrator.calculateKineticEnergy()
                ) / kilojoule_permol
            )
        )
    
    def _getTitle(self):
        self.title = ''
        for key, value in list(self.flag_dict.items()):
            if value[0]:
                form = '{:<%d}' %value[1]
                self.title += form.format(key)
        return self.title
    
    def bindSimulation(self, simulation):
        super().bindSimulation(simulation)
        io = open(self._output_file, 'a')
        print(self._getTitle(), file=io)
        io.close()
            
    def dump(self):
        self._test_bound()
        self.info = ''
        for key, value in list(self.flag_dict.items()):
            if value[0]:
                self.info += value[2]()
    
        io = open(self._output_file, 'a')
        print(self.info, file=io)
        io.close()
            