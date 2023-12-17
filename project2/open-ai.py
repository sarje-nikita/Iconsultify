# import os
# import django
# import openai
# from tqdm import tqdm  # Import tqdm for the progress bar
# import time

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
# django.setup()
# from asgiref.sync import sync_to_async
# from model.models import Business

# # Configure OpenAI API with your API key
# openai.api_key = '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'

# # Define a synchronous function to process and save a single business
# def process_and_save_business(business):
#     prompt = f'Name: {business.name}\n'
#     if business.address:
#         prompt += f'Address: {business.address}\n'
#     prompt += f'Category: {business.main_business}\n'
#     prompt += f'Sub Category: {business.sub_business}\n'
#     prompt += f'City: {business.city}\n'
#     if business.phone_number:
#         prompt += f'Contact: {business.phone_number}\n'
#     if business.website:
#         prompt += f'Website: {business.website}\n'
#     if business.reviews_average >= 1:
#         prompt += f'Review: {business.reviews_average}\n'
#         if business.reviews_count:
#             prompt += f'Review count: {business.reviews_count}\n'
#     prompt += '\nUse all the above details properly, and then the response should be in a 3-paragraph form and not use bullet points\n'
#     print("start")
#     response = openai.Completion.create(
#         engine="text-davinci-002",  # Use the appropriate ChatGPT engine
#         prompt=prompt,
#         max_tokens=800,
#     )
#     print("end")

#     business.text = response.choices[0].text
#     # print(response.choices[0].text)
#     business.save()

# # Query businesses without text
# def main():
#     businesses_without_text = Business.objects.filter(text="")
#     for i in businesses_without_text:
#         # print(time.time())
#         process_and_save_business(i)
#         # print(f"finished {i}")

# if __name__ == "__main__":
#     main()




import os
import django
import openai
from tqdm import tqdm  # Import tqdm for the progress bar
import time

# List of API keys to rotate through
api_keys = [
    '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',
    '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',
    # Add more API keys as needed
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
django.setup()
from asgiref.sync import sync_to_async
from model.models import Business

# Initialize API key index
api_key_index = 0

# Function to get the current API key and increment the index
def get_current_api_key():
    global api_key_index
    current_api_key = api_keys[api_key_index]
    api_key_index = (api_key_index + 1) % len(api_keys)  # Rotate through keys
    return current_api_key

# Configure OpenAI API with the initial API key
openai.api_key = get_current_api_key()

# Define a synchronous function to process and save a single business
def process_and_save_business(business):
    prompt = f'Name: {business.name}\n'
    if business.address:
        prompt += f'Address: {business.address}\n'
    prompt += f'Category: {business.main_business}\n'
    prompt += f'Sub Category: {business.sub_business}\n'
    prompt += f'City: {business.city}\n'
    if business.phone_number:
        prompt += f'Contact: {business.phone_number}\n'
    if business.website:
        prompt += f'Website: {business.website}\n'
    if business.reviews_average >= 1:
        prompt += f'Review: {business.reviews_average}\n'
        if business.reviews_count:
            prompt += f'Review count: {business.reviews_count}\n'
    prompt += '\nUse all the above details properly, and then the response should be in a 3-paragraph form and not use bullet points\n'
    print("start")
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Use the appropriate ChatGPT engine
            prompt=prompt,
            max_tokens=800,
        )
        print("end")
        print(response.choices[0].text)
    except openai.error.OpenAIError as e:
        # Handle API errors, e.g., rate limiting
        print(f"Error: {e}")
        # Switch to the next API key
        openai.api_key = get_current_api_key()
        return
    
    business.text = response.choices[0].text
    business.save()

# Query businesses without text
def main():
    businesses_without_text = Business.objects.filter(text="")
    
    # Create a tqdm progress bar
    progress_bar = tqdm(total=len(businesses_without_text))
    tm = time.time()
    a=0
    for i in businesses_without_text:
        if(a>3):
            break
        a+=1
        process_and_save_business(i)
        progress_bar.update(1)  # Update the progress bar
        progress_bar.set_description(f"Processed: {i.name}")
    
    # Close the progress bar
    print(time.time()-tm)
    progress_bar.close()

if __name__ == "__main__":
    main()
