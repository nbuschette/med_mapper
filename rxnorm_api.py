import requests
import xml.etree.ElementTree
import json

def get_rxnorm_ingredients(name):#(rxcui):
    base_uri = 'http://rxnav.nlm.nih.gov/REST'
    url = '{base_uri}/rxcui.json?name={name}'.format(base_uri = base_uri, name = name)
    response = requests.get(url)
    json_dict = json.loads(response.text)
    try:
        ID = json_dict['idGroup']['rxnormId']
        #catch multiple mapped medication
        if len(ID) > 1:
            print(name+' multi rxcui')
        else:
            in_dictionary = {name: {'IN' : ID[0]}}
        return in_dictionary
    except:
        print(name+' name error')

def get_rxnorm_scd(rxcui):
    base_uri = 'http://rxnav.nlm.nih.gov/REST'
    url = '{base_uri}/rxcui/{rxcui}/allrelated'.format(base_uri = base_uri, rxcui = rxcui)
    response = requests.get(url)
    tree = xml.etree.ElementTree.fromstring(response.text)
    xml_ingredients = tree.findall("./allRelatedGroup/conceptGroup[tty='SCD']/conceptProperties")
    scd_list = []
    for xml_ingredient in xml_ingredients:
        #generic drugs
        assert xml_ingredient.findtext('tty') == 'SCD'
        scd_list.append(xml_ingredient.findtext('rxcui'))
        
    xml_ingredients = tree.findall("./allRelatedGroup/conceptGroup[tty='SBD']/conceptProperties")
    for xml_ingredient in xml_ingredients:
        #brand drugs
        assert xml_ingredient.findtext('tty') == 'SBD'
        scd_list.append(xml_ingredient.findtext('rxcui'))
    #returns a list of rxcuis
    return scd_list

def get_ndc(rxcui):
    base_uri = 'http://rxnav.nlm.nih.gov/REST'
    url = '{base_uri}/ndcproperties?id={rxcui}'.format(base_uri = base_uri, rxcui = rxcui)
    response = requests.get(url)
    tree = xml.etree.ElementTree.fromstring(response.text)
    xml_ingredients = tree.findall("./ndcPropertyList/ndcProperty")
    ndc_list = []
    for xml_ingredient in xml_ingredients:
        ndc_list.append(xml_ingredient.findtext('ndcItem'))
    #returns a list of ndcs
    return ndc_list

def make_med_data(name):
    try:
        ingred_dict = get_rxnorm_ingredients(name)#RXCUI IN/MIN
        multi_list = get_rxnorm_scd(ingred_dict[name]['IN'])#RXCUI SCD
        ndc_dict = {}
        for rxcui in multi_list:
            ndc_dict[rxcui] = get_ndc(rxcui)#ndc list
        #returns a dictionary with a list of NDCs for each rxcui
        return ndc_dict
    except:
        print(str(name) + ' error')
        return {}