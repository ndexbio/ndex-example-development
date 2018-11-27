## Process for running HiView caching script

#### Install dependencies
```javascript
npm install
```

#### Run the processing script
```javascript
node_modules/.bin/babel-node app.js 1
```

#### Script explaination

The script is run by using the babel version of node.js and accepts a single command line parameter (see above example). Regular node.js doesn't fully support the syntax used in cyjs2tree.js.


#### Input
1. To specify which uuids you want to process load them in `uuids.txt`.  One uuid per line.


2. Which process to run:

    |Command line parameter value   |Description   |Notes   |
    |---|---|---|
    | 1  | Run CX to Cytoscape.js conversion.  Result(s) stored in **cyjs_files\\\<uuid\>.json** |Uses the **CX Mate** service running at [http://35.203.154.74:3001/ndex2cyjs/uuid/?server=test](http://35.203.154.74:3001/ndex2cyjs/'7b070b40-e555-11e8-9c46-0660b7976219/?server=test) to convert cx to ctyoscape.js.|
    | 2  | Run CX to D3 conversion. Result(s) stored in **D3_files\\\<uuid\>.json**  |Uses cyjs2tree.js (Kei) to convert CX to the d3-hierarchy format|
    | 3  | Run Cytoscape.js to D3 conversion. Result(s) stored in **D3_files\\\<uuid\>.json**  |None|




