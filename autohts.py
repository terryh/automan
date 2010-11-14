# -*- encoding: utf-8 -*-
import threading
import calendar, datetime, time
import ctypes
import logging
import os,sys
__version__ = '0.8'
class PeriodicExecutor(threading.Thread):
    def __init__(self,sleep,func,params):
        """ execute func(params) every 'sleep' seconds """
        self.func = func
        self.params = params
        self.sleep = sleep
        threading.Thread.__init__(self,name = "PeriodicExecutor")
        self.setDaemon(1)
    def run(self):
        while 1:
            time.sleep(self.sleep)
            apply(self.func,self.params)

hts = ctypes.WinDLL('HTSAPITradeClient.dll')

class HTS(object):
    def __init__(self, signalfile=""):
        """initial for HTS module"""
        if signalfile:
            fn = os.path.splitext(signalfile)[0]
            logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=fn+".log",
            )
            self.logger = logging.getLogger('') 
            self.signalf = signalfile
            self.lockf = fn+".lock"
            self.htsorder = hts.HTSOrder
    def getcurrent(self):
        today = datetime.date.today()
        
        cd = calendar.Calendar()
        counter = 0
        contractdate = 0
        for ww in cd.monthdatescalendar(today.year,today.month):
            if ww[2].month == today.month:
                counter +=1
                if counter == 3:
                    contractdate = ww[2]
                    break
        return contractdate
    def checksignal(self):
        """ signal file format
        Date,time,contractdate,lots,acount,contractname,price,position
        contractdate YYYYMM, or 0 current month
        lots number or 0 mean 1
        account you account
        contractname 
            臺股期貨(TXF) 
            電子期貨(EXF) 
            金融期貨(FXF) 
            小型臺指期貨(MXF) 
            台灣50期貨 (T5F)
            非金電期貨 (XIF) 
            櫃買期貨(GTF) 
            新台幣計價黃金期貨 (TGF)
        price 0 為IOC 市價, 非 0 為 ROD 限價單
        position 1 buy, 0 no contract, -1 sell
        """
        signalf = "" 
        if self.signalf:
            try:
                signalf = file(self.signalf).read()
            except:
                #open(self.signalf,"w")
                #signalf = file(self.signalf).read()
                print "Sorry, No signal file %s" % (self.signalf)
                #sys.exit()
                return ""
            try:
                lockf = file(self.lockf).read()
                #print "LOCKF",lockf,not lockf
                if not lockf:
                    fp = open(self.lockf,"w")
                    fp.write(signalf)
                    fp.close()
                    lockf = file(self.lockf).read()
            except:
                fp = open(self.lockf,"w")
                fp.write(signalf)
                fp.close()
                lockf = file(self.lockf).read()

            sl = signalf.split(',')
            ll = lockf.split(',')
            #print ll 
            try:
                sp = int(sl[-1])
            except:
                # not correct signal file, wait next run
                return ""

            lp = int(ll[-1])
            cdate =  int(sl[2])
            lots = int(sl[3])
            account = sl[4]
            cname = sl[5]
            price = int(sl[6])
            pos = sl[7]
            today = datetime.date.today()
            ordertype = ""
            fokiocrod = ""
            if cdate == 0:
                if today <= self.getcurrent():
                    cdate = self.getcurrent().strftime("%Y%m")
                else:
                    cdate = self.getcurrent()+datetime.timedelta(days=30)
                    cdate = cdate.strftime("%Y%m")
            else:
                cdate = sl[2]
            
            if lots == 0:
                lots = 1
            else:
                lots = lots
            if price:
                # limit price,Rod
                ordertype = "L"
                fokiocrod = "R"
            else:
                # market order, Ioc
                ordertype = "M"
                fokiocrod = "I"
                
            buyorder  = "Market=F,Account=%s,ContractName=%s,ContractDate=%s,OpenCloseAuto=A,BuySell=B,Lots=%d,OrderType=%s,Price=%d,FokIocRod=%s,DayTrade=N" % (account,cname,cdate,lots,ordertype,price,fokiocrod) 
            sellorder  = "Market=F,Account=%s,ContractName=%s,ContractDate=%s,OpenCloseAuto=A,BuySell=S,Lots=%d,OrderType=%s,Price=%d,FokIocRod=%s,DayTrade=N" % (account,cname,cdate,lots,ordertype,price,fokiocrod) 
            if sp != lp:
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Position Change"
                if lp == 0:
                    #have no position
                    if sp == 1:
                        print "BUY\n",buyorder                
                        self.htsorder(buyorder)
                        self.logger.info(u"倉位改變 => 買進")

                    elif sp == -1:    
                        print "SELL\n",sellorder                
                        self.htsorder(sellorder)
                        self.logger.info(u"倉位改變 => 賣出")

                elif lp == 1:
                    #had long
                    if sp == 0:
                        print "EXITLONG\n",sellorder
                        self.htsorder(sellorder)
                        self.logger.info(u"倉位改變 => 多單平倉")
                    elif sp == -1:
                        print "EXITLONG\n",sellorder
                        self.htsorder(sellorder)
                        self.logger.info(u"倉位改變 => 多單平倉")
                        print "SELL\n",sellorder
                        self.htsorder(sellorder)
                        self.logger.info(u"倉位改變 => 賣出")
                elif lp == -1:
                    #had short
                    if sp == 0:
                        print "EXITSHORT\n",buyorder
                        self.htsorder(buyorder)
                        self.logger.info(u"倉位改變 => 空單平倉")
                    elif sp == 1:    
                        print "EXITSHORT\n",buyorder
                        self.htsorder(buyorder)
                        self.logger.info(u"倉位改變 => 空單平倉")
                        print "BUY\n",buyorder
                        self.htsorder(buyorder)
                        self.logger.info(u"倉位改變 => 買進")
                # after make position change, copy to lock file
                fp = open(self.lockf,"w")
                fp.write(signalf)
                fp.close()

    def dellock(self):
        if self.lockf:
            try:
                os.remove(self.lockf)
            except:
                pass

    def run(self):
        while 1:
            time.sleep(0.25)
            self.checksignal()

if __name__ == '__main__':
    if  sys.argv[1:]:
        myhts = HTS(sys.argv[1:][0])
        myhts.dellock()
        myhts.run()
        
    else:
        print """
        Please execute this program with an signal file

        Ex:
            command signalfile.txt
            
            signal file format
            Date,time,contractdate,lots,acount,contractname,price,position
        
        AUTOHTS V0.8 TerryH 2009-11-26
        """    
