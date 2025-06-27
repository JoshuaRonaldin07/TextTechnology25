from lxml import etree
from collections import defaultdict
import csv
import itertools
import os

# === Config ===
tei_file = "C:/Users/bluem/Desktop/PythonFiles/shake000002-two-gentlemen-of-verona.tei (3).xml"
output_csv = 'character_network.csv'

# === Parse XML ===
tree = etree.parse(tei_file)
root = tree.getroot()

# Namespace handling (TEI uses default namespace)
ns = {'tei': root.nsmap[None]} if None in root.nsmap else {}

# === Build Co-occurrence Graph ===
co_occurrence = defaultdict(int)

# Find all scenes
scenes = root.xpath(".//tei:div[@type='scene']", namespaces=ns)

for scene in scenes:
    # Find all speakers in the scene
    speakers = set(scene.xpath(".//tei:sp/@who", namespaces=ns))
    
    # Normalize speakers (remove # if present)
    speakers = {s.replace('#', '') for s in speakers}
    
    # Get all unique pairs (combinations)
    for pair in itertools.combinations(sorted(speakers), 2):
        co_occurrence[pair] += 1

# === Write CSV for Gephi ===
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Source', 'Target', 'Weight'])
    
    for (char1, char2), weight in co_occurrence.items():
        writer.writerow([char1, char2, weight])

print(f" Character network exported to {output_csv}")
