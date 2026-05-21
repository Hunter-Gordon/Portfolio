import os
import sys
import re
import random

# ----------------------------
# PyInstaller-safe path
# ----------------------------
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(__file__)

DATA_FILE = os.path.join(BASE_PATH, "gcl_data.txt")

# ----------------------------
# Load & parse data file
# ----------------------------
knowledge = {}

pattern = re.compile(r"\[(.*?)\](?:\[(.*?)\])?(?:\[(.*?)\])?\s+(.*)")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        match = pattern.match(line)
        if not match:
            continue

        school, tag1, tag2, fact = match.groups()
        school = school.lower()

        tags = [t for t in [tag1, tag2] if t]

        if school not in knowledge:
            knowledge[school] = {}

        for tag in tags:
            knowledge[school].setdefault(tag, []).append(fact)

# ----------------------------
# Aliases
# ----------------------------
ALIASES = {
    "st xavier": "stxavier",
    "st x": "stxavier",
    "stx": "stxavier",
    "elder": "elder",
    "moeller": "moeller",
    "la salle": "lasalle",
    "lasalle": "lasalle",
    "gcl south": "gcl_south"
}

# ----------------------------
# Conversation memory
# ----------------------------
last_school = None
last_topic = None

# ----------------------------
# Topic detection
# ----------------------------
def detect_topic(text):
    if "football" in text:
        return "football"
    if any(word in text for word in ["mascot", "bomber", "panther", "crusader", "lancer"]):
        return "mascot"
    if any(word in text for word in ["history", "founded", "oldest"]):
        return "history"
    if any(word in text for word in ["academics", "school"]):
        return "school"
    if any(word in text for word in ["conference", "gcl"]):
        return "conference"
    if any(word in text for word in ["championship", "titles"]):
        return "state_championships"
    return None

# ----------------------------
# School detection
# ----------------------------
def detect_school(text):
    for phrase, key in ALIASES.items():
        if phrase in text:
            return key
    return None

# ----------------------------
# Chat loop
# ----------------------------
print("GCL South Bot ready. Ask about schools, sports, or conferences. (type 'quit' to exit)\n")

while True:
    user = input("You: ").lower()
    if user == "quit":
        break

    school = detect_school(user)
    topic = detect_topic(user)

    if school:
        last_school = school
    if topic:
        last_topic = topic

    # Follow-up handling
    if not school and last_school:
        school = last_school
    if not topic and last_topic:
        topic = last_topic

    if not school:
        print("Bot: Which school are you asking about?")
        continue

    if school not in knowledge:
        print("Bot: I don’t have data for that yet.")
        continue

    # Try topic-based answer
    if topic and topic in knowledge[school]:
        facts = knowledge[school][topic]
        print("Bot:", random.choice(facts))
    else:
        # Fallback: summarize
        all_facts = []
        for facts in knowledge[school].values():
            all_facts.extend(facts)

        print("Bot:", random.choice(all_facts))
