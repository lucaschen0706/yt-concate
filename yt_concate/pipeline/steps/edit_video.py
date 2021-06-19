
from .step import Step

from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

class EditVideo(Step):
    def process(self, data, inputs, utils):
        clips = []
        for found in data:
            print(found.yt.video_filepath)
            start, end = self.parse_caption_time(found.time)
            try:
                video = VideoFileClip(found.yt.video_filepath).subclip(start, end)
                clips.append(video)
            except:
                print('can not found video', found.yt.id)

            if len(clips) >= inputs['limit']:
                break
        final_clip = concatenate_videoclips(clips)
        output_filepath = utils.get_output_file(inputs['channel_id'], inputs['search_word'])
        final_clip.write_videofile(output_filepath)

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h), int(m), int(s) + int(ms) / 1000