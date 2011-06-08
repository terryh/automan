#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: terryh.tp at gmail.com

# wxPython
import wx
from wx.lib.wordwrap import wordwrap
from wxobject import MyFrame,MyS,MyA
# patch for wxFormBuilder, fake wxICON to nothing but return content
wx.ICON = lambda a: a

import cPickle as pickle
import os
import sys
import types
import logging
import threading
import re

import calendar, datetime, time

from shutil import copyfile

import wx.lib.activex
# only work on windows 

import comtypes.client as cc
import comtypes

app_realpath = os.path.realpath(sys.argv[0])
app_dir = os.path.dirname(app_realpath)

__version__ = 'V0.3 BETA'
__DEAD__ = u"201312"

re_dead = re.compile("[0-9]+")
def loadpickle(datafile=""):
    content = {}
    if datafile:
        try:
            fp = file(datafile)
            content = fp.read()
            fp.close()
        except:
            fp = open(datafile,"w")
            fp.close()
        if content:
            return pickle.loads(content)
    return content

def writepickle(datafile="",newvalue={}):
    # do a db update like interface
    if datafile and newvalue:
        dd = loadpickle(datafile)
        if not dd:
            dd = {}

        if type(newvalue)==types.DictType:
            for k in newvalue.keys():
                dd[k]=newvalue[k]

        fp = open(datafile,"w")
        pickle.dump(dd,fp)
        fp.close()



def gethts():
    hts = ""
    try:
        dirname = app_dir
        if os.path.isfile(dirname+"/"+"HTSAPITradeClient.dll"):
            hts = comtypes.WinDLL('HTSAPITradeClient.dll')
            
        elif os.path.isfile("C:/JihSun/HTS2/Dll/HTSAPITradeClient.dll"):
            target = dirname+"/"+"HTSAPITradeClient.dll"
            copyfile("C:/JihSun/HTS2/Dll/HTSAPITradeClient.dll",target)
            hts = comtypes.WinDLL('HTSAPITradeClient.dll')

    except:
        pass
    return hts

                                 
            

def getcon():
    progID=""
    try:  
        # try version 1 OCX api
        cc.GetModule( ('{8E4A0C4A-9B62-41D7-B99A-2B48F81D744A}', 1, 0) )
        progID = 'SGTPOCXAPI.SgtpOcxApiCtrl.1'
    except WindowsError:
        # try version 2 OCX api
        cc.GetModule( ('{D10B2D9E-71D1-49AC-8919-FF5E122E2172}', 2, 0) )
        progID = 'SGTPOCXAPI.SgtpOcxApiCtrl.2'
    except:
        pass    
    return progID

# ActiveX control for SgtpOcxApiCtrl
class AxWindow(wx.lib.activex.ActiveXCtrl):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name=''):
        wx.lib.activex.ActiveXCtrl.__init__(self, parent, getcon(),
                                            id, pos, size, style, name)
