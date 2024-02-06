#import Levenshtein
import bibtexparser

def are_entries_similar(title1, title2):
    distance = Levenshtein.distance(title1, title2)
    similarity_threshold = 0.95  # Adjust this threshold as needed
    similarity_score = 1 - (distance / max(len(title1), len(title2)))
    return similarity_score >= similarity_threshold

def serialize_entry(entry, out_file=None):
    db = bibtexparser.library.Library(entry)
    if not out_file:
        entry_str = bibtexparser.write_string(db)
        return entry_str
    else:
        bibtexparser.write_file(out_file, db)


file_path = "citations.txt"

with open(file_path, 'r') as file:
    citations = file.read()

parsed_bib = bibtexparser.parse_file(file_path)
print(parsed_bib.entries[0]['title'])

out_str = "main:\n\n"

bib_folder = 'assets/bib/'

for i in range(len(parsed_bib.entries)):
    print(i)
    '''for j in range(i + 1, len(parsed_bib.entries)):
        entry1 = parsed_bib.entries[i]
        entry2 = parsed_bib.entries[j]
        if are_entries_similar(entry1['title'], entry2['title']):
            print(f"Entries {i} and {j} are similar")'''
    pub_str = " - title: " + parsed_bib.entries[i]['title'].replace(':', '') + "\n"
    pub_str += "   authors: " + parsed_bib.entries[i]['author'] + "\n"
    entry_keys = [x.key for x in parsed_bib.entries[i].fields]
    if 'booktitle' in entry_keys:
        pub_str += "   conference: '" + parsed_bib.entries[i]['booktitle'].replace(':', '') + "'\n"
    elif 'journal' in entry_keys:
        pub_str += "   conference: " + parsed_bib.entries[i]['journal'].replace(':', '') + "\n"
    else:
        print('missing')
    pub_str += "   pdf: " + parsed_bib.entries[i].key + ".pdf\n"
    pub_str += "   image: " + parsed_bib.entries[i].key + ".png\n"
    pub_str += "   bibtex: " + bib_folder + parsed_bib.entries[i].key + ".bib\n"

    pub_str += "\n"
    out_str += pub_str

    #serialize_entry(parsed_bib.entries[i], bib_folder + parsed_bib.entries[i].key + ".bib")

with open('_data/publications.yml', 'w') as file:
    file.write(out_str)


