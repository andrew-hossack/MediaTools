'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-02 20:45:26
 # @ Description:
 '''

from TikTokApi import TikTokApi

class TikTok():
    '''
    TikTok Tools Class leverages TikTokApi heavily

    https://github.com/davidteather/TikTok-Api
    '''
    def __init__(self, **kwargs):
        self.api = TikTokApi(**kwargs)


if __name__ == "__main__":
    instance = TikTok()

    results = 10

    # Since TikTok changed their API you need to use the custom_verifyFp option. 
    # In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.
    trending = instance.api.trending(count=results, custom_verifyFp="")

    for tiktok in trending:
        # Prints the id of the tiktok
        print(tiktok['id'])

    print(len(trending))