#------------------------------------------
# FIXME need refactor
class Worker(threading.Thread):
    def __init__(self, win="", sname=""):
        """initial for signal module"""
        self.win = win
        self.login = win.login
        self.running = False
        self.interval = 0.1
        self.pos = 0
        self.hts = False
        self.con = False 
        if sname:
            self.loginfo = win.loginfo
            self.sname = sname
            self.verify()
            self.dellock()
        threading.Thread.__init__(self)
        self.setDaemon(1)

    def verify(self):
        if hasattr(self,'win') and self.win.data.has_key('sctrl'):
            for index in range(len(self.win.data['sctrl'])):
                i = self.win.data['sctrl'][index]
                if unicode(self.sname) == unicode(i[0]):
                    self.running = True
                    self.signalf = i[1]
                    fn = os.path.splitext(self.signalf)[0]
                    self.lockf = fn+".lock"
                    self.colindex = index
                    break
            if self.win.hts:
                self.hts = True
            if self.win.login:
                self.con = True
    
    def Start(self):
        self.running = True

    def Stop(self):
        self.running = False
        self.dellock()

    def updateui(self):
        if self.running:
            #print self.pos,type(self.pos)
            if self.pos == 1:
                self.win.sctrl.SetItemBackgroundColour(self.colindex, wx.Color(255,136,136))
            elif self.pos == -1 :
                self.win.sctrl.SetItemBackgroundColour(self.colindex, wx.Color(136,255,136))
            else: 
                self.win.sctrl.SetItemBackgroundColour(self.colindex, wx.Color(229,229,229))
            
            self.win.sctrl.SetStringItem(self.colindex, 1, unicode(self.pos))
            

            for i in range(len(self.win.data['actrl'])):
                # structure [aname,abroker,acompany,account,aproduct,aym,asignal,
                #            anumber,aintraday,amarket,acurrency]
                item = self.win.data['actrl'][i]
                
                if len(item)>10 and unicode(item[6]) == unicode(self.sname):
                    number = int(item[7])
                    
                    if self.pos*number > 0:
                        self.win.actrl.SetStringItem(i, 7, unicode(self.pos*number))
                        self.win.actrl.SetItemBackgroundColour(i, wx.Color(255,136,136))
                    elif self.pos*number < 0:
                        self.win.actrl.SetStringItem(i, 7, unicode(self.pos*number))
                        self.win.actrl.SetItemBackgroundColour(i, wx.Color(136,255,136))
                    else:
                        self.win.actrl.SetStringItem(i, 7, u"0")
                        self.win.actrl.SetItemBackgroundColour(i, wx.Color(229,229,229))
                        

    def dellock(self):
        if self.running and self.lockf:
            try:
                os.remove(self.lockf)
            except:
                pass

    def run(self):
        while self.running:
            time.sleep(self.interval)
            self.checksignal()
            #print self.win.data
        
        self.running = False
    
    def getcurrent():
        today = datetime.date.today()
        
        cd = calendar.Calendar()
        counter = 0
        contractdate = 0
        cdate = ""
        for ww in cd.monthdatescalendar(today.year,today.month):
            if ww[2].month == today.month:
                counter +=1
                if counter == 3:
                    contractdate = ww[2]
                    break
        if today <= contractdate:
            cdate = contractdate.strftime("%Y%m")
        else:
            # make sure to cross one month
            cdate = datetime.date(contractdate.year,contractdate.month,1)+datetime.timedelta(days=40)
            cdate = cdate.strftime("%Y%m")
        return cdate

    getcurrent = staticmethod(getcurrent)
    
    def buyorder(self,price):
        cc = '0|%s|%s|%s|B|NTT|||||%s|%s|%s|A|%s'
        hh = "Market=F,Account=%s-%s,ContractName=%s,ContractDate=%s,OpenCloseAuto=A,BuySell=B,Lots=%d,OrderType=%s,Price=%d,FokIocRod=%s,DayTrade=%s"
        if price:
            # limit price,Rod
            ordertype = "L" # HTS
            fokiocrod = "R" # HTS
            conot = "LMT"   # CON
            confok= "ROD"   # CON
        else:
            # market order, Ioc
            ordertype = "M" # HTS
            fokiocrod = "I" # HTS
            conot = "MKT"   # CON
            confok= "IOC"   # CON

        for i in self.win.data['actrl']:
            if i[7]>0 and i[6]==self.sname:
                # lots > 0
                lots = i[7]
                broker = i[1]
                company = i[2]
                account = i[3]
                cname = i[4]
                if i[5] ==u"0" or i[5]==0 or i[5]=="": 
                    cdate = self.getcurrent()
                else:
                    cdate = i[5]
                
                if i[8]==u"YES":
                    daytrade = u"Y"
                else:
                    daytrade = u"N"
                
                if broker == u"康和" and self.con:
                    orderstring = cc % (daytrade,cname,cdate,conot,price,confok,lots)
                    self.win.con.FutureOrder(company,account,orderstring)
                elif broker == u"日盛" and self.hts:
                    # FIXME HTSOrder do not accept unicode 
                    orderstring = hh % (company,account,cname,cdate,lots,ordertype,price,fokiocrod,daytrade)
                    self.win.hts.HTSOrder(str(orderstring))

    def sellorder(self,price):

        # structure [aname,abroker,acompany,account,aproduct,
        # aym,asignal,anumber,aintraday,amarket,acurrency]
        
        cc = '0|%s|%s|%s|S|NTT|||||%s|%s|%s|A|%s'
        #% (daytrade,cname,cdate,conot,price,confok,lots) 
        hh = "Market=F,Account=%s-%s,ContractName=%s,ContractDate=%s,OpenCloseAuto=A,BuySell=S,Lots=%d,OrderType=%s,Price=%s,FokIocRod=%s,DayTrade=%s"
        #% (company,account,cname,cdate,lots,ordertype,price,fokiocrod,daytrade) 
        if price:
            # limit price,Rod
            ordertype = "L" # HTS
            fokiocrod = "R" # HTS
            conot = "LMT"   # CON
            confok= "ROD"   # CON
        else:
            # market order, Ioc
            ordertype = "M" # HTS
            fokiocrod = "I" # HTS
            conot = "MKT"   # CON
            confok= "IOC"   # CON
        
        for i in self.win.data['actrl']:
            if i[7]>0 and i[6]==self.sname:
                # lots > 0
                lots = i[7]
                broker = i[1]
                company = i[2]
                account = i[3]
                cname = i[4]
                if i[5] ==u"0" or i[5]==0 or i[5]=="": 
                    cdate = self.getcurrent()
                else:
                    cdate = i[5]
                
                if i[8]==u"YES":
                    daytrade = u"Y"
                else:
                    daytrade = u"N"
                
                if broker == u"康和" and self.con:
                    orderstring = cc % (daytrade,cname,cdate,conot,price,confok,lots)
                    self.win.con.FutureOrder(company,account,orderstring)
                elif broker == u"日盛" and self.hts:
                    # FIXME HTSOrder do not accept unicode 
                    orderstring = hh % (company,account,cname,cdate,lots,ordertype,price,fokiocrod,daytrade)
                    self.win.hts.HTSOrder(str(orderstring))

    def checksignal(self):
        """ signal file format
        Date,time,position,price
        price 0 為IOC 市價, 非 0 為 ROD 限價單
        position 1 buy, 0 no contract, -1 sell
        """
        signalf = "" 
        if self.signalf:
            try:
                signalf = file(self.signalf).read().strip()
            except:
                #print "Sorry, No signal file %s" % (self.signalf)
                # no signal file do nothing
                return ""
            try:
                lockf = file(self.lockf).read().strip()
                #print "LOCKF",lockf,not lockf
                if not os.path.isfile(self.lockf):
                    fp = open(self.lockf,"w")
                    #print self.lockf
                    fp.write(signalf)
                    fp.close()
                    lockf = file(self.lockf).read().strip()
            except:
                #print sys.exc_info()
                fp = open(self.lockf,"w")
                #print "No file so touch it",self.lockf
                fp.write(signalf)
                fp.close()
                lockf = file(self.lockf).read().strip()
            if "," in signalf:
                sl = signalf.split(',')
            elif " " in signalf:
                sl = signalf.split(' ')
            
            if "," in lockf:
                ll = lockf.split(',')
            elif " " in lockf:
                ll = lockf.split(' ')

            #print ll 
            try:
                # test number
                sp = int(sl[2])
            except:
                # not correct signal file, wait next run
                return ""
            
            try:
                # test number
                lp = int(ll[2])
            except:
                # not correct signal file, wait next run
                lp = 0

            price = 0 # init val
            try:
                if len(sl)>3:
                    if "." in sl[3]:
                        price = float(sl[3])
                    else:
                        price = int(sl[3])
            except:
                pass
                
            # dump checking
            if price >=0:
                price = price
            else:
                price = 0
            #print sp,lp
            if sp != lp:
                if lp == 0:
                    #have no position
                    if sp == 1:
                        #print "BUY\n"              
                        self.buyorder(price)
                        self.loginfo(self.sname+u" => 買進")

                    elif sp == -1:    
                        #print "SELL\n"
                        self.sellorder(price)
                        self.loginfo(self.sname+u" => 賣出")

                elif lp == 1:
                    #had long
                    if sp == 0:
                        #print "EXITLONG\n"
                        self.sellorder(price)
                        self.loginfo(self.sname+u" => 多單平倉")
                    elif sp == -1:
                        #print "EXITLONG\n"
                        self.sellorder(price)
                        self.loginfo(self.sname+u" => 多單平倉")
                        #print "SELL\n"
                        self.sellorder(price)
                        self.loginfo(self.sname+u" => 賣出")
                elif lp == -1:
                    #had short
                    if sp == 0:
                        #print "EXITSHORT\n"
                        self.buyorder(price)
                        self.loginfo(self.sname+u" => 空單平倉")
                    elif sp == 1:    
                        #print "EXITSHORT\n"
                        self.buyorder(price)
                        self.loginfo(self.sname+u" => 空單平倉")
                        #print "BUY\n"
                        self.buyorder(price)
                        self.loginfo(self.sname+u" => 買進")
                # after make position change, copy to lock file

                fp = open(self.lockf,"w")
                fp.write(signalf)
                fp.close()

            # update position and ui
            if sp != self.pos:
                self.pos = sp
                self.updateui()

