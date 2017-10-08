# Movie Trailer Website

A Python project to generate a text file report of queries made on a log database.

_Created in partial fulfillment of Udacity's Full Stack Web Developer Nanodegree_

## Requirements
* [Python3.x](https://www.python.org/)
* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)

## Project Files
* log-analysis-tool.py - main executable Python script; generates text file report
* log_output.txt - sample report file 

## Setup
1. Install all required programs.
2. Clone OR download [VM](https://github.com/udacity/fullstack-nanodegree-vm) repository.
3. Download and unzip [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into the Vagrant directory.
4. Clone this repository OR download and unzip the project zip file into Vagrant directory.

## Running the Project
1. In the command-line interface, launch the Vagrant VM from inside the Vagrant directory using:

`$ vagrant up`

`$ vagrant ssh`

2. Change directory to /vagrant.
3. Load the data using:

`psql -d news -f newsdata.sql`

4. Run the analysis tool using:

`$ python3 log-analysis-tool.py`


A text file report will be saved in the same directory.
