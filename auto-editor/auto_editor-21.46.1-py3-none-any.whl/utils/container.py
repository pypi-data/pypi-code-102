'''utils/container.py'''

wav_formats = [
    'pcm_s16le', # default format

    'pcm_alaw',
    'pcm_f32be',
    'pcm_f32le',
    'pcm_f64be',
    'pcm_f64le',
    'pcm_mulaw',
    'pcm_s16be',
    'pcm_s24be',
    'pcm_s24le',
    'pcm_s32be',
    'pcm_s32le',
    'pcm_s8',
    'pcm_u16be',
    'pcm_u16le',
    'pcm_u24be',
    'pcm_u24le',
    'pcm_u32be',
    'pcm_u32le',
    'pcm_u8',
    'pcm_vidc',

    'mp3',
]

containers = {
    'apng': {
        'name': 'Animated Portable Network Graphics',
        'allow_video': True,
        'max_video_streams': 1,
        'vcodecs': ['apng'],
        'strict': True,
    },
    'gif': {
        'name': 'Graphics Interchange Format',
        'allow_video': True,
        'max_video_streams': 1,
        'vcodecs': ['gif'],
        'strict': True,
    },
    'aac': {
        'name': 'Advanced Audio Coding',
        'allow_audio': True,
        'max_audio_streams': 1,
        'acodecs': ['aac'],
        'strict': True,
    },
    'adts': {
        'name': 'Advanced Audio Coding',
        'allow_audio': True,
        'max_audio_streams': 1,
        'acodecs': ['aac'],
        'strict': True,
    },
    'wav': {
        'name': 'Waveform Audio File Format',
        'allow_audio': True,
        'max_audio_streams': 1,
        'acodecs': wav_formats,
        'strict': True,
    },
    'mp3': {
        'name': 'MP3 / MPEG-2 Audio Layer 3',
        'allow_audio': True,
        'max_audio_streams': 1,
        'acodecs': ['mp3'],
        'strict': True,
    },
    'opus': {
        'name': 'Opus',
        'allow_audio': True,
    },
    'oga': {
        'allow_audio': True,
    },
    'flac': {
        'name': 'Free Lossless Audio Codec',
        'allow_audio': True,
        'max_audio_streams': 1,
        'acodecs': ['flac'],
    },
    'ogg': {
        'allow_video': True,
        'allow_audio': True,
        'allow_subtitle': True,
        'vcodecs': ['theora'],
        'acodecs': ['opus', 'flac', 'vorbis'],
    },
    'ogv': {
        'allow_video': True,
        'allow_audio': True,
        'allow_subtitle': True,
        'vcodecs': ['theora'],
        'acodecs': ['opus', 'vorbis'],
    },
    'webm': {
        'name': 'WebM',
        'allow_video': True,
        'allow_audio': True,
        'allow_subtitle': True,
        'vcodecs': ['vp9', 'vp8', 'av1', 'libaom-av1'],
        'acodecs': ['opus', 'vorbis'],
    },
    'srt': {
        'name': 'SubRip Text / Subtitle Resource Tracks',
        'allow_subtitle': True,
        'scodecs': ['srt'],
        'max_subtitle_streams': 1,
        'strict': True,
    },
    'vtt': {
        'name': 'Web Video Text Track',
        'allow_subtitle': True,
        'scodecs': ['webvtt'],
        'max_subtitle_streams': 1,
        'strict': True,
    },
    'ass': {
        'name': 'SubStation Alpha',
        'allow_subtitle': True,
        'scodecs': ['ass', 'ssa'],
        'max_subtitle_streams': 1,
        'strict': True,
    },
    'ssa': {
        'name': 'SubStation Alpha',
        'allow_subtitle': True,
        'scodecs': ['ass', 'ssa'],
        'max_subtitle_streams': 1,
        'strict': True,
    },
    'avi': {
        'name': 'Audio Video Interleave',
        'allow_video': True,
        'allow_audio': True,
        'vcodecs': ['mpeg4'],
        'acodecs': ['mp3'],
    },
    'wmv': {
        'name': 'Windows Media Video',
        'allow_video': True,
        'allow_audio': True,
        'vcodecs': ['msmpeg4v3'],
        'acodecs': ['wmav2'],
    },
    'h264': {
        'name': 'H.264 / Advanced Video Coding (AVC) / MPEG-4 Part 10',
        'allow_video': True,
        'vcodecs': ['h264', 'mpeg4', 'hevc'],
    },
    'h265': {
        'name': 'H.265 / High Efficiency Video Coding (HEVC) / MPEG-H Part 2',
        'allow_video': True,
        'vcodecs': ['hevc', 'mpeg4', 'h264'],
    },
    'hevc': {
        'name': 'H.265 / High Efficiency Video Coding (HEVC) / MPEG-H Part 2',
        'allow_video': True,
        'vcodecs': ['hevc', 'mpeg4', 'h264'],
    },
    'mp4': {
        'name': 'MP4 / MPEG-4 Part 14',
        'allow_video': True,
        'allow_audio': True,
        'allow_subtitle': True,
    },
    'swf': {
        'name': 'ShockWave Flash / Small Web Format',
        'allow_video': True,
        'allow_audio': True,
        'vcodecs': ['flv1'],
        'acodecs': ['mp3'],
        'samplerate': [44100, 22050, 11025],
    },
    'not_in_here': {
        'allow_video': True,
        'allow_audio': True,
        'allow_subtitle': True,
    },
    'default': {
        'name': None,
        'allow_video': False,
        'allow_audio': False,
        'allow_subtitle': False,
        'max_video_streams': None,
        'max_audio_streams': None,
        'max_subtitle_streams': None,
        'vcodecs': None,
        'acodecs': None,
        'scodecs': None,
        'strict': False, # There may be more valid codecs than ones listed.
        'samplerate': None, # Any samplerate is allowed.
    },
}
