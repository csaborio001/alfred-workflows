function run() {
 var m=Application('Mail'), rows=[], seen={}, failures=[];
 function pathOf(b) {
  var parts=[b.name()], current=b;
  for(var i=0;i<50;i++) {
   try {current=current.container();var name=current.name();if(!name)break;parts.unshift(name);} catch(e){break;}
  }
  return parts.join('/');
 }
 function collect(boxes, account, accountId) {
  boxes.forEach(function(b){
   var path=pathOf(b);
   if(accountId && path.indexOf(account+'/')===0)path=path.slice(account.length+1);
   var key=accountId+'|'+path;
   if(seen[key])return;seen[key]=true;
   rows.push({account:account,account_id:accountId,path:path,name:b.name(),kind:'mailbox'});
   collect(b.mailboxes(),account,accountId);
  });
 }
 m.accounts().forEach(function(a){try{collect(a.mailboxes(),a.name(),a.id());}catch(e){failures.push(a.name()+': '+e);}});
 try{collect(m.mailboxes(),'On My Mac','');}catch(e){failures.push('Local mailboxes: '+e);}
 ['inbox','sentMailbox','draftsMailbox','junkMailbox','trashMailbox'].forEach(function(key){
  try{var b=m[key]();b.name();rows.push({account:'All Accounts',account_id:'',path:key,name:({inbox:'Inbox',sentMailbox:'Sent',draftsMailbox:'Drafts',junkMailbox:'Junk',trashMailbox:'Trash'})[key],kind:'unified'});}catch(e){}
 });
 return JSON.stringify({mailboxes:rows,warnings:failures});
}
