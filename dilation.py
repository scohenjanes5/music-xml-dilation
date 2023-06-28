import xml.etree.ElementTree as ET

class Note:

    def __init__(self, note_element):
        # Extract note attributes
        pitch_element = note_element.find("pitch")
        if pitch_element is not None:
            self.step = pitch_element.find("step").text
            self.octave = int(pitch_element.find("octave").text)
            #alter is accidentals?
        else: #is a rest
            self.step = "R"
            self.octave = 0
            
        self.duration = int(note_element.find("duration").text)
        self.voice = int(note_element.find("voice").text)

        try:
            self.type = note_element.find("type").text
        except:
            self.type = None

        try:
            self.stem = note_element.find("stem").text
        except:
            self.stem = None

    def __str__(self):
        return(f" Name: {self.step}, Octave number: {self.octave}, Duration: {self.duration}, Voice: {self.voice}, Type: {self.type}, Stem dir: {self.stem}")
    
    def stretch(self, scaling_factor):
        self.duration *= scaling_factor
        if scaling_factor == 2:
            idx_shift = +1
        elif scaling_factor == 0.5:
            idx_shift = -1

        types = ["eigth", "quarter", "half", "whole", "twowholes"]
        for i, type in enumerate(types):
            if type == self.type:
                self.type = types[i+idx_shift]
                if self.type == "whole":
                    self.stem = None
                elif self.stem is None:
                    self.stem = "up"

                break

    
class Measure:
    """
        Initialize Measure object.

        Args:
            measure_element (optional): Measure element object to extract information from.
            **kwargs: Additional keyword arguments to directly assign values to class inputs.
                - n: Integer representing the number.
                - divisions: Integer representing the divisions.
                - key: String representing the key.
                - ts_numerator: Integer representing the time signature numerator.
                - ts_denominator: Integer representing the time signature denominator.
                - clef_type: String representing the clef type.
                - clef_line: Integer representing the clef line.
                - notes_list: List of Note objects.
    """

    def __init__(self, measure_element=None, **kwargs):
        if measure_element is not None:
            self.info_from_measure_element(measure_element)
        else:
            self.number = kwargs.get('n')
            self.divisions = kwargs.get('divisions')
            self.key = kwargs.get('key')
            self.ts_numerator = kwargs.get('ts_numerator')
            self.ts_denominator = kwargs.get('ts_denominator')
            self.clef_type = kwargs.get('clef_type')
            self.clef_line = kwargs.get('clef_line')
            self.notes_list = kwargs.get('notes_list')
            
    def info_from_measure_element(self, measure_element):
        self.number = measure_element.get("number")
        try:
            attribs = measure_element.find("attributes")
            self.divisions = int(attribs.find("divisions").text)
            try:
                key = attribs.find("key")
                self.key = int(key.find("fifths").text)
            except:
                self.key = None
            
            try:
                time = attribs.find("time")
                self.ts_numerator = time.find("beats").text
                self.ts_denominator = time.find("beat-type").text
            except:
                self.ts_numerator, self.ts_denominator = None, None

            try:
                clef = attribs.find("clef")
                self.clef_type = clef.find("sign").text
                self.clef_line = clef.find("line").text
            except:
                self.clef_type, self.clef_line = None, None
        
        except:
            self.divisions = None
            self.key = None
            self.ts_numerator, self.ts_denominator = None, None
            self.clef_type, self.clef_line = None, None

        self.notes_list = self.getNotes(measure_element)

    def getNotes(self, measure_element):
        notes = []
        for note_element in measure_element.findall("note"):
            note = Note(note_element)
            notes.append(note)
        return notes
    
    def __str__(self):
        printout = f"#{self.number} Contains {len(self.notes_list)} notes."      

        if self.clef_line is not None:
            printout += f"\n{self.clef_type} Clef on line {self.clef_line}"

        if self.key is not None:
            printout += f"\nKey code: {self.key}"
        
        if self.ts_numerator is not None:
            printout += f"\nTS: {self.ts_numerator}/{self.ts_denominator}"

        return printout
    
    def print_full_details(self):
        print(self)
        for note in self.notes_list:
            print(note)
   
class Passage:

    def __init__(self, root_element, part_nuber=1):
        part_element = root_element.find(f".//part[@id='P{part_nuber}']")

        self.measure_list = self.measures_from_part(part_element)
        self.important_measures = self.find_important_measures()

    def find_important_measures(self):
        indicies = []
        for measure in self.measure_list:
            if any(attr is not None for attr in (measure.divisions, measure.key, measure.ts_numerator, measure.ts_denominator, measure.clef_type, measure.clef_line)):
                indicies.append(measure.number)
        return indicies

    def measures_from_part(self, part_element):
        measures = []
        for measure in part_element.findall("measure"):
            measure_obj = Measure(measure)
            measures.append(measure_obj)
            # print(measure_obj)
            # measure_obj.print_full_details()

        return measures
    
    def stretch(self, scaling_factor):
        notes = []
        # if new number of measures would be fractional, i.e. 2.5,
        # 3rd will only be half filled. Round to avoid this.
        new_num_measures = round(len(self.measure_list)*scaling_factor)
        new_important_indicies = [(int(i)-1)*scaling_factor for i, in self.important_measures]
        print(new_important_indicies)
        for measure in self.measure_list:
            for note in measure.notes_list:
                note.stretch(scaling_factor)
                print(note)
                notes.append(note)
        


def parse_musicxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    return Passage(root)

# Usage example
file_path = "tuba_bg.musicxml"
#file_path = "tuba_lengthened.musicxml"
#file_path = "tuba_shortened.musicxml"
scaling_factor = 2
passage = parse_musicxml(file_path)
notes = [note for measure in passage.measure_list for note in measure.notes_list]
for note in notes:
    print(note)

print()

passage.stretch(scaling_factor)

# for measure in measures:
#     for note in measure.notes_list:
#         note.duration *= scaling_factor

# notes = [note for measure in passage.measure_list for note in measure.notes_list]
# for note in notes:
#     print(note)


