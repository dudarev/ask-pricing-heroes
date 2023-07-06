from pathlib import Path

from cache import Cache

GOOD_QUESTIONS_FILE = Path(__file__).parent.parent / "data/cache/good_questions.json"

cache = Cache(GOOD_QUESTIONS_FILE)

GOOD_QUESTIONS = [k for k in cache.keys()]
