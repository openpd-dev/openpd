from . import BaseDimension, Unit, Quantity

######################
## BaseDimensions   ##
######################
constant = BaseDimension()
length = BaseDimension(length_dimension=1)
mass = BaseDimension(mass_dimension=1)
time = BaseDimension(time_dimension=1)
temperature = BaseDimension(temperature_dimension=1)
charge = BaseDimension(charge_dimension=1)
mol_dimension = BaseDimension(mol_dimension=1)

force = mass * length / time**2
energy = force * length
power = energy / time
velocity = length / time
accelration = length / time**2

######################
## Constants        ##
######################

k_b = Quantity(1.38064852e-23, Unit(energy/temperature, 1))
n_a = Quantity(6.0221e23, Unit(1/mol_dimension, 1))

######################
## Length Unit      ##
######################

meter = Quantity(1, Unit(length, 1))
decimeter = Quantity(1, Unit(length, 1e-1))
centermeter = Quantity(1, Unit(length, 1e-2))
millimeter = Quantity(1, Unit(length, 1e-3))
micrometer = Quantity(1, Unit(length, 1e-6))
nanometer = Quantity(1, Unit(length, 1e-9))
angstrom = Quantity(1, Unit(length, 1e-10))

######################
## Mass Unit        ##
######################

kilogram = Quantity(1, Unit(mass, 1))
gram = Quantity(1, Unit(mass, 1e-3))
amu = Quantity(1, Unit(mass, 1.66053904e-27))
dalton = Quantity(1, Unit(mass, 1.66053904e-27))

######################
## Time Unit        ##
######################

day = Quantity(1, Unit(time, 60*60*24))
hour = Quantity(1, Unit(time, 60*60))
minute = Quantity(1, Unit(time, 60))
second = Quantity(1, Unit(time, 1))
millisecond = Quantity(1, Unit(time, 1e-3))
microsecond = Quantity(1, Unit(time, 1e-6))
nanosecond = Quantity(1, Unit(time, 1e-9))
picosecond = Quantity(1, Unit(time, 1e-12))
femtosecond = Quantity(1, Unit(time, 1e-15))

######################
## Temperature Unit ##
######################

kelvin = Quantity(1, Unit(temperature, 1))

######################
## Charge Unit      ##
######################

coulomb = Quantity(1, Unit(charge, 1))
e = Quantity(1, Unit(charge, 1.602176634e-19))

######################
## Mol Unit         ##
######################

mol = Quantity(1, Unit(mol_dimension, 1))
kilomol = Quantity(1, Unit(mol_dimension, 1e3))

######################
## Energy Unit      ##
######################

joule = Quantity(1, Unit(energy, 1))
kilojoule = Quantity(1, Unit(energy, 1e3))
joule_permol = Quantity(1, Unit(energy, 1/6.0221e23))
kilojoule_permol = Quantity(1, Unit(energy, 1e3/6.0221e23))

calorie = Quantity(1, Unit(energy, 4.184))
kilocalorie = Quantity(1, Unit(energy, 4.184e3))
calorie_premol = Quantity(1, Unit(energy, 4.184/6.0221e23))
kilocalorie_permol = Quantity(1, Unit(energy, 4.184e3/6.0221e23))

ev = Quantity(1, Unit(energy, 1.60217662e-19))
hartree = Quantity(1, Unit(energy, 4.3597447222071e-18))

######################
## Force Unit       ##
######################

newton = Quantity(1, Unit(force, 1))
kilonewton = Quantity(1, Unit(force, 100))
kilojoule_permol_over_angstrom = kilojoule_permol / angstrom
kilojoule_permol_over_nanometer = kilojoule_permol / nanometer
kilocalorie_permol_over_angstrom = kilocalorie_permol / angstrom
kilocalorie_permol_over_nanometer = kilocalorie_permol / nanometer

######################
## Power Unit       ##
######################

watt = Quantity(1, Unit(power, 1))
kilowatt = Quantity(1, Unit(power, 1e3))