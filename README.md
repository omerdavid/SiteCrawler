# Site Crawler

This project crawls `https://pastes.com` with interval of 2 seconds and store the new pastes into a local database (sqlite).


## Installation

clone repository :
```
git clone git@github.com:omerdavid/SiteCrawler.git
```

1. Copy the provided db file pastes.db to Db folder under root

   ```
   ./Db/pastes.db
   ```

2. Run
   ```
   pipenv install
   ```

- Once installed run
   ```
   pipenv run python app.py
   ```
