# Wikirace - Shortest path between two Wikipedia articles

This web application loads a graph representing Wikipedia pages and their links. It offers a web interface to find the shortest path between a starting and target article.

## Prerequisites 

### Resources from wikipedia

- Unpacked list of all articles titles e.g. https://dumps.wikimedia.org/dewiki/latest/ dewiki-latest-all-titles-in-ns0.gz 
- Directed unweighted graph of Wikipedia (nodes are the articles and edges are the links) in Networkit binary format (see: https://networkit.github.io/dev-docs/python_api/graphio.html#networkit.graphio.NetworkitBinaryReader)

### Networkit 

For now the default Networkit python module. In future the fork https://github.com/CyberSchrotti/networkit will be required.

### ENVs

- FLASK_SECRET_KEY: Key used by flask
- WIKIRACE_WORKING_DIR: path to dir that contains the Wikipedia resources (prefix of WIKIRACE_GRAPHPATH and WIKIRACE_ALLTITLESPATH)
- WIKIRACE_GRAPHPATH: path to the wikipedia graph
- WIKIRACE_ALLTITLESPATH: path to list of all articles titles