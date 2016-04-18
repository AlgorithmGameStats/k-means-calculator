"""
Calculate KMeans from the data input
Input:
------
date := Game stats data input. file with 1 JSON object per line.
k := number of centroids
class_name := name of KMeans cluster
save := If we should save the resulting cluster data to a file (./clusters/class_name.json), in JSON format (defaults to True)
transmit := If we should transmit the results to the server (defaults to False)

Example:

Calculate KMeans cluster with k=2, class='killer', save and transmit for all levels (1-4)
python k-means-calculator.py -st -k 2 -c "killer" ./data/data.20160414.txt
"""
import sys, json, argparse, requests
from kmeans.kmeans import KMeans

# Configurable transmit
game_server = 'http://localhost:5000'
game_clusters_api = 'api/1.0/clusters'
game_server_user = 'something'
game_server_password = 'something secret'

def calculate_kmeans(file_name=None, class_name=None, centroids=2, save=True):
  """
  Calculate KMeans....
  """
  if (not file_name) or (not class_name):
    # If no 'file_name' or no 'class_name', we error
    sys.exit(1)
  
  # Create the KMeans Object
  k = KMeans(class_name=class_name, k=centroids)

  # Open the file, assuming that we have a json object per line
  data = list()
  with open(file_name, 'rb') as f:
    for line in f:
      stat = json.loads(line)
      item = [
        float(stat['time_used']) / float(stat['time_total']), 
        float(stat['coins_collected']) / float(stat['coins_total']), 
        float(stat['enemies_killed']) / float(stat['enemies_total'])
      ]
      data.append(item)

  # Calculate KMeans
  k.put(data)

  # If enabled, save
  if save:
    for i in xrange(1, 5): # Save the same for each level
      save_kmeans(kmeans=k, level=i)

def save_kmeans(kmeans=None, level=1):
  """
  Save the KMeans data as a json object ready to be sent to the server
  """
  if kmeans: # if the object is passed in
    with open('./clusters/{0}.{1}.json'.format(kmeans.class_name(), level), 'wb') as f:
      output = {
        'class_name': kmeans.class_name(),
        'level': level,
        'k': kmeans.k(),
        'centroids': kmeans.centroids,
        'clusters': kmeans.clusters
      }
      f.write(json.dumps(output, indent=2))


if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Calculate KMeans from the data input')
  parser.add_argument('-s', '--save', help='Save cluster data', action='store_true', default=True)
  parser.add_argument('-k', help='Value of \'k\' (centroids)', required=True, type=int, default=2)
  parser.add_argument('-c', help='Class name of KMeans cluster', required=True, default='killer')
  parser.add_argument('file', help='path to the file containing list of integers', default='')

  # Get/parse arguments
  args = parser.parse_args()

  calculate_kmeans(
    file_name=args.file, 
    class_name=args.c.strip(), 
    centroids=args.k,
    save=args.save
  )