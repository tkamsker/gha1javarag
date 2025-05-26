# prep

cd crewai
pip install -r requirements.txt

# 
OPENAI_API_KEY=your_api_key_here

# 
python main.py

# 
ava_crew_ai/
├── __init__.py
├── agents/
│   ├── __init__.py
│   └── java_agents.py
├── tasks/
│   ├── __init__.py
│   └── java_tasks.py
├── tools/
│   ├── __init__.py
│   └── rag_tools.py
├── main.py
└── setup.py

# run 
python run_java_analysis.py