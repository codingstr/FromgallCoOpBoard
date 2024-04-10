import copy
import bs4
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 게시글 클래스
class Post:
    def __init__(self, num, title, date, writer) :
        self.num = num
        self.title = title
        self.date = date
        self.writer = writer
        self.content = ""

    def saveContent(self, content) :
        self.content = content

    def getContent(self) :
        return self.content

    def __str__(self) :
        return "num: " + str(self.num) + ", title: " + self.title + ", date: " + self.date + ", writer: " + self.writer

    def __eq__(self, other) :
        return self.num == other.num

    def __hash__(self) :
        return hash(self.num)


# 핵심 변수
lastPostNum = 0
newPostNumList = []
postsInfo = []
postCount = 0
gallUrl = "https://gall.dcinside.com/mgallery/board/lists/?id=fromsoftware&sort_type=N&search_head=130&page=1"


# 게시글 목록 가져오기
def getNewPosts() :

    global lastPostNum
    global newPostNumList
    global postsInfo
    global postCount

    try :
        req = urllib.request.Request(
            gallUrl, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response = urllib.request.urlopen(req)
        soup = bs4.BeautifulSoup(response.read(), 'html.parser')

        rows = soup.find_all('tr', {'class': 'ub-content us-post'})
        insertLoc = copy.deepcopy(postCount)
        tempLastPostNum = copy.deepcopy(lastPostNum)
        for row in rows:
            postNum = row.find('td', {'class': 'gall_num'})
            if int(postNum.text) > tempLastPostNum :
                if tempLastPostNum != 0 : 
                    print("New Post Found!" + str(tempLastPostNum))
                newPostNumList.insert(insertLoc, int(postNum.text))
                postTitle = row.find('a')
                postDate = row.find('td', {'class': 'gall_date'})
                postWriter = row.find('td', {'class': 'gall_writer ub-writer'})
                time = str(postDate.get('title')).split(' ')[1]
                time = time[:5]
                post = Post(int(postNum.text), str(postTitle.text.strip()), time, str(postWriter.get('data-nick')))
                writerIP = row.find('span', {'class': 'ip'})
                if writerIP is not None:
                    post.writer += " " + writerIP.text
                else :
                    post.writer += " (ID)"
                post.saveContent(getPostContent(postNum.text))
                postsInfo.insert(insertLoc, post)
                postCount += 1
                if lastPostNum < int(postNum.text) :
                    lastPostNum = int(postNum.text)
        return insertLoc
    except :
        print("Error")

# 게시글 내용 가져오기
def getPostContent(postNum) :

    postUrl = "https://gall.dcinside.com/mgallery/board/view/?id=fromsoftware&no=" + postNum

    try :
        req = urllib.request.Request(
            postUrl, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response = urllib.request.urlopen(req)
        soup = bs4.BeautifulSoup(response.read(), 'html.parser')

        postContent = soup.find('div', {'class': 'writing_view_box'}).get_text(separator='\n', strip=True)
        postTxt = str(postContent)

        return postTxt
    except :
        return "Error"
