from music21 import converter, stream, duration, environment

# get environment
env = environment.Environment()

# # check the path
# print('Environment settings:')
# print('musicXML:  ', env['musicxmlPath'])
# print('musescore: ', env['musescoreDirectPNGPath'])

# set path if necessary
env['musicxmlPath'] = 'C:\Program Files\MuseScore 3\\bin\MuseScore3.exe'
env['musescoreDirectPNGPath'] = 'C:\Program Files\MuseScore 3\\bin\MuseScore3.exe'

# print('Environment settings:')
# print('musicXML:  ', env['musicxmlPath'])
# print('musescore: ', env['musescoreDirectPNGPath'])

file_path = "tuba_bg.musicxml"  # Replace with the actual file path
score = converter.parse(file_path)

# score.show('text')

scaling_factor = 2.0  # Replace with your desired scaling factor

# Create a new stream to store the modified notes and rests
modified_stream = stream.Stream()

instrument = score.recurse().getElementsByClass('Instrument')[0]
key_signature = score.recurse().getElementsByClass('KeySignature')[0]
time_signature = score.recurse().getElementsByClass('TimeSignature')[0]
tempo = score.recurse().getElementsByClass('MetronomeMark')[0]

modified_stream.append([instrument, tempo, key_signature, time_signature])

for element in score.recurse().notesAndRests:
    if element.isNote or element.isRest:
        element.duration.quarterLength *= scaling_factor
        modified_stream.append(element)
    
# Show the modified passage
modified_stream.show('text')

output_file = "tuba_dilated.musicxml"  # Replace with the desired output file path
modified_stream.write('musicxml', fp=output_file)
