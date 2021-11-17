# -----------------------------------------------------------------------------
# BEGIN driver.py
# -----------------------------------------------------------------------------

import os
import sys
import time
import logging
from optparse import OptionParser
from src.sheng.compile import *
from src.sheng.utils import *


SYSTEM_STREAMS = {
    'stdin': sys.stdin,
    'stdout': sys.stdout,
    'stderr': sys.stderr,
}


def default(str):
    return str + ' [Default: %default]'

def read_command(argv):
    usage_str = 'sheng [option] [file]'
    parser = OptionParser(usage_str)

    parser.add_option(
        '--debug', action='store_true', dest='debug',
        help=default('debug'), default=False
    )

    parser.add_option(
        '--debug-lex', action='store_true', dest='debug_lex',
        help=default('debug lex'), default=False
    )

    parser.add_option(
        '--debug-yacc', action='store_true', dest='debug_yacc',
        help=default('debug yacc'), default=False
    )
    
    parser.add_option(
        '--input-stream', dest='input_stream',
        help=default('input stream'), default='stdin'
    )

    parser.add_option(
        '--output-stream', dest='output_stream',
        help=default('output stream'), default='stdout'
    )

    parser.add_option(
        '--error-stream', dest='error_stream',
        help=default('error stream'), default='stderr'
    )

    parser.add_option(
        '--log-stream', dest='log_stream',
        help=default('log stream'), 
        default='stderr'
    )

    parser.add_option(
        '--log-file', action='store_true', dest='log_file',
        help=default('generate log file'), default=False
    )

    options, other = parser.parse_args(argv[1:])
    if (len(other) == 0):
        parser.error('no input file')
    if (len(other) > 1):
        parser.error('Command line input not understood: ' + str(other[1:]))

    args = dict()
    args['file'] = other[0]

    # Debug and log stream
    if (options.debug or options.debug_lex or options.debug_yacc):
        # Debug flags
        Global().debug = options.debug
        if (options.debug_lex or options.debug_yacc):
            Global().debug = True
            Global().debug_lex = options.debug_lex
            Global().debug_yacc = options.debug_yacc

        # Log stream
        log_stream = None
        if (options.log_file):
            log_stream_path = f'./log/sheng_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.log'
            os.makedirs(os.path.dirname(log_stream_path), exist_ok=True)
            log_stream = open(log_stream_path, 'w')
        elif (options.log_stream in SYSTEM_STREAMS):
            log_stream = SYSTEM_STREAMS[options.log_stream]
        else:
            log_stream = open(options.log_stream, 'w')
        Global().log_stream = log_stream

        # Set up a logging object
        logging.basicConfig(
            level = logging.DEBUG,
            stream = Global().log_stream,
            format = '「日志」排除故障：%(filename)s:%(lineno)d:%(message)s'
        )
        log = logging.getLogger()
        Global().log = log

    # Input stream
    input_stream = None
    if (options.input_stream in SYSTEM_STREAMS):
        input_stream = SYSTEM_STREAMS[options.input_stream]
    else:
        input_stream = open(options.input_stream, 'r')
    Global().input_stream = input_stream

    # Output stream
    output_stream = None
    if (options.output_stream in SYSTEM_STREAMS):
        output_stream = SYSTEM_STREAMS[options.output_stream]
    else:
        output_stream = open(options.output_stream, 'w')
    Global().output_stream = output_stream

    # Error stream
    error_stream = None
    if (options.error_stream in SYSTEM_STREAMS):
        error_stream = SYSTEM_STREAMS[options.error_stream]
    else:
        error_stream = open(options.error_stream, 'w')
    Global().error_stream = error_stream

    return args

def read_file(file):
    f = open(file, "r", encoding='utf-8')
    data = f.read()
    f.close()
    return data

def main():
    args = read_command(sys.argv)
    data = read_file(**args)
    return execute(data)


# -----------------------------------------------------------------------------
# END driver.py
# -----------------------------------------------------------------------------
