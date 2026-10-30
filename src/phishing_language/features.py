"""Illustrative feature extractor; not a reconstruction of the original private scripts.

Uses lexicons transcribed from the original paper's Appendix A. Sentence
segmentation and readability are approximations, and numbers must not be
presented as an exact reproduction of the historical results.
"""
import html
import re
import unicodedata
from collections import Counter
from pathlib import Path

PRONOUNS = {
    "first_person_singular": set("i me my mine myself".split()),
    "first_person_plural": set("we us our ours ourselves".split()),
    "second_person": set("you your yours yourself yourselves".split()),
    "third_person": set("he him his himself she her hers herself they them their theirs themselves".split()),
}
MODALS = {
    "core_modals": set("can could may might must shall should will would".split()),
    "obligation_modals": set("must shall should".split()),
    "possibility_modals": set("can could may might".split()),
    "will_would_modals": set("will would".split()),
}
HEDGING = set("apparently approximately arguably generally likely maybe perhaps possibly probably roughly seem seems seemed seemingly somewhat unlikely".split())
CERTAINTY = set("certain certainly certainty definite definitely clearly obviously surely undoubtedly guarantee guaranteed guarantees".split())
URGENCY = set("urgent urgently immediate immediately asap deadline expire expires expired expiring hurry quickly promptly".split())
URGENCY_PHRASES = (
    "act now", "action required", "as soon as possible", "without delay", "right away",
    "within 24 hours", "within 48 hours", "final warning", "last chance"
)
# This is an illustrative preprocessing rule; original paper reports additional NLTK work.
CONTRACTIONS = {"we're":"we are", "you'll":"you will", "can't":"can not", "won't":"will not",
                "don't":"do not", "doesn't":"does not", "i'm":"i am", "it's":"it is",
                "they're":"they are", "i've":"i have", "we've":"we have"}
WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?", re.I)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)


def clean(text):
    text = unicodedata.normalize('NFKC', html.unescape(str(text)))
    text = re.sub(r'<[^>]+>', ' ', text)
    text = URL_RE.sub(' ', EMAIL_RE.sub(' ', text))
    return text


def tokens(text):
    text = clean(text).lower().replace('’', "'")
    for contraction, replacement in CONTRACTIONS.items():
        text = re.sub(r'\b' + re.escape(contraction) + r'\b', replacement, text)
    return WORD_RE.findall(text)


def mattr(words, window=20):
    if not words:
        return 0.0
    if len(words) < window:
        return len(set(words)) / len(words)
    return sum(len(set(words[i:i+window])) / window for i in range(len(words)-window+1)) / (len(words)-window+1)


def syllables(word):
    """Approximate syllable count; NOT the paper's original Flesch implementation."""
    w = word.lower()
    matches = re.findall(r'[aeiouy]+', w)
    count = len(matches)
    if w.endswith('e') and not w.endswith(('le','ye')) and count > 1:
        count -= 1
    return max(1,count)


def sentence_groups(text):
    text = clean(text)
    segments = re.split(r'[.!?]+|\n+', text)
    return [tokens(s) for s in segments if len(tokens(s)) >= 3]


def read_emolex(path):
    """Load licensed local NRC Emotion Lexicon TSV; DO NOT redistribute it.

    Format: word<TAB>emotion<TAB>binary_association (usual EmoLex format).
    """
    lex={'positive':set(), 'negative':set(), 'fear':set()}
    if path is None:
        return None
    with Path(path).open('r',encoding='utf-8-sig') as f:
        for line in f:
            fields=line.strip().split('\t')
            if len(fields) != 3: continue
            word, emotion, value = fields
            if emotion in lex and value == '1':lex[emotion].add(word.lower())
    if not all(lex.values()):
        raise ValueError('NRC Emotion Lexicon not loaded: check correct TSV file and license.')
    return lex


def extract(text, emolex=None):
    """Return 16 transparent non-emotion features; 19 with licensed NRC lexicon."""
    words = tokens(text)
    if not words:
        raise ValueError('No alphabetic words in email body')
    counts = Counter(words)
    rate=lambda terms: sum(counts[t] for t in terms)*100/len(words)
    output = {key:rate(group) for key,group in PRONOUNS.items()}
    output['personal_pronouns_overall'] = sum(output.values())
    output.update({key:rate(group) for key,group in MODALS.items()})
    output['hedging_markers']=rate(HEDGING)
    output['certainty_markers']=rate(CERTAINTY)
    lower_clean = ' '.join(words)
    phrase_count=sum(len(re.findall(r'(?<!\w)' + re.escape(p) + r'(?!\w)', lower_clean)) for p in URGENCY_PHRASES)
    output['urgency_markers']=(sum(counts[t] for t in URGENCY)+phrase_count)*100/len(words)
    sentences=sentence_groups(text)
    flat=[word for sent in sentences for word in sent]
    avg_sentence_length = (sum(map(len,sentences))/len(sentences)) if sentences else None
    output['average_sentence_length']=avg_sentence_length
    output['average_word_length']=sum(map(len,words))/len(words)
    output['mattr_20']=mattr(words,20)
    if sentences:
        estimated_syllables=sum(syllables(w) for w in flat)
        output['flesch_reading_ease']=206.835 - 1.015*(len(flat)/len(sentences)) - 84.6*(estimated_syllables/len(flat))
    else:
        output['flesch_reading_ease']=None
    if emolex is not None:
        for emotion in ('positive','negative','fear'):
            output[f'{emotion}_emotion' if emotion!='fear' else 'fear_vocabulary']=rate(emolex[emotion])
    return output
