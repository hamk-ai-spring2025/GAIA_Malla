"""
Generate a versatile command line utility for image generator using your favorite image generator. 
User should be able to adjust the prompt, possible negative prompt (if the image generator supports it), 
seed (if the image generator supports it) and aspect ratio of the image (e.g. square 1:1, 16:9, 4:3, 3:4). 
You can add more parameters if you want. User can also define the number of images it generates. 
The program will print out the URL where they can be downloaded, but it will also download them and save into current directory 
with automatically generated file names and prints out those file names.
"""
import replicate

print ("Welcome to the image generator!")
print ("This program uses Replicate API to generate images.")
print ("\n")


prompt_text =  input("Prompt for generated image: ")
seed = int(input("Set seed for reproducible generation (integer): "))
ar = input("Set aspect ratio (e.g. 1:1, 16:9, 4:3, 3:4): ")
format = input("Set output format (webp, png, jpg): ")
number_of_images = int(input("Set number of images to generate (1-4): "))
output_quality = int(input("Set output quality (1-100): "))
num_inference_steps = int(input("Set number of inference steps (1-4): "))

# validatate inputs
if number_of_images < 1 or number_of_images > 4:    
    print("Number of images must be between 1 and 4")
    exit()
if output_quality < 1 or output_quality > 100:
    print("Output quality must be between 1 and 100")
    exit()
if num_inference_steps < 1 or num_inference_steps > 4:
    print("Number of inference steps must be between 1 and 4")
    exit()
if format not in ["webp", "png", "jpg"]:            
    print("Output format must be webp, png or jpg")
    exit()      
if ar not in ["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "4:3", "3:4", "9:16","9:21"]:
    print("Aspect ratio must be 1:1, 16:9, 4:3 or 3:4")
    exit()
if (prompt_text == ""):
    print("Prompt text cannot be empty")
    exit()


print("\nGenerating image using Replicate with the following parameters:")
print (f"Prompt: {prompt_text}")
print (f"Seed: {seed}")
print (f"Aspect ratio: {ar}")   
print (f"Output format: {format}")
print (f"Number of images: {number_of_images}")   
print (f"Output quality: {output_quality}")  
print (f"Number of inference steps: {num_inference_steps}")
print ("\n")

go_on = input ("Do you want to continue? (y/n)")

if go_on != "y":
    print("Exiting")
    exit()          

print("Generating image...")   

output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": prompt_text,
        "seed": seed,
        "aspect_ratio": ar,
        "output_format": format,
        "num_outputs": number_of_images,
        "output_quality": output_quality,
        "num_inference_steps": num_inference_steps,
        "go_fast": True,
        "megapixels": "1",
    }
)

print(output)

#save the generated images
for i in range(len(output)):
    with open(f'output_{i}.png', 'wb') as f:
        f.write(output[i].read())
    print(f"Image saved as output_{i}.png")

# show urls of the generated images
print("\n\nURLs of the generated images:")          
for i in range(len(output)):
    print(f"output_{i}.png: {output[i].url}")

