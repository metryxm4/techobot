#!/bin/bash

(
    flock -x 200 || exit 1
    
    export PATH=$HOME/bin/:/usr/bin/
    export PYTHONPATH=$HOME/bin/
    
    cd $HOME/projects/u-techobot/
    ./techobot.py
    
    # Some duplicated runs will have like 10 sec difference
    sleep 20
) 200>/<SET-FULL-PATH-IN-DEPLOYMENT>/projects/u-techobot/techobot.lockfile
