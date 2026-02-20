from nltk.tokenize import WordPunctTokenizer


def prepare_input_text(text):
    text = text.lower()
    tokens = WordPunctTokenizer().tokenize(text.strip())
    text = ' '.join(tokens)

    return text, len(tokens)