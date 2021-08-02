# Peer-to-Peer chat application #
### Project is divided in 5 files: Server, Client and twitter credentials scripts + ImagesDownloaded file ###
Libraries needed: Tweepy (see .txt on how to get the Access Token Keys)

### Instructions ###
1. Open 3 new command prompts and go to the directory were all these 3 files are (on all 3 command prompts).
2. First run the server script("server3D3.py") on one of the commands and then run the client scripts ("client3D3.py") on the other 2 command prompts.
3. The server command will output "The Server is ready to receive" if it succesfully run it. The other 2 commands will output "Username: "
4. Type in a desired username for each client and press enter(eg: "Fernando", "Antonio").
5. Server should accept both connections and output the local address, port number and the hashed usernames (SHA256) (eg:"66384278", "90479205")
6. From now on, clients will be able to communicate between them sending messages.
7. Note: In clients command prompts, real usernames will be displayed(eg: "Fernando", "Antonio") but on server command prompt,the hashed value of the usernames will be displayed, this way if someone access the server, he/se won't know the real username.
8. Note: Encryption of the username is modified (with respect the original SHA256) so the mapping of the username outputs an 8 digit number.

### Reserved Key-words in chat ###
1. "TWEETS: When typed "TWEETS" by any of the clients, that clients command prompt will ask for a "Twitter username".
		  When entered an existing username (eg: "spacex") --> The tweets twitted by that account in the last 2 days will be outputted to that clients command prompt.
		  When entered a non-existing username (eg:"3d3compnet") --> Command prompt will output "That account doesn't exist".
      NB: Twitter username is not case sensitive (It is the same inserting "spacex" instead of "SpaceX")
      
2. "PIC": When typed "PIC" by any of the clients, that clients command prompt will ask for an "Image URL to download".
		  When entered a valid URL (eg:"https://i.kym-cdn.com/entries/icons/original/000/000/091/TrollFace.jpg") --> Command prompt will ask for a file name(eg: "first").
	  	When enter is pressed, it will save that file as a .png in the "ImagesDownloaded" file.
		  NB: If 2 images are downloaded under the same file name (eg: "first.png"), the last one will be the one saved.
		  NB: If you want to download a picture, find the picture in google, open it in a new tab, and copy that URL.
