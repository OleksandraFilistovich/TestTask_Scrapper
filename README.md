# TestTask_Scrapper
Web scrapper

TO RUN APPLICATION:
- make .env file using .env_example
- run:
    docker-compose up --build

To run at exact time every day:
- write wanted time to .env
- comment 58 line in app/app.py (left uncommented for easy test)
- Kiev timezone

STRUCTURE & REMARKS:
- docker-compose loads one servise for app and one for db
- database/ contains table creating and docker servise for postgres config
- app/ have requirements.txt to install everything via Docker
- app/app.py conects everything and is responsible for timed start
- app/modules/database.py works with db connection and insertion of data
- app/modules/scrapper.py scraps data from website and returns them (function page_processing() is long, might need rework)
- app/modules/car.py is a dataclass for car info to be more easy to work with
