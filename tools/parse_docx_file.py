import os
from io import BytesIO

from docx import Document

from data.answer_questions import AnswerQuestion
from data.db_session import create_session
from data.questions import Question
from data.theme_questions import ThemeQuestions
from data.training_class import TrainingClass

bukvs = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
         'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
         'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
         'я': 'ya', '-': '_'}


def translate_rus_to_eng(word, replase_space='_'):
    return ''.join([bukvs.get(x.lower(), x) for x in word.replace(' ', replase_space)])


def save_photo(part_rels, translate_theme, train_class):
    work_dir = 'tools/static/img/questions'
    if not os.path.isdir(work_dir):
        os.makedirs(work_dir)
    save_dir = f'{work_dir}/{train_class}'
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    count_img = 0
    for rel in part_rels:
        rel = part_rels[rel]
        if "image" in rel.target_ref:
            img_data = rel.target_part.blob
            img_name = rel.target_ref.split('/')[-1].split('.')
            with open(f'{save_dir}/{translate_theme}_{count_img}.{img_name[1]}', 'wb') as f:
                f.write(img_data)
            count_img += 1
    return count_img - 1


def create_new_theme(file, train_class):
    name = file.data.filename
    with create_session() as session:
        try:
            theme_id = session.query(ThemeQuestions).all()[-1].id
        except IndexError:
            theme_id = 0

        try:
            question_id = session.query(Question).all()[-1].id
        except IndexError:
            question_id = 0
        class_id = session.query(TrainingClass).filter(TrainingClass.name == train_class).first().id

        doc = Document(BytesIO(file.data.read()))
        tr = translate_rus_to_eng(name).split('.')[0]

        count_img = save_photo(doc.part._rels, tr, train_class)

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
                theme = ThemeQuestions(id=theme_id, class_id=class_id, name=x[1:].strip())
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
                que.question = que.question + f'\n/static/img/questions/{train_class}/{tr}_{min(img_ind, count_img)}.png'

        session.commit()
