# Interview Simulation

This project provides a tool for simulating conversations between an AI assistant and a user. It's designed to help developers rapidly iterate on and improve their AI assistants, particularly for tasks like conducting interviews or generating reports.

## Features

- Simulates back-and-forth conversations using OpenAI's API
- Retrieves initial context from Pinecone vector database
- Saves conversation logs for review and analysis
- Allows easy modification of system prompts and initial contexts

## Prerequisites

- Python 3.7+
- OpenAI API key
- Pinecone API key
- An OpenAI assistant ID

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/grandSpecial/interview-simulation.git
   cd interview-simulation
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and add your API keys and other required information.

## Usage

Run the simulation script:

```
python3 simulate.py
```

The script will generate a simulated conversation and save the log in the `logs` directory.

## Configuration

Adjust the following in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ORGANIZATION_ID`: Your OpenAI organization ID (if applicable)
- `PINECONE_KEY`: Your Pinecone API key
- `ASSISTANT_ID`: The ID of your OpenAI assistant
- `INDEX`: Your Pinecone index name
- `DOC_ID`: The document ID for initial context
- `SYSTEM_PROMPT`: The system prompt for the simulated respondent

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for development and testing purposes only. Ensure you comply with OpenAI's use-case policy and terms of service when using this simulation tool.