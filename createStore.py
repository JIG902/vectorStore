import sqlite3
import os
import glob
import re
import requests
import json
import logging
from typing import Optional, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the API key is set in the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY is not set. Please set it in your environment.")
    raise EnvironmentError("Missing OPENAI_API_KEY")

# Database configuration
db_path = 'vectorstore.db'

# Function to initialize the database
def initialize_database(db_path: str):
    """
    Initialize the SQLite database with a table for storing vectors and metadata.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vectors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vector BLOB NOT NULL,
                    chapterNumber INTEGER,
                    chapterTitle TEXT,
                    sectionNumber INTEGER,
                    sectionContent TEXT
                )
            ''')
            logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")
        raise

# Function to create metadata
def create_metadata(chapter_number: int, chapter_title: str, section_number: int, text: str) -> Dict:
    """
    Create metadata for a given section of text.
    """
    return {
        'chapterNumber': chapter_number,
        'chapterTitle': chapter_title,
        'sectionNumber': section_number,
        'sectionContent': text
    }

# Placeholder for vector generation
def generate_vector(text: str) -> Optional[list]:
    """
    Generate an embedding vector for the given text using OpenAI API.
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "input": text,
            "model": "text-embedding-ada-002"
        }

        response = requests.post("https://api.openai.com/v1/embeddings", headers=headers, json=data)
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("data", [{}])[0].get("embedding")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error generating vector: {e}")
        return None

# Function to process a single file
def process_file(filename: str, db_connection):
    """
    Process a single text file, extract metadata and vectors, and save them to the database.
    """
    try:
        if not os.path.exists(filename):
            logging.warning(f"File not found: {filename}")
            return

        with open(filename, 'r', encoding='utf-8') as file:
            logging.info(f"Processing file: {filename}")
            chapter_number = int(re.search(r'(\d+)', filename).group(1))
            chapter_title = file.readline().strip()

            buffer = []
            section_number = 1

            for line in file:
                line = line.strip()
                if line:
                    buffer.append(line)
                    if buffer:
                        text = ' '.join(buffer)
                        vector = generate_vector(text)
                        if vector:
                            metadata = create_metadata(chapter_number, chapter_title, section_number, text)
                            save_to_database(db_connection, vector, metadata)
                        buffer.pop(0)
                        section_number += 1
    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}", exc_info=True)

# Function to save data to the database
def save_to_database(connection, vector: list, metadata: Dict):
    """
    Save vector and metadata to the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO vectors (vector, chapterNumber, chapterTitle, sectionNumber, sectionContent)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            json.dumps(vector),  # Serialize vector properly
            metadata['chapterNumber'],
            metadata['chapterTitle'],
            metadata['sectionNumber'],
            metadata['sectionContent']
        ))
        connection.commit()
        logging.info("Data saved to database successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error saving to database: {e}")

if __name__ == "__main__":
    # Initialize database
    initialize_database(db_path)

    # Connect to the database
    with sqlite3.connect(db_path) as conn:
        # Iterate through text files in the 'data' directory
        for filename in glob.glob('data/*.txt'):
            process_file(filename, conn)

    logging.info("File processing complete.")
