import numpy as np
import pandas as pd

from rocketcea.cea_obj import CEA_Obj, add_new_fuel,add_new_oxidizer

fuel_str = """
fuel C2H5OH(L)   C 2 H 6 O 1
h,cal=-66370.0      t(k)=298.15       wt%=100.
"""
add_new_fuel( 'C2H5OH', fuel_str )
ox_str = """
oxid NitrousOxide  N 2.0 O 1.0  wt%=100.00
h,cal= 19467.0 t(k)=298.15
"""
add_new_oxidizer( 'N20', ox_str )

C = CEA_Obj( oxName='N20', fuelName='C2H5OH')

PsiaOvBar = 14.503773800722
rankinToKelvin = lambda R: (R-491.67)/1.8 + 273.15 

Pc_list = np.arange(17,40,.5) #bar
Pc_list = Pc_list * PsiaOvBar #bar * psia/bar = psia
Pe = 10.13 #bar
Pe = Pe * PsiaOvBar # bar * psia/bar = psia
MR_list = np.arange(.75,8,.25) 
PcOvPe_list = Pc_list/10
eps_list = np.arange(40,60,.5)
subar_list = [3,2]

for Pc in Pc_list:
    PcOvPe = Pc/Pe
    for MR in MR_list:
        for subar in subar_list:
            eps = C.get_eps_at_PcOvPe(Pc=Pc, MR=MR, PcOvPe=PcOvPe)  
            Tc, Tt, Te = C.get_Temperatures(Pc=Pc, MR=MR, eps=eps)
            Isp = C.get_Isp(Pc, MR, eps)
            molwt, gamma = C.get_exit_MolWt_gamma(Pc=Pc, MR=MR, eps=eps)

            instance_data = {'Pc':[Pc/PsiaOvBar],'eps':[eps],'MR':[MR],'PcOvPe':PcOvPe,'subar':[subar],'Tc':[rankinToKelvin(Tc)],'Tt':[rankinToKelvin(Tt)],'Te':[rankinToKelvin(Te)],'Isp':[Isp], 'gamma':[gamma]}

            try:
                df2 = pd.DataFrame(instance_data)
                df = df.append(df2,ignore_index=True)
            except NameError:
                df = pd.DataFrame(instance_data)

df.to_csv('combustion.csv')

print(df.head())