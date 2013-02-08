
# random ID generator
import string
import random
def id_generator(size=10, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

# segment cropper 
from pyannote import Segment
def crop_segment(segment, duration=3.):
    middle = segment.middle
    return Segment(middle-.5*duration, middle+.5*duration)

# format seconds
from datetime import timedelta
def format_seconds(seconds):
    td = timedelta(seconds=seconds)
    days = td.days
    seconds = td.seconds
    microseconds = td.microseconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%02d:%02d:%02d.%03d' % (hours, minutes, seconds, microseconds/1000)

from pyannote.parser import AnnotationParser, LSTParser
from pyannote import Timeline

# load speech turns groundtruth
Speaker = AnnotationParser().read('/people/bredin/Data/QCompere/phase1/dev/groundtruth/speaker.mdtm')
# load face tracks groundtruth
Head = AnnotationParser().read('/people/bredin/Data/QCompere/phase1/dev/groundtruth/head.mdtm')
# list of videos 
uris = LSTParser().read('/people/bredin/Data/QCompere/phase1/dev/lists/uri.lst')

duration = 3.

# ========================================================================
# EXTRACT SEGMENTS WHERE THE UNIQUE FACE CORRESPONDS TO THE UNIQUE SPEAKER
# ========================================================================

f = open('/tmp/activeLipInSync.txt', 'w')

for uri in uris:
    
    print uri
    
    speaker = Speaker(uri)
    head = Head(uri)
    
    # timeline where there is exactly one speaker
    tmp = speaker >> speaker.timeline.segmentation()
    oneSpeakerTL = Timeline([s for s in tmp if len(tmp.tracks(s)) == 1],
                          uri=uri)
    
    # timeline where there is exactly one head
    tmp = head >> head.timeline.segmentation()
    oneHeadTL = Timeline([s for s in tmp if len(tmp.tracks(s)) == 1],
                          uri=uri)
    
    # focus on the intersection
    oneSpeakerOneHeadTL = (oneSpeakerTL & oneHeadTL).segmentation()
    
    # timeline where speaker and head are the same
    speaker = speaker >> oneSpeakerOneHeadTL
    head = head >> oneSpeakerOneHeadTL
    timeline = Timeline([s for s in oneSpeakerOneHeadTL 
                           if speaker.get_labels(s) == head.get_labels(s)],
                        uri=uri).coverage()
    
    # remove segments smaller than 3 seconds
    # and extract the middle 3 seconds
    timeline = Timeline([crop_segment(s, duration=duration) for s in timeline if s.duration > duration], uri=uri)
    
    speaker = speaker.crop(timeline, mode='intersection')
    head = head.crop(timeline, mode='intersection')
    
    for s,t,l in speaker.iterlabels():
        f.write('%s %s %s %s %s\n' % (uri, format_seconds(s.start),
                                           format_seconds(s.duration), 
                                           id_generator(), 
                                           id_generator()))
        f.flush()

f.close()


# =========================================================================
# EXTRACT SEGMENTS WHERE THE UNIQUE FACE DOES NOT CORRESPOND TO ANY SPEAKER
# =========================================================================

f = open('/tmp/inactiveLip.txt', 'w')

for uri in uris:
    
    print uri
    
    speaker = Speaker(uri)
    head = Head(uri)
    
    # timeline where there is exactly one head
    tmp = head >> head.timeline.segmentation()
    oneHeadTL = Timeline([s for s in tmp if len(tmp.tracks(s)) == 1],
                          uri=uri)
    
    anySpeakerOneHeadTL = (speaker.timeline & oneHeadTL).segmentation()
    
    
    # timeline where unique head is not among speaker
    speaker = speaker >> anySpeakerOneHeadTL
    head = head >> anySpeakerOneHeadTL
    timeline = Timeline([s for s in anySpeakerOneHeadTL 
                           if head.get_labels(s).pop() not in speaker.get_labels(s)],
                        uri=uri).coverage()
    
    # remove segments smaller than 3 seconds
    # and extract the middle 3 seconds
    timeline = Timeline([crop_segment(s, duration=duration) for s in timeline if s.duration > duration], uri=uri)
    
    speaker = speaker.crop(timeline, mode='intersection')
    head = head.crop(timeline, mode='intersection')
    
    for s,t,l in speaker.iterlabels():
        f.write('%s %s %s %s %s\n' % (uri, format_seconds(s.start),
                                        format_seconds(s.duration), 
                                        id_generator(),
                                        id_generator()))
        f.flush()

f.close()

