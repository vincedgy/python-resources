#!/usr/bin/env python
# coding: utf-8
# ---------------------------------------------------------------------------------
# Analyse and transform docx file to JSON representation
#
# - author: Vincent DAGOURY
# - date: 2020-05-01
# - email: vincent.dagoury@gmail.com
# - github : [https://github.com/vincedgy](https://github.com/vincedgy)
#
# ---------------------------------------------------------------------------------
#
# The purpose of this notebook/script is to analyse the content of formated docx files.
# This files are used for medical report.
# Each file needs to be placed in 'data' directory.
# The result are json files in 'json' directories with a unique name (uuid based).
#
# note : you can delete all files in 'json' directory if you want to process
#        all json files without duplicates from previous processing
# ---------------------------------------------------------------------------------
# TODO:
# - Not that much at this point :-)
# ---------------------------------------------------------------------------------

from pyfiglet import Figlet
import pyfiglet
import docx
import re
import sys
import uuid
import zipfile
import json
import docx
from datetime import datetime
import pandas as pd
from lxml import etree
import os.path as path
from os import walk


def read_docx(docx_file, **kwargs):
    """Read tables as DataFrames from a Word document"""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(docx_file).open('word/document.xml') as f:
        root = etree.parse(f)
    for el in root.xpath('//w:tbl', namespaces=ns):
        el.tag = 'table'
    for el in root.xpath('//w:tr', namespaces=ns):
        el.tag = 'tr'
    for el in root.xpath('//w:tc', namespaces=ns):
        el.tag = 'td'
    return pd.read_html(etree.tostring(root), **kwargs)


def clean_token(token):
    """Cleans token"""
    t = str(token).strip()
    t = t.replace('\xa0', '')
    t = t.replace('«', '')
    t = t.replace('»', '')
    t = t.replace(':', '')
    return t


def read_tokens_from_docx(docx_file, **kwargs):
    """Read tokens of text from a Word document"""
    blacklist = ['', ':', '&', '-', '.']
    tokens = []
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(docx_file).open('word/document.xml') as f:
        root = etree.parse(f)
    for el in root.xpath('//w:t', namespaces=ns):
        t = clean_token(el.text)
        if t != '' and t not in blacklist:
            tokens.append(t)
    return tokens


