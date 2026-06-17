Waifu Lore is a Python-based LLM character agent project.



It supports configurable character presets, prompt-based personality settings, recent conversation context, optional local voice generation, and persistent long-term memory summarization with SQLite.



The goal of this project is to build an AI character companion system that can be extended into an agent with memory retrieval, tool usage, and voice interaction.



Features

Multiple character preset support

Character configuration with character.json

Independent prompt file for each character

LLM-powered dialogue through DeepSeek API

Recent conversation context management

Optional local voice generation with Voicebox

Voice files saved separately in the voices/ folder

SQLite-based persistent memory storage

Conversation summarization for long-term memory

Automatic memory compression after long conversations

Memory saving before program exit

Project Structure

Waifu Lore/

├── main.py

├── api.py

├── character\_manager.py

├── database.py

├── memory\_manager.py

├── voice\_generate.py

├── characters/

│   └── example\_character/

│       ├── character.json

│       └── prompt.md

├── voices/

├── .env

├── .gitignore

└── README.md

Tech Stack

Python

DeepSeek API

OpenAI-compatible SDK

SQLite

Prompt Engineering

Voicebox local TTS API

Git / GitHub

How It Works



The program starts by loading available character presets from the characters/ folder.



Each character has its own:



character.json

prompt.md



After the user selects a character, the program builds a system prompt from the selected character prompt and starts a conversation through the DeepSeek API.



During the conversation, recent messages are kept as short-term context. When the conversation becomes long, older messages are summarized into long-term memory and saved into SQLite.



The system keeps recent messages for continuity while compressing older messages into persistent memory.



Memory Design



Waifu Lore currently uses two levels of memory:



Short-term Context



Recent conversation messages are kept in memory during the current session.



Long-term Memory



Older conversation messages are summarized by the LLM and saved into SQLite.



The memory table stores:



id

character\_id

content

created\_at



Each memory is linked to a specific character by character\_id.



Voice Interaction



Waifu Lore can optionally generate local voice output through Voicebox.



The current flow is:



LLM reply

↓

clean text for voice

↓

generate voice file

↓

display text

↓

play voice



Voice files are saved into the voices/ folder and ignored by Git.



How to Run



Install dependencies:



pip install openai python-dotenv requests playsound==1.2.2



Create a .env file:



DEEPSEEK\_API\_KEY=your\_api\_key\_here



Run the project:



python main.py

Current Status



Implemented:



Character preset selection

Character prompt loading

DeepSeek API dialogue

Recent context handling

Optional Voicebox voice output

SQLite memory database

Long conversation summarization

Long-term memory persistence



Planned:



RAG-based memory retrieval

Embedding-based memory search

Memory deduplication

Tool-style agent actions

Web UI or desktop UI

Better character creation workflow

Project Goal



The long-term goal of Waifu Lore is to become an LLM-powered character agent with:



configurable persona

persistent memory

RAG-based memory retrieval

tool calling

voice interaction

extensible character presets

