# YU Terms List

A small proejct to download terms from Data Cookbook API

## Development Environment Setup 

* Clone this repo:
```bash
git clone git@github.com:firozkabir/yu-terms-list.git
```

* Setup python virtual environment and install requirements:
```bash
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip3 install -r requirements.txt 
```

## Add configuration: 

```bash
cp config.ini.sample config.ini 
```

* Using your favourite editor, fill in the following inside config.ini
```
[MYENV]
username=myusername
password=mypassword
instance=my.instance
```

## Run the program
```bash
source venv/bin/activate
./main.py --configfile config.ini --env MYENV --outputfile terms.json
```

