from flask_restful import Resource
from flask import jsonify, request
import re, datetime, pytz
# from .models import PageModel
from .db import db

def jj(obj):
    ret = {}
    ret["_id"] = str(obj['_id'])
    ret['article_id'] = obj['article_id']
    ret['section_name'] = obj['section_name']
    ret['title'] = obj['title']
    ret['author_name'] = obj['author_name']
    ret['place'] = obj['place']
    ret['post_time'] = obj['post_time']
    ret['img_name'] = obj['img_name']
    ret['img_url'] = obj['img_url']
    ret['description'] = obj['description']
    ret['content'] = obj['content']
    # ret[''] = obj['']
    return ret

class Page(Resource):

    def get(self):
        page = int(request.args['page'])
        date = datetime.datetime.now(pytz.timezone('Asia/Calcutta')) + datetime.timedelta(days = 0)
        date = date.strftime('%B %d, %Y')
        filter={'post_time': re.compile(date)}
        sort=list({'_id': -1}.items())
        skip = (page-1)*20
        limit=20
        ps = []
        page_con = db.db.page_data
        if page_con:
            for i in page_con.find(skip=skip,limit=limit,sort=sort):
                # print(i)
                ps.append(jj(i))
            prv_link = '/api/latest_news?page=' + str(page - 1)
            nxt_link = '/api/latest_news?page=' + str(page + 1)
            return {'prv_link':prv_link,'nxt_link':nxt_link,'out':ps}
        return {'message': "Something's wrong i can feel it" }, 404
