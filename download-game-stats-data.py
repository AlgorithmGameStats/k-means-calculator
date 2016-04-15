"""
Download stats data from the game-server
The data stored is only for one day: as shown by 'stats_date'
Saves the data in ./data/data.YYYYMMDD.txt
"""
import json, datetime, requests
from datetime import datetime
from dateutil import tz

# Configurable Fetching
game_server = 'http://localhost:5000'
game_stats_api = 'api/1.0/stats'
game_server_user = 'something'
game_server_password = 'something secret'
stats_date = "04/15/2016" # format dd/mm/yyyy


#### Special Time converting stuff
# Timestamp Format
# "timestamp": "Fri, 15 Apr 2016 20:01:51 GMT"
timestamp_format = '%a, %d %b %Y %H:%M:%S %Z'
date_format = '%m/%d/%Y'
default_date = datetime.utcnow().strftime(timestamp_format)
comp_date = datetime.strptime(stats_date, date_format).date()

# JSON Datetime Encoder
class DatetimeEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime(timestamp_format)
    # Let the base class default method raise the TypeError
    return json.JSONEncoder.default(self, obj)
####


# Make the HTTP GET request.
r = requests.get(
  '{0}/{1}'.format( game_server, game_stats_api ),
  auth=( game_server_user, game_server_password )
)

# Parse the response as json
stats = r.json()

# Open the output file
with open('./data/data.{0}.txt'.format(comp_date.strftime('%Y%m%d')), 'wb') as f:
  # For each item in the stats array
  for stat in stats.get('stats', []):

    # Convert the timestamp field to an actual date/time
    stat['timestamp'] = datetime.strptime(stat.get('timestamp', default_date), timestamp_format)
    from_zone = tz.tzutc() # We assume the server sends data in UTC/GMT as we should ...
    to_zone = tz.tzlocal()

    # Tell the datetime object that it's in UTC time zone since 
    # datetime objects are 'naive' by default
    stat['timestamp'] = stat['timestamp'].replace(tzinfo=from_zone)

    # Convert time zone
    stat['timestamp'] = stat['timestamp'].astimezone(to_zone)

    # Store data ONLY if the date is the one we want
    if stat['timestamp'].date() == comp_date:
      print stat['timestamp']

      # Convert line to String and store in file
      line = json.dumps(stat, cls=DatetimeEncoder)
      f.write('{0}\n'.format(line))