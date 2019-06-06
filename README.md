# Map tiles for QGIS
Project for creating map tiles in QGIS for use in Atlas

## Usage
- Add script to scripts folder in QGIS or add script in tools window
- run script MT (map tiles):

![Script settings](https://github.com/stumpam/map_tiles/blob/master/screenshot.png)

## Required Options
-  `Input layer` - vector point layer, from which will be map tiles calculated
   - optionally you can pick just selected items
- `Width` - default: *600* - width of map tile in meters
- `Height` - default: *400* - height of map tile in meters
- `Extra` - default: *5* - extra width and height of a buffer of input elemets
- `Output layer` - name of output layer, it should also be the virtual one
