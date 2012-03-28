# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Mar 19 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"AUTOMAN 康和日盛下單機", pos = wx.DefaultPosition, size = wx.Size( 700,450 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.menumain = wx.Menu()
		self.news = wx.MenuItem( self.menumain, wx.ID_ANY, u"新建監控策略"+ u"\t" + u"CTRL+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.news.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FIND,  ) )
		self.menumain.AppendItem( self.news )
		
		self.newa = wx.MenuItem( self.menumain, wx.ID_ANY, u"新建下單設定"+ u"\t" + u"CTRL+A", wx.EmptyString, wx.ITEM_NORMAL )
		self.newa.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NEW,  ) )
		self.menumain.AppendItem( self.newa )
		
		self.menumain.AppendSeparator()
		
		self.quit = wx.MenuItem( self.menumain, wx.ID_ANY, u"離開"+ u"\t" + u"CTRL+X", wx.EmptyString, wx.ITEM_NORMAL )
		self.quit.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_QUIT,  ) )
		self.menumain.AppendItem( self.quit )
		
		self.m_menubar1.Append( self.menumain, u"新建" ) 
		
		self.menuabout = wx.Menu()
		self.about = wx.MenuItem( self.menuabout, wx.ID_ANY, u"關於這個軟體", wx.EmptyString, wx.ITEM_NORMAL )
		self.about.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP_PAGE,  ) )
		self.menuabout.AppendItem( self.about )
		
		self.m_menubar1.Append( self.menuabout, u"關於" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.sbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		vSizer = wx.BoxSizer( wx.VERTICAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"監控策略" ), wx.VERTICAL )
		
		self.sctrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		self.sctrl.SetToolTipString( u"您可以設定您的訊號檔來源" )
		
		sbSizer8.Add( self.sctrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer20.Add( sbSizer8, 1, wx.EXPAND, 5 )
		
		sbSizer9 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"系統紀錄" ), wx.VERTICAL )
		
		self.log = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		sbSizer9.Add( self.log, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer20.Add( sbSizer9, 1, wx.EXPAND, 5 )
		
		
		bSizer16.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		
		vSizer.Add( bSizer16, 5, wx.EXPAND, 5 )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer10 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"所有下單設定" ), wx.VERTICAL )
		
		self.actrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		self.actrl.SetToolTipString( u"設定您的下單條件" )
		
		sbSizer10.Add( self.actrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer17.Add( sbSizer10, 1, wx.EXPAND, 5 )
		
		
		vSizer.Add( bSizer17, 5, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"登入帳號", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		bSizer19.Add( self.m_staticText18, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.username = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.username.SetToolTipString( u"輸入您康和的登入帳號\n日盛不需設定,但要開啟下單控制程式" )
		
		bSizer19.Add( self.username, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"登入密碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		bSizer19.Add( self.m_staticText27, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PASSWORD )
		self.password.SetToolTipString( u"輸入您康和的登入密碼\n日盛不需設定,但要開啟下單控制程式" )
		
		bSizer19.Add( self.password, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		vSizer.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"憑證位址", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		bSizer9.Add( self.m_staticText28, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.cert = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE )
		self.cert.SetToolTipString( u"輸入您康和的憑證位址的目錄,像是\nC:\\ekey\\845\\F123456789\\F\n日盛不需設定,但要開啟下單控制程式" )
		
		bSizer9.Add( self.cert, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, u"憑證密碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		bSizer9.Add( self.m_staticText29, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.certpass = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PASSWORD )
		self.certpass.SetToolTipString( u"輸入您康和的憑證密碼\n日盛不需設定,但要開啟下單控制程式" )
		
		bSizer9.Add( self.certpass, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		vSizer.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.saveall = wx.Button( self, wx.ID_ANY, u"儲存所有設定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.saveall, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.autostart = wx.CheckBox( self, wx.ID_ANY, u"啟動後自動開始下單", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.autostart, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer21.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.start = wx.ToggleButton( self, wx.ID_ANY, u"開始下單", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.start, 0, wx.ALIGN_CENTER|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		vSizer.Add( bSizer21, 1, wx.EXPAND, 5 )
		
		self.ocxSizer = wx.BoxSizer( wx.VERTICAL )
		
		
		vSizer.Add( self.ocxSizer, 0, wx.EXPAND, 0 )
		
		
		self.SetSizer( vSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onQuit )
		self.Bind( wx.EVT_MENU, self.onAddS, id = self.news.GetId() )
		self.Bind( wx.EVT_MENU, self.onAddA, id = self.newa.GetId() )
		self.Bind( wx.EVT_MENU, self.onQuit, id = self.quit.GetId() )
		self.Bind( wx.EVT_MENU, self.onAbout, id = self.about.GetId() )
		self.sctrl.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.onSActive )
		self.actrl.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.onAActive )
		self.saveall.Bind( wx.EVT_BUTTON, self.onSave )
		self.start.Bind( wx.EVT_TOGGLEBUTTON, self.onStart )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onQuit( self, event ):
		event.Skip()
	
	def onAddS( self, event ):
		event.Skip()
	
	def onAddA( self, event ):
		event.Skip()
	
	
	def onAbout( self, event ):
		event.Skip()
	
	def onSActive( self, event ):
		event.Skip()
	
	def onAActive( self, event ):
		event.Skip()
	
	def onSave( self, event ):
		event.Skip()
	
	def onStart( self, event ):
		event.Skip()
	

###########################################################################
## Class MyS
###########################################################################

class MyS ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"監控訊號設定", pos = wx.DefaultPosition, size = wx.Size( 650,60 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.sindex = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 0,-1 ), wx.TE_READONLY )
		bSizer24.Add( self.sindex, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"訊號名稱", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer24.Add( self.m_staticText31, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.sname = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sname.SetToolTipString( u"取個訊號名字吧,不可以重複" )
		
		bSizer24.Add( self.sname, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"訊號檔案來源", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		bSizer24.Add( self.m_staticText32, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.sfile = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, wx.EmptyString, u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.sfile.SetToolTipString( u"請選擇訊號檔案,不可以重複, 格式, 可以用逗點(半形),或是一個空白隔開,最後一欄 Price 可以沒有,會自動設成市價\n\nDATE,TIME,MarketPosition,Price\n或是\nDATE TIME MarketPosition Price\n\nDATE 代表日期\nTIME  代表時間\nMarketPosition 倉位 0 空手, -1 作空,1作多\nPrice  0,市價單 有實際價位,限價單,程式交易建議市價單,不然不確定成交" )
		
		bSizer24.Add( self.sfile, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"確定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.m_button7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.sdelete = wx.Button( self, wx.ID_ANY, u"刪除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.sdelete, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer24 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button7.Bind( wx.EVT_BUTTON, self.onSChange )
		self.sdelete.Bind( wx.EVT_BUTTON, self.onSDelete )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSChange( self, event ):
		event.Skip()
	
	def onSDelete( self, event ):
		event.Skip()
	

###########################################################################
## Class MyA
###########################################################################

class MyA ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"下單條件設定", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gSizer1 = wx.GridSizer( 6, 2, 0, 0 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"下單名稱", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.aname = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.aname.SetToolTipString( u"為下單條件取個名字" )
		
		gSizer1.Add( self.aname, 0, wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"期貨商", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		abrokerChoices = [ u"康和", u"日盛" ]
		self.abroker = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, abrokerChoices, 0 )
		self.abroker.SetSelection( 0 )
		gSizer1.Add( self.abroker, 0, wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"公司代碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.acompany = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.acompany.SetToolTipString( u"請輸入期貨分公司代碼\n\n例如 F029000 就是代表康和總公司\n\n康和\n\n期貨總公司 F029000\n台南分公司 F029002\n台中分公司 F029003\n高雄分公司 F029004\n彰化分公司 F029005\n\n日盛\n\n台北總公司 000\n其他請自行查明" )
		
		gSizer1.Add( self.acompany, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"帳號代碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.account = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.account.SetToolTipString( u"您的期貨帳號" )
		
		gSizer1.Add( self.account, 0, wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"商品代碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gSizer1.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.aproduct = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.aproduct.SetToolTipString( u"交易商品的代碼\n\n例如要下康和小台指就填 MXF\n\n康和的例子,交易所的代碼也必須填,其他商品請自行查閱\n\nTXF   台指期\nMXF  小台指\nFXF   金融期\nEXF   電子期\nGTF   櫃買期\nCPF   利率期貨\nT5F   台灣五十\nXIF     非金電期\nTGF   台黃期\nGDF   黃金期\n\n日盛的例子\n\nTXF   台指期\nMXF   小台指\nFXF    金融期\nEXF    電子期" )
		
		gSizer1.Add( self.aproduct, 0, wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"年月代碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		gSizer1.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.aym = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.aym.SetToolTipString( u"交易商品的年月份\n台彎期交所的格式是 YYYYMM\n不填資料,或是 0 就會預設交易當月\n" )
		
		gSizer1.Add( self.aym, 0, wx.ALL, 5 )
		
		self.m_staticText161 = wx.StaticText( self, wx.ID_ANY, u"使用策略", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText161.Wrap( -1 )
		gSizer1.Add( self.m_staticText161, 0, wx.ALL, 5 )
		
		asignalChoices = []
		self.asignal = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, asignalChoices, 0 )
		self.asignal.SetSelection( 0 )
		gSizer1.Add( self.asignal, 0, wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"下單口數", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		gSizer1.Add( self.m_staticText14, 0, wx.ALL, 5 )
		
		self.anumber = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 99, 0 )
		self.anumber.SetToolTipString( u"選您實際要下單的口數,0 就是不下單" )
		
		gSizer1.Add( self.anumber, 0, wx.ALL, 5 )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"是否當沖", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		gSizer1.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		aintradayChoices = [ u"NO", u"YES" ]
		self.aintraday = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, aintradayChoices, 0 )
		self.aintraday.SetSelection( 0 )
		gSizer1.Add( self.aintraday, 0, wx.ALL, 5 )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"交易所代碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		gSizer1.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		self.amarket = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.amarket.SetToolTipString( u"康和的帳號需填,下面是例子\nTIM 台灣期貨交易所\nSMX 新加坡交易所\nCME 美國芝加哥商業交易所\nCBT 美國芝加哥期貨交易所\nTCE 日本東京工業品交易所\nHKF 香港期貨交易所" )
		
		gSizer1.Add( self.amarket, 0, wx.ALL, 5 )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"幣別代碼", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		gSizer1.Add( self.m_staticText16, 0, wx.ALL, 5 )
		
		self.acurrency = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.acurrency.SetToolTipString( u"康和需填\n\nNTT 台幣\nUSD 美金\nJPY  日圓" )
		
		gSizer1.Add( self.acurrency, 0, wx.ALL, 5 )
		
		self.aindex = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 0,0 ), wx.TE_READONLY )
		gSizer1.Add( self.aindex, 0, wx.ALL, 5 )
		
		self.auniquekey = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 0,0 ), wx.TE_READONLY )
		gSizer1.Add( self.auniquekey, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_ANY, u"確定", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_button4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.adelete = wx.Button( self, wx.ID_ANY, u"刪除", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.adelete, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		self.SetSizer( gSizer1 )
		self.Layout()
		gSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_KEY_DOWN, self.onKey )
		self.abroker.Bind( wx.EVT_CHOICE, self.onBroker )
		self.m_button4.Bind( wx.EVT_BUTTON, self.onAChange )
		self.adelete.Bind( wx.EVT_BUTTON, self.onADelete )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onKey( self, event ):
		event.Skip()
	
	def onBroker( self, event ):
		event.Skip()
	
	def onAChange( self, event ):
		event.Skip()
	
	def onADelete( self, event ):
		event.Skip()
	

