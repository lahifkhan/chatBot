import tkinter as tk
from tkinter import scrolledtext, PhotoImage, Button, Entry, Frame, Label, messagebox
import datetime
import threading
import time
import nltk
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import random
import re

# Download required NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Lab Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Set color scheme
        self.bg_color = "#f5f5f7"
        self.header_color = "#0a2540"
        self.input_bg = "#ffffff"
        self.user_msg_color = "#e1f5fe"
        self.bot_msg_color = "#f0f0f0"
        self.button_color = "#0a2540"
        self.button_hover = "#1e3a5f"
        self.accent_color = "#2d88ff"

        # Initialize game state
        self.game_active = False
        self.game_number = None
        self.game_attempts = 0

        # Initialize chatbot data
        self.setup_chatbot_data()

        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Create UI components
        self.create_header()
        self.create_chat_area()
        self.create_input_area()

        # Initialize chat history
        self.chat_history = []

        # Get user's name
        self.get_user_name()

    def setup_chatbot_data(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "goodbye": ["bye", "goodbye", "see you", "farewell"],
            "how_are_you": ["how are you", "how's it going", "how are things"],
            "name": ["what is your name", "who are you", "your name", "name"],
            "time": ["what time is it", "current time", "tell me the time", "time"],
            "date": ["what is the date", "today's date", "what day is it", "date"],
            "thanks": ["thank you", "thanks", "thx", "tnx"],
            "help": ["help", "what can you do", "assist me", "options"],
            "weather": ["what's the weather", "weather update", "tell me the weather", "weather"],
            "game": ["play game", "let's play", "game", "play", "number game"],
            "joke": ["tell me a joke", "joke", "make me laugh", "funny"],
            "fact": ["tell me a fact", "fact", "interesting fact", "did you know"]
        }

        self.jokes = [
            "Why did the computer go to therapy? It had too many bytes of memory! 😂",
            "Why do programmers prefer dark mode? Because light attracts bugs! 💡🐛",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why don't scientists trust atoms? Because they make up everything! ⚛️",
            "What did the grape say when it got stepped on? Nothing, it just let out a little wine! 🍇",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the math book look so sad? Because it had too many problems! 📚"
        ]

        self.facts = [
            "Python was named after Monty Python, not the snake! 🐍",
            "The first computer bug was an actual moth found in a computer in 1947! 🦋",
            "Honey never spoils! Archaeologists found 3000-year-old honey still edible! 🍯",
            "The shortest war in history lasted only 38 minutes between Britain and Zanzibar! ⚔️",
            "A day on Venus is longer than its year! 🌟",
            "Bananas are berries, but strawberries aren't! 🍌",
            "The average person spends 6 months of their lifetime waiting for red lights! 🚦",
            "Octopuses have three hearts! 🐙"
        ]

        self.responses = {
            "greeting": ["Hi {name}! 👋", "Hello {name}! 😊", "Hey {name}! How can I help you?"],
            "goodbye": ["Goodbye {name}! Have a great day! 👋", "Bye {name}! Take care!", "See you soon, {name}!"],
            "how_are_you": ["I'm doing great, thanks for asking! 😄", "All systems running smoothly!",
                            "Fantastic! Ready to chat and help! 🌟"],
            "name": ["I'm your friendly AI Lab Assistant! 🤖", "You can call me Lab Assistant! I'm here to help! 🤖"],
            "time": [lambda: f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"],
            "date": [lambda: f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"],
            "thanks": ["You're welcome! 😊", "Anytime!", "Happy to help! 🌟"],
            "help": [
                "I can help with:\n- Chat and conversation\n- Time and date information\n- Math calculations\n- Jokes and facts\n- Weather updates\n- Play number guessing game\n- Sentiment analysis\n\nTry commands like:\n- 'tell me a joke'\n- 'tell me a fact'\n- 'let's play'\n- Or just chat naturally!"
            ],
            "weather": ["It's sunny and bright! ☀️", "Looks like rain today 🌧️", "Perfect weather for coding! 🌤️"],
            "game": [
                "Let's play the number guessing game! I'm thinking of a number between 1 and 100. Try to guess it! 🎮"]
        }

        self.compliments = [
            "You're doing amazing! 🌟",
            "You're smart and capable — never forget that! 💪",
            "You light up the chat! 🔆",
            "Your curiosity is inspiring! 🌈",
            "You make learning fun! 📚",
            "You're a natural problem solver! 🧩"
        ]

    def get_user_name(self):
        def submit_name():
            name = name_entry.get().strip()
            if name:
                self.user_name = name
                name_window.destroy()
                self.add_bot_message(
                    f"Welcome {self.user_name}! How can I help you today? Type 'help' to see what I can do!")
            else:
                messagebox.showwarning("Input Required", "Please enter your name!")

        name_window = tk.Toplevel(self.root)
        name_window.title("Welcome")
        name_window.geometry("300x150")
        name_window.transient(self.root)
        name_window.grab_set()

        Label(name_window, text="Please enter your name:", font=("Arial", 12)).pack(pady=10)
        name_entry = Entry(name_window, font=("Arial", 12))
        name_entry.pack(pady=10)
        name_entry.focus()

        Button(name_window, text="Start Chat", command=submit_name,
               bg=self.button_color, fg="white", font=("Arial", 12)).pack(pady=10)

        name_entry.bind("<Return>", lambda e: submit_name())

    def create_header(self):
        header_frame = Frame(self.root, bg=self.header_color, height=60)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)

        header_label = Label(header_frame, text="AI LAB ASSISTANT", fg="white",
                             bg=self.header_color, font=("Arial", 16, "bold"))
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        clear_button = Button(
            header_frame,
            text="Clear Chat",
            bg=self.header_color,
            fg="white",
            font=("Arial", 10),
            relief="flat",
            command=self.clear_chat,
            activebackground=self.button_hover,
            activeforeground="white",
            bd=0,
            padx=10
        )
        clear_button.place(relx=0.95, rely=0.5, anchor="e")

    def create_chat_area(self):
        self.chat_container = Frame(self.root, bg=self.bg_color)
        self.chat_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(0, weight=1)

        self.chat_display = scrolledtext.ScrolledText(
            self.chat_container,
            bg=self.bg_color,
            font=("Arial", 11),
            padx=10,
            pady=10,
            wrap=tk.WORD,
            relief="flat"
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew")

        self.chat_display.tag_configure("user", background=self.user_msg_color,
                                        lmargin1=50, rmargin=15)
        self.chat_display.tag_configure("bot", background=self.bot_msg_color,
                                        lmargin1=15, rmargin=50)
        self.chat_display.tag_configure("time", foreground="gray",
                                        font=("Arial", 8))
        self.chat_display.tag_configure("sender", font=("Arial", 10, "bold"))

    def create_input_area(self):
        input_frame = Frame(self.root, bg=self.bg_color, height=80)
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)

        self.entry = Entry(
            input_frame,
            font=("Arial", 12),
            bg=self.input_bg,
            relief="solid",
            bd=1
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), ipady=8)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = Button(
            input_frame,
            text="Send",
            font=("Arial", 12, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="flat",
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(0, 0), ipady=5, ipadx=15)

    def handle_game(self, message):
        if not self.game_active and message.lower() in ["play game", "let's play", "game", "play"]:
            self.game_active = True
            self.game_number = random.randint(1, 100)
            self.game_attempts = 0
            return "Let's play the number guessing game! I'm thinking of a number between 1 and 100. Try to guess it! 🎮"

        if self.game_active:
            try:
                guess = int(message)
                self.game_attempts += 1

                if guess < self.game_number:
                    return f"Higher! You've made {self.game_attempts} attempts. 🔼"
                elif guess > self.game_number:
                    return f"Lower! You've made {self.game_attempts} attempts. 🔽"
                else:
                    self.game_active = False
                    return f"Congratulations! You got it in {self.game_attempts} attempts! 🎉\nWant to play again? Just say 'play'!"
            except ValueError:
                if message.lower() in ["quit", "exit", "stop"]:
                    self.game_active = False
                    return "Game stopped. The number was " + str(
                        self.game_number) + ". Chat with me or type 'play' to start a new game! 🎮"
                return "Please enter a number between 1 and 100 (or 'quit' to stop playing)"

        return None

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.entry.delete(0, tk.END)
            self.add_user_message(message)
            self.process_message(message)
            return "break"

    def add_user_message(self, message):
        timestamp = self.get_timestamp()

        self.chat_display.config(state="normal")
        if self.chat_display.index('end-1c') != '1.0':
            self.chat_display.insert(tk.END, "\n\n")

        self.chat_display.insert(tk.END, f"{timestamp}\n", "time")
        self.chat_display.insert(tk.END, "You: \n", "sender")
        self.chat_display.insert(tk.END, f"{message}", "user")

        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")

        self.chat_history.append(("user", message, timestamp))

    def add_bot_message(self, message):
        timestamp = self.get_timestamp()

        self.show_typing_indicator()

        def show_response():
            self.remove_typing_indicator()

            self.chat_display.config(state="normal")
            if self.chat_display.index('end-1c') != '1.0':
                self.chat_display.insert(tk.END, "\n\n")

            self.chat_display.insert(tk.END, f"{timestamp}\n", "time")
            self.chat_display.insert(tk.END, "AI Lab Assistant: \n", "sender")
            self.chat_display.insert(tk.END, f"{message}", "bot")

            self.chat_display.see(tk.END)
            self.chat_display.config(state="disabled")

            self.chat_history.append(("bot", message, timestamp))

        self.root.after(1000, show_response)

    def show_typing_indicator(self):
        self.chat_display.config(state="normal")
        if self.chat_display.index('end-1c') != '1.0':
            self.chat_display.insert(tk.END, "\n\n")
        self.chat_display.insert(tk.END, f"{self.get_timestamp()}\n", "time")
        self.chat_display.insert(tk.END, "AI Lab Assistant is typing...", "sender")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")

    def remove_typing_indicator(self):
        self.chat_display.config(state="normal")
        last_line_start = self.chat_display.index("end-1c linestart")
        last_line_end = self.chat_display.index("end")
        self.chat_display.delete(last_line_start, last_line_end)
        self.chat_display.config(state="disabled")

    def get_timestamp(self):
        return datetime.datetime.now().strftime("%I:%M %p")

    def process_message(self, message):
        # Check for game-related messages first
        game_response = self.handle_game(message)
        if game_response:
            self.add_bot_message(game_response)
            return

        # Special commands
        if message.lower() in ["joke", "tell me a joke", "make me laugh"]:
            self.add_bot_message(random.choice(self.jokes))
            return
        elif message.lower() in ["fact", "tell me a fact", "interesting fact"]:
            self.add_bot_message(random.choice(self.facts))
            return
        elif message.lower() == "compliment":
            self.add_bot_message(random.choice(self.compliments))
            return

        # Math expressions
        if re.match(r"^[\d\s\+\-\*\/\.\(\)]+$", message):
            try:
                result = str(eval(message))
                self.add_bot_message(f"The answer is {result}")
                return
            except:
                self.add_bot_message("That doesn't look like a valid math problem. ❌")
                return

        # Intent matching
        corrected = str(TextBlob(message).correct())
        if corrected != message:
            self.add_bot_message(f"(Did you mean: '{corrected}'?)")

        tokens = word_tokenize(corrected)
        clean_input = " ".join(tokens)

        intent = None
        for intent_name, patterns in self.intents.items():
            if any(pattern in clean_input.lower() for pattern in patterns):
                intent = intent_name
                break

        if intent:
            response = random.choice(self.responses[intent])
            if callable(response):
                response = response()
            response = response.format(name=self.user_name)
        else:
            response = "I'm not sure how to respond to that. Try asking for 'help'!"

        # Add sentiment analysis
        sentiment = TextBlob(message).sentiment.polarity
        if sentiment > 0.3:
            response += "\nYou sound happy! 😊"
        elif sentiment < -0.3:
            response += "\nYou sound a bit down. I'm here for you. 💙"

        self.add_bot_message(response)

    def clear_chat(self):
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state="disabled")
        self.chat_history = []
        self.add_bot_message("Chat cleared. How can I help you today?")


def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()