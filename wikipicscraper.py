# Downloads all the thumbnail images on a Wikipedia page
# Adapted from https://automatetheboringstuff.com/chapter11/ (xkcd example)

import os, requests, bs4

def downloadPic(imageUrl, caption):
     res = requests.get(imageUrl)
     try:
          res.raise_for_status()
          imageFileName = caption + imageUrl[-4:]
          imageFile = open(os.path.join('wikipics', os.path.basename(imageFileName)), 'wb') #write binary
          for chunk in res.iter_content(100000): #max 100,000 bytes at a time
               imageFile.write(chunk)
          imageFile.close()
     except requests.exceptions.MissingSchema:
          print("Could not download %s\n" % (imageUrl))

status = True

while status == True:
     
     base = 'https://en.wikipedia.org/wiki/'
     query = input("Enter query (case sensitive):\n")
     query.strip()
     query.replace(" ", "_")
     url = base + query

     # Make directory
     os.makedirs("wikipics", exist_ok=True)

     # Download and parse HTML
     res = requests.get(url)
     try:
          res.raise_for_status()
     except Exception as ex:
          print("Error: %s" % (ex))

     soup = bs4.BeautifulSoup(res.text, features="html.parser")

     #Download main image
     infobox = soup.select('.infobox')
     if infobox == []:
          print("Could not find an infobox on %s\n" % (url))
     else:
          img = infobox[0].select('img')[0]
          imageUrl = 'http:' + img.get('src')
          caption = img.get('alt')
          if caption == "":
               caption = infobox.select('div')[0].getText()
          print ("Downloading image: %s" % (caption))
          downloadPic(imageUrl, caption)

     # Download thumnail images
     divs = soup.select('.thumb')
     if divs == []:
          print("Could not find any thumbnail divs on this page\n")
     else:
          for i in range(len(divs)):
               img = divs[i].select('img')[0]
               imageUrl = 'http:' + img.get('src')
               caption = divs[i].select('.thumbcaption')[0].getText()
               print("Downloading image: %s" % (caption))
               downloadPic(imageUrl, caption)

     response = input("Continue downloading? (Y/N)\n")
     if response.upper()[0] == 'N':
          status = False
          print("Goodbye")
   
