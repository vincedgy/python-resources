![](https://scrutinizer-ci.com/g/vincedgy/python-resources/badges/quality-score.png?b=master)
![](https://scrutinizer-ci.com/g/vincedgy/python-resources/badges/code-intelligence.svg?b=master)

# python-resources
My python scripts & resources

## One very inspiring talk and github repo for CLI
https://github.com/judy2k/command-line-talk

## Scripts & Files
### Files : 
    * .pylintrc : stores pylint configuration
    * requirements.txt : store package requierments. It can be used with
    ```
    pip install -r requirements.txt
    ```
### Scripts & Samples
    * cli : contains first version directly inspired by Web/Youtube ref (see up)
    * AWS : python script wuth boto3
    * csv : CSV file manipulations
    * datatimes : datetime manipulations
    * db : using databases and ORM
    * encrypt : encryption
    * rx : Reactive programming
    * samples : various scripts
    * webScraping : scrap a website to download things
    * wotkWithExcel : its name says everything right ?

## Virtual Env
    ```
    cd $project_dir
    sudo pip install virtualenv
    virtual venv
    . venv/bin/activate
    ```

/!\ venv dir is gitignored

## Manage packages

### Install pip
    ```
    curl -O https://bootstrap.pypa.io/get-pip.py
    python ./get-pip.py
    ```

### Install pip-review
    ``` 
    pip install pip-review
    ```

## Progress bar
https://github.com/tqdm/tqdm
