#!/usr/bin/env python3
# LOAD CONFIG - needs config.py
import config as cfg

#import needed libraries
from langchain.document_loaders import PyPDFLoader 
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import Cassandra 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
import time
import datetime
import logging

# configure the logging module
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#establish Astra connection
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# set parameters for AstraDB
ASTRA_DB_TOKEN_BASED_USERNAME=cfg.config_astra_db_token_id
ASTRA_DB_TOKEN_BASED_PASSWORD=cfg.config_astra_db_token_password
ASTRA_DB_KEYSPACE=cfg.config_astra_db_keyspace
ASTRA_DB_TABLE_NAME=cfg.config_astra_db_vector_tablename
ASTRA_DB_SECURE_CONNECT_BUNDLE_PATH=cfg.config_astra_db_secure_connect_bundle_path

# create a session for AstraDB
cloud_config = {
   'secure_connect_bundle': ASTRA_DB_SECURE_CONNECT_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_DB_TOKEN_BASED_USERNAME, ASTRA_DB_TOKEN_BASED_PASSWORD)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()


#set parameters for openAI
import os
os.environ['OPENAI_API_KEY'] = cfg.config_open_ai_secret







# loop through all files in the folder all X seconds
while True:
	for filename in os.listdir(cfg.config_inputdir):
		# check if the file is a PDF
		if filename.endswith(".pdf"):
			# load the PDF file
			doc_path = os.path.join(cfg.config_inputdir, filename)
			loader = PyPDFLoader(doc_path)
			pages = loader.load_and_split()
			logging.info(f"Processed PDF file: {filename}")
		# check if the file is a TXT 
		elif filename.endswith(".txt"):
			doc_path = os.path.join(cfg.config_inputdir, filename)
			loader = TextLoader(doc_path)
			pages = loader.load_and_split()
			logging.info(f"Processed TXT file: {filename}")
		# other files will not be processed
		else:
				# handle the case where the file has an unsupported extension
				logging.info(f"Unsupported file type: {filename}")

		# if some file was loaded 
		if len(pages) > 0:
			# store in our vectordb
			embeddings = OpenAIEmbeddings()
			vectordb = Cassandra.from_documents(documents=pages, 
				embedding=embeddings, 
				persist_directory=".",
				session=session,
				keyspace=ASTRA_DB_KEYSPACE,
				table_name=ASTRA_DB_TABLE_NAME,
			)
			
			# move processed files into another folder
			output_file = os.path.join(cfg.config_outputdir, filename)
			os.rename(doc_path, output_file)

			# empty pages
			pages = ""
	logging.info(f"Run completed - {datetime.datetime.now()}")
	time.sleep(5)
#this python code will now loop infinitely. 