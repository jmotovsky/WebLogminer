"""
Base idea of single parallel file reader:
http://www.blopig.com/blog/2016/08/processing-large-files-using-python/
http://www.blopig.com/blog/2016/08/processing-large-files-using-python-part-duex/
"""

from .FileReaderParallel import FileReaderParallel
from .FileReaderParallelConfig import FileReaderParallelConfig, ChunkerEnum
from .Sequence import BaseSequence
