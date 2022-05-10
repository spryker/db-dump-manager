# DB dump manager
This manager may help you to convert data from postgresql to MariaDB

# Install
1. you need to have `python3` on your PC.
2. you need to have `pip` - it's dependency manager for `python3`
3. install dependencies `python3 -m pip install -r requirements.txt`
You can have a problem with this instalation, it require database packages, so you will need to install postgresql to your local machine

# Configuration
 - `dump-clean-config.dist.yaml` - prepared config for everything that should be replaced during converting. You can extend it with your own parameters.
 - `config.dist.yaml` - main config. You should define database settings and the next configs:
```yaml
dump: tables
clean: tables

scripts:
  global: true
  session: false
```

# Run
Just run `python3 main.py`

it's also possible to run only part of migration
 - `dump` - for dumping data from postgresql to `/dump/origin`
 - `clean` - for clearing data from postgresql specific syntax, result will be stored to `/dump/clean`
 - `upload` - for upload cleared data to MariaDB

Example: `python3 main.py upload`