#------------------------------------------


class SS(MyS):
    def __init__(self, *args, **kwds):
        MyS.__init__(self, *args, **kwds)
        wx.EVT_CHAR_HOOK(self, self.onKey)

        dirname = app_dir
        self.our_file = dirname+"/"+"automan.pickle" # share same file
        self.data = {}
        self.loaddata()

    
    def onSChange(self,event):
        sindexs = self.sindex.GetValue()
        if sindexs:
            sindex = int(sindexs)
        sname = self.sname.GetValue()
        sfile = self.sfile.GetPath()
        signal_file_list = [i[1] for i in self.data['sctrl']]
        signal_name_list = [i[0] for i in self.data['sctrl']]
        if signal_file_list and sfile in signal_file_list:

            sindexs = str(signal_file_list.index(sfile))
            sindex = int(sindexs)

        if sindexs and sname in signal_name_list and signal_name_list.index(sname) != sindex:
            # dupicate sname
            dlg = wx.MessageDialog(self, 
                    u'您的訊號名稱有重複',
                    u'監控訊號修改',
                    wx.OK | wx.ICON_INFORMATION 
                    )
            val = dlg.ShowModal()
            dlg.Destroy()
        
        elif sname and  os.path.isfile(sfile):
            dlg = wx.MessageDialog(self, 
                    u'您確定要新增或修改嗎?',
                    u'監控訊號修改',
                    wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION
                    )
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == wx.ID_YES:

                if sindexs:
                    sitem = [sname,sfile]
                    sindex = int(sindexs) # make sure
                    # test if have same name item 

                    # update, the data should have sctrl
                    self.data['sctrl'][sindex]=sitem
                    writepickle(self.our_file,self.data)

                elif sfile:
                    # insert
                    sitem = [sname,sfile]
                    self.data['sctrl'].append(sitem)
                    writepickle(self.our_file,self.data)

                self.Destroy()
            
        else:
            #something wrong
            dlg = wx.MessageDialog(self, 
                    u'您的訊號檔案不存在，或是沒取名字',
                    u'監控訊號',
                    wx.OK | wx.ICON_INFORMATION 
                    )
            val = dlg.ShowModal()
            dlg.Destroy()
    
    def onSDelete(self,event):
        sindex = self.sindex.GetValue()
        sname = self.sname.GetValue()
        sfile = self.sfile.GetPath()
        if sindex:
            dlg = wx.MessageDialog(self, 
                    u'您確定要刪除嗎?',
                    u'監控訊號',
                    wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION
                    )
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == wx.ID_YES:
                # update, the data should have sctrl
                sitem = [sname,sfile]
                sindex = int(sindex) # turn to integer
                self.data['sctrl'].pop(sindex)
                writepickle(self.our_file,self.data)
        self.Destroy()
    
    def onKey(self,event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip()

    
    def loaddata(self):
        dd = loadpickle(self.our_file)
        if not dd:
            dd = {}
        if dd.has_key('sctrl') and type(dd['sctrl'])==types.ListType:
            self.data = dd
        else:
            self.data = dd
            self.data['sctrl'] = []
 
    def loaditem(self,index):
        if self.data and len(self.data['sctrl'])>=int(index)+1:
            item = self.data['sctrl'][int(index)]
            self.sindex.SetValue(unicode(index))
            self.sname.SetValue(item[0])
            self.sfile.SetPath(item[1])

class AA(MyA):
    def __init__(self, *args, **kwds):
        MyA.__init__(self, *args, **kwds)
        wx.EVT_CHAR_HOOK(self, self.onKey)
        dirname = app_dir
        self.our_file = dirname+"/"+"automan.pickle" # share same file
        self.data_ids = ['aname','abroker','acompany','account','aproduct','aym','asignal',
                         'anumber','amarket','acurrency','auniquekey']
        # structure [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,aintraday,amarket,acurrency]
        self.data = {}
        self.loaddata()
        self.brokers = self.abroker.GetItems()
        self.signals = []
        self.intradays = [u"NO",u"YES"]
        if self.data.has_key('sctrl') and len(self.data['sctrl'])>0:
                self.signals = [ i[0] for i in self.data['sctrl'] ]
        self.asignal.SetItems(self.signals)
    
    def onAChange(self,event):
        aindexs = self.aindex.GetValue()
        aname = self.aname.GetValue()
        abroker = self.abroker.GetSelection()
        acompany = self.acompany.GetValue()
        account = self.account.GetValue()
        aproduct = self.aproduct.GetValue()
        aym = self.aym.GetValue()
        asignal = self.asignal.GetSelection()
        anumber = self.anumber.GetValue()
        aintraday = self.aintraday.GetSelection()
        amarket = self.amarket.GetValue()
        acurrency = self.acurrency.GetValue()
        
        # structure [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,aintraday,amarket,acurrency]
        if abroker>-1:
            abroker = self.brokers[abroker]
        if asignal>-1:
            asignal = self.signals[asignal]
        if aintraday>-1:
            aintraday = self.intradays[aintraday]

        item = [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,aintraday,amarket,acurrency] 
        if aindexs:
            # update
            aindex = int(aindexs) 
            dlg = wx.MessageDialog(self, 
                    u'您確定要新增或修改嗎?',
                    u'下單條件',
                    wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION
                    )
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == wx.ID_YES:
                if aindexs:
                    self.data['actrl'][aindex]=item
                    writepickle(self.our_file,self.data)

                self.Destroy()
            
        else:
            # going to insert
            self.data['actrl'].append(item)
            writepickle(self.our_file,self.data)
                
            self.Destroy()
    
    def onADelete(self,event):
        aindex = self.aindex.GetValue()
        aname = self.aname.GetValue()
        if aindex:
            dlg = wx.MessageDialog(self, 
                    u'您確定要刪除嗎?',
                    u'下單條件',
                    wx.YES_NO | wx.YES_DEFAULT | wx.ICON_INFORMATION
                    )
            val = dlg.ShowModal()
            dlg.Destroy()
            if val == wx.ID_YES:
                # update, the data should have actrl
                aindex = int(aindex) # turn to integer
                self.data['actrl'].pop(aindex)
                writepickle(self.our_file,self.data)
        self.Destroy()
    
    def onBroker(self,event):
        abroker = self.abroker.GetSelection()
        if abroker>-1:
            # [u"康合",u"日盛"]
            if abroker == 1:
                self.amarket.SetValue(u"")
                self.acurrency.SetValue(u"")
                self.amarket.Enable(False)
                self.acurrency.Enable(False)
            else:
                self.amarket.Enable(False)
                self.acurrency.Enable(False)
                self.amarket.Enable()
                self.acurrency.Enable()

    def onKey(self,event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip()
                
    
    def loaddata(self):
        dd = loadpickle(self.our_file)
        if not dd:
            dd = {}
        if dd.has_key('actrl') and type(dd['actrl'])==types.ListType:
            self.data = dd
        else:
            self.data = dd
            self.data['actrl'] = []
 
    def loaditem(self,index):
        # structure [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,aintraday,amarket,acurrency]
        if self.data and len(self.data['actrl'])>=int(index)+1:
            item = self.data['actrl'][int(index)]
            if len(item)==11:
                self.aindex.SetValue(unicode(index))
                self.aname.SetValue(item[0])
                self.abroker.SetSelection(self.brokers.index(item[1]))
                self.acompany.SetValue(item[2])
                self.account.SetValue(item[3])
                self.aproduct.SetValue(item[4])
                self.aym.SetValue(item[5])
                if item[6] in self.signals:
                    self.asignal.SetSelection(self.signals.index(item[6]))
                
                self.anumber.SetValue(int(item[7]))
                
                if item[8] in self.intradays:
                    self.aintraday.SetSelection(self.intradays.index(item[8]))
                self.amarket.SetValue(item[9])
                self.acurrency.SetValue(item[10])
            abroker = self.abroker.GetSelection()
            if abroker == 1:
                self.amarket.SetValue(u"")
                self.acurrency.SetValue(u"")
                self.amarket.Enable(False)
                self.acurrency.Enable(False)

class FF(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        # art work
        #self.quit = wx.MenuItem( self.menumain, wx.ID_ANY, u"離開"+ u"\t" + u"CTRL+X", wx.EmptyString, wx.ITEM_NORMAL )
                                
        #self.quit.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT,wx.ART_MENU,(16,16)))
        #self.menumain.AppendItem( self.quit )
        
        self.hts = False
        self.ocx = False
        self.con = False
        self.login = False
        self.cdate = "" # current month contract YYYYMM
        self.threads = []
        self.sl = [] # signal dict or list
        self.al = [] # action dict or list
        self.data_ids = ['username','password','cert','certpass','autostart',]#'sctrl','actrl']
        dirname = app_dir
        self.our_file = dirname+"/"+"automan.pickle"
        self.logfilename = dirname+"/"+"automan.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.logfilename,
        )
        self.logger = logging.getLogger('') 
        
        self.sctrl.InsertColumn(0,u'策略名稱')
        self.sctrl.InsertColumn(1,u'策略狀態')
        self.sctrl.InsertColumn(2,u'策略監控檔案位址')
        self.sctrl.SetColumnWidth(2, 150)
        
        self.actrl.InsertColumn(0,u'下單名稱')
        self.actrl.InsertColumn(1,u'期貨商')
        self.actrl.InsertColumn(2,u'公司代碼')
        self.actrl.InsertColumn(3,u'帳號代碼')
        self.actrl.InsertColumn(4,u'商品代碼')
        self.actrl.InsertColumn(5,u'年月代碼')
        self.actrl.InsertColumn(6,u'策略')
        self.actrl.InsertColumn(7,u'目前倉位')
        self.actrl.InsertColumn(8,u'下單口數')
        
        self.actrl.SetColumnWidth(1, 60)
        self.actrl.SetColumnWidth(7, 60)
        self.actrl.SetColumnWidth(8, 60)
        #self.actrl.SetColumnWidth(7, 80)
        #self.actrl.SetColumnWidth(8, 80)
        self.data = {}
        self.loaddata()
        self.get_our()
        self.render_all()
        # check broker support 
        self.checkbroker()
        self.checkautostart()
    
    def checkautostart(self):
        autostart =  self.autostart.GetValue()
        if autostart:
            self.start.SetValue(True)
            self.onStart(True)
            self.loginfo(u"自動開始下單")

    def checkbroker(self):
        progID = getcon()
        hts = ""
        self.loginfo(u"系統檢查...")
        self.loginfo(u"軟體使用期限%s"% (__DEAD__))
        self.loginfo(u"目前未支援下國外商品")
        if progID:
            self.loginfo(getcon())
            self.ocx = AxWindow(self,  size=wx.Size(0,0) )
            self.ocxSizer.Add( self.ocx, 0, wx.ALL|wx.EXPAND, 5 )
            self.con = self.ocx.ctrl
            self.loginfo(u"支援康合API")
        else:
            self.loginfo(u"未安裝康合API元件")
            
        hts = gethts()
        if hts:
            self.hts = hts
            self.loginfo(u"支援日盛API，需開啟APITradeMgr.exe")
        else:
            self.loginfo(u"找不到日盛HTSAPITradeClient.dll")

         

    def onAddS(self,event):
        dlg = SS(self)
        dlg.sdelete.SetLabel(u"取消")
        dlg.ShowModal()
        dlg.Destroy()
        self.loaddata()
        self.render_signal()
    
    def onSActive(self,event):
        item_index = event.m_itemIndex
        #print item_index

        dlg = SS(self)
        dlg.loaditem(item_index)
        dlg.ShowModal()
        dlg.Destroy()
        self.loaddata()
        self.render_signal()

    def onAddA(self,event):
        dlg = AA(self)
        dlg.adelete.SetLabel(u"取消")
        dlg.ShowModal()
        dlg.Destroy()
        self.loaddata()
        self.render_action()
    
    def onAActive(self,event):
        item_index = event.m_itemIndex
        #print item_index
        # if pressed start button, only can stop order condition, no edit, delete
        start =  self.start.GetValue()
        #print start
        if start:
             #item = [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,aintraday,amarket,acurrency] 
            if item_index>=0 and len(self.data['actrl'])>item_index:
                # update
                # update, the data should have actrl
                aname = self.data['actrl'][item_index][0]
                #  [7] is anumber
                dlg = wx.MessageDialog(self, 
                        u'您確定要停止%s的下單' % (aname),
                        u'停止下單條件',
                        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                        )
                val = dlg.ShowModal()
                dlg.Destroy()
                if val == wx.ID_YES:
                    if item_index>=0:
                        self.data['actrl'][item_index][7] = 0
                        writepickle(self.our_file,self.data)
                        self.actrl.SetStringItem(item_index, 8, u"0") # setup number
                        self.loginfo(u'停止%s的下單' % (aname))
        else: 
            dlg = AA(self)
            dlg.loaditem(item_index)
            dlg.ShowModal()
            dlg.Destroy()
            self.loaddata()
            self.render_action()
    
    def onSave(self,event):
        dd = {}
        for k in self.data_ids:
            item = getattr(self,k)
            if hasattr(item,'GetValue'):
                if k == 'username':
                    dd[k] = item.GetValue().upper()
                else:
                    dd[k] = item.GetValue()
            elif hasattr(item,'GetPath'):
                dd[k] = item.GetPath()


        self.data = dd
        self.write_our()
    
    def onStart(self,event):
        start =  self.start.GetValue()
        if start:
            
            self.start.SetLabel(u"停止下單")
            self.sctrl.Enable(False)
            #self.actrl.Enable(False)
            self.saveall.Enable(False)
            # disable menu
            self.news.Enable(False)
            self.newa.Enable(False)
            self.conlogin()
            self.startworker()

        else:
            self.start.SetLabel(u"開始下單")
            self.sctrl.Enable()
            #self.actrl.Enable()
            self.saveall.Enable()
            # enable menu
            self.news.Enable()
            self.newa.Enable()
            self.stopworker()
            self.loginfo(u"停止下單")
            self.conlogout()

    
    def onAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = u"AUTOMAN 康和日盛下單機"
        info.Version = __version__
        info.Copyright = u"(C) 2011 TerryH"
        info.Description = wordwrap(
            u"此下單機可以下康合及日盛的期貨單，"
            u"目前未支援下國外商品，"
            u"會想寫康和的，純粹是比較，康和，"
            u"怨大，日剩，保來，凱饑，軟體後的結果，"
            u"日剩是以前用的，順便把程式整理一起。"
            u"版權所有，沒有保固，錢賠光了自己負責。"
            u"作者： TerryH",
            350, wx.ClientDC(self))
        info.WebSite = (u"http://blog.lifetaiwan.net", u"TerryH's Blog")
        wx.AboutBox(info)
    
    def onQuit(self,event):
        dlg = wx.MessageDialog(self, 
                u'您確定要關閉程式嗎?',
                u'結束程式',
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                )
        val = dlg.ShowModal()
        dlg.Destroy()
        if val == wx.ID_YES:
            
            # close all threads
            self.stopworker()
            self.Destroy()
    
    def conlogin(self):
        username = self.username.GetValue().upper()
        password = self.password.GetValue()
        cert = self.cert.GetPath()
        certpass = self.certpass.GetValue()

        if self.con and username and password and cert and certpass:
            res = ''
            try:
                res = self.con.Login(username,password,"")
            except:
                pass

            self.loginfo(u"康合API登入...")
            if res[:2] == u"OK":
                self.con.CertSign = 1
                self.loginfo(res)
                self.loginfo(u"康合憑證檢查...")
                res = self.con.AddUserInfo(username,certpass,cert)
                if res[:2] == u"OK":
                    self.loginfo(res)
                    self.login = True
                else:
                    self.loginfo(u"康和憑證資料錯誤，登入失敗")
            else:
                self.loginfo(res)

        else:
            self.loginfo(u"康和登入資料不完整或是分析OCX API 錯誤，未登入")
            
    def conlogout(self):

        if self.con and self.login:
            self.loginfo(u"康合API登出")
            res = self.con.Logout()
            if res[:2] == u"OK":
                self.loginfo(res)
                self.login = False
        

    def startworker(self):
        for i in self.al:
             #item = [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,aintraday,amarket,acurrency] 
             cym = Worker.getcurrent()
             aym = i[5]
             if cym:
                self.cdate = cym
             if cym > __DEAD__:
                self.loginfo(u"已超過軟體使用期限，不監控策略")
                return ""

             if len(aym)>=6:
                aym = "".join(re_dead.findall(aym))
                if aym > __DEAD__:
                    self.loginfo(u"已超過軟體使用期限，不監控策略")
                    return ""
            
        for i in self.sl:
            if len(i) == 2:
                t = Worker(self,i[0])
                if t.running:
                    t.start()
                self.threads.append(t)
    def stopworker(self):
        while len(self.threads)>0:
            t = self.threads.pop()
            t.Stop()
            if t.isAlive():
                t.join()
        self.render_all()

    def render_all(self):
        self.render_signal()
        self.render_action()

    def render_signal(self):
        self.sctrl.DeleteAllItems()
        for i in self.sl:
            if len(i) == 2:
                index = self.sctrl.InsertStringItem(sys.maxint,i[0])
                self.sctrl.SetStringItem(index, 1, u"")
                self.sctrl.SetStringItem(index, 2, i[1])

                self.sctrl.SetItemBackgroundColour(index, wx.Color(229,229,229))

        
    def render_action(self):
        self.actrl.DeleteAllItems()
        for i in self.al:
            #if len(i) == 2:
            #structure [aname,abroker,acompany,account,aproduct,aym,asignal,anumber,amarket,acurrency]
            index = self.actrl.InsertStringItem(sys.maxint,i[0])
            self.actrl.SetStringItem(index, 1, i[1]) # broker
            self.actrl.SetStringItem(index, 2, i[2]) # company
            self.actrl.SetStringItem(index, 3, i[3]) # account
            self.actrl.SetStringItem(index, 4, i[4]) # product code
            self.actrl.SetStringItem(index, 5, i[5]) # a ym
            self.actrl.SetStringItem(index, 6, unicode(i[6])) # signal
            self.actrl.SetStringItem(index, 7, u"") # real state
            self.actrl.SetStringItem(index, 8, unicode(i[7])) # setup number
            self.actrl.SetItemBackgroundColour(index, wx.Color(229,229,229))
    def loaddata(self):
        dd = loadpickle(self.our_file)
        if not dd:
            dd = {}
        for k in self.data_ids:
            if dd.has_key(k):
                self.data[k]=dd[k]
            else:
                self.data[k]=u''
        
        if dd.has_key('actrl') and type(dd['actrl'])==types.ListType:
            self.data['actrl'] = dd['actrl']
            self.al = dd['actrl']
        else:
            self.data['actrl'] = []
        
        if dd.has_key('sctrl') and type(dd['sctrl'])==types.ListType:
            self.data['sctrl'] = dd['sctrl']
            self.sl = dd['sctrl']
        else:
            self.data['sctrl'] = []
    
    def get_our(self):
        if not self.data:
            self.loaddata()
        
        if self.data:
            for k in self.data_ids:
                if k in self.data and self.data[k]:
                    item = getattr(self,k)
                    if hasattr(item,'SetValue'):
                        item.SetValue(self.data[k])
                    elif hasattr(item,'SetPath'):
                        item.SetPath(self.data[k])


    def write_our(self):
        if self.data:
            writepickle(self.our_file,self.data)
            self.loginfo(u"己將設定儲存")

    def loginfo(self,text=u""):
        if text:
            self.log.AppendText(datetime.datetime.now().strftime("%m-%d %H:%M:%S")+u" "+text+u"\n")
            self.logger.info(text)
    

if __name__ == '__main__':
    app = wx.PySimpleApp(False)
    frm = FF(None)
    
    
    frm.Show()
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
