from pyannote.parser import AnnotationParser, LSTParser
from pyannote import Timeline

# load speech turns groundtruth
speaker = AnnotationParser().read('/people/bredin/Data/QCompere/phase1/train/groundtruth/speaker.mdtm')
# load face tracks groundtruth
head = AnnotationParser().read('/people/bredin/Data/QCompere/phase1/train/groundtruth/head.mdtm')
# list of videos 
uris = LSTParser().read('/people/bredin/Data/QCompere/phase1/train/lists/uri.LCP_PileEtFace.lst')

for uri in uris[:1]:
    
    oneSpeakerOneHeadMatch = Timeline(uri=uri)
    oneSpeakerOneHeadMismatch = Timeline(uri=uri)
    oneSpeakerTwoHeadsMatch = Timeline(uri=uri)
    oneSpeakerTwoHeadsMismatch = Timeline(uri=uri)
    
    s = speaker(uri)
    h = head(uri)
    
    # focus on segments were exactly one person is speaking
    s = s >> s.timeline.segmentation()
    timeline = Timeline([segment for segment in s 
                                 if len(s.tracks(segment)) == 1], 
                        uri=uri)
    focus = timeline.coverage()
    s = s.crop(focus, mode='intersection').smooth()
    h = h.crop(focus, mode='intersection').smooth()
    
    # project both annotations on common timeline
    timeline = (s.timeline + h.timeline).segmentation()
    s = s >> timeline
    h = h >> timeline
    
    for segment in timeline:
        ls = s.get_labels(segment)
        lh = h.get_labels(segment)
        if len(ls) != 1:
            raise ValueError('Overlapping speech!')
        ls = ls.pop()
        if len(lh) == 1:
            lh = lh.pop()
            if ls == lh:
                oneSpeakerOneHeadMatch += segment
            else:
                oneSpeakerOneHeadMismatch += segment
        elif len(lh) == 2:
            if ls in lh:
                oneSpeakerTwoHeadsMatch += segment
            else:
                oneSpeakerTwoHeadsMismatch += segment
        