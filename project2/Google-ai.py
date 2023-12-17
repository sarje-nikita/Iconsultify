# import pprint
# import os
# import django
# import google.generativeai as palm
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
# django.setup()
# from asgiref.sync import sync_to_async
# from model.models import Business
# async def save_businesses(business_list):
#     await sync_to_async(Business.objects.bulk_create)(business_list)  

# palm.configure(api_key='AIzaSyCiAF--tTSTrDqfdSMKKhm0H6mIb1lTSEg')

# models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
# model = models[0].name
# print(model)


# elements = Business.objects.filter(text="")

# for i in elements:
#     prompt = f'Name	{i.name}'
#     if i.address!="":
#         prompt+=f'\nAddress	{i.address}'
#     prompt+=f'\nCategory	{i.main_business}'   
#     prompt+=f'\nSub Category	{i.sub_business}'   
#     prompt+=f'\nCity	{i.city}'   
#     if i.phone_number!="":
#         prompt+=f'\nContact	{i.phone_number}'
#     if i.website!="":
#         prompt+=f'\nWebsite	{i.website}'
#     if i.reviews_average>=1:
#         prompt+=f'\nReview	{i.reviews_average}'
#         if i.reviews_count!="":
#             prompt+=f'\nReview count	{i.reviews_count}'
#     prompt+=f'\n\nuse all the above details properly and then response should be in 3 paragraph form and not use bullet points\n'        

#     # print(prompt)

#     completion = palm.generate_text(
#         model=model,
#         prompt=prompt,
#         temperature=0,
#         # The maximum length of the response
#         max_output_tokens=800,
#     )
    
#     i.text = completion.result
#     # print(completion.result)
#     # print(completion.result)









import os
import django
import google.generativeai as palm
import asyncio
from tqdm import tqdm  # Import tqdm for progress bar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')
django.setup()
from asgiref.sync import sync_to_async
from model.models import Business

# Configure PALM API
palm.configure(api_key='AIzaSyCiAF--tTSTrDqfdSMKKhm0H6mIb1lTSEg')

# Get supported generation methods and select a model
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

# Define an asynchronous function to process and save a single business
@sync_to_async
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

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=800,
    )

    business.text = completion.result
    business.save()

# Query businesses without text
businesses_without_text = Business.objects.filter(text="")

# Create a progress bar with fractional values
with tqdm(total=1.0, unit_scale=True, unit="point") as pbar:
    async def process_and_save_with_progress(business):
        await process_and_save_business(business)
        pbar.update(1 / len(businesses_without_text))  # Update the progress bar with fractional values

    # Process and save businesses asynchronously with progress
    loop = asyncio.get_event_loop()
    awaitables = [process_and_save_with_progress(business) for business in businesses_without_text]
    loop.run_until_complete(asyncio.gather(*awaitables))

# Close the PALM API connection if necessary
palm.close()
