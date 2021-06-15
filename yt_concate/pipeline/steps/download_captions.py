from pytube import YouTube

from .step import Step
import time
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        # download the package by:  pip install pytube
        for url in data:
            if utils.caption_file_exists(url):
                print('found existing caption file')
                continue
            print(url)
            try:
                source = YouTube(url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (AttributeError, KeyError):
                print('Error when downloading caption for', url)
                continue

            # print(en_caption_convert_to_srt)
            # save the caption to a file named Output.txt

            text_file = open(utils.get_caption_filepath(url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        end = time.time()
        print('took', end - start, 'seconds')


