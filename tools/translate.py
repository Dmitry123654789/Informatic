import os

from docx import Document

from data.answer_questions import AnswerQuestion
from data.db_session import global_init, create_session
from data.questions import Question
from data.theme_questions import ThemeQuestions

bukvs = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
         'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
         'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
         'я': 'ya', '-': '_'}


def translate_rus_to_eng(word, replase_space='_'):
    return ''.join([bukvs.get(x.lower(), x) for x in word.replace(' ', replase_space)])

global_init('../db/informatic_questions.db')

CLASS_ID = 1
CLASS = 9
NAMES_TESTS = sorted(os.listdir(os.path.join('../', f'tests_{CLASS}')))

with create_session() as session:
    theme_id = 0
    question_id = 0
    for name in NAMES_TESTS:
        doc = Document(os.path.join('../', f'tests_{CLASS}/{name}'))

        lines = []
        for x in [x.text for x in doc.paragraphs]:
            lines += x.splitlines()

        for x in lines:
            x = x.strip()
            if not x:
                continue

            tr = translate_rus_to_eng(name).split('.')[0]
            if x[0] == '!':
                theme_id += 1
                theme = ThemeQuestions(id=theme_id, class_id=CLASS_ID, name=x[1:].strip())
                session.add(theme)
                session.commit()
            elif x[0] == '?':
                img_ind = 0
                question_id += 1
                question = Question(id=question_id, question=x[1:].strip(), theme_id=theme_id)
                session.add(question)
                session.commit()
            elif x[0] == '@':
                question = AnswerQuestion(answer=x[1:].strip(), question_id=question_id)
                session.add(question)
                session.commit()
            elif x[0:3] == 'img':
                img_ind += 1
                que = session.get(Question, question_id)
                que.question = que.question + f'\nstatic/img/questions/{CLASS}/{tr}_{img_ind}.png'
                session.commit()


        for rel in doc.part._rels:
            rel = doc.part._rels[rel]
            if "image" in rel.target_ref:
                img_data = rel.target_part.blob
                img_name = rel.target_ref.split('/')[-1].split('.')
                with open(f'../static/img/questions/{CLASS}/{tr}_{img_name[0][5:]}.{img_name[1]}', 'wb') as f:
                    f.write(img_data)