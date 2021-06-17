from pytube import YouTube

from .step import Step
import time
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        # download the package by:  pip install pytube
        for yt in data:
            if utils.caption_file_exists(yt):
                print('found existing caption file')
                continue
            print(yt.url)
            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            # except (AttributeError, KeyError):
            except:
                print('Error when downloading caption for', yt.url)
                continue

            # print(en_caption_convert_to_srt)
            # save the caption to a file named Output.txt

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        end = time.time()
        print('took', end - start, 'seconds')
        return data