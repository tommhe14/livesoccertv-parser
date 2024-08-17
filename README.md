Run "await fetch_matches(country, team, timezone=None)" 

eg. 

```py
matches = await fetch_matches('england', 'arsenal', timezone='Europe/London')
print([match.__dict__ for match in matches])

>>> [
  {'live': False, 'played': True, 'competition': 'Unknown', 'time': 'Unknown', 'game': 'Arsenal vs AFC Bournemouth', 'tvs': ['Bet365', 'Sport TV1', 'Arena Sport 1 Croatia', 'Sport Plus', 'MAXtv To Go'], 'date': 'Full Time'},
  ...
]
