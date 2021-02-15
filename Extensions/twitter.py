from twython import Twython
import emoji
from emoji import UNICODE_EMOJI

t = Twython(
    '5wyHzyYilg93Lx0DGTJTMzloP',
    'gdtMZ6WeXGDZyl67vDFy2FbAVBfs7xpBYDBFyzxd2GWSNaEd32'
)

def get_text(url):
    #url = 'https://twitter.com/VictorIsrael_/status/1348272317663731713?s=20'
    i_d = url.split('/')[-1] # Return the last string after '/'
    num = i_d.split('?')[0] # Return the ID before '?' 
    # The show status function from twython accepts the tweet ID
    tweet = t.show_status(id=int(num),tweet_mode='extended')
    text = tweet['full_text']

    emoji_count = sum([text.count(emoji) for emoji in UNICODE_EMOJI])
    
    if emoji_count == 0: # If there is no emoji
        return (text) # Return the text from status
    else:
        return emoji.get_emoji_regexp().sub(u'', text) # Return the text without emojis