# route planning for location spoofing
API endpoint which provides a different location coordinate for each GET request, ultimately simulating 'a walk' (infinitely looped) if requested frequent enough. 

Route can be set along pokestops thus allowing pokestop visits and egg hatching.

# How
Make a mobile client which pings the endpoint pokemongo.zerongtonywang.com/location/?secret=<PROVIDED_BY_ME> with GET, ideally every 2~5 seconds. Use coordinates to spoof mobile location.

# Future
* allow public facing, user set their own routes etc
* create coordinate fluxuation to avoid precise locations

NOTE: words are Niantic is big on banning location spoofers, lol
