class Entry():
    "Class for Entries"
    def __init__(self, id, concept, mood_id, date, entry = ""):
        self.id = id
        self.concept = concept
        self.mood_id = mood_id
        self.date = date
        self.entry = entry
