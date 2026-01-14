from google import genai
import json 
import os 
from datetime import datetime 
from collections import deque 
from dotenv import load_dotenv

class Chatbot: 
    def __init__(self, api_key, cache_file="chat_data.json"):
        self.client = genai.Client(api_key=api_key)
        self.cache_file = cache_file
        self.conversation_history = deque(maxlen=50)
        self.user_preferences = {
            "likes": [],
            "dislikes": [],
            "topics_discussed": {},
            "emotional_patterns": []
        }
        self.load_data()

    def load_data(self): 
        if os.path.exists(self.cache_file):
            try: 
                with open(self.cache_file, 'r') as f: 
                    data = json.load(f)
                    self.conversation_history = deque(data.get("history", []), maxlen=50)
                    self.user_preferences = data.get("preferences", self.user_preferences)
            except:
                pass

    def save_data(self):
        data = {
            "history": list(self.conversation_history),
            "preferences": self.user_preferences,
            "last_updated": datetime.now().isoformat()
        }
        with open(self.cache_file, "w") as f:
            json.dump(data, f, indent=2)

    def detect_emotion(self, user_input):
        emotion_prompt = f"""Analyze the emotion in this message and respond with only a JSON object: 
        Message: "{user_input}"
        return format: 
            {{"emotion": "happy/sad/angry/anxious/neutral/excited/frustrated", "intensity": "low/medium/high", "keywords": ["word1", "word2"]}}"""
        
        try: 
            response = self.client.models.generate_content(
                model = "gemini-3-flash-preview",
                contents = emotion_prompt
            )

            emotion_data = json.loads(response.text.strip())
            return emotion_data
        except:
            return {"emotion": "neutral", "intensity": "low", "keywords": []}
        
    def track_preferences(self, user_input, bot_response):
        if any(word in user_input.lower() for word in ["love", "like", "enjoy", "favourite"]):
            self.user_preferences["likes"].append({
                "statement": user_input,
                "timestamp": datetime.now().isoformat()
            })

        if any(word in user_input.lower() for word in ["hate", "dislike", "don't like", "annoying"]):
            self.user_preferences["dislikes"].append({
                "statement": user_input,
                "timestamp": datetime.now().isoformat()
            })

        self.save_data()

    def summarize_old_conversation(self):
        if len(self.conversation_history) < 10:
            return 
        
        to_summarize = list(self.conversation_history)[:5]
        summary_prompt = f"Summarize the following interaction into 3 key bullet points regarding user facts or mood: {to_summarize}"

        try: 
            response = self.client.models.generate_content(
                model = "gemini-3-flash-preview",
                contents = summary_prompt
            )

            if "summaries" not in self.user_preferences: 
                self.user_preferences["summaries"] = []

            self.user_preferences["summaries"].append(response.text.strip())

            for _ in range(5):
                self.conversation_history.popleft()

            self.save_data()
        except Exception as e: 
            print("fSummarization failed: {e}")

    def build_context_prompt(self, user_input, emotion_data):
        recent_context = "\n".join([
            f"User: {msg['user']}\nBot: {msg['bot']}" 
            for msg in list(self.conversation_history)[-5:]
        ]) if self.conversation_history else "No previous conversation"

        likes_summary = ", ".join([item["statement"] for item in self.user_preferences["likes"][-3:]])
        dislikes_summary = ", ".join([item["statement"] for item in self.user_preferences["dislikes"][-3:]])

        summaries = self.user_preferences.get("summaries", [])
        long_term_memory = "\n".join(summaries[-3]) if summaries else ""

        context_prompt = f"""You are Doccy, an empathetic and helpful assistant. 
        LONG-TERM MEMORY (Past Interactions):
        {long_term_memory if long_term_memory else "No long-term memories yet."}

        EMOTIONAL CONTEXT: 
        User's current emotion {emotion_data["emotion"]} (intensity: {emotion_data["intensity"]})

        USER PREFERENCES: 
        Things they like: {likes_summary if likes_summary else "Not yet known"}
        Things they dislike: {dislikes_summary if dislikes_summary else "Not yet known"}

        RECENT CONVERSATION: 
        {recent_context}

        CURRENT MESSAGE: {user_input}

        Respond empathetically based on their emotional state. If they seems {emotion_data["emotion"]}, acknowledge it naturally and adjust your tone accordingly. Be helpful and warm."""

        return context_prompt
    
    def generate_response(self, user_input): 
        emotion_data = self.detect_emotion(user_input)

        full_prompt = self.build_context_prompt(user_input, emotion_data)

        bot_response = "Sorry, I couldn't generate a response right now."

        try: 
            response = self.client.models.generate_content(
                model = "gemini-3-flash-preview",
                contents=full_prompt
            )
            bot_response = response.text
        except Exception as e: 
            print(f"Error generating a respomse: {e}")

        self.conversation_history.append({
            "user": user_input,
            "bot": bot_response,
            "emotion": emotion_data,
            "timestamp": datetime.now().isoformat()
        })

        self.track_preferences(user_input, bot_response)

        if len(self.conversation_history) >= 20: 
            self.summarize_old_conversation()

        return bot_response
    
def text_chat(chatbot):
   print("\nHow can Doccy help you today. Type 'quit' anytime to exit")

   while True:
       user_input = input("\nYou: ").strip()

       if user_input.lower() in ["quit", "exit", "bye"]:
           print("Doccy: Take care! Our conversation is saved for next time.")
           break 
       
       if not user_input:
           continue
       
       response = chatbot.generate_response(user_input)
       print(f"\nDoccy: {response}")

def main():
    load_dotenv()

    API_KEY = os.getenv("GEMINI_API_KEY")

    chatbot = Chatbot(api_key=API_KEY)
    
    text_chat(chatbot)

if __name__ == "__main__":
    main()

    