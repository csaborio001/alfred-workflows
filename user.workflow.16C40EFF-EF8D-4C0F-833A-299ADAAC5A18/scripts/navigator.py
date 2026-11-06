"""Cached, dependency-free Apple Mail mailbox navigator."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unicodedata

BUNDLE = 'org.csaborio.alfred.mail-navigator'
HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get('alfred_workflow_cache', Path.home() / 'Library/Caches' / BUNDLE))
DATA = Path(os.environ.get('alfred_workflow_data', Path.home() / 'Library/Application Support/Alfred/Workflow Data' / BUNDLE))
TTL = 900

def read(path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as stream:
            temporary = stream.name
            json.dump(value, stream, ensure_ascii=False)
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)

def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if not unicodedata.combining(c))

def subsequence(needle, haystack):
    chars = iter(haystack)
    return all(any(c == x for x in chars) for c in needle)

def rank(row, query):
    name = normalize(row['name'])
    aliases = {'inbox':'inbox incoming', 'sent mail':'sent outgoing', 'sent messages':'sent outgoing',
               'spam':'spam junk', 'deleted messages':'trash deleted', 'all mail':'archive all mail'}
    text = normalize(row['account']+' '+row['path']+' '+aliases.get(name, ''))
    query = normalize(query.strip())
    if not query:
        return 0
    if query == name:
        return 0
    if name.startswith(query):
        return 1
    if all(token in text for token in query.split()):
        return 2
    if all(subsequence(token, text) for token in query.split()):
        return 3
    return None

def automation(script, *args, javascript=False, timeout=30):
    command = ['/usr/bin/osascript'] + (['-l','JavaScript'] if javascript else []) + [str(HERE/script)] + list(args)
    result = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        error = result.stderr.strip()
        if '-1743' in error:
            raise RuntimeError('Allow Alfred to control Mail in System Settings → Privacy & Security → Automation, then refresh.')
        raise RuntimeError(error or 'Mail automation failed. Open Mail and refresh mailbox data.')
    return result.stdout.strip()

def refresh():
    CACHE.mkdir(parents=True, exist_ok=True)
    with (CACHE/'refresh.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        write(CACHE/'status.json', {'running':True,'started':time.time()})
        try:
            data = json.loads(automation('discover.js', javascript=True, timeout=60))
            for row in data['mailboxes']:
                row['id'] = hashlib.sha256(json.dumps([row['kind'],row['account_id'],row['path']]).encode()).hexdigest()[:24]
            data['updated'] = time.time()
            write(CACHE/'mailboxes.json', data)
            write(CACHE/'status.json', {'running':False,'error':'','warnings':data.get('warnings',[])})
        except Exception as error:
            write(CACHE/'status.json', {'running':False,'error':str(error),'failed':time.time()})

def spawn_refresh():
    subprocess.Popen([sys.executable, '-B', str(HERE/'navigator.py'), 'refresh'],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)

def command_item(title, action, subtitle):
    return {'title':title,'subtitle':subtitle,'arg':json.dumps({'action':action}), 'valid':True}

def listing(query):
    cache = read(CACHE/'mailboxes.json', {})
    status = read(CACHE/'status.json', {})
    history = read(DATA/'history.json', {})
    running = status.get('running',False) and time.time()-status.get('started',0)<70
    stale = time.time()-cache.get('updated',0)>TTL
    if stale and not running and time.time()-status.get('failed',0)>60:
        spawn_refresh()
        running = True
    items = []
    if query.startswith(':'):
        commands = [command_item('Refresh mailboxes', 'refresh', 'Discover accounts and mailbox changes again'),
                    command_item('Clear mailbox history', 'clear', 'Reset recent and frequent mailbox ranking')]
        items = [item for item in commands if query[1:].casefold() in item['title'].casefold()]
    else:
        scored=[]
        for row in cache.get('mailboxes',[]):
            score=rank(row,query)
            if score is not None:
                usage=history.get(row['id'],{})
                favourite = 0 if row['kind']=='unified' else 1
                scored.append((score,-usage.get('last',0),-usage.get('count',0),favourite if not query else 0,len(row['name']) if query else 0,row['name'].casefold(),row['account'],row))
        scored.sort(key=lambda entry:entry[:-1])
        for *_,row in scored:
            path=row['account']+' → '+(row['name'] if row['kind']=='unified' else row['path'].replace('/',' → '))
            items.append({'uid':row['id'],'title':row['name'], 'subtitle':path,
                          'arg':json.dumps({'action':'open','id':row['id']}),
                          'match':row['name']+' '+row['account']+' '+row['path'],
                          'autocomplete':row['name'], 'valid':True,
                          'mods':{'cmd':{'arg':path,'subtitle':'Copy '+path}},
                          'text':{'copy':path}})
        if not items:
            items.append({'title':'Discovering mailboxes…' if running else 'No matching mailboxes',
                          'subtitle':'Try an account name or type :refresh to refresh.','valid':False})
    error=read(CACHE/'action-error.json',{}).get('error') or status.get('error')
    if error:
        items.insert(0,command_item('Mail Navigator needs attention','refresh',error))
    for warning in status.get('warnings',[]):
        items.append(command_item('Some mailboxes could not be discovered','refresh',warning))
    if not query:
        items.append(command_item('Refresh mailboxes','refresh','Also available with mail :refresh · mail :clear clears history'))
    result={'items':items,'skipknowledge':True}
    if running:result['rerun']=0.5
    return result

def action(payload):
    request=json.loads(payload)
    if request['action']=='clear':
        write(DATA/'history.json',{})
        show('')
        return
    if request['action']=='refresh':
        write(CACHE/'action-error.json',{})
        spawn_refresh()
        show('')
        return
    cache=read(CACHE/'mailboxes.json',{})
    row=next((r for r in cache.get('mailboxes',[]) if r['id']==request.get('id')),None)
    try:
        if row is None:raise RuntimeError('Mailbox is no longer cached. Refresh and select it again.')
        automation('open.applescript',row['account_id'],row['path'],row['kind'])
        history=read(DATA/'history.json',{})
        usage=history.get(row['id'],{})
        history[row['id']]={'last':time.time(),'count':usage.get('count',0)+1}
        write(DATA/'history.json',history)
        write(CACHE/'action-error.json',{})
    except Exception as error:
        write(CACHE/'action-error.json',{'error':str(error)})
        show('')

def show(query):
    # Use argv, never interpolate mailbox text into executable AppleScript.
    script='on run argv\ntell application "Alfred 5" to search ("mail " & item 1 of argv)\nend run'
    subprocess.run(['/usr/bin/osascript','-e',script,query],capture_output=True,timeout=10)

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'list'
    if mode=='list':print(json.dumps(listing(' '.join(sys.argv[2:])),ensure_ascii=False))
    elif mode=='refresh':refresh()
    elif mode=='action':action(sys.argv[2])
    elif mode=='show':show('')
