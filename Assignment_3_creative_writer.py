# Assignment #3
# Create a standalone program (command line application), which is uses large language model (LLM) to be a creative writer 
# e.g. marketing materials, memes, song lyrics, poems or blog posts, 
# which are search engine optimized (SEO) by using as many possible synonyms as possible. 
# The program should by default produce 3 different versions from the same prompt. 
# Try adjusting the system prompt, temperature, top-p, presence penalty and frequency penalty for best possible results. 
# Use OpenAI API. You are free to use any version of LLM you want, but try to choose a one suitable for the project 
# (e.g. gpt-4o-mini is most likely not ideal).


from openai import OpenAI

# LM Studio is running on localhost:1234
# Make sure to start LM Studio first

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

   #  client.chat.completions.create
   # a method that is used to create responses in conversational format.

# history = list, a list of dictionaries, 
# each dictionary contains a role and content.
# The role can be "system", "user", or "assistant".
# The content is the actual message.

history = [
    {"role": "system", "content": "You are a creative writer. you write a very short rhyne about given subject. Don't use preamble."}, # This is system prompt, Ai's role in this play
]

model = "gemma-3-12b-it"  # LLM, remmber to start server in LM Studio first !!

print(f"Give me topic, {model} crafts you a rhyme.")
print(" Enter 'exit' or 'quit' to say goodbye.")

while True:
    prompt = input("Give me a topic .. ")
    if prompt == "exit" or prompt == "quit" or len(prompt) == 0:
        print("\nFarewell!")
        #break()
        exit(0)

    # while loop, creates 3 different versions of the same prompt in this loop
    i = 0
    while (i < 3):

        history.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=model,
            messages=history,
            temperature=1.0,
            stream=True,
            top_p=1,
            presence_penalty=1.0,
            frequency_penalty=1.0,
        )

        print (f"\nVersion {i+1}:")

        # role assistant gives the answer from the model (gemma-3-12b-it in this case)
        new_message = {"role": "assistant", "content": ""}
   
        # print the answer as it comes, chunk by chunk
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content

        history.append(new_message)
        print()

        i+=1







