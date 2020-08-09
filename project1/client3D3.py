import socket
import sys
import select
import errno
import urllib.request
import urllib.error

#twwitter stuff
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twitter_credentials #own file, INCLUDE IN SUBMISSION
import datetime, time

#-----------------------------------------------------------------------
#Required authentication for Twitter api.
#-----------------------------------------------------------------------------
authenticator = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
authenticator.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticator)
#-----------------------------------------------------------------------------

#Socket stuff (address, port, username of clients, connections)
header_length = 10
TCP_IP = "127.0.0.1"
TCP_PORT = 1234

my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((TCP_IP, TCP_PORT))

client_socket.setblocking(False)#receive (recv) functionallity won't be blocking.

username = my_username.encode('utf-8')
username_header = f"{len(username):<{header_length}}".encode('utf-8')

client_socket.send(username_header + username)

#-----------------------------------------------------------------------
#this is the function to get the image from internet, we can see that it creates
# a path to save the image and it gets the image from an input URL
#------------------------------------------------------------------------------PIC function
def get_png(url, file_path, file_name):

    all_path = file_path + file_name + '.png'
    urllib.request.urlretrieve(url, all_path)

#-----------------------------------------------------------------------------TWEET function
#-----------------------------------------------------------------------
#this is the function to the the tweets, it first loads the tweets in the first
#page of the username's Twitter wall and it then only selectes the tweets
#from the last 2 days. If there are no more tweets, the function exits, and if
#there are more tweets but not in this wall page, it loads the next one.
#-----------------------------------------------------------------------
def get_tweets(api, username):
    page = 1
    deadend = False
    while True:
        tweets = api.user_timeline(username, page = page)

        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 2: #the 2 indicates the number of days to look back for a tweet.
                last_tweet = tweet.text.encode('utf-8')
                print(last_tweet.decode('utf-8'))
               # print(tweet.text.encode('utf-8'))
            else:
                deadend = True
                return
        if not deadend:
            page + 1
            time.sleep(500)

#-----------------------------------------------------------------------
#this loop will wait for input messages and will send to the server the message
#inputted. It will also deal with the 2 reserved words (PIC and TWEETS)
#-----------------------------------------------------------------------

#[1].
while True:
    message = input(f"{my_username} > ")

    if message:

        if message == 'PIC':
            url = input('Enter image URL to download: ')

            if url == '':
                break
            file_name = input('Enter file name to save as:')

            if file_name == '':
                break
            try:
                get_png(url, 'imagesDownloaded/', file_name) #"hardcoded" the input file, will need a file named like this. Could ask the user for a folder as well...

            except urllib.error.HTTPError as e:
                print (e.code)

            except urllib.error.URLError as e:
                print (e.reason)

        if message == 'TWEETS':
            twitter_acc = input('Enter a Twitter username: ')

            try:
                get_tweets(api, twitter_acc)

            except:
                print('That account doesnt exist.') #assume this is the only error ("wrong")
                pass
            
        message = message.encode("utf-8")
        message_header = f"{len(message) :<{header_length}}".encode("utf-8")
        client_socket.send(message_header + message)

#-----------------------------------------------------------------------
#this loop will receive the username of the client that sent a message and
# the message itself, it will then output it to its screen.
#-----------------------------------------------------------------------
    try:
    
        while True:
            username_header = client_socket.recv(header_length)

            #if we didnt get any data for whatever reason
            if not len(username_header):
                print('Connection will close by the server.')
                sys.exit()

#get the username
            username_length = int(username_header.decode("utf-8"))  
            username = client_socket.recv(username_length).decode("utf-8")

#get the message
            message_header = client_socket.recv(header_length)
            message_length = int(message_header.decode("utf-8"))
            message = client_socket.recv(message_length).decode("utf-8")

#output it to screen
            print(f'{username} > {message}')
    except:
        pass
    #except IOError as e:
     #   if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
      #      print('Reading error: {}', format(str(e)))
       #     sys.exit()
       # continue
