print("VERCELWORK")

"""
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("fill-mask", model="google-bert/bert-base-uncased")


#__________________________________________________________________________________________________________________________


import re
from transformers import pipeline

# Load the NER pipeline from Hugging Face
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def extract_schedule_info(user_input):
    # Use the NER pipeline to extract entities from the input
    entities = ner_pipeline(user_input)

    # Initialize variables to hold event, time, and date
    event = ""
    time = ""
    date = ""

    # Process the entities to identify event, time, and date
    for entity in entities:
        if entity['entity_group'] in ['MISC', 'ORG']:
            event += " " + entity['word']  # Capture miscellaneous events or organization names
        elif entity['entity_group'] == 'TIME':
            time += " " + entity['word']  # Capture time entities
        elif entity['entity_group'] == 'DATE':
            date += " " + entity['word']  # Capture date entities

    # Clean up the extracted information
    event = event.strip()
    time = time.strip()
    date = date.strip() if date.strip() else None  # Set date to None if not found

    # If event is still empty, use regex to find the main event description
    if not event:
        # Capture everything after "I have" up to the next "at" or "on"
        main_event_pattern = r'(?i)(?:I have|I need|I will|attend|working on|I want|work|homework|task|project|event|meeting|activity|upcoming)?\s*(.*?)(?=\s+at\s+|\s+on\s+|$)'
        main_event_match = re.search(main_event_pattern, user_input)

        if main_event_match:
            event = main_event_match.group(1).strip()  # Extract the main task

    # Use regex to find time and date if they weren't detected by the NER
    time_patterns = r'(\d{1,2}:\d{2} ?[APMapm]{2}|\d{1,2} ?[APMapm]{2})|(\d{1,2} - \d{1,2} ?[APMapm]{2})'
    date_patterns = r'(?:(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(?: to (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))?)|(\b\w+ \d{1,2}(?:th|st|nd|rd)?(?: of \w+)? \d{4})|\b(\w+ \d{1,2})'

    # Initialize regex matches for time and date
    time_matches = re.findall(time_patterns, user_input)
    date_matches = re.findall(date_patterns, user_input)

    # Initialize variables for day detection
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    found_days = [day for day in day_names if day.lower() in user_input.lower()]

    # Set date from found days if applicable
    if found_days:
        date = ', '.join(found_days)

    # Clean up time matches
    if time_matches:
        # Flatten time matches
        flat_time_matches = [match for group in time_matches for match in group if match]  # Flattening tuples
        time = ', '.join(flat_time_matches)  # Join valid time matches

    # Create a dictionary for the schedule information
    events_info = {'event': event.strip(), 'time': time.strip(), 'date': date.strip()}

    return events_info

# Test the function with an example input
if __name__ == "__main__":
    user_input = str(input("Test User Input: "))
    schedule_info = extract_schedule_info(user_input)

    print("Extracted Schedule Information:")
    print(schedule_info)

"""