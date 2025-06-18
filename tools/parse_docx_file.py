import os

from docx import Document

from data.answer_questions import AnswerQuestion
from data.db_session import create_session
from data.questions import Question
from data.theme_questions import ThemeQuestions

CLASS_ID = 3
CLASS = 10
NAMES_TESTS = sorted(os.listdir(os.path.join('../', f'tests_{CLASS}')))[1:]

bukvs = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
         'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
         'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
         'я': 'ya', '-': '_'}


def translate_rus_to_eng(word, replase_space='_'):
    return ''.join([bukvs.get(x.lower(), x) for x in word.replace(' ', replase_space)])


def save_photo(part_rels, translate_theme):
    for rel in part_rels:
        rel = part_rels[rel]
        if "image" in rel.target_ref:
            img_data = rel.target_part.blob
            img_name = rel.target_ref.split('/')[-1].split('.')
            with open(f'../static/img/questions/{CLASS}/{translate_theme}_{img_name[0][5:]}.{img_name[1]}', 'wb') as f:
                f.write(img_data)


def create_new_theme():
    with create_session() as session:
        theme_id = session.query(ThemeQuestions).all()[-1].id
        question_id = session.query(Question).all()[-1].id
        for name in NAMES_TESTS:
            doc = Document(os.path.join('../', f'tests_{CLASS}/{name}'))
            tr = translate_rus_to_eng(name).split('.')[0]

            lines = []
            for x in [x.text for x in doc.paragraphs]:
                lines += x.splitlines()

            for x in lines:
                x = x.strip()
                if not x:
                    continue

                if x[0] == '!':
                    img_ind = 0
                    theme_id += 1
                    theme = ThemeQuestions(id=theme_id, class_id=CLASS_ID, name=x[1:].strip())
                    session.add(theme)
                elif x[0] == '?':
                    question_id += 1
                    question = Question(id=question_id, question=x[1:].strip(), theme_id=theme_id)
                    session.add(question)
                elif x[0] == '@':
                    question = AnswerQuestion(answer=x[1:].strip(), question_id=question_id)
                    session.add(question)
                elif x[0:3] == 'img':
                    img_ind += 1
                    que = session.get(Question, question_id)
                    que.question = que.question + f'\n/static/img/questions/{CLASS}/{tr}_{img_ind}.png'

            save_photo(doc.part._rels, tr)

        session.commit()
