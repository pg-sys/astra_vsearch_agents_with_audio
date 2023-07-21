from langchain.tools import BaseTool
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import streamlit as st
import openai
import config as cfg

### parameters #########
SECURE_CONNECT_BUNDLE_PATH = cfg.config_astra_db_secure_connect_bundle_path
ASTRA_CLIENT_ID = cfg.config_astra_db_token_id
ASTRA_CLIENT_SECRET = cfg.config_astra_db_token_password
cloud_config = {
    'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
    }
auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
openai.api_key = cfg.config_open_ai_secret

### Character Recognition and Vector Search tool #########
class AudioSearch(BaseTool):
    name = "AudioSearch"
    description = "Use this tool that you are asked information about invoice" \
                    "Give the summary of the solution "

    def _run(self,user_question):
        KEYSPACE_NAME = cfg.config_astra_db_keyspace
        TABLE_NAME = cfg.config_astra_db_vector_tablename
        model_id = "text-embedding-ada-002"
        embedding = openai.Embedding.create(input=user_question, model=model_id)['data'][0]['embedding']
        for row in session.execute(f"SELECT document_id,document,embedding_vector FROM {KEYSPACE_NAME}.{TABLE_NAME} ORDER BY embedding_vector ANN OF {embedding} LIMIT 1"):
                med_res = row.document 

        return med_res 

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
