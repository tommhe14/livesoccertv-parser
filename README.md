Syntax:

```py
await fetch_matches(country, team, timezone=None)
```
*COUNTRY*: The team's origin country\n
*TEAM*: Team Name\n
*TIMEZONE*: Your specific PYTZ timezone, Defaults to whatever you specify in `DEFAULT_TIMEZONE`

Example Usage:

```py
matches = await fetch_matches('england', 'arsenal', timezone='Europe/London')
print([match.__dict__ for match in matches])

>>> [
  {
    'live': False,
    'played': True,
    'competition': 'Unknown',
    'time': 'Unknown',
    'game':'Arsenal vs AFC Bournemouth',
    'tvs': ['Bet365', 'Sport TV1', 'Arena Sport 1 Croatia', 'Sport Plus', 'MAXtv To Go'],
    'date': 'Full Time'
  },
    ...
]
```


