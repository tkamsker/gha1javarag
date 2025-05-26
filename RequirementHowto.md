
# loaded coe into rag 
python pyingest_java2chroma.py

# logfile -> 2025-05-23.log


# example of processing callgraph
import json

call_graph = {}
with open("call-graph.txt") as f:
    for line in f:
        caller, callee = line.strip().split(" ")
        call_graph.setdefault(caller, []).append(callee)

with open("call-graph.json", "w") as f:
    json.dump(call_graph, f)



