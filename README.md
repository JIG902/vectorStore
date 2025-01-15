# Vector Store Builder

## Overview
This project is a Python-based sample script that demonstrates how to process text files, generate vector embeddings using OpenAI's API, and store the data in a SQLite database. The resulting database can be used for semantic searches over the processed text.

## Features
- Reads text files from the `./data` folder.
- Extracts metadata from each file, including chapter number, title, and section content.
- Uses OpenAI's `text-embedding-ada-002` model to vectorize text.
- Stores vectors and metadata in a SQLite database (`vectorstore.db`).
- Logs all major operations and errors for easy debugging.

## Prerequisites
- Python 3.7+
- OpenAI API key (set as the environment variable `OPENAI_API_KEY`).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/JIG902/vectorStore.git
   cd vectorStore
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   - **Linux/macOS**:
     ```bash
     export OPENAI_API_KEY="your_api_key_here"
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     set OPENAI_API_KEY=your_api_key_here
     ```
   - **Windows (PowerShell)**:
     ```powershell
     $env:OPENAI_API_KEY="your_api_key_here"
     ```

## Usage
1. Place your text files in the `./data` directory. Ensure filenames include chapter numbers (e.g., `chapter1.txt`).

2. Run the script:
   ```bash
   python createVector.py
   ```

3. The script will process the text files, generate embeddings, and store them along with metadata in `vectorstore.db`.

## File Format
Each text file should:
- Have the chapter title as the first line.
- Contain the text content divided into sections by blank lines (if applicable).

## Output
- A SQLite database (`vectorstore.db`) with the following table:
  - **`id`**: Auto-incrementing primary key.
  - **`vector`**: Serialized vector embedding.
  - **`chapterNumber`**: Numeric identifier from the filename.
  - **`chapterTitle`**: First line of the file.
  - **`sectionNumber`**: Sequential section number.
  - **`sectionContent`**: The actual text content of the section.

## Semantic Search Example
Once the database is populated, you can use it for semantic search by querying vectors and comparing embeddings.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- OpenAI for the embedding API.

