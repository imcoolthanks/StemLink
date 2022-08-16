import requests    

# Search up a certain number of news by interest using...
# results = get_news_by_interest(interest, num)
#
# results will be an array. It contains the inputted number of arrays
# given in the format of [title, author, description, url, url to cover image]
 
def get_news_by_interest(interest, num):
    # BBC news api
    # following query parameters are used
    # source, sortBy and apiKey
    query_params = {
      "sortBy": "top",
      "apiKey": "803faabb3328410ebf50846c453353e2",
      "q": interest,
      "language":"en"
    }
    main_url = " https://newsapi.org/v2/everything"
 
    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    data = res.json()
 
    # getting all articles in a string article
    article = data["articles"]
 
    # empty list which will
    # contain all trending news
    all_results = []
      
    for i in range(5):
        curr = []

        ar = article[i]

        curr.append(ar["title"])
        curr.append(ar["author"])
        curr.append(ar["description"])
        curr.append(ar["url"])
        curr.append(ar["urlToImage"])

        all_results.append(curr)

    return all_results

#FOR EXAMPLE, TEST CODE
results = get_news_by_interest("climate change", 3)
for a in results:
    print(a)
    print('\n')