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
    
class Measure:

    def __init__(self, measure_element):
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

   

def parse_musicxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()    

    measures = []

    # Find the relevant part in the XML structure
    part_element = root.find(".//part[@id='P1']")

    for measure in part_element.findall("measure"):
        measure_obj = Measure(measure)
        measures.append(measure_obj)
        # print(measure_obj)
        measure_obj.print_full_details()

    return measures    

# Usage example
file_path = "tuba_bg.musicxml"
#file_path = "tuba_lengthened.musicxml"
#file_path = "tuba_shortened.musicxml"
notes = parse_musicxml(file_path)

