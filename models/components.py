import math
import numpy as np

class CoolingCycle:
    def __init__(self, water_flow, in_water_temp):
        self.water_flow = water_flow #[m3/s]
        self.in_water_temp = in_water_temp #[°C]
        self.out_water_temp = 0 #[°C]

    def get_out_water_temp(self, total_power):
        WATER_DENSITY = 1000  # [kg/m3]
        SPECIFIC_HEAT_CAPACITY = 4120  # [J/(kg.K)]

        self.out_water_temp = self.in_water_temp + ((total_power)/(self.water_flow*WATER_DENSITY*SPECIFIC_HEAT_CAPACITY))

class NeutronSource:
    def __init__(self):
        self.additional_raw_n_flux__120 = 1.27e10 #[1/(m2*s)]   POZN: pro jednoduchost uvažuji všude konstatní rozložení odpovídající rozpytlu do koule
        self.additional_raw_n_flux = self.additional_raw_n_flux__120

    def change_voltage_on_external_source(self, voltage):   #kV
        N= 4 #konstanta úměrnosti

        self.additional_raw_n_flux = self.additional_raw_n_flux__120*((voltage/120)**N)

class FuelRod:
    def __init__(self, fueltype, dict_of_types):
        self.enrichment = dict_of_types[fueltype]["enrichment"]
        self.burnup = dict_of_types[fueltype]["burnup"]

        self.max_rod_flux = 0.0
        self.total_rod_flux = 0.0
        self.total_rod_power = 0.0 #[W]

    def get_convert_coeficient(self):
        v = 2.4 #počet n uvolněných na jedno štěpení
        sigma_f = 585e-24 #mikroskopický štěpný průřez U-235
        N_A = 6.022e23 #Avogadrova konstanta
        ro = 10.500 #hustota paliva (UO2)
        A = 270 #molární hmostnost UO2
        ref_neutron_flux = 10e13

        return v*sigma_f*N_A*(ro/A)*ref_neutron_flux

    def get_own_flux(self):
        C= self.get_convert_coeficient()
        return C*self.enrichment*(1.0-self.burnup)

    def get_total_rod_flux(self):
        H = 4.72 #[m] délka palivové tyče
        self.total_rod_flux = self.max_rod_flux*(2.0*H/math.pi)

    def get_max_rod_power(self):
        Q_f = 3.2e-11  # [J] uvolněné teplo na jedno štěpení
        m_sigma_f = 585e-28  # mikroskopický štěpný průřez U-235
        N_A = 6.022e23  # Avogadrova konstanta
        ro = 10.5  # hustota paliva (UO2)
        A = 270  # molární hmostnost UO2

        sigma_f_T = ((self.enrichment * ro * N_A) / (A)) * m_sigma_f  # Makroskopický štěpný průřez
        return Q_f * sigma_f_T * self.max_rod_flux

    def get_total_rod_power(self):
        Q_f = 3.2e-11 #[J] uvolněné teplo na jedno štěpení
        m_sigma_f = 585e-28  # mikroskopický štěpný průřez U-235
        N_A = 6.022e23  # Avogadrova konstanta
        ro = 10.5  # hustota paliva (UO2)
        A = 270  # molární hmostnost UO2

        sigma_f_T = ((self.enrichment * ro * N_A)/(A))*m_sigma_f  #Makroskopický štěpný průřez

        self.get_total_rod_flux()

        self.total_rod_power = Q_f * sigma_f_T * self.total_rod_flux

    def get_axial_profile(self, resolution=200):
        max_rod_power  = self.get_max_rod_power()

        H = 4.72 #m délka tyče
        z = np.linspace(0, H, resolution)
        power_z = max_rod_power*np.sin((math.pi*z)/H)
        return {"z": z.tolist(), "power": power_z.tolist()}

class ControlRod:
    def __init__(self):
        self.retract = 0.0 #jendá se o poměr délek, tj. 0 je vytáhnutá, 1 je plně zasunutá
        self.absorbtion_c = 0.8

    def change_position_to(self, new_retract):
        self.retract = new_retract

    def get_total_absorbtion(self):
        return (1.0- self.retract*self.absorbtion_c)
