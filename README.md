# K-Means Calculator

Here we have several script that will calculate KMeans and update the 
Game-Server cluster data.

## Set up:

* Have Python 2.7.x installed
* Have pip installed
* Install dependencies via pip: `pip install -r requirements.txt`

## How to Run:
* Modify the files `download-game-stats-data.py` and `k-means-calculator.py`
** Do this to add the correct server information, the variables below should be at the top of the file
** `game_server`, `game_server_user`, `game_server_password`
* Modify the variable `stats_date` in `download-game-stats-data.py` to the date on which the data you want ocurred
* Run:
** First, run `python download-game-stats-data.py` to download the data
*** e.g. `python download-game-stats-data.py`
** Then run `k-means-calculator.py` to calculate kmeans, store the calculated data (and/or transmit it to the server)
*** e.g. `python k-means-calculator.py -st -k 2 -c "killer" ./data/data.20160414.txt`