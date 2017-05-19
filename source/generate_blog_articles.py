import os
import shutil
import hashlib
import json
from root import global_value
from datetime import datetime
import time


def generate():
    path = global_value.WORK_PATH
    print path
    articles_path = path + 'articles'
    resource_path = path + 'resource'
    shutil.rmtree(articles_path, ignore_errors = True)
    shutil.copytree(resource_path, articles_path)
    os.chdir(articles_path)

    arthicles = []
    for lists in os.listdir('./'):
        if lists == '.DS_Store':
            continue
        article_dic = {}
        title = ""
        _id = ""
        time = ""
        tag = []
        f = open(lists, 'r')
        d = open(lists + '_new', 'w')
        first_Title = False
        for line in f:
            fields = line.split(" ", 1)
            if fields[0] == "#" and first_Title is False:
                first_Title = True
                d.write(line)
                title = fields[1]
                _id = hashlib.md5(fields[1]).hexdigest()
            elif fields[0] == "[date]":
                time = fields[1].strip('\n')
            elif fields[0] == "[tag]":
                tag = line.split(" ")[1:]

                def remove_n(x):
                    return x.strip('\n')
                tag = map(remove_n, tag)
            else:
                d.write(line)

        d.close()
        f.close()
        old_file = os.path.join(articles_path, lists + '_new')
        new_file = os.path.join(articles_path, _id + '.md')
        os.rename(old_file, new_file)
        os.remove(os.path.join(articles_path, lists))

        article_dic['id'] = _id
        article_dic['title'] = title
        article_dic['tags'] = tag
        article_dic['time'] = time
        if not title or not _id:
            continue
        arthicles.append(article_dic)

    arthicles = sorted(arthicles, key=sortByDate, reverse=True)
    ret = json.dumps(arthicles, indent=1)

    json_file = open('./list.json', 'w')
    json_file.writelines(ret)
    json_file.close()


# sort by date
def sortByDate(item):
    datetime_obj = datetime.strptime(item['time'], "%Y-%m-%d %H:%M:%S")
    ret = time.mktime(datetime_obj.timetuple())
    return ret



