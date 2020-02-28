# Setup guide

## Initial setup

1. Clone repository.
2. Make sure [Python 3](https://www.python.org/downloads/) is installed.
3. Install a [MySQL server](https://www.mysql.com/)
4. Execute all sql scripts in [db/](db/) starting with [db/database.sql](db/database.sql) then V1, V2, etc...
5. Run the command  ```pip install .``` while inside the repository to install the project and dependencies, if installing for development use the command ```pip install -e .``` to allow editing of the installed package.
6. Check permissions for the installed packages.
7. Make sure to put [config.json](/config.json) in any of the below directories and update the settings specific to your system:
    * ```~/arxivdigest/config.json```
    * ```etc/arxivdigest/config.json```
    * ```%cwd%/config.json```

Many of the scripts are recurrent processes that should be automated to run at specific times. This can be achieved by running the script with a cronjob.

The scripts should be run in the following order:

  * [Keyword scraper](keyword_scraper/): Should be run when a new [DBLP dump](https://dblp.uni-trier.de/faq/How+can+I+download+the+whole+dblp+dataset) is available.
  * [Article scraper](scraper/): Should be run when ArXiv releases new articles. ArXiv release schedule can be found [here](https://arxiv.org/help/submit#availability).
  * [Interleaver](interleave/): Should be run after the Article scraper, make sure that there is enough time for the recommender systems to generate recommendations between running the two scripts.
  * [Evaluation](scripts/evaluation.py): Can be run at any time to evaluate the performance of the systems.
     
### Frontend and API

How to deploy a flask application can be found [here](http://flask.pocoo.org/docs/0.12/deploying/)

An example frontend.wsgi file, for the api just switch frontend with api:

```
#!/opt/anaconda3/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/opt/anaconda3/lib/python3.6/site-packages/")

from arxivdigest.frontend.app import app as application
application.secret_key = SOME_SECRET_KEY
```

#### Development

The API and frontend should be started by running 'app.py' in their respective folder while developing.

Make sure that port 80 is free for the frontend and 5000 is free for the API or configure the frontend and api dev_ports in [config.json](/config.json)

### Core

This package contains shared functionality between the different parts of the project.

### Scraper

Is run by running storeMetadata.py: ``python storeMetadata.py``
Articles are not released every day, so this script will not always insert any articles. 

### Keyword scraper

Is run by running keyword_scraper.py: ``python keyword_scraper.py``

### Interleaver

Is run by running interleave.py: ``python interleave.py``

### Evaluation

Is run by running evaluation.py: ``python evaluation.py``

### Sample system

1. Download and run an [Elasticsearch](https://www.elastic.co/) server.
2. Update the constants in [system.py](sample/system.py) such that the system uses the correct API-key and API-url.
3. Run  ``python system.py``

## Updates

1. Pull changes. 
2. Execute any new sql scripts in [db/](db/)
3. Run the command  ```pip install .``` while inside the repository to update the project and dependencies.
4. Check permissions for the installed packages.
5. Make sure that your config json includes any new configurations from [config.json](/config.json)




