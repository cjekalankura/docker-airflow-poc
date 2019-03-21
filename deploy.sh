#!/bin/bash
cd ~/dev/docker-airflow
docker-compose down
rm -rf pgdata
ssh airflow-qa 'cd ~/dev/docker-airflow && docker-compose down && cd ~/dev/ && sudo rm -rf docker-airflow/'
cd ~/dev
COPYFILE_DISABLE=true tar -czvf docker-airflow.tar.gz docker-airflow/
scp docker-airflow.tar.gz airflow-qa:~/dev/
ssh airflow-qa 'cd ~/dev && tar -xzvf docker-airflow.tar.gz'
ssh airflow-qa 'cd ~/dev/docker-airflow && docker-compose up -d'
cd ~/dev/docker-airflow
