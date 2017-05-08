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
    * mycli (dir) : contains first version directly inspired by Web/Youtube ref (see up)
    * click-expl??.py : different 'Click' (the CLI framework) examples

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
