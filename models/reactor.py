from models.components import CoolingCycle, FuelRod, NeutronSource, ControlRod
from physics import max_rod_flux_equation
from models.fuel_types import fuel_types_dict

class Reactor:
    def __init__(self):
        #main variables
        self.total_power = 0
        self.keff = None    #pro statický model nelze určit, dopracuji mimo PPY1

        #components
        self.core = [[None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None]]
        self.c_cycle = CoolingCycle(0.00005, 20)
        self.n_source = NeutronSource()
        self.control_rod = ControlRod()

    # spočítá hodnotu maximálního toku pro jednotlivé tyče
    def get_max_flux_on_rods(self):
        abs_c = self.control_rod.get_total_absorbtion() #celková absorbce
        add_flux = self.n_source.additional_raw_n_flux

        # projde zónu a určí vlastní tok tyčí, vyexportuje ji jako tabulku
        own_fluxes_of_rods = []
        for i in range(len(self.core)):
            list = []
            for j in range(len(self.core[i])):
                if self.core[i][j] == None:
                    c = 0
                else:
                    c = self.core[i][j].get_own_flux()
                list.append(c)
            own_fluxes_of_rods.append(list)

        # spočítá hodnotu maximálního toku pro jednotlivé tyče
        for i in range(len(self.core)):
            for j in range(len(self.core[i])):
                rod = self.core[i][j]
                if rod == None:
                    continue
                rod.max_rod_flux = max_rod_flux_equation(grid=own_fluxes_of_rods, target_coords = (i, j), external_source_flux = add_flux, abs_c = abs_c, B_T= own_fluxes_of_rods[i][j])

    def get_total_power(self):
        self.get_max_flux_on_rods()
        self.total_power = 0

        for row in self.core:
            for rod in row:
                if rod == None:
                    continue

                rod.get_total_rod_power()
                self.total_power += rod.total_rod_power

    def add_fuel_rod(self, x, y, fueltype, dict_of_types = fuel_types_dict):
        self.core[x][y] = FuelRod(fueltype, dict_of_types)

    def recalculate_main_stats(self):
        self.get_total_power()
        self.c_cycle.get_out_water_temp(self.total_power)

    def get_power_map(self):
        power_map = []
        for row in self.core:
            map_row = []
            for rod in row:
                if rod == None:
                    map_row.append(0)
                else:
                    p = rod.get_max_rod_power()
                    map_row.append(rod.get_max_rod_power())
            power_map.append(map_row)

        return power_map


