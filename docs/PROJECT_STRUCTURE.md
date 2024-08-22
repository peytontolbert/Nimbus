# Project Structure

## Root Directory
- SimSun.ttf
- agent_data/
- gpt/
- main.py
- requirements.txt
- __pycache__/
- autodevin.py
- interfaces/
- memory/
- tests/
- agent/
- data/
- llm/
- models/
- workspace/

## agent
- __init__.py
- boostrap.py
- main.py
- task_manager.py
- idle_activities.py
- message_handler.py
- utils.py

## agent/__pycache__
- __init__.cpython-310.pyc
- boostrap.cpython-310.pyc

## agent_data
- agent_data.json
- episodic_memory/
- semantic_memory/

## gpt
- chatgpt.py
- llm_server.py

## interfaces
- __init__.py
- http_server.py
- user_interface.py

## llm
- __pycache__/
- generate_task_plan/
- list_output_parser.py
- summarize/
- extract_entity/
- json_output_parser.py
- reason/

## llm/extract_entity
- __init__.py
- __pycache__/
- prompt.py
- schema.py

## llm/generate_task_plan
- __pycache__/
- prompt.py

## llm/reason
- __init__.py
- __pycache__/
- prompt.py
- schema.py

## llm/summarize
- __pycache__/
- prompt.py

## memory
- HuggingFaceEmbeddings
- __init__.py
- memory.py
- Pooling.py
- __pycache__/
- procedural_memory.py
- Transformer.py
- episodic_memory.py
- semantic_memory.py

## models
- __init__.py
- __pycache__/
- chatgpt_interface.py

## tests

## workspace
- toolbag/
- tools/
- work/

## workspace/toolbag
- __pycache__/
- toolbag.py
- tools.json

## workspace/tools
- __pycache__/
- gamification.py
- reminders.py
- base.py
- imageprocessing.py
- socialmediaautomation.py
- coding.py
- integration.py
- taskautomation.py
- contentgeneration.py
- languageprocessing.py
- think.py
- datacleaning.py
- message.py
- toolmanagement.py
- datavisualization.py
- networkmonitoring.py
- virtualassistance.py
- eventmanagement.py
- notes.py
- webscraping.py
- filemanager.py
- personalizedlearning.py

## workspace/tools/__pycache__
- SerpAPIWrapper.cpython-310.pyc
- languageprocessing.cpython-311.pyc
- audioanalysis.cpython-310.pyc
- message.cpython-310.pyc
- audioanalysis.cpython-311.pyc
- message.cpython-311.pyc
- base.cpython-310.pyc
- networkmonitoring.cpython-310.pyc
- base.cpython-311.pyc
- networkmonitoring.cpython-311.pyc
- coding.cpython-310.pyc
- notes.cpython-310.pyc
- coding.cpython-311.pyc
- notes.cpython-311.pyc
- contentgeneration.cpython-310.pyc
- personalizedlearning.cpython-310.pyc
- contentgeneration.cpython-311.pyc
- personalizedlearning.cpython-311.pyc
- datacleaning.cpython-310.pyc
- quantumcomputing.cpython-310.pyc
- datacleaning.cpython-311.pyc
- reminders.cpython-310.pyc
- datavisualization.cpython-310.pyc
- reminders.cpython-311.pyc
- datavisualization.cpython-311.pyc
- socialmediaautomation.cpython-310.pyc
- eventmanagement.cpython-310.pyc
- socialmediaautomation.cpython-311.pyc
- eventmanagement.cpython-311.pyc
- taskautomation.cpython-310.pyc
- filemanager.cpython-310.pyc
- taskautomation.cpython-311.pyc
- filemanager.cpython-311.pyc
- think.cpython-310.pyc
- gamification.cpython-310.pyc
- think.cpython-311.pyc
- gamification.cpython-311.pyc
- toolmanagement.cpython-310.pyc
- imageprocessing.cpython-310.pyc
- toolmanagement.cpython-311.pyc
- imageprocessing.cpython-311.pyc
- virtualassistance.cpython-310.pyc
- integration.cpython-310.pyc
- virtualassistance.cpython-311.pyc
- integration.cpython-311.pyc
- webscraping.cpython-310.pyc
- languageprocessing.cpython-310.pyc
- webscraping.cpython-311.pyc

