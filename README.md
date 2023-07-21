# Vector Search Agents with Audio support for Q/A

## Sample Company - Call Center Support
This project is a sample implementation of a call center support system that utilizes large language models (LLMs) and audio input to provide accurate and contextual responses to customer queries. The system is built using Python and utilizes various libraries, including Streamlit, OpenAI, and PIL.

# Requirements
To run this project, you will need to install the following dependencies:
* Streamlit
* OpenAI
* PIL
* audiorecorder
* Astra DB / Cassandra
  
You will also need to obtain an OpenAI API key and set it as a global variable in the config.py file. Additionally, you will need to set the following variables in the config.py file:
* config_astra_db_secure_connect_bundle_path: the path to the secure connect bundle for your Astra DB instance
* config_astra_db_token_id: the client ID for your Astra DB instance
* config_astra_db_token_password: the client secret for your Astra DB instance
* config_astra_db_keyspace: the name of the keyspace in your Astra DB instance
* config_astra_db_vector_tablename: the name of the table in your Astra DB instance that contains the vector embeddings
* config_open_ai_secret: your OpenAI API key

# Usage
To use the system, run the main.py file and click the "Click to record" button to start recording audio. Once you have finished recording, the system will transcribe the audio and generate a response using Astra DB for Vector Search and the Open AI LLM for Q/A. 
The response will be displayed on the Streamlit interface, along with the original audio recording.

# License
This project is licensed under the Apache License, Version 2.0. See the LICENSE file for more details.

# Contributing
Contributions to this project are welcome. Please refer to the CONTRIBUTING file for guidelines on how to contribute.

# Support
If you encounter any issues or have any questions, please open an issue on the GitHub repository.


# Tools
This project includes a tools.py file that contains the following tools:

AudioSearch

This tool utilizes vector search to find the most relevant document in a Astra DB database based on the user's audio input. The tool uses the OpenAI API to generate an embedding for the user's audio input and then queries the Cassandra database to find the document with the most similar embedding. To use this tool, import it from tools.py and call its _run method with the user's audio input as a parameter. The tool will return the most relevant document from the database.
For more information on the tools included in this project, please refer to the comments in the tools.py file.
