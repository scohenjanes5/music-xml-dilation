from music21 import converter, stream, duration, environment, tempo
import argparse, json, warnings

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="Filename to dilate", default="tuba-bg.musicxml")
parser.add_argument("-d", "--dilation", type=float, help="Factor by which to dilate durations", default=2.0)
args = parser.parse_args()

# get environment
env = environment.Environment()

# # check the path
# print('Environment settings:')
# print('musicXML:  ', env['musicxmlPath'])
# print('musescore: ', env['musescoreDirectPNGPath'])

# set path if necessary
env['musicxmlPath'] = '/home/AppImages/musescore_studio_45_portable.appimage'
env['musescoreDirectPNGPath'] = '/home/AppImages/musescore_studio_45_portable.appimage'
#env['musicxmlPath'] = 'C:\Program Files\MuseScore 3\\bin\MuseScore3.exe'
#env['musescoreDirectPNGPath'] = 'C:\Program Files\MuseScore 3\\bin\MuseScore3.exe'

# print('Environment settings:')
# print('musicXML:  ', env['musicxmlPath'])
# print('musescore: ', env['musescoreDirectPNGPath'])

file_path = args.filename
scaling_factor = args.dilation

parts = file_path.split(".")
parts[0] += "-dilated"
output_file = ".".join(parts)
score = converter.parse(file_path)

# Create a new stream to store the modified notes and rests
modified_stream = stream.Stream()

important_elements = {'Instrument':None, 'KeySignature':None, 'TimeSignature':None, 'MetronomeMark':None, "Clef":None}

for k in important_elements.keys():
    try:
        important_elements[k] = score.recurse().getElementsByClass(k)[0]
    except:
        warnings.warn(f"Key {k} is not found in the provided part")

modified_stream.append([v for v in important_elements.values() if v is not None])

for element in score.recurse().notesAndRests:
    if element.isNote or element.isRest:
        element.duration.quarterLength *= scaling_factor
        modified_stream.append(element)
    
# Show the modified passage
modified_stream.show('text')

# Write output file
modified_stream.write('musicxml', fp=output_file)
