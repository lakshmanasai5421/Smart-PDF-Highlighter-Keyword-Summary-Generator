 
**Smart PDF Highlighter & Keyword Summary Generator**

---

## 🚀 What’s This All About?

Going through long PDFs to find specific details can be a real headache. This project is designed to **make that process much faster and smarter**.

It automatically:

✅ **Highlights important keywords** in yellow  
✅ **Highlights the full sentence** containing the keyword in light green  
✅ **Adds a clean summary page at the end** with all the highlighted sentences (with one special condition)  
✅ **Excludes sentences from the summary page** if they contain certain unwanted words or phrases

> The catch: while the script highlights both the keyword and the sentence on the page, it will **eliminate any sentence on the summary page** if it contains certain unwanted words. For example, if a sentence includes terms like “terms” or “conditions,” it will not be included in the summary page—even if the sentence is highlighted.

---

## 🧠 Why Use This?

This is especially helpful if you're:

- Reviewing lengthy reports, contracts, or policies  
- Looking for specific actions, issues, or clauses  
- Trying to get the **essence of a document quickly**, without reading the whole thing

---

## ⚙️ Key Features

### 🔍 1. Highlight Keywords in the PDF  
The script looks for a set of predefined keywords (like `"penalty"`, `"due date"`, `"failure"`, etc.) and highlights them directly in the document **in yellow**.

### ✨ 2. Highlight the Whole Sentence  
It also finds the full sentence containing each keyword and highlights that sentence **in light green**, so you can easily understand the context.

### 📄 3. Add a Summary Page  
A new page is added at the **end of the PDF** which lists all important sentences, organized by the page number they appear on.

### ❗ 4. Smart Filtering on the Summary Page  
While all matching keywords and sentences are highlighted within the pages, **the summary only includes meaningful full sentences**, and **ignores any sentence that just contains a base keyword and isn't useful alone**.

That means you won't see clutter like:
```
"Terms and conditions."
"Document submitted."
```
on the summary page — because they don’t really say much!

### ❌ 5. Eliminate Unwanted Sentences from the Summary  
Additionally, if a sentence contains certain **unwanted words or phrases**, it will be **automatically excluded from the summary**. For example, sentences with "terms" or "conditions" will not appear in the summary page, even if those words are relevant to the keyword list.

---

## 💪 Under the Hood

| Component | Description |
|----------|-------------|
| **base_keywords** | The list of important words we want to track (e.g., "penalty", "cancel", etc.) |
| **PyMuPDF (`fitz`)** | Used to extract text, search and highlight directly in the PDF |
| **NLTK** | Breaks the page text into sentences |
| **Regex** | Used to search for exact word matches |
| **Summary filtering** | Ensures only *meaningful*, multi-word sentences are added to the summary |
| **Exclusion logic** | Excludes sentences containing unwanted words from appearing in the summary page |

---

## 🛠️ You Can Customize:

- 🔤 **Add/Remove keywords**: Just edit the `base_keywords` list in the code  
- 🎨 **Change colors**: Update the RGB values in the script  
- 📁 **Use a different PDF**: Change the `input_pdf_path` variable  
- 📏 **Filter short/irrelevant sentences**: Adjust the `min_words_in_summary_sentence` threshold  
- ❌ **Exclusion Words**: Customize unwanted words/phrases to exclude from the summary (like "terms", "conditions", etc.)

---

## 📄 What the Output Looks Like

Let's say this sentence appears on Page 3:
> "The penalty will be charged if the due date is missed."

In the output:
- "penalty" and "due date" are highlighted in **yellow**
- The entire sentence is highlighted in **light green**
- The sentence will be listed on the summary page like:
```
[Pg 3] The penalty will be charged if the due date is missed.
```

But something like:
> "Terms and conditions."

Will be highlighted on the page, but **won’t** show up in the summary because it's deemed irrelevant.

---

## ✅ Final Words

This project is like a personal document assistant—it **saves time**, helps you **focus on what’s important**, and **summarizes everything for easy review**.

Perfect for students, professionals, legal reviewers, analysts, or anyone tired of reading through pages and pages to find just a few key points.

