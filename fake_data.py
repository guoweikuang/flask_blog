# -*- coding: utf-8 -*-
import random
import datetime
from uuid import uuid4

from models import User, Post, Tag, db


user = User(id=str(uuid4()), username='guoweikuang1', password='gwk2014081029')
db.session.add(user)
db.session.commit()

user = db.session.query(User).first()
tag_one = Tag(name=u'机器学习')
tag_one.id = str(uuid4())
tag_two = Tag(name=u"爬虫")
tag_two.id = str(uuid4())
tag_three = Tag(name=u'Vim')
tag_three.id = str(uuid4())
tag_four = Tag(name=u'MySQL')
tag_four.id = str(uuid4())
tag_list = [tag_one, tag_two, tag_three, tag_four]

s = 'Hello, World! guoweikuang'

for i in range(1, 100):
    new_post = Post(title='Post ' + str(i))
    new_post.id = str(uuid4())
    new_post.user = user
    new_post.create_time = datetime.datetime.now()
    new_post.text = s
    new_post.tags = random.sample(tag_list, random.randint(1, 3))
    db.session.add(new_post)

db.session.commit()
    
