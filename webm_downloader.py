import json
import requests

def req_page(link):
    r = requests.get(link)
    page = r.text
    return page

def load_n_save(link, file_name):
    r = requests.get(link)
    print('Download', file_name)
    with open(file_name, 'wb') as data:
        data.write(r.content)
    data.close()

def get_posts(page):
    js = json.loads(page)
    posts = js['threads'][0]['posts']
    return posts

def find_files(posts):
    i = 0
    files = {}
    files['names'] = {0: str}
    files['paths'] = {0: str}
    for post in posts:
        if 'files' in post:
            for attach in post['files']:
                files['names'][i] = attach['displayname']
                files['paths'][i] = attach['path']
                i += 1
    return files

def find_threads(board):
    thread_nums = []
    first_page = req_page('https://2ch.hk/'+board+'/1.json')
    js_first_page = json.loads(first_page)
    pages_count = js_first_page['pages']
    pages_count.remove(1)
    pages_count.remove(2)
    c = 1
    for page in pages_count:
        a = 0
        board_text = req_page('https://2ch.hk/'+board+'/'+str(c)+'.json')
        board_js = json.loads(board_text)
        for tr in board_js['threads']:
            thread_nums.append(board_js['threads'][a]['thread_num'])
            a += 1
        c += 1
    print('Founded ', len(thread_nums), 'threads')
    return thread_nums
def main():
    #Доска с которой надо скачивать webm'ки
    board = 'b'
    threads = find_threads(board)
    for num in threads:
        print('Open thread ' + num)
        try:
            posts = get_posts(req_page('https://2ch.hk/'+board+'/res/'+num+'.json'))
            files = find_files(posts)
            for name in files['names']:
                if files['names'][name][-4:] == 'webm':
                    load_n_save('https://2ch.hk' + files['paths'][name], './webm/' + files['names'][name])
        except KeyboardInterrupt:
            print('Stopped by user')
            break
            exit(0)
if __name__ == '__main__':
    main()
