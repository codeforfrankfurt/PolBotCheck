

#using this now for testing... 
import botornotapi
screen_name='@malechanissen'
results = botornotapi.get_followers(screen_name)
print(results)
botornotapi.get_bot_or_not(results[0])
