import fitz  # PyMuPDF
import os
import re
import nltk
from nltk.tokenize import sent_tokenize

# === CONFIG ===
input_pdf_path = "main.pdf"
output_pdf_path = "highlighted_output.pdf"
base_keywords = [
    "qualification", "scope", "penalty", "due date", "clarification",
    "document", "deposit", "failure", "terms", "conditions", "reject", "cancel"
]
term_to_base = {kw.lower(): kw.lower() for kw in base_keywords}
sentence_hits = []
min_words_in_summary_sentence = 5

# === Open PDF ===
if not os.path.exists(input_pdf_path):
    print("❌ File not found!")
    exit()

doc = fitz.open(input_pdf_path)

for page_num, page in enumerate(doc):
    full_text = page.get_text()
    lines = full_text.split('\n')
    paragraph_lines = [line.strip() for line in lines if len(line.strip().split()) >= 3]
    paragraph_text = " ".join(paragraph_lines)
    sentences = sent_tokenize(paragraph_text)

    for sentence in sentences:
        sentence_clean = sentence.strip()
        if not sentence_clean.endswith('.'):
            sentence_clean += '.'
        sentence_lower = sentence_clean.lower()

        skip_phrases = [
            "notwithstanding",
            "for offic",
            "signat",
            "reserves the right",
            "reserves for right"
        ]
        if any(skip in sentence_lower for skip in skip_phrases):
            continue

        matched_keywords = []
        for term in term_to_base:
            if re.search(r'\b' + re.escape(term) + r'\b', sentence_lower):
                matched_keywords.append(term)
                for inst in page.search_for(term):
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=(1, 1, 0))  # Yellow
                    highlight.update()

        if matched_keywords:
            for inst in page.search_for(sentence_clean):
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(0.8, 1, 0.8))  # Light green
                highlight.update()
            sentence_hits.append((page_num + 1, sentence_clean, matched_keywords))

    for line in lines:
        if len(line.strip().split()) < 3:
            line_str = line.strip()
            line_lower = line_str.lower()

            if any(skip in line_lower for skip in skip_phrases):
                continue

            matched_keywords = []
            for term in term_to_base:
                if re.search(r'\b' + re.escape(term) + r'\b', line_lower):
                    matched_keywords.append(term)
                    for inst in page.search_for(term):
                        highlight = page.add_highlight_annot(inst)
                        highlight.set_colors(stroke=(1, 1, 0))
                        highlight.update()

            if matched_keywords:
                for inst in page.search_for(line_str):
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors(stroke=(0.9, 0.9, 0.5))
                    highlight.update()
                sentence_hits.append((page_num + 1, line_str, matched_keywords))

# === Filter short sentences from summary ===
sentence_hits = [
    (pg, sentence, kws)
    for pg, sentence, kws in sentence_hits
    if len(sentence.split()) >= min_words_in_summary_sentence
]

# === Add summary page ===
sentence_hits.sort(key=lambda x: x[0])
summary_page = doc.new_page(-1)
y = 50

summary_page.insert_text((50, y), "📝 Highlighted Sentences", fontsize=16, fill=(0, 0, 1))
y += 30

# === Updated drawing function ===
def draw_highlighted_text(page, x, y, sentence, keywords, width_limit=480):
    fontsize = 10
    line_spacing = fontsize * 1.8
    fontname = "helv"
    space_width = fitz.get_text_length(" ", fontname=fontname, fontsize=fontsize)

    current_x = x
    current_y = y

    words = sentence.split(" ")
    for idx, word in enumerate(words):
        stripped_word = word.strip()
        clean_word = re.sub(r"[^\w\._-]", "", stripped_word.lower())
        word_width = fitz.get_text_length(stripped_word, fontname=fontname, fontsize=fontsize)

        if current_x + word_width > x + width_limit:
            current_y += line_spacing
            current_x = x

        if clean_word in keywords:
            rect = fitz.Rect(
                current_x,
                current_y - fontsize * 0.75,
                current_x + word_width,
                current_y + fontsize * 0.25
            )
            page.draw_rect(rect, fill=(1, 1, 0), overlay=True)

        page.insert_text(
            (current_x, current_y),
            stripped_word,
            fontsize=fontsize,
            fontname=fontname,
            fill=(0, 0, 0)
        )

        current_x += word_width + space_width

    return current_y + line_spacing

# === Render sentences to summary ===
for page_number, sentence, _ in sentence_hits:
    full_sentence = f"[Pg {page_number}] {sentence}"
    norm_sent = re.sub(r'[^\w\s\._-]', '', sentence.lower())
    detected_keywords = [kw for kw in term_to_base if re.search(r'\b' + re.escape(kw) + r'\b', norm_sent)]

    if y > 750:
        summary_page = doc.new_page(-1)
        y = 50
        summary_page.insert_text((50, y), "📝 Continued Highlights", fontsize=16, fill=(0, 0, 1))
        y += 30

    y = draw_highlighted_text(summary_page, 60, y, full_sentence, detected_keywords, width_limit=480)

# === Save PDF ===
doc.save(output_pdf_path, garbage=4, deflate=True)
doc.close()

print("\n✅ PDF processing complete.")
print("🟨 Keywords highlighted in yellow (page + summary)")
print("🟩 Sentences highlighted in light green on page")
print("📄 Output saved to:", output_pdf_path)