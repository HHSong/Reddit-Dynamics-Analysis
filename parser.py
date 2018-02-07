import treeNode
from bs4 import BeautifulSoup

with open("./redditHtmlData/6ttui.html") as fp:
    soup = BeautifulSoup(fp)


comments = soup.select('div[class^=thing]')
# print(comments[0].prettify())

for comment in comments:
  entry = comment.find(attrs={'class':'entry'})
  nonCollapse = entry.find(attrs={'class':'noncollapsed'})
  content = nonCollapse.find('form').find('p').contents[0]
  if content == '[deleted]':
    continue
  print(content)