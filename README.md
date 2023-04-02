D-Link Dir-2150 sql injection 

This router has usb media support. 

When USB storage is in use, it is also possible to enable DLNA service.

There is a sql injection vulnerability in minidlnad (it uses sqlite3).

SetBookmark handler:
```
void FUN_0040e1d4(int param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined auStack96 [76];
  
  ParseNameValue(*(int *)(param_1 + 0x20) + *(int *)(param_1 + 0x2c),*(undefined4 *)(param_1 + 0x28)
                 ,auStack96,0);
  iVar1 = GetValueFromNameValueList(auStack96,"ObjectID");
  iVar2 = GetValueFromNameValueList(auStack96,"PosSecond");
  if ((iVar1 == 0) || (iVar2 == 0)) {
    FUN_0040df44(param_1,0x192,"Invalid Args");
  }
  else {
    iVar3 = sql_exec(db,
                     "INSERT OR REPLACE into BOOKMARKS VALUES ((select DETAIL_ID from OBJECTS where OBJECT_ID = \'%q\'), %q)"
                     ,iVar1,iVar2);
    if (iVar3 != 0) {
      log_err(3,5,"upnpsoap.c",0x700,"Error setting bookmark %s on ObjectID=\'%s\'\n",iVar2,iVar1);
    }
    FUN_0040d1e0(param_1,
                 "<u:X_SetBookmarkResponse xmlns:u=\"urn:schemas-upnp-org:service:ContentDirectory:1\"></u:X_SetBookmarkResponse>"
                 ,0x6d);
  }
  ClearNameValueList(auStack96);
  return;
}
```

Second argument (iVar2) is not escaped (%q without quotes).

```
$ cat /VERSION 
NAME:           DIR_2150_MT7621D
VERSION:        4.0.0
DATAMODEL:      2.40.0
SYSBUILDTIME:   Fri Jun  5 18:21:26 MSK 2020
VENDOR:         D-Link Russia
BUGS:           <support@dlink.ru>
SUMMARY:        Root filesystem image for DIR_2150_MT7621D
```

How to repoduce:
```
1) unsert usb media and enable DLNA
2) run t1.py, file /tmp/t2.db should be created on a device

$ ls -al /tmp/t2.db
-rw-r-----    1 root     system        8192 /tmp/t2.db

```
