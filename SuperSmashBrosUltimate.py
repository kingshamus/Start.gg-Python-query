SuperSmashBrosUltimate.py
import requests
import json
import pandas as pd
import time

# Replace *** within token with your Start.gg api key

token = "***"
headers = {"Authorization": "Bearer " + token}

# I recommend leaving the perPage as 450 as start.gg has an issue with pulling to much tournament info as the results become more complex
# Here you can change the videogameId to the desired game

query = """query TournamentsByVideogame($perPage: Int!, $videogameId: ID!) {
  tournaments(query: {
    perPage: $perPage
    page: 1
    sortBy: "startAt asc"
    filter: {
      upcoming: true
      videogameIds: [
        $videogameId
      ]
    }
  }) {
    nodes {
      name
      url
      venueAddress
      isRegistrationOpen
      }
    }
  }
  """
variables = {
  "perPage": 450,
  "videogameId": 1386
} 

url = 'https://api.start.gg/gql/alpha'
r = requests.post('https://api.smash.gg/gql/alpha', json={'query': query, 'variables': variables}, headers=headers)

print(r.status_code)
print(r.text)

json_data = json.loads(r.text)

# The section below structures the json data into a csv file, it removes any tournaments that have closed registration adds the url so the tournaments now have hyperlinks and saves the info as a CSV file for easy reading, The CSV file name can be changed here

df_data = json_data['data']['tournaments']['nodes']
df = pd.DataFrame(df_data)
df2 = df
df2
new_row = {'remove':'row'}
df2 = df.append(new_row, ignore_index=True)
df2 = df2[df2.isRegistrationOpen != False]
df2.insert(1, 'game', 'Super Smash Bros Ultimate')
df2
df2['link'] = "https://start.gg" + df2['url']
df2 = df2.drop(['isRegistrationOpen', 'url'], axis=1)
time.sleep(5)

df2.to_csv('Super Smash Bros Ultimate.csv', index=False)

# The sleep below is optional, I include it as I run multiple scripts back to back and prefer them running one at a time, so the sleep is to reduce the possibility of them overlapping

time.sleep(5)
