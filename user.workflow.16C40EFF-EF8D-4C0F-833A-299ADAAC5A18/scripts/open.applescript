on run argv
 set accountID to item 1 of argv
 set mailboxPath to item 2 of argv
 set mailboxKind to item 3 of argv
 tell application "Mail"
  with timeout of 20 seconds
   if mailboxKind is "unified" then
    if mailboxPath is "inbox" then
     set targetBox to inbox
    else if mailboxPath is "sentMailbox" then
     set targetBox to sent mailbox
    else if mailboxPath is "draftsMailbox" then
     set targetBox to drafts mailbox
    else if mailboxPath is "junkMailbox" then
     set targetBox to junk mailbox
    else if mailboxPath is "trashMailbox" then
     set targetBox to trash mailbox
    else
     error "Unsupported unified mailbox"
    end if
   else if accountID is "" then
    set targetBox to mailbox mailboxPath
   else
    set targetAccount to first account whose id is accountID
    set targetBox to mailbox mailboxPath of targetAccount
   end if
   set targetName to name of targetBox
   activate
   if (count of message viewers) is 0 then make new message viewer
   set viewer to message viewer 1
   set selected messages of viewer to {}
   set selected mailboxes of viewer to {targetBox}
   repeat 80 times
    set currentBoxes to selected mailboxes of viewer
    if (count of currentBoxes) is 1 then
     if item 1 of currentBoxes is targetBox then
      set selected messages of viewer to {}
      return "OK"
     end if
    end if
    delay 0.1
   end repeat
   error "Mail did not confirm the requested mailbox selection. Refresh mailbox data and retry."
  end timeout
 end tell
end run
