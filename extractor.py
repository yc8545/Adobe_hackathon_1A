import fitz  # PyMuPDF
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"] + " "
                block_text = block_text.strip()
                if len(block_text) > 40:
                    paragraphs.append(block_text)
    return paragraphs

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = set()
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]
                        if text and size > 14 and len(text.split()) <= 10:
                            headings.add(text)
    return sorted(list(headings))

def generate_mindmap(headings):
    mindmap = {"Root": [{head: []} for head in headings]}
    return mindmap

def main(pdf_path):
    result = {
        "paragraphs": extract_text(pdf_path),
        "headings": extract_headings(pdf_path),
        "mind_map": generate_mindmap(extract_headings(pdf_path))
    }
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python extractor.py <path_to_pdf>")
    else:
        main(sys.argv[1])
