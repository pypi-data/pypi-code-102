import hashtags_extract


def is_hashtag(hashtag):
    if ' ' in hashtag:
        return False
    if '\n' in hashtag:
        return False
    if not hashtag.startswith('#'):
        return False
    return True


def in_hashtag(string):
    if len(hashtags_extract.hashtags(string)) > 0:
        return True
    else:
        return False
