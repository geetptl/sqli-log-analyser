# sqli-log-analyser
### A project for CS553: Design of Internet Services, Spring 2023 at Rutgers University

----

This project uses Apache Spark and other helper libraries from python to implement a distributed 
computing framework to set up a log analysis system for the web log files.

`log-analysis.ipynb` is used to train and save models. This is done on google colab. This doesn't require
usage of Spark, or any special configurations.

----

`python3 filewriter.py`: This command starts a filewriter process that dumps shuffled training data into `web.log` file.

`python3 filereader.py`: This starts a filereader process that reads data from `web.log` and processes it in different batch sizes
over apache spark. This will require you have apache spark correctly configured.

In case you write huge chunks of data to `web.log`, just use `$ > web.log` from your terminal to truncate the file.

----

Code for regex-based matcher is in `regex` branch, and can be used in the same manner after switching the branches.

