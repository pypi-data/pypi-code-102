import librosa

def load_audio(file_path):
    """Load audio file.

    Args:
        file_path ([str]): [description]
        
    Returns:
        y: [vector] : time series of audio
        sr: [int] : sampling rate
    """
    y, sr = librosa.load(file_path)
    return y, sr  