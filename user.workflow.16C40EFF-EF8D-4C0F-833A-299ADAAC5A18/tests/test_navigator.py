import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
w=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('nav',w/'scripts/navigator.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
class Tests(unittest.TestCase):
 def test_matching(self):
  row={'name':'Archive','account':'Wórk','path':'Projects/Archive'}
  self.assertEqual(n.rank(row,'archive'),0);self.assertEqual(n.rank(row,'arch'),1)
  self.assertEqual(n.rank(row,'work arch'),2);self.assertEqual(n.rank(row,'wrk arc'),3)
  self.assertIsNone(n.rank(row,'zzzz'))
 def test_cache_history_errors(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(n,'CACHE',Path(tmp)/'cache'),patch.object(n,'DATA',Path(tmp)/'data'),patch.object(n,'spawn_refresh') as spawn,patch.object(n,'show'):
   rows=[dict(id=str(i),name='Sent',account=a,account_id=a,path='Sent',kind='mailbox') for i,a in enumerate(['A','B'])]
   n.write(n.CACHE/'mailboxes.json',{'updated':n.time.time(),'mailboxes':rows})
   n.write(n.DATA/'history.json',{'1':{'last':10,'count':1}})
   self.assertEqual(json.loads(n.listing('sent')['items'][0]['arg'])['id'],'1');spawn.assert_not_called()
   with patch.object(n,'automation',side_effect=RuntimeError('Permission denied')):
    n.action(json.dumps({'action':'open','id':'0'}))
   self.assertIn('Permission denied',n.listing('sent')['items'][0]['subtitle'])
   n.action(json.dumps({'action':'clear'}));self.assertEqual(n.read(n.DATA/'history.json',None),{})
   (n.CACHE/'mailboxes.json').write_text('broken');n.listing('');spawn.assert_called()
 def test_graph(self):
  import plistlib
  d=plistlib.loads((w/'info.plist').read_bytes());ids={o['uid'] for o in d['objects']}
  for source,edges in d['connections'].items():
   self.assertIn(source,ids)
   for edge in edges:self.assertIn(edge['destinationuid'],ids)
  self.assertEqual(d['connections']['mail-list'][1]['modifiers'],1048576)
if __name__=='__main__':unittest.main()
