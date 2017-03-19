import requests, bs4, regex, operator, itertools, multiprocessing, multiprocessing.pool
from multiprocessing import Pool  
base_url='https://lyrics.az/'  #lyrics scraped from this website

#Without this pool cannot call functions with another pool
class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

#Create MyPool as a slightly different version of Pool which is not a daemonized function
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

#Get input from input.txt at the same location as python
def getinput():
    inp=[]
    with open('input.txt') as f:
        inp=[line.rstrip('\n') for line in f]
    return inp

#Get the count of word in song
def count(song,word):
    wordRegex=regex.compile(word)
    return len(wordRegex.findall(song))

#Get album list of artist as a list
def getAlbums(artist):
    artist=artist.replace(' ','-')
    artist_url=base_url+artist+'/allalbums.html'
    albumLinkList=[]
    res=requests.get(artist_url)
    try:
        res.raise_for_status()
    except:
        print('Could not find page at ',base_url,'. Assuming that the artist did not use the word ever') #did not find the page, could handle the situation better
    soup=bs4.BeautifulSoup(res.text, 'html.parser')   
    for link in soup.find_all('a', style=True):      #getting links of all albums
        albumLinkList.append(link['href'])
    return albumLinkList

#Get all track links in album as a list
def getTracks(album):
    tracksLinkList=[]
    res=requests.get(base_url+album)
    try:
        res.raise_for_status()
    except:
        print('Could not find page at ',album)
    soup=bs4.BeautifulSoup(res.text, 'html.parser')
    matchstr=r'^'+album
    for link in soup.find_all('a', href=regex.compile(matchstr)):  #getting links of all tracks from the album
        tracksLinkList.append(link['href'])
    return tracksLinkList

#Get lyrics of track given as link
def getLyrics(track):
    res=requests.get(base_url+track)
    try:
        res.raise_for_status()
    except:
        print('Could not find page at ',track)
    soup=bs4.BeautifulSoup(res.text, 'html.parser')
    if soup.find(id='lyrics') is not None:
        return soup.find(id='lyrics').get_text().lower()
    else:
        return ""

#Get the number of times artist has said word
def getScore(artist,word):
    pool=MyPool()  #multiple processes for each album
    score=0
    al=[]
    albums=getAlbums(artist)
    d=dict((el,word) for el in albums)
    for sc in pool.starmap(getScoreAl,d.items()):    #adding score for each album
        score=score+sc
    pool.terminate()                                 #terminating for safe operation
    return (score)

#Get the number of times word was said in album link
def getScoreAl(album,word):
    pool=MyPool() #creating multiple processes for each song
    score=0
    trackList=getTracks(album)
    d=dict((el,word) for el in trackList)
    for sc in pool.starmap(getScoreTr,d.items()):   #adding score for each track
        score+=sc
    pool.terminate()                                 #terminating for safe operation
    return (score)

#Get the number of times word was said in track link
def getScoreTr(track,word):
    return count(getLyrics(track),word)

#main
if __name__ == "__main__":
    inp=getinput()                                  #received input
    d = dict.fromkeys(inp[:-2], 0)                  #made it into a dictionary with key as singer and value as score
    for key in d:
        d[key]=getScore(key,inp[-1])                #get score for each artist
    sorted_d=sorted(d.items(), key=operator.itemgetter(1))   #convert dictionary which is unordered into a sorted list of tuples
    f = open('output.txt', 'w+')
    for artTup in reversed(sorted_d):
        print (artTup[0])
        f.write(artTup[0]+'\n')
    f.close()
    

        
