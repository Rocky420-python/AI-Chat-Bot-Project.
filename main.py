import customtkinter as tk
import json
import wikipedia

from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

class ChatBot(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My ChatBot")
        self.geometry("400x500")

        # Output Textbox
        self.output_box = tk.CTkTextbox(self, width=350, height=300)
        self.output_box.pack(pady=20)

        # Entry for user input
        self.entry = tk.CTkEntry(self, width=300)
        self.entry.pack(pady=10)

        # Send Button
        self.button = tk.CTkButton(self, text="Send", command=self.send_message)
        self.button.pack(pady=10)

        # Load existing memory
        try:
            with open("Memory.json", "r") as f:
                self.memory = json.load(f)
        except:
            self.memory = {}

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.output_box.insert("end", f"You: {user_text}\n\n")
        self.output_box.see("end")

        # Check memory first
        if user_text in self.memory:
            bot_text = self.memory[user_text]
        else:
            # Try Wikipedia
            try:
                summary = wikipedia.summary(user_text, sentences=2)
                bot_text = summary
            except wikipedia.DisambiguationError as e:
                bot_text = f"Multiple results found: {e.options[:5]}"
            except wikipedia.PageError:
                bot_text = "Page not found."

            # Save to memory
            self.memory[user_text] = bot_text
            try:
                with open("Memory.json", "w") as f:
                    json.dump(self.memory, f, indent=4)
            except Exception as e:
                print(f"Error saving memory: {e}")

        self.output_box.insert("end", f"Bot: {bot_text}\n\n")
        self.output_box.see("end")
        self.entry.delete(0, "end")


# Run the App
if __name__ == "__main__":
    app = ChatBot()
    app.mainloop()