def process_file(file):
    """The main processing function"""
    analyse = {}

    # Building attributes
    key_metadata = 'metadata'
    key_data = 'data'
    analyse[key_metadata] = {}
    analyse[key_data] = {}

    # Producing ids for this analyse
    now = datetime.now()
    analyse['datetime'] = now.strftime("%Y%m%d%H%M%S")
    analyse['timestamp'] = str(now.timestamp())
    analyse['id'] = str(uuid.uuid4())

    # Process the doc (with python-docx)
    doc = docx.Document(file)

    # Process XML tokens in docx file
    tokens = read_tokens_from_docx(docx_file=file)
    analyse[key_data]['title'] = tokens[0]

    # Also build tables to DataFrames
    df2 = read_docx(docx_file=file)

    # ## Document metadata
    analyse[key_metadata]['title'] = doc.core_properties.title
    analyse[key_metadata]['author'] = doc.core_properties.author
    analyse[key_metadata]['created'] = str(doc.core_properties.created)
    analyse[key_metadata]['modified'] = str(doc.core_properties.modified)
    analyse[key_metadata]['last_modified_by'] = str(doc.core_properties.last_modified_by)
    analyse[key_metadata]['last_printed'] = str(doc.core_properties.last_printed)
    analyse[key_metadata]['revision'] = doc.core_properties.revision
    analyse[key_metadata]['subject'] = doc.core_properties.subject
    analyse[key_metadata]['identifier'] = doc.core_properties.identifier
    analyse[key_metadata]['comments'] = doc.core_properties.comments
    analyse[key_metadata]['category'] = doc.core_properties.category
    analyse[key_metadata]['keywords'] = doc.core_properties.keywords
    analyse[key_metadata]['content_status'] = doc.core_properties.content_status
    analyse[key_metadata]['language'] = doc.core_properties.language
    analyse[key_metadata]['version'] = doc.core_properties.version
    analyse[key_metadata]

    # ### Catching specific paragraphs
    all_paragraphs = doc.paragraphs
    fullText = []
    for paragraph in all_paragraphs:
        text = paragraph.text
        fullText.append(text)
        # 'Indication'
        if 'Indication' in text:
            analyse[key_data]['Indication'] = re.search(r'^Indication\s:\s(.+)$', text).group(1)
        # 'Remarque'
        if 'Remarque' in text:
            analyse[key_data]['Remarque'] = re.search(r'^Remarque\s:\s(.+)$', text).group(1)
        # 'Fermeture'
        if 'Fermeture' in text:
            analyse[key_data]['Fermeture'] = text

    # ### 'Main tab' part
    df_tab1 = df2[0]
    analyse[key_data]['Nom'] = clean_token(df_tab1[1][0])
    analyse[key_data]['Prénom'] = clean_token(df_tab1[3][0])
    analyse[key_data]['Né(e) le'] = clean_token(df_tab1[1][1])
    analyse[key_data]['Opérateur(s)'] = clean_token(df_tab1[1][2])
    analyse[key_data]['Anesthésiste'] = clean_token(df_tab1[1][3])
    analyse[key_data]['Anesthésie'] = clean_token(df_tab1[3][3])
    analyse[key_data]['Début - Fin'] = clean_token(df_tab1[2][4])
    analyse[key_data]['NIP'] = clean_token(df_tab1[5][1])
    analyse[key_data]['Durée Rx (min)'] = clean_token(df_tab1[1][5])
    analyse[key_data]['PDS (µGy.m²)'] = clean_token(df_tab1[3][5])
    # With tokens
    for i in range(len(tokens)):
        if 'Date opératoire' in tokens[i]:
            analyse[key_data]['Date opératoire'] = clean_token(tokens[i + 1])
        if 'Scopie' in tokens[i]:
            analyse[key_data]['Scopie'] = clean_token(tokens[i + 1])
    analyse[key_data]

    # ### 'Symptomes' part
    df_tab2 = df2[1]
    analyse[key_data]['symptomes'] = {}
    for i in range(4):
        analyse[key_data]['symptomes'][df_tab2[i][0]] = clean_token(df_tab2[i][1])
    analyse[key_data]['symptomes']

    # ### 'Protocole' part
    df_tab3 = df2[2]
    analyse[key_data]['protocole'] = {}
    analyse[key_data]['protocole'][df_tab3[0][0]] = clean_token(df_tab3[0][1])
    analyse[key_data]['protocole'][df_tab3[1][0]] = clean_token(df_tab3[1][1])
    analyse[key_data]['protocole'][df_tab3[1][0] + "-2"] = clean_token(df_tab3[2][1])
    analyse[key_data]['protocole'][df_tab3[2][0]] = clean_token(df_tab3[3][1])
    analyse[key_data]['protocole'][df_tab3[2][0] + "-2"] = clean_token(df_tab3[4][1])
    analyse[key_data]['protocole'][df_tab3[3][0]] = clean_token(df_tab3[3][1])
    # NYHA and FE with tokens
    for i in range(len(tokens)):
        if 'NYHA' in tokens[i]:
            analyse[key_data]['protocole']['NYHA'] = clean_token(tokens[i + 9])
        if 'FE' in tokens[i]:
            analyse[key_data]['protocole']['FE'] = clean_token(tokens[i + 9])

    # ### 'Sondes' part
    df_tab4 = df2[3]
    analyse[key_data]['materiel'] = {}
    analyse[key_data]['materiel']['sondes'] = []
    for i in range(3):
        materiel = {}
        for j in range(11):
            materiel[clean_token(df_tab4[0][j])] = clean_token(df_tab4[i + 1][j])
        for k in range(len(tokens)):
            if 'Date d’implantation' in tokens[k]:
                materiel['Date d’implantation'] = tokens[k + i + 1]
        analyse[key_data]['materiel']['sondes'].append(materiel)

    # ### 'Boitier' part
    df_tab5 = df2[4]
    analyse[key_data]['materiel']['boitier'] = {}
    analyse[key_data]['materiel']['boitier'][df_tab5[0][0]] = df_tab5[1][0]
    analyse[key_data]['materiel']['boitier'][df_tab5[3][0]] = df_tab5[4][0]
    analyse[key_data]['materiel']['boitier'][df_tab5[2][1]] = df_tab5[3][1]
    # Add tokens for 'boitier'
    found_boitier = False
    for i in range(len(tokens)):
        # This starts 'boitier' section
        if 'Boîtier' in tokens[i]:
            analyse[key_data]['materiel']['boitier']['Etat'] = tokens[i + 4]
            found_boitier = True
        if found_boitier and 'Position' in tokens[i]:
            analyse[key_data]['materiel']['boitier']['Position'] = tokens[i + 1]
        if found_boitier and 'Localisation' in tokens[i]:
            analyse[key_data]['materiel']['boitier']['Localisation'] = tokens[i + 1]
        if found_boitier and 'IRM' in tokens[i] and 'conditional' in tokens[i + 1]:
            analyse[key_data]['materiel']['boitier']['IRM conditional'] = tokens[i + 2]
            found_boitier = False
            # This ends 'boitier' section

    # ### 'Ancien boitier' part
    df_tab6 = df2[5]
    analyse[key_data]['materiel']['ancien_boitier'] = {}
    analyse[key_data]['materiel']['ancien_boitier'][df_tab6[0][0]] = df_tab6[1][0]
    analyse[key_data]['materiel']['ancien_boitier'][df_tab6[3][0]] = df_tab6[4][0]
    analyse[key_data]['materiel']['ancien_boitier'][df_tab6[2][1]] = df_tab6[3][1]
    # Add tokens for 'ancien_boitier'
    found_ancien_boitier = False
    for i in range(len(tokens)):
        if 'Ancien boitier' in tokens[i]:
            analyse[key_data]['materiel']['ancien_boitier']['Etat'] = tokens[i + 4]
            found_ancien_boitier = True
        if found_ancien_boitier and 'Position' in tokens[i]:
            analyse[key_data]['materiel']['ancien_boitier']['Position'] = tokens[i + 1]
        if found_ancien_boitier and 'Localisation' in tokens[i]:
            analyse[key_data]['materiel']['ancien_boitier']['Localisation'] = tokens[i + 1]
            found_ancien_boitier = False

    return (analyse, analyse['id'])


