
import db
import seaborn as sns


def follower_botness_histogram(username):
 
    scorelist=[]
    followers = db.getFollowers(toName=username)   
    for f in followers:
        follower = f['_from'].split('/')[1]
        score=db.getUser(follower)['botness']['score']
        scorelist.append(score)
    ax = sns.distplot(scorelist, name='probability of follower bot')
    fig = ax.get_figure()
    fig.savefig('plots/testfig.png')



