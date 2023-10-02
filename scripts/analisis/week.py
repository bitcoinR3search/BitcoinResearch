# Este scrip automatiza la elaboracion
# de las graficas todos los lunes a dom 8 pm (lun 00 GMT)

import subprocess
import os
import numpy as np

os.chdir('D:/proyectos/BitcoinResearch/BitcoinResearch/scripts/analisis')



def run_script(script_name):
    os.system(f'python {script_name}')


scripts = ['block_size.py', 'btcsupply.py', 'brcsupply.py','hashrate.py','ntx']

for script in scripts:
    run_script(script)