# ------------------------------------------------------------------------
custom_fig = Figlet(font='small')
ascii_banner = custom_fig.renderText("Py-Cardio docx")
print(ascii_banner)
print("""
'Py-Cardio docx' : is a Python based processing cardio report docs files
                   A free tool for ICPS - URSC / MASSY (91300)
Author: Vincent DAGOURY 
Version : 0.1b
LICENSE: The MIT License (MIT) Copyright © 2020
""")

if __name__ == "__main__":

    # List all files in 'data' directory
    f = []
    for (dirpath, dirnames, filenames) in walk('./data'):
        f.extend(filenames)
        break

    # Process each file
    for FILE in f:
        filename = f'data/{FILE}'
        if not path.exists(filename) or not path.isfile(filename):
            print(f'ERROR : the given file {FILE} does not exists')
            sys.exit(1)

        print(f'INFO : Processing {FILE}...')
        (result, result_id) = process_file(filename)

        FILE_OUTPUT = f'./json/{path.splitext(path.basename(FILE))[0]}-{result_id}.json'
        print(f'INFO : Extracting to {FILE_OUTPUT}')

        # Write the json file
        with open(FILE_OUTPUT, 'w') as w:
            w.write(json.dumps(result, sort_keys=True, indent=2))

    print(f'INFO : Done. You should check files in \'json\' directory.')
