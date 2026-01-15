# Doccy: Emotionally-Aware Chatbot
Doccy is an emotionally intelligent chatbot designed to understand and adapt to the user's emotional state. Unlike standard stateless bots, Doccy tracks preferences, emotional patterns, and conversation history over time to create a truly personalized conversational experience.

## Features
- **Emotion Detection**: Analyzes user input to recognize emotional states (happy, sad, angry, anxious, etc.) and their intensity levels
- **Preference Tracking**: Automatically detects and remembers what users like and dislike based on natural language cues (e.g., "love", "hate", "enjoy")
- **Context-Aware Responses**: Incorporates recent conversation history and long-term preferences into every interaction for meaningful continuity
- **Persistent Memory**: Uses local JSON-based caching to store conversation history across sessions
- **Intelligent Summarization**: Automatically condenses older conversations into concise summaries, maintaining context while reducing memory overhead and API costs
- **Empathetic Responses**: Adjusts tone and content based on detected emotional state to provide supportive, context-appropriate replies

## Technologies Used
- **Language**: Python 3.x
- **AI Engine**: Google gemini-3-flash-preview
- **Data Structures**: `collections.deque` for efficient conversation history management
- **Storage**: JSON-based local file caching
- **Environment Management**: python-dotenv

## Why I Built This
I built Doccy to move beyond basic, stateless chatbots and explore how conversational AI can become more personal, emotionally aware, and context-driven.

While learning to work with AI APIs, I realized that many chatbot projects stop at simple prompt–response interactions. I wanted to understand what it actually takes to build a chatbot that remembers, adapts, and responds differently based on the user's emotional state and past interactions.

### Key Learning Goals
Through this project, I explored:

- **Emotional Intelligence**: How emotions can influence conversation flow, tone, and the usefulness of responses
- **Memory Management**: How past conversations and preferences can be stored, summarized, and reused to improve personalization
- **Prompt Engineering**: How prompt design and memory management directly affect response quality, cost, and performance with LLMs
- **Efficient Summarization**: Using AI-powered summarization to retain important context while reducing token usage and API costs
- **Stateful AI Systems**: Building systems where memory, emotion detection, and personalization work together cohesively

Doccy became a hands-on way for me to experiment with stateful AI systems and understand the real-world constraints of LLM-based applications, such as efficiency, context limits, and cost-awareness.

Ultimately, I built Doccy to deepen my understanding of how modern chatbots can be designed to feel more human, intentional, and useful, while remaining technically lightweight and extensible for future improvements.

## How It Works
1. **Emotion Analysis**: Your message is first sent to the Gemini API to analyze emotional content, detecting both emotion type and intensity
2. **Context Gathering**: The system retrieves your last 5 messages, top preferences (likes/dislikes), long-term memory summaries, and current emotional state
3. **Personalized Response Generation**: Using the "Doccy" persona (an empathetic and warm assistant), a context-rich prompt is constructed and sent to generate a tailored response
4. **Preference Extraction**: Before replying, Doccy scans your input for preference keywords ("love", "like", "hate", "dislike") and saves them to the local cache
5. **Memory Management**: After 20 messages, older conversations are automatically summarized to maintain context without exceeding token limits

## Getting Started
### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Code editor (VS Code recommended)

### Steps to setup and run locally
1. **Clone the repository**
```bash
   git clone https://github.com/VD-17/Doccy.git
   cd Doccy
```

2. **Install dependencies**
```bash
   pip install google-genai python-dotenv
```
   
   Or use requirements.txt if available:
```bash
   pip install -r requirements.txt
```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
```bash
   .env
```
   
   Add your Gemini API key:
```
   GEMINI_API_KEY=your_api_key_here
```

4. **Run the bot**
```bash
   python main.py
```

5. **Start chatting!**
   
   Type your message and press Enter. Type `quit`, `exit`, or `bye` to end the conversation. Your conversation history is automatically saved for next time.

## Project Structure
```
Doccy/
├── main.py              # Main chatbot implementation
├── chat_data.json       # Conversation history and preferences (auto-generated)
├── .env                 # Environment variables (create this)
├── .env.example         # Example environment file
└── README.md           # Project documentation
```

## Data Storage
Doccy stores all conversation data locally in `chat_data.json`, including:

- Conversation history (last 50 messages)
- User preferences (likes and dislikes)
- Emotional patterns
- Conversation summaries
- Timestamps for all interactions

This file is automatically created on first run and updated after each interaction.

## Future Improvements

- [ ] **Offline Mode**: Integrate a local LLM for privacy-focused, internet-free operation
- [ ] **Domain Specialization**: Adapt Doccy for specific use cases (mental health support, learning assistant, customer service)
- [ ] **Web/Mobile UI**: Build an intuitive graphical interface using Flask/FastAPI and React
- [ ] **Voice Integration**: Add speech-to-text and text-to-speech capabilities
- [ ] **Multi-user Support**: Enable separate conversation histories for different users
- [ ] **Export Functionality**: Allow users to export their conversation history
- [ ] **Analytics Dashboard**: Visualize emotional patterns and conversation insights over time
