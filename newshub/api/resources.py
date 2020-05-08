from flask_restful import Resource, reqparse
from flask import jsonify, request
import re, datetime, pytz, urllib
# from .models import PageModel
from .db import mon_db
page_con = mon_db.db.pages
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

def page_args(page):
    if page == None:
        page = 1
    return page
def cat_arg(page,cat):
    if page == None:
        page = 1
    return {'page':page,'cat':cat}

def find_arg(page,find):
    if page == None:
        page = 1
    return {'page':page,'find':find}

class Page(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',
                        type=int,
                        required=False,
                        help="Page Num"
                        )
        data = parser.parse_args()
        page = page_args(**data)
        date = datetime.datetime.now(pytz.timezone('Asia/Calcutta')) + datetime.timedelta(days = 0)
        date = date.strftime('%B %d, %Y')
        filter={'post_time': re.compile(date)}
        sort=list({'_id': -1}.items())
        skip = (page-1)*20
        limit=20
        ps = []
        # page_con = mon_db.db.pages
        if page_con:
            tot = page_con.count(filter=None)
            for i in page_con.find(skip=skip,limit=limit,sort=sort,filter=None):
                # print(i)
                ps.append(jj(i))
            prv_link = '/api/latest_news?page=' + str(page - 1)
            nxt_link = '/api/latest_news?page=' + str(page + 1)
            return {'tot':tot,'pagenum':page,'prv_link':prv_link,'nxt_link':nxt_link,'out':ps}
        return {'message': "Something's wrong i can feel it" }, 666

class Page_by_cat(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cat',
                        type=str,
                        required=True,
                        help="Page Num"
                        )
        parser.add_argument('page',
                        type=int,
                        required=False,
                        help="Page Num"
                        )
        data = parser.parse_args()
        cat_args = cat_arg(**data)
        page = cat_args['page']
        cat = cat_args['cat']
        date = datetime.datetime.now(pytz.timezone('Asia/Calcutta')) + datetime.timedelta(days = 0)
        date = date.strftime('%B %d, %Y')
        filter={'section_name':'\n'+cat+'\n'}
        sort=list({'_id': -1}.items())
        skip = (page-1)*20
        limit=20
        ps = []
        # page_con = mon_db.db.pages
        if page_con:
            tot = page_con.count(filter=filter)
            for i in page_con.find(skip=skip,limit=limit,sort=sort,filter=filter):
                # print(i)
                ps.append(jj(i))
            prv_link = '/api/news?cat='+urllib.parse.quote(cat)+'&page=' + str(page - 1)
            nxt_link = '/api/news?cat='+urllib.parse.quote(cat)+'&page=' + str(page + 1)
            return {'tot':tot,'pagenum':page,'prv_link':prv_link,'nxt_link':nxt_link,'out':ps}
        return {'message': "Something's wrong i can feel it" }, 404

class Page_search(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('find',
                        type=str,
                        required=True,
                        help="Page Num"
                        )
        parser.add_argument('page',
                        type=int,
                        required=False,
                        help="Page Num"
                        )
        data = parser.parse_args()
        find_args = find_arg(**data)
        page = find_args['page']
        find = find_args['find']
        date = datetime.datetime.now(pytz.timezone('Asia/Calcutta')) + datetime.timedelta(days = 0)
        date = date.strftime('%B %d, %Y')
        filter={'title':re.compile(find,re.IGNORECASE)}
        sort=list({'_id': -1}.items())
        skip = (page-1)*20
        limit=20
        ps = []
        # page_con = db.db.pages
        if page_con:
            tot = page_con.count(filter=filter)
            for i in page_con.find(skip=skip,limit=limit,sort=sort,filter=filter):
                # print(i)
                ps.append(jj(i))
            prv_link = '/api/news?find='+urllib.parse.quote(find)+'&page=' + str(page - 1)
            nxt_link = '/api/news?find='+urllib.parse.quote(find)+'&page=' + str(page + 1)
            return {'tot':tot,'pagenum':page,'search_key':find,'prv_link':prv_link,'nxt_link':nxt_link,'out':ps}
        return {'message': "Something's wrong i can feel it" }, 404
