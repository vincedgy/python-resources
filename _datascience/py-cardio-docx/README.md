# Analyse and transform docx file to JSON representation

- author: Vincent DAGOURY
- date: 2020-05-01
- email: vincent.dagoury@gmail.com
- github : [https://github.com/vincedgy](https://github.com/vincedgy)

## Objectives

The purpose of this notebook/script is to analyse the content of formated docx files.
This files are used for medical report.
Each file needs to be placed in 'data' directory.
The result are json files in 'json' directories with a unique name (uuid based).

> note : you can delete all files in 'json' directory if you want to process
> all json files without duplicates from previous processing

## Install

### Install a virtualenv

You should have virtualenv first

```sh
virtualenv .env
```

### Install requirements

```sh
source .env/bin/activate
pi` install -r requirements.txt
```

### Tun the script

```sh
$ time python ./process-cardio-files-docx.py
Processing file.docx...
Extracting to ./json/file-b5343a08-8c0b-40ba-8222-1b0319804193.json
Processing Extracction données Lacotte.docx...
Extracting to ./json/Extracction données Lacotte-6d027489-f15f-4af8-ab6f-3a2e06f43f33.json
Done
python ./process-cardio-files-docx.py  1.35s user 0.23s system 193% cpu 0.817 total
```

## Jupyter notebook

A Jupyter [notebook](process-cardio-files-docx.ipynb) helps to understand the methodology and technics of this script


## TODO

  - Not that much at this point :-)
