def cipher(text, shift, encrypt=True):

    """
    The cipher function allows you to encrypt text by shifting each letter a certain amount.
    

    Parameters
    ----------
    text : string
      text is a string that contains the text to be encrypted
    shift : integer
      shift is an integer that determines the amount of places each letter should be shifted (from a to z) and replaced with
    encrpyt: boolean
      when true, leads to encryption of the text

    Returns
    -------
    new_test
      The new shifted text string.

    Examples
    --------
    >>> import cipher_asa2249.cipher_asa2249
    >>> from cipher_asa2249 import cipher_asa2249
    >>> a = 'cat'
    >>> b = 3
    >>> cipher_asa2249.cipher(a,b)
    'fdw'
    """

    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_text = ''
    for c in text:
        index = alphabet.find(c)
        if index == -1:
            new_text += c
        else:
            new_index = index + shift if encrypt == True else index - shift
            new_index %= len(alphabet)
            new_text += alphabet[new_index:new_index+1]
    return new_text