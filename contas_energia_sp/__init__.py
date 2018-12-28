import re
from time import sleep
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


conta = namedtuple("Conta", "status dt_pag mes_ref venc valor")


class EnelPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://portalhome.eneldistribuicaosp.com.br/#/login"
    
    def login(self, cpf, num_instalacao):
        self.driver.get(self.url)
        cpf_input = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_id("cpfcnpj"))
        cpf_input.send_keys(cpf)
        inst_input = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_id("anlage"))
        inst_input.send_keys(num_instalacao)
        inst_input.submit()
        wait = WebDriverWait(self.driver, 10)
        btnLogin = wait.until(EC.element_to_be_clickable((By.ID,"btnLogin")))
        # btnLogin = self.driver.find_element_by_id("btnLogin")
        sleep(1)
        btnLogin.click()
        btnEntrar = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_css_selector(
                ".md-button.md-lightDefault-theme.flex"))
        btnEntrar.click()

    def navigate_contas(self):
        wait = WebDriverWait(self.driver, 20)
        btns = wait.until(EC.element_to_be_clickable((By.NAME, 'Minha Conta')))
            # lambda x: x.find_elements_by_tag_name("button"))

        minha_conta_btn = btns
        # actions = ActionChains(self.driver)
        # actions.move_to_element(minha_conta_btn)
        # self.driver.execute_script("arguments[0].scrollIntoView();", minha_conta_btn)
        # WebDriverWait(minha_conta_btn, 5).until(
        #     lambda x: x.click())
        minha_conta_btn.click()
        contas_pagamentos = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_id("contas-e-pagamentos"))
        contas_pagamentos.click()
    def get_todas_contas(self):
#        self._navigate_contas()
        wait = WebDriverWait(self.driver, 20)
        label_todas = wait.until(EC.element_to_be_clickable((By.ID, 'radio_13')))
        # label_todas = self.driver.find_element_by_id("radio_13")
        label_todas.click()
        boxes = self.driver.find_elements_by_class_name("faturas-card")
        contas = []
        ref_regex = re.compile("Referente à (\w+/\d{2})")
        venc_regex = re.compile("Vencimento: (\d{2}/\d{2}/\d{4})")
        valor_regex = re.compile("R\$(\d+,\d+)")
        dt_pag_regex = re.compile("Pago em: (\d{2}/\d{2}/\d{4})")
        paga_regex = re.compile("(Paga|Extrato)")

        for box in boxes:
            se = paga_regex.search(box.text)
            dt_pag = None
            paga = "Aberta"
            if se:
                paga = se.group(0)
                se = dt_pag_regex.search(box.text)
                dt_pag = se.group(1)
                
            se = ref_regex.search(box.text)
            ref = se.group(1)
            se = venc_regex.search(box.text)
            venc = se.group(1)
            se = valor_regex.search(box.text)
            valor = se.group(1)
            contas.append(conta(paga, dt_pag, ref, venc, float(valor.replace(',','.'))))
        return contas
            



