# DB dump manager
This manager may help you to convert data from postgresql to MariaDB

# Install
1. you need to have `python3` on your PC.
2. you need to have `pip` - it's dependency manager for `python3`
3. install dependencies `python3 -m pip install -r requirements.txt`
You might have a problem with this installation, it requires database packages, so you will need to install PostgreSQL and MariaDB on your local machine since the tool uses the `pg_dump` and the `mysql` console commands. The `psycopg2` Python library also requires the OpenSSL library to be installed on your environment.

# Configuration
 - `dump-clean-config.dist.yaml` - prepared config for everything that should be replaced during converting. You can extend it with your own parameters.
 - `config.dist.yaml` - main config. You should define database settings and the next configs:
```yaml
rows_per_insert: 1000
dump: tables
clean: tables

scripts:
  global: true
  session: false
```
The `rows_per_insert` configuration stands for the number of rows per one `INSERT` statement used for bulk insert.
# Run
Just run `python3 main.py`

it's also possible to run only part of migration
 - `dump` - for dumping data from postgresql to `/dump/origin`
 - `clean` - for clearing data from postgresql specific syntax, result will be stored to `/dump/clean`
 - `upload` - for upload cleared data to MariaDB

Example: `python3 main.py upload`
