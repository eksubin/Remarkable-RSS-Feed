agent_prompt = """"
---
Task: "Read RSS Feed and go through individual links and provide the human user with title and it's description for a link like this: https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"

Thought: My goal is to find the news articles from the given RSS feed, get their titles and descriptions, and present them in a clear, structured manner for a human reader. I will begin by using the `fetch_news_items` tool to open the RSS feed URL.
<code>
answer = fetch_news_items("https://timesofindia.indiatimes.com/rssfeeds/296589292.cms")
print(answer)
</code>
Observation: "The answer contained a list of news links as `news_links`"

Thought: Now i have `news_links` as a list or 'url'. I will open each of these 'url` using the `visit_webpage`, then i will read it and save the results as 'website_result'. I will also print my thought process in each step.
<code>
website_result = []
for url in news_links:
    website_result.append(visit_webpage(url))
</code>
Observation: "I have successfully retrieved the individual urls and the website data"

Thought: Now, find out the title and description of that news from the data for each of the ,then save the title and description as final answer, The description will be usually the longest continous text data from the `website_result`.
The `final_answer` will contain the title and the description, I will also print my thought process in each step.
<code>
final_answer(final_news)
</code>
"""
