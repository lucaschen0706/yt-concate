import concurrent.futures
import os
from threading import Thread

from pytube import YouTube

from .step import Step
import time
from .step import StepException


class DownloadCaptions(Step):

    def process(self, data, inputs, utils):
        start = time.time()
        # threads = []
        #
        # for i in range(os.cpu_count()):
        #     t = Thread(target=self.download_captions_by_multi_thread, args=(data[i::4], utils))
        #     threads.append(t)
        #
        #
        # for thread in threads:
        #     thread.start()
        # for thread in threads:
        #     thread.join()

        ThreadPools = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for i in range(os.cpu_count()):
                t = executor.submit(self.download_captions_by_multi_thread, data[i::4], utils)
                ThreadPools.append(t)

        for threadpool in ThreadPools:
            threadpool.result()

        end = time.time()
        print('download caption took', end - start, 'seconds')
        return data

    @staticmethod
    def download_captions_by_multi_thread(data, utils):
        for yt in data:
            if utils.caption_file_exists(yt):
                print('found existing caption file')

            print(yt.url)
            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (AttributeError, KeyError):
                print('Error when downloading caption for', yt.url)

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
