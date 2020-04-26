import multiprocessing as mp
from typing import Tuple
from .FileReaderParallelConfig import FileReaderParallelConfig
from .Sequence import BaseSequence
from .Chunker import Chunker


def _worker(job_id: int, chunker: Chunker, chunk: list, input_file: str, sequence_worker: BaseSequence, kwargs) -> list:
    output = list(chunker.parse(chunker.read(input_file, chunk)))

    return sequence_worker.worker(output)


class FileReaderParallel(object):
    def __init__(self, input_file: str, config: FileReaderParallelConfig = FileReaderParallelConfig()):
        self.__input_file = input_file
        self.__config = config

    def manage_work(self, sequence_worker: BaseSequence, kwargs={}) -> Tuple[int, list]:
        self.__init_process()

        for jobID, chunk in enumerate(self.__config.chunker.chunkify(self.__input_file)):
            job = self.__pool.apply_async(_worker, (jobID, self.__config.chunker, chunk, self.__input_file, sequence_worker, kwargs))
            self.__jobs[jobID] = job

        for jobID, job in self.__jobs.items():
            yield jobID, job.get()

        self.__finalize_process()

    def __init_process(self) -> None:
        self.__pool = mp.Pool(self.__config.cores)
        self.__set_default_jobs()

    def __finalize_process(self) -> None:
        self.__pool.close()
        self.__set_default_jobs()

    def __set_default_jobs(self) -> None:
        self.__jobs = {}
