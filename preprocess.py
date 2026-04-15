import pandas as pd
import ast
import email
import re
import contractions

def clean_email_content(raw_str):
    # use ast to parse the email for easy preprocessing
    content_list = ast.literal_eval(raw_str)
    if len(content_list) > 0:
        raw_email = content_list[0]
    
    # parse email structure
    msg = email.message_from_string(raw_email)
    
    # extract subject
    subject = msg.get('Subject', '')
    
    # extract body
    body = []
    try:
        payload = msg.get_payload(decode=True)
        if payload:
            payload = payload.decode('utf-8', errors='ignore')
        else:
            payload = msg.get_payload()
        body.append(payload)
    except:
        body.append(msg.get_payload())
            
    # Combine Subject and Body
    full_text = str(subject) + " " + " ".join([str(b) for b in body if b])
    
    # remove HTML tags and excessive newlines
    full_text = re.sub(r'<[^>]+>', ' ', full_text)
    full_text = re.sub(r'[\r\n\t]+', ' ', full_text)
    
    # normalization (URL, Email, Numbers, Money)
    full_text = re.sub(r'https?://\S+', ' urladdr ', full_text)
    full_text = re.sub(r'\S+@\S+\.\S+', ' emailaddr ', full_text)
    full_text = re.sub(r'\b\d+\b', ' number ', full_text)
    full_text = re.sub(r'[\$\£\€]', ' moneylimit ', full_text)
    
    # expand contractions (e.g. don't -> do not, I'm -> I am)
    full_text = contractions.fix(full_text)
    
    # remove special characters and punctuation
    full_text = re.sub(r'[^a-zA-Z\s]', ' ', full_text)
    
    # lowercase and normalize whitespace
    full_text = full_text.lower()
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    return full_text