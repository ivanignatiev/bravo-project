import logging
import sys
sys.path.append("./src/bravo-core")

from survey import Survey 

logging.basicConfig(level=logging.DEBUG)

# def test_user_questions():
s = Survey("ABC Inc.", "Technology")
print(s.get_user_questions())