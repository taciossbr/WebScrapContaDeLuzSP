import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from contas_energia_sp import *

options = Options()
options.add_argument('-headless')
ff = webdriver.Firefox(options=options)
# ff = webdriver.Firefox()

ep = EnelPage(ff)
ep.login(sys.argv[1], sys.argv[2])
ep.navigate_contas()
contas = ep.get_todas_contas()

with open("contas.csv", "w") as _file:
    _file.write("status,dt_pag,mes_ref,venc,valor\n")
    for conta in contas:
        _file.write(",".join(map(str, conta))+"\n")


ff.close()