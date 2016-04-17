kmeansimport sys, json, argparse

def min_max(file_name=''):
  """
  Find the min and max values from a KMeans cluster
  """
  final = ""
  with open(file_name, 'rb') as f:
    final += f.read()

  # Load the json cluster data
  kmeans = json.loads(final)

  # find the 'x' value
  x = list()
  y = list()
  z = list()
  for i in range(kmeans['k']):
    for item in kmeans['clusters'][i]:
      x.append(item[0])
      y.append(item[1])
      z.append(item[2])

  return [min(x), min(y), min(z)], [max(x), max(y), max(z)]

  return final_array

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Find the min and max values from a KMeans cluster')
  parser.add_argument('file', help='path to the file containing list of integers', default='')

  # Get/parse arguments
  args = parser.parse_args()

  mins, maxes = min_max = min_max(
    file_name=args.file
  )

  print mins
  print maxes