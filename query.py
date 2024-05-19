import warnings
warnings.filterwarnings('ignore')

from pymatgen.core import Element
#from pymatgen.ext.matproj import MPRester
import seaborn as sns
import numpy as np
from monty.serialization import dumpfn, loadfn
import pandas as pd

from megnet.models import MEGNetModel

from pymatgen.core.composition import Composition
from pymatgen.core.structure import Structure
from pymatgen.io.cif import CifWriter

all_models = [MEGNetModel.from_file('/global/homes/y/yagmurco/megnet/mvl_models/mf_2020/pbe_gllb_hse_exp/%d/best_model.hdf5' % i) for i in range(6)]

database_url = "https://optimade-gnome.odbx.science"
#re_actinitides="AND NOT elements HAS ANY "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb""
query = 'elements HAS "Be" AND nelements=3 AND NOT elements HAS ANY "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb"'
params = {
  "filter": query, "page_limit": 400
}
query_url = f"{database_url}/v1/structures"
import requests
response = requests.get(query_url, params=params)
print(response)
json_response = response.json()
import pprint
print(json_response.keys())
structures = json_response["data"]
meta = json_response["meta"]
print(f"Query from {query_url} returned {meta['data_returned']} structures")


all_data = pd.DataFrame()

for i in structures:
    print(i['attributes']['chemical_formula_reduced'])
    compo=Composition(i['attributes']['chemical_formula_reduced'])
    struct=Structure(i['attributes']['lattice_vectors'],i['attributes']['species_at_sites'],i['attributes']['cartesian_site_positions'],coords_are_cartesian=True)

    # predict band gap with MEGNet
    #struct.state = [0] # predict PBE band gap
    struct.state = [2] # predict HSE band gap 
    predictions = [model.predict_structure(struct) for model in all_models]
    bandgap = np.mean(predictions)
    print(bandgap)
    
    data = pd.DataFrame({'formula':i['attributes']['chemical_formula_reduced'],
                          'bandgap':[bandgap]})
    all_data = all_data.append(data, ignore_index=True)
    
    w = CifWriter(struct)
    w.write_file('./cifs_Be/'+i['attributes']['chemical_formula_reduced']+'.cif')

all_data.to_csv('HSE_data.csv', index=False)
