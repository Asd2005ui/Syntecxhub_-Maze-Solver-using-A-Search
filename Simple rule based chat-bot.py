import re
import datetime

# Define patterns for intents using regular expressions
patterns = {
    'greeting': [r'\bhello\b', r'\bhi\b', r'\bhey\b', r'\bgood morning\b', r'\bgood afternoon\b'],
    'help': [r'\bhelp\b', r'\bwhat can you do\b', r'\bassist\b', r'\bsupport\b'],
    'small_talk': [r'\bhow are you\b', r'\bwhat\'s up\b', r'\bhow do you do\b', r'\bwhat are you doing\b'],
    'goodbye': [r'\bbye\b', r'\bgoodbye\b', r'\bsee you\b', r'\bexit\b']
}

# Define responses for each intent
responses = {
    'greeting': 'Hello! How can I help you today?',
    'help': 'I am a simple chatbot. I can greet you, provide help, engage in small talk, and answer questions about animals (e.g., "What is a cat?"). Type "bye" to exit.',
    'small_talk': 'I\'m doing well, thank you! How about you?',
    'goodbye': 'Goodbye! Have a great day!'
}

# Small knowledge base for domain questions (animals)
knowledge_base = {
    'what is a cat': 'A cat is a small domesticated carnivorous mammal with soft fur, a short snout, and retractable claws.',
    'what is a dog': 'A dog is a domesticated descendant of the wolf, known for its loyalty and ability to be trained.',
    'what is a bird': 'A bird is a warm-blooded vertebrate animal that has feathers, wings, and a beak.',
    'what is a fish': 'A fish is a cold-blooded aquatic animal with gills for breathing and fins for swimming.',
    'what is an elephant': 'An elephant is a large mammal with a trunk, tusks, and big ears, known for its intelligence and memory.'
}

# Function to match user input to intents or knowledge base
def get_response(user_input):
    user_input = user_input.lower()
    
    # Check for intent matches
    for intent, pats in patterns.items():
        for pat in pats:
            if re.search(pat, user_input):
                return responses[intent]
    
    # Check knowledge base for domain questions
    for question, answer in knowledge_base.items():
        if question in user_input:
            return answer
    
    # Default response if no match
    return "I'm sorry, I don't understand that. Try asking about animals or say 'help' for more info."

# Main interactive loop
def main():
    conversation = []
    print("Bot: Hello! I'm a simple chatbot. Type 'bye' to exit.")
    conversation.append(f"Bot: Hello! I'm a simple chatbot. Type 'bye' to exit. (Started at {datetime.datetime.now()})")
    
    while True:
        user_input = input("You: ")
        conversation.append(f"You: {user_input}")
        
        if re.search(r'\b(exit|bye|goodbye)\b', user_input.lower()):
            response = responses['goodbye']
            print(f"Bot: {response}")
            conversation.append(f"Bot: {response}")
            break
        
        response = get_response(user_input)
        print(f"Bot: {response}")
        conversation.append(f"Bot: {response}")
    
    # Log conversation to a file
    with open('conversation_log.txt', 'a') as f:
        f.write(f"\n--- New Conversation at {datetime.datetime.now()} ---\n")
        for line in conversation:
            f.write(line + '\n')
    print("Conversation logged to 'conversation_log.txt'.")

if __name__ == "__main__":
    main()