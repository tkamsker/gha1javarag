've made several important changes to fix the clustering issues and improve the code:
1. In cluster_engine.py:
- Added threadpool configuration to prevent warnings
- Forced single-threaded execution for KMeans
- Improved error handling and logging
- Added better cluster statistics

2. In main.py:
- Created a new SemanticAnalyzer class to better organize the code
- Improved error handling and logging
- Added better results organization and output
- Simplified the configuration loading
- Added a summary output

3. Created a new config.json with basic settings for:
- Clustering parameters
- Embedding model configuration
- Logging settings

To run the code:
Make sure you have the Doxygen XML files in the data/xml directory
Run the main script:

python src/main.py


The script will:
1. Parse the Doxygen XML files
2. Generate embeddings for each artifact
3. Cluster the artifacts
4. Save the results to data/results/clustering_results.json
5. Print a summary of the analysis
- The results will include:
- Total number of artifacts analyzed
- Number of clusters
- Size of each cluster
- Detailed information about each artifact in its cluster
