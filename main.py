import requests
import bs4

#Base URL, searches for all articles
searchURL = 'https://destiny.bungie.org/index.html?&search=+&page='

#Open URL
res = requests.get(searchURL + '1')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

pageList = soup.select("a[href*=match]") #List all hyperlinks with the word "match" in their URL
pageCount = int(pageList[-2].getText()) #Get last hyperling (not counting "Next Results") ! ! Might break on the edge-case of a single page of results ! !

globalTagList = []

#Loop through pages
for iPage in range(pageCount):
    pageURL = searchURL + str(iPage + 1) #Sets URL with page number

    #Open URL
    resPage = requests.get(pageURL)
    pageSoup = bs4.BeautifulSoup(resPage.text,'html.parser')
    print('Parsing page: ', iPage + 1, ' of ', pageCount)

    #Search all left-justified auxiliary fields
    pageArticleTagList = soup.select('.fl')

    #Loop through search results
    for item in pageArticleTagList:
        articleTagList = item.select('a') #Find all hyperlinks (should be tags already)
        for tagItem in articleTagList:
            tag = tagItem.getText() #Get tag text
            globalTagList.append(tag) #Append tag to list

globalTagList = list(dict.fromkeys(globalTagList)) #Remove duplicates in a roundabout way that work with standard objects

#Print tags on console
for tag in globalTagList:
    print(tag)