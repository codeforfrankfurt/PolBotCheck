import db
import seaborn as sns
import numpy as np

# takes data (that should come from the frontend) and creates the output we would like to have 
# on the front end.




def follower_botness(username):
"""  given a username, it creates the histogram of the botness of the followers 
    and saves it in plots (for now)  it also returns the probable percentage of follower bots
    (cutoff needs to be defined, for now it is 0.7)""" 
    cutoff = 0.7
    scorelist = []
    followers = db.getFollowers(toName=username)   
    for f in followers:
        follower = f['_from'].split('/')[1]
        score=db.getUser(follower)['botness']['score']
        scorelist.append(score)
    ax = sns.distaplot(scorelist, name='probability of follower bot')
    fig = ax.get_figure()
    fig.savefig('plots/testfig.png')
    botpercent = sum(np.array(scorelist)>cutoff)/len(scorelist)
    return botpercent


