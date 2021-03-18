# Fog Map Demo

This project is to test the feasibility of the fog map idea:
map starts as covered by something like fog and as user physically 
visits location the fog gets cleared up.

### Tile Considerations

This demo uses open streets map. The way maps works is they render 
squares (tiles) based on the location and also on zoom.

If you zoom out completely the entire map is likely comprised of 2/4 tiles.
If you zoom in at highest level there are normally several tiles.

What this means is that London city can be **one tile** if seen zoomed out, or be **many tiles** if you zoom in.

Problem: how does the fog covering change for a wide area such as London given 
that the user has only seen a bunch of locations?

### Proposed approach

Remember that tiles change with zoom level.
We set a zoom level that correspond to our minimum resolution
(i.e. if you have been in any point inside a tile at that zoom level, the entire tile is marked as "seen")

This means that if a user views the map with a zoom level equal to our chosen 
minimum resolution zoom level, the map will appear as squares that are either 
covered entirely with fog or entirely visible.

If you zoom out we need to calculate how many tiles inside the bigger tiles the user has seen.
If they have seen all sub-tiles then the super-tile will be cleared, otherwise
it's gonna be covered with "fog" with a transparency inversely proportional
to number of sub-tiles visited.


## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

