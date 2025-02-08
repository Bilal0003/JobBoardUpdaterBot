#!/bin/bash
cd /home/bilal0003/Projects/JobBoardUpdaterBot/
source venv/bin/activate
for site in apec hellowork
do
    python3 scripts/"$site".py
done
deactivate
