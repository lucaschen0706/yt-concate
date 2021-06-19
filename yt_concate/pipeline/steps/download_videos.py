import concurrent.futures
import os
import time

from .step import Step

from pytube import YouTube
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        # start = time.time()
        # yt_set = set([found.yt for found in data])
        # print('video to download=', len(yt_set))
        # for yt in yt_set:
        #     url = yt.url
        #
        #     if utils.video_file_exists(yt):
        #         print(f'found existing video file {url}, skipping')
        #         continue
        #
        #     try:
        #         print('downloading', url)
        #         YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
        #     except:
        #         print('Download Error', url)
        # end = time.time()
        # print('download video took', end - start, 'seconds')

        start = time.time()
        yt_set = set([found.yt for found in data])
        yt_list = list(yt_set)
        print('video to download=', len(yt_list))
        threadpools = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for i in range(os.cpu_count()):
                t = executor.submit(self.download_captions_by_multi_thread, yt_list[i::os.cpu_count()], utils)
                threadpools.append(t)

        for threadpool in threadpools:
            threadpool.result()

        end = time.time()
        print('download video took', end - start, 'seconds')

        return data

    @staticmethod
    def download_captions_by_multi_thread(yt_list, utils):

        for yt in yt_list:
            url = yt.url

            if utils.video_file_exists(yt):
                print(f'found existing video file {url}, skipping')
                continue

            try:
                print('downloading', url)
                YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
            except:
                print('Download Error', url)
