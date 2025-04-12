from deep_consultation.core import consult_with_deepchat
import json
from PyQt5.QtWidgets import QMessageBox
from smart_news_organizer.modules.wmessage import show_message
from datetime import datetime

def safe_wrapper(func):
    def wrapped_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            return error_message
    return wrapped_function

def summarize_news(config_data, list_data):
    #for data in list_data:
        #print(data['title'])
        #print(data['summary'])
        #print("")
    
    titles = [{"title": data.get('title',"No title"), "date":data.get("published","Unknown published")} for data in list_data]
    titles_str = json.dumps(titles)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    system_msg = f'''
You are a journalist who is an expert in summarizing news.
You will always receive a list of titles and dates of news articles in JSON list format as the only message from the user.

Your task is to:

* Infer the predominant language used in the articles and reply entirely in that language.
* Analyze all articles and generate a coherent and concise journalistic summary that conveys the most important information.
* Ensure the summary flows naturally, as if written by a human journalist.
* MANDATORY: Group the information to avoid repeating similar information, and focus on key facts, trends, and developments.
* As a journalist, take care with your language so as not to be redundant in the use of words and to present the news fluently.
* Do not mention the number of articles or the fact that you received a list.
* Do not include any metadata, formatting, or explanations — only the final summary in plain text.
* Current date: {current_date}. Since you know the current date then use phrases like: this week, today, etc.

If the input list is empty or contains only empty strings, respond with: "No news articles were provided."



    '''
    safe_consult_with_deepchat = safe_wrapper(consult_with_deepchat)

    res = safe_consult_with_deepchat(   config_data["base_url"],
                                        config_data["api_key"],
                                        config_data["model"],
                                        titles_str,
                                        system_msg)
    
    
    return res
