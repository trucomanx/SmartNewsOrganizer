from deep_consultation.core import consult_with_deepchat
import json
from PyQt5.QtWidgets import QMessageBox


def summarize_news(parent, config_data, list_data):
    #for data in list_data:
        #print(data['title'])
        #print(data['summary'])
        #print("")
    
    if len(list_data) ==0:
        QMessageBox.warning(parent, "Void list", "The list is void please select a node in the left tree view.")
        return
    
    titles = [data['title'] for data in list_data]
    titles_str = json.dumps(titles)
        
    system_msg = '''
You are an expert news summarizer.

You will always receive a list of news articles in JSON format as the only message from the user. The list contains only the text content of each article, ordered from most recent to oldest.

Your task is to:
1. Infer the majority language used in the articles and reply entirely in that language.
2. Analyze all articles and generate a coherent and concise summary that captures the most important information.
3. Give slightly more weight to more recent news at the top of the list, but do not overemphasize them if they are too many or too short.
4. Avoid repeating similar information and focus on key facts, trends, and developments.
5. Make sure the summary flows naturally, as if written by a human journalist.
6. Do not mention the number of articles or the fact that you received a list.
7. Do not include any metadata, formatting, or explanation — only the final summary in plain text.

If the input list is empty or contains only empty strings, respond with: "No news articles were provided."

    '''

    res = consult_with_deepchat(config_data["base_url"],
                                config_data["api_key"],
                                config_data["model"],
                                titles_str,
                                system_msg)
    QMessageBox.warning(parent, "Response",res)
