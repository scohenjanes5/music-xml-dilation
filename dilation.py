from music21 import converter, stream, duration, environment
import argparse, json

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

file_path = 'tuba-bg.musicxml'  # Replace with the actual file path
parts = file_path.split(".")
parts[0] += "-dilated"
output_file = ".".join(parts)
score = converter.parse(file_path)

# score.show('text')

scaling_factor = 2.0  # Replace with your desired scaling factor

# Create a new stream to store the modified notes and rests
modified_stream = stream.Stream()

important_elements = ['Instrument', 'KeySignature', 'TimeSignature', 'MetronomeMark']

for i, element in enumerate(important_elements):
    try:
        important_elements[i] = score.recurse().getElementsByClass(element)[0]
    except:
        important_elements.remove(element)

modified_stream.append(important_elements)

for element in score.recurse().notesAndRests:
    if element.isNote or element.isRest:
        element.duration.quarterLength *= scaling_factor
        modified_stream.append(element)
    
# Show the modified passage
modified_stream.show('text')

# Write output file
modified_stream.write('musicxml', fp=output_file)
