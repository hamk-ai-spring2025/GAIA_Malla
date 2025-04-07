# Task 5 - by Malla 

# Image-to-text-to-image generator. 
# Generate a command line or GUI program, which reads an image 
# and uses AI to generate textual description of it. 
# It prints the description to standard output, but also attempts to generate image 
# using the description of image as input prompt for the image generation. 
# You can use OpenAI Vision API and Dall-E 3 or some other if you want. 
# However: this assignment is not supposed to be real image-to-image model, 
# but really image-to-text and then feed that text output to text-to-image model.


# from markitdown import MarkItDown
from openai import OpenAI
import base64
import sys
import replicate

# LM Studio is running on localhost:1234
# Make sure to start LM Studio first

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# my_messages = list, a list of dictionaries, 
# each dictionary contains a role and content.
# The role can be "system", "user", or "assistant".
# The content is the actual message.

my_messages = []
my_messages = [
    {"role": "system", 
     "content": "Describe in details the given picture. Don't use any preamble."}, # This is system prompt, Ai's role in this play
]

model = "llava-v1.5-7b"  # LLM, remmber to start server in LM Studio first !!

def describe_image():
    input_image = input("Give me a file to describe: ")
    print("\n")

    # Read the image and encode it to base64:

    ## MarkItDown could also be used to convert images to text
    ## md = MarkItDown(llm_client=client, llm_model=model) 
    
    ## # Converts image to text using the LLM
    ## result = md.convert(image).text_content

    ## print("result:", result)    # here is the result of the image description via MarkItDown


    base64_image = ""

    try:
        image = open(input_image.replace("'", ""), "rb").read()
        base64_image = base64.b64encode(image).decode("utf-8")
    except:
        print(f"Converting image *{image}* to base64 failed. Make sure the path is correct and the file exists.")
        sys.exit()

    my_messages.append(
        {   "role": "user", 
            "content": [
                        {"type": "text", "text": "Describe this image."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ]
        }   
        )
    
    completion = client.chat.completions.create(
        model=model,
        messages=my_messages,
        temperature=1.0,
        stream=True,
        top_p=1,
        presence_penalty=1.0,
        frequency_penalty=1.0,
     )

        
        
    new_message = {"role": "assistant", "content": ""}
   
    # print the answer as it comes, chunk by chunk
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    
    return (new_message["content"])


def generate_image_from_text(image_as_text):
    # Use Replicate to generate an image from the text description
    model = "black-forest-labs/flux-schnell"
    output = replicate.run(
        model,
        input={"prompt": image_as_text,     # Text description of the image
               "num_outputs": 1,            # Number of images to generate
               "aspect_ratio": "1:1",       # Aspect ratio of the generated image
               "output_format": "png",      # Output format of the generated image
               "output_quality": 30,        # Quality of the generated image (1-100)
               "num_inference_steps": 4 ,   # Number of inference steps
               "seed": 42}                  # Random seed for reproducibility
    )

    # Save the generated image
    with open('output.png', 'wb') as f:
        f.write(output[0].read())
 
    print(f"\nImage saved as output.png")
    

def main():

    image_as_text =""

    image_as_text = describe_image()

    #save the image description to a file
    with open('image_description.txt', 'w') as f:
        f.write(image_as_text)
    
    print(f"\n\nDescription of the image saved as image_description.txt\n")
    
    generate_image_from_text(image_as_text)


if __name__ == "__main__":
    main()
    






