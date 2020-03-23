import os
import os.path
from win32com.client import Dispatch
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
import xlwt
import xlrd
import re
import datetime
from kivy.uix.popup import Popup
from xlutils.copy import copy
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.config import Config
from xlwt import Workbook 
from kivymd.list import BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.theming import ThemeManager
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
data=0
scandata=0
rows=1
NamaUser=''
cols=0
GenderAsli=''
gender=''
resetText=0
JumlahUser=1
rowBarang=1
JdataPenjualan=1
totalBarang=0
ParamBarangArray=0
hargaBarangTotal=0
nu_text=''
kondImage=''
screen_manager = ScreenManager()
waktu=datetime.datetime.now()
simpanwaktu= waktu.strftime("%d-%m-%Y")
class setNamePopup(Popup):
    def FadePopup(self):
        #self.manager.current='login'#program untuk pindah ke layout yang lain berdasarkan name window
        self.dismiss()
        print('gajadiKeluar')
    def FadePopupYes(self):
        global resetText
        resetText=1
        self.dismiss()
        print('keluar')
class WelcomeBack(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username=[]
        self.password=[]
        self.namauser=[]
        self.gender=[]
    def loginreset(self):
        self.ids.username_field.text=''
        self.ids.pwd_field.text=''
        self.ids.money_field.text=''
        self.ids.info.text=''
    def validate_user(self):
        global NamaUser
        global reset
        global kondImage
        global GenderAsli
        loc = ("data.xls")
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        for row in range(1,sheet.nrows):
            print(sheet.cell_value(row,5))
            print(sheet.cell_value(row,6))
            print(sheet.cell_value(row,1))
            print(sheet.cell_value(row,4))
            self.username.append(sheet.cell_value(row, 5))
            self.password.append(sheet.cell_value(row,6))
            self.namauser.append(sheet.cell_value(row,1))
            self.gender.append(sheet.cell_value(row,4))
            print(self.username)
            print(self.password)
            print(self.namauser)
            print(self.gender)
        #parameter untuk mengecheck nilai pada array
        UserData=-1
        user= self.ids.username_field
        pwd= self.ids.pwd_field
        kembalian= self.ids.money_field
        info= self.ids.info

        uname=user.text
        passw=pwd.text
        UangKembalian=kembalian.text
        xparamUangKembalian=re.findall("[a-zA-Z]",UangKembalian)
        xparamUangKembalian2=1
        panjangChange=len(UangKembalian)
        l2=[ord(c) for c in UangKembalian]
        print(l2)
        if UangKembalian < '0' :
            xparamUangKembalian2=0
        elif panjangChange>1:
            if UangKembalian.startswith('0'):
                xparamUangKembalian2=0
            else:
                for i,c in enumerate(l2):
                    if c >= 33 and c < 48 or c>=58 and c< 65 or c >=91 and c < 97 or c == 126:
                        xparamUangKembalian2=0
                        break
                    else:
                        xparamUangKembalian2=1
        #xparamUangKembaliancond3= UangKembalian.startswith('[0][0-9]')
        if uname== '' or passw=='' or UangKembalian=='' :
            info.text='[color=#FF0000]Username ,Password,and Change  required[/color]'
        elif xparamUangKembalian or xparamUangKembalian2==0 :
            info.text='[color=#FF0000]Masukkan jumlah uang dengan format yang benar[/color]'
            self.ids.money_field.text=''
        else:
            for i,c in enumerate(self.username):
                if c == uname:
                    UserData=i
            if UserData>=0:
                if uname==self.username[UserData] and passw==self.password[UserData] and xparamUangKembalian2==1:
                    info.text='[color=#1764ff]Logged In Successfully!!![/color]'
                    self.manager.current='Home_Win'#program untuk pindah ke layout yang lain berdasarkan name window
                    self.ids.username_field.text=''
                    self.ids.pwd_field.text=''
                    self.ids.money_field.text=''
                    self.ids.info.text=''
                    NamaUser=self.namauser[UserData]
                    self.manager.get_screen('Home_Win').labelText = NamaUser
                    self.manager.get_screen('Home_Win').dataWaktu = simpanwaktu
                    #untuk mengganti gambar profil cewek atau cowok
                    if self.gender[UserData]=='Male':
                        self.manager.get_screen('Home_Win').img_src = 'man_home.png'
                    else:
                        self.manager.get_screen('Home_Win').img_src = 'woman.png'
                    reset=' '
                
                else:
                    info.text='[color=#FF0000]Invalid Username or Password!!![/color]'
                    self.ids.pwd_field.text=''
                    self.ids.money_field.text=''

            else:
                info.text='[color=#FF0000]Username and Password not registered[/color]'
                self.ids.username_field.text=''
                self.ids.pwd_field.text=''
                self.ids.money_field.text=''
        self.username=[]
        self.password=[]
        self.namauser=[]
        self.gender=[]
        print(kondImage)
class ProfileWindow(Popup):
    def FadePopup(self):
        print(kondImage)
        self.dismiss()

class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
    
class HomeWindow(Screen):
    global resetText
    global GenderAsli
    img_src=StringProperty('')
    labelText = StringProperty('')
    dataWaktu=StringProperty('')
    #datanama = StringProperty(0)
    def setName(self,*args):
        setNamePopup().open()
        self.ids.list_item.text=''
        self.ids.pembayaran.text=''
        self.JumlahProduct=[]
        self.codeItem=[]
        self.NamaProduct=[]
        self.HargaBarang=[]
    def __init__(self, **kwargs):
        global d1
        super().__init__(**kwargs)
        self.JumlahProduct=[]
        self.codeItem=[]
        self.NamaProduct=[]
        self.HargaBarang=[]
        self.hargaperBarang=[]
        self.checkscanproduct=[]
        self.checknamaProduct=[]
        self.checkhargabarang=[]
        #self.waktu.text=simpanwaktu
        #waktuSaatIni= Label(text=d1,color=(.06,.45,.45,1))

        #self.waktu.text = time.asctime()   
    def reset(self):
        global totalBarang
        global hargaBarangTotal
        global ParamBarangArray
        self.ids.list_item.text=''
        self.ids.total_barang.text='0'
        self.ids.total_pay.text=''
        self.ids.pembayaran.text=''
        self.ids.Kembalian.text=''
        self.codeItem=[]
        self.NamaProduct=[]
        self.hargaperBarang=[]
        self.JumlahProduct=[]
        self.HargaBarang=[]
        hargaBarangTotal=0
        totalBarang=0
        ParamBarangArray=0
    def nameUser(self):
        global NamaUser
        self.datanama=NamaUser
    def barang1(self):
        global scandata
        scandata=1
        self.list_data()
    def barang2(self):
        global scandata
        scandata=2
        self.list_data()
    def oreo(self):
        global scandata
        scandata=3
        self.list_data()
    def taro(self):
        global scandata
        scandata=4
        self.list_data()
    def lays(self):
        global scandata
        scandata=5
        self.list_data()
    def slaiolai(self):
        global scandata
        scandata=6
        self.list_data()
    def potabee(self):
        global scandata
        scandata=7
        self.list_data()
    def chitato(self):
        global scandata
        scandata=8
        self.list_data()
    def romakelapa(self):
        global scandata
        scandata=9
        self.list_data()
    def sarigandum(self):
        global scandata
        scandata=10
        self.list_data()
    def rinbee(self):
        global scandata
        scandata = 11
        self.list_data()
    def sponge(self):
        global scandata
        scandata=12
        self.list_data()
    def tango(self):
        global scandata
        scandata=13
        self.list_data()
    def SIIP(self):
        global scandata
        scandata= 14
        self.list_data()
    def gery(self):
        global scandata
        scandata=15
        self.list_data()
    def crackers(self):
        global scandata
        scandata=16
        self.list_data()
    def frestea(self):
        global scandata
        scandata=17
        self.list_data()
    def goodday(self):
        global scandata
        scandata=18
        self.list_data()
    def ichiocha(self):
        global scandata
        scandata=19
        self.list_data()
    def leminerale(self):
        global scandata
        scandata=20
        self.list_data()
    def minutemaid(self):
        global scandata
        scandata=21
        self.list_data()
    def tehpucuk(self):
        global scandata
        scandata=22
        self.list_data()
    def TehKotak(self):
        global scandata
        scandata=23
        self.list_data()
    def ultramilk(self):
        global scandata
        scandata=24
        self.list_data()
    def fruittea(self):
        global scandata
        scandata=25
        self.list_data()
    def fruitbtl(self):
        global scandata
        scandata=26
        self.list_data()
    def aqua(self):
        global scandata
        scandata=27
        self.list_data()
    def cleo(self):
        global scandata
        scandata=28
        self.list_data()
    def tehgelasbtl(self):
        global scandata
        scandata=29
        self.list_data()
    def hydro(self):
        global scandata
        scandata=30
        self.list_data()
    def tehbtl(self):
        global scandata
        scandata=31
        self.list_data()
    def logout(self,*args):
        ProfileWindow().open()
    def list_data(self):
        global data
        global scandata
        global totalBarang
        global hargaBarangTotal
        global ParamBarangArray
        if scandata== 0:
            scanproduct = self.ids.qty_inp_scan.text
        else:
            scanproduct=str(scandata)
        loc = ("ListProduk.xls")
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        for row in range(1,sheet.nrows):
            print(sheet.cell_value(row,0))
            print(sheet.cell_value(row,1))
            print(sheet.cell_value(row,2))
            self.checkscanproduct.append(str(int(sheet.cell_value(row,0))))
            self.checknamaProduct.append(sheet.cell_value(row,1))
            self.checkhargabarang.append(int(sheet.cell_value(row,2)))
            print(self.checkscanproduct)
            print(self.checknamaProduct)
            print(self.checkhargabarang)
        ParamProduct= -1
        print(scanproduct)
        for i,c in enumerate(self.checkscanproduct):
            print(c)
            if c == scanproduct:
                ParamProduct=i
        print(ParamProduct)
        #scandata=scanproduct
        if ParamProduct>=0:
            print('halo')
            pname=self.checknamaProduct[ParamProduct]
            pprice=self.checkhargabarang[ParamProduct]
            pqty=str(1)
            subtotal=int(pprice)
            '''if scanproduct == '1234':
                pname ="Product One"
                pprice = '3500'
                pqty = str(1)
                subtotal=3500
            elif scanproduct == '2345':
                pname ="Product Two"
                pprice = '2000'
                pqty = str(1)
                subtotal=2000'''
            preview = self.ids.list_item
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]
            ptarget = -1

            for i,c in enumerate(self.codeItem):
                if c == scanproduct:
                    ptarget=i
            if ptarget >=0 :
                pqty= self.JumlahProduct[ptarget]+1
                self.JumlahProduct[ptarget]=pqty
                subtotal=self.HargaBarang[ptarget]+self.checkhargabarang[ParamProduct]
                panjangSubtotal=len(str(subtotal))
                self.HargaBarang[ptarget]=subtotal
                hargaBarangTotal+=self.checkhargabarang[ParamProduct]
                #regexPython berdasarkan rexpr
                #\d+ = untuk mengganti suatu digit jika + maka 1 atau lebih digit dibelakangnya
                expr ='%s\t\t\t%s\t\t\tx\d+\t\t\d+'%(pname,pprice)
                #regex
                rexpr =pname+'\t\t\t'+str(pprice)+'\t\t\tx'+str(pqty)+'\t\t'+str(subtotal)
                nu_text = re.sub(expr,rexpr,prev_text)
                #expr1 ='%s\t\t%s\t\tx\d\t\d'%(pname,pprice)
                #New_text = re.sub(expr1,rexpr,nu_text)
                #nu_text = re.sub('%s\t\t%s\t\tx\d\t\d+'%(pname,pprice), '', prev_text, 4)
                preview.text = nu_text
                totalBarang+=1
            else:
                self.codeItem.append(scanproduct)
                self.HargaBarang.append(subtotal)
                self.hargaperBarang.append(subtotal)
                self.JumlahProduct.append(1)
                self.NamaProduct.append(pname)
                nu_preview = '\n'.join([prev_text,pname+'\t\t\t'+str(pprice)+'\t\t\tx'+pqty+'\t\t'+str(subtotal)+'\t`'])
                preview.text = nu_preview
                hargaBarangTotal+=self.checkhargabarang[ParamProduct]
                totalBarang+=1
                ParamBarangArray+=1

        else :
            print('data tdk masuk')
        self.ids.total_barang.text=str(totalBarang)
        self.ids.total_pay.text=str(hargaBarangTotal)
        print(self.JumlahProduct)
        self.ids.qty_inp_scan.text=""
        self.checkscanproduct=[]
        self.checknamaProduct=[]
        self.checkhargabarang=[]
        #nilai scancode di nolkan kembali agar tidak mempegaruhi button sebelah scan
        scandata=0
    def pembayaran(self):
        global hargaBarangTotal
        global JdataPenjualan
        global rowBarang
        global ParamBarangArray
        global simpanwaktu
        global totalBarang
        os.system("taskkill /im EXCEL.EXE /f")#Untuk Meng - Close Program Excel yang running
        Cash=self.ids.pembayaran.text
        if Cash=='' or Cash=='0.0':
            Cash=0
        if int(Cash) < hargaBarangTotal:
            print('Uang Pembayaran kurang')
            self.ids.pembayaran.text=''
            self.ids.Kembalian.text=''
        else:
            Kembalian=int(Cash)-hargaBarangTotal
            self.ids.Kembalian.text=str(Kembalian)
            datafile='Penjualan_'+str(simpanwaktu)+'.xls'
            if os.path.isfile(datafile):
                rb = xlrd.open_workbook(datafile)
                wb = copy(rb)
                sheet = rb.sheet_by_index(0)
                for row in range(1,sheet.nrows):
                    JdataPenjualan+=1
                w_sheet = wb.get_sheet(0)
                rowBarang=JdataPenjualan+1
                w_sheet.write(rowBarang,0,'kode produk')
                w_sheet.write(rowBarang,1,'nama produk')
                w_sheet.write(rowBarang,2,'harga produk')
                w_sheet.write(rowBarang,3,'Jumlah Produk')
                w_sheet.write(rowBarang,4,'Subtotal')
                rowBarang+=1
                for i in range(0,ParamBarangArray):  
                    w_sheet.write(rowBarang,0,self.codeItem[i])
                    w_sheet.write(rowBarang,1,self.NamaProduct[i])
                    w_sheet.write(rowBarang,2,self.hargaperBarang[i])
                    w_sheet.write(rowBarang,3,self.JumlahProduct[i])
                    w_sheet.write(rowBarang,4,self.HargaBarang[i])
                    rowBarang+=1
                w_sheet.write(rowBarang+1,4,hargaBarangTotal)
                w_sheet.write(rowBarang+1,0,'Harga Total')
                w_sheet.write(rowBarang+2,4,Cash)
                w_sheet.write(rowBarang+2,0,'Pembayaran')
                w_sheet.write(rowBarang+3,4,Kembalian)
                w_sheet.write(rowBarang+3,0,'Uang Kembalian')
                wb.save(datafile)
            else:
                wb = xlwt.Workbook()
                w_sheet = wb.add_sheet('Sheet 1')
                w_sheet.write(0,0,'kode produk')
                w_sheet.write(0,1,'nama produk')
                w_sheet.write(0,2,'harga produk')
                w_sheet.write(0,3,'Jumlah Produk')
                w_sheet.write(0,4,'Subtotal')
                rowBarang=1
                for i in range(0,ParamBarangArray):  
                    w_sheet.write(rowBarang,0,self.codeItem[i])
                    w_sheet.write(rowBarang,1,self.NamaProduct[i])
                    w_sheet.write(rowBarang,2,self.hargaperBarang[i])
                    w_sheet.write(rowBarang,3,self.JumlahProduct[i])
                    w_sheet.write(rowBarang,4,self.HargaBarang[i])
                    rowBarang+=1
                w_sheet.write(rowBarang+1,4,hargaBarangTotal)
                w_sheet.write(rowBarang+1,0,'Harga Total')
                w_sheet.write(rowBarang+2,4,Cash)
                w_sheet.write(rowBarang+2,0,'Pembayaran')
                w_sheet.write(rowBarang+3,4,Kembalian)
                w_sheet.write(rowBarang+3,0,'Uang Kembalian')
                wb.save(datafile)
            self.codeItem=[]
            self.NamaProduct=[]
            self.hargaperBarang=[]
            self.JumlahProduct=[]
            self.HargaBarang=[]
            self.ids.list_item.text=''
            hargaBarangTotal=0
            JdataPenjualan=1
            totalBarang=0
            ParamBarangArray=0



class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username=[]
        self.password=[]
        self.namauser=[]
        self.gender=[]
    def loginreset(self):
        self.ids.username_field.text=''
        self.ids.pwd_field.text=''
        self.ids.money_field.text=''
        self.ids.info.text=''
    def validate_user(self):
        global NamaUser
        global reset
        global kondImage
        global GenderAsli
        loc = ("data.xls")
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        for row in range(1,sheet.nrows):
            print(sheet.cell_value(row,5))
            print(sheet.cell_value(row,6))
            print(sheet.cell_value(row,1))
            print(sheet.cell_value(row,4))
            self.username.append(sheet.cell_value(row, 5))
            self.password.append(sheet.cell_value(row,6))
            self.namauser.append(sheet.cell_value(row,1))
            self.gender.append(sheet.cell_value(row,4))
            print(self.username)
            print(self.password)
            print(self.namauser)
            print(self.gender)
        #parameter untuk mengecheck nilai pada array
        UserData=-1
        user= self.ids.username_field
        pwd= self.ids.pwd_field
        kembalian= self.ids.money_field
        info= self.ids.info

        uname=user.text
        passw=pwd.text
        UangKembalian=kembalian.text
        xparamUangKembalian=re.findall("[a-zA-Z]",UangKembalian)
        xparamUangKembalian2=1
        panjangChange=len(UangKembalian)
        l2=[ord(c) for c in UangKembalian]
        print(l2)
        if UangKembalian < '0' :
            xparamUangKembalian2=0
        elif panjangChange>1:
            if UangKembalian.startswith('0'):
                xparamUangKembalian2=0
            else:
                for i,c in enumerate(l2):
                    if c >= 33 and c < 48 or c>=58 and c< 65 or c >=91 and c < 97 or c == 126:
                        xparamUangKembalian2=0
                        break
                    else:
                        xparamUangKembalian2=1
        #xparamUangKembaliancond3= UangKembalian.startswith('[0][0-9]')
        if uname== '' or passw=='' or UangKembalian=='' :
            info.text='[color=#FF0000]Username ,Password,and Change  required[/color]'
        elif xparamUangKembalian or xparamUangKembalian2==0 :
            info.text='[color=#FF0000]Masukkan jumlah uang dengan format yang benar[/color]'
            self.ids.money_field.text=''
        else:
            for i,c in enumerate(self.username):
                if c == uname:
                    UserData=i
            if UserData>=0:
                if uname==self.username[UserData] and passw==self.password[UserData] and xparamUangKembalian2==1:
                    info.text='[color=#1764ff]Logged In Successfully!!![/color]'
                    self.manager.current='Home_Win'#program untuk pindah ke layout yang lain berdasarkan name window
                    self.ids.username_field.text=''
                    self.ids.pwd_field.text=''
                    self.ids.money_field.text=''
                    self.ids.info.text=''
                    NamaUser=self.namauser[UserData]
                    self.manager.get_screen('Home_Win').labelText = NamaUser
                    self.manager.get_screen('Home_Win').dataWaktu = simpanwaktu
                    #untuk mengganti gambar profil cewek atau cowok
                    if self.gender[UserData]=='Male':
                        self.manager.get_screen('Home_Win').img_src = 'man_home.png'
                    else:
                        self.manager.get_screen('Home_Win').img_src = 'woman.png'
                    reset=' '
                
                else:
                    info.text='[color=#FF0000]Invalid Username or Password!!![/color]'
                    self.ids.pwd_field.text=''
                    self.ids.money_field.text=''

            else:
                info.text='[color=#FF0000]Username and Password not registered[/color]'
                self.ids.username_field.text=''
                self.ids.pwd_field.text=''
                self.ids.money_field.text=''
        self.username=[]
        self.password=[]
        self.namauser=[]
        self.gender=[]
        print(kondImage)
#Register
   
class RegistWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username=[]
        self.nomorHand=[]
    def reset(self):
        self.usernameku.text=''
        self.namaAwal.text=''
        self.namaAkhir.text=''
        self.nomorTelp.text=''
        self.passwrd.text=''
        self.address.text=''
        self.confpasswr.text=''
        self.ids.info_regist.text=''
    def regist(self):
        global rows
        global cols
        global gender
        global simpanwaktu
        global JumlahUser
        info= self.ids.info_regist
        # create a workbook and add a worksheet 
        #write some data headers
        rb = xlrd.open_workbook('data.xls')
        wb = copy(rb)
        sheet = rb.sheet_by_index(0)
        w_sheet = wb.get_sheet(0)
        for row in range(1,sheet.nrows):
            print(sheet.cell_value(row,5))
            print('\n')
            print(sheet.cell_value(row,3))
            self.username.append(sheet.cell_value(row, 5))
            self.nomorHand.append(sheet.cell_value(row,3))
            #Mengecheck jumlah user account yang terdaftar
            JumlahUser+=1
            print(self.username)
            print(self.nomorHand)
        print(JumlahUser)
        emaildata= self.usernameku.text
        dataFirstName = self.namaAwal.text
        dataLastName = self.namaAkhir.text
        nomorHP = self.nomorTelp.text
        passw = self.passwrd.text
        addr = self.address.text
        confPass=self.confpasswr.text
        #check username atau nomorHP yang sama
        UserData=-1
        xparamPhoneFront=1
        for i,c in enumerate(self.username):
                if c == emaildata:
                    UserData=i
        namalengkap=dataFirstName+' '+dataLastName
        xparamname=re.findall("\d",namalengkap)
        #parameter untuk memasukkan digit nomor telp pada array
        temp = re.findall('\d', nomorHP)
        res=list(map(int,temp))
        #parameter untuk mengecheck format pada nomortelp
        if temp:
            if res[0]== 0:
                xparamPhoneFront=0
            else:
                print('tidak')
        xparamPhoneNumber=re.findall("[a-zA-Z]",nomorHP)
        xparamPasswNumber=re.findall("\d",passw)
        xparamPasswType=re.findall("[a-zA-Z]",passw)
        LengthPass=len(passw)
        lengthNumberP=len(nomorHP)
        print(xparamPhoneFront)
        if emaildata=='' or dataFirstName=='' or dataLastName=='' or gender=='' or nomorHP=='' or passw=='' or confPass=='':
            print('Harap Lengkapi Data Diri Anda')
            info.text='[color=#FF0000]Harap Lengkapi Data Diri Anda[/color]'
        elif xparamname:
            info.text='[color=#FF0000]tulis nama dengan format yang benar[/color]'
        elif lengthNumberP<10 or lengthNumberP>12:
            info.text='[color=#FF0000]jumlah digit nomor telepon anda tidak sesuai [/color]'
        elif xparamPhoneNumber:
            info.text='[color=#FF0000]Masukkan Nomor Telepon berupa angka saja[/color]'
        elif xparamPhoneFront == 1 :
            info.text='[color=#FF0000]invalid Phone Number[/color]'
        #elif xparamPasswNumber == None or xparamPasswType == None:
            #print('Password harus terdiri dari huruf dan angka')
        elif UserData >= 0:
            if emaildata==self.username[UserData]:
                info.text='[color=#FF0000]Username Telah Digunakan[/color]'
            elif nomorHP==self.nomorHand[UserData]:
                info.text='[color=#FF0000]Nomor Handphone ini telah terdaftar[/color]'
        elif confPass!= passw:
            print('ulangi password yang anda masukkan')
            info.text='[color=#FF0000]Ulangi Password Yang Anda Masukkan[/color]'
            self.passwrd.text=''
            self.confpasswr.text=''
        elif xparamPasswNumber and xparamPasswType and xparamPhoneFront==0:
            if LengthPass<8:
                print('Minimal terdapat 8 karakter')
                info.text='[color=#FF0000]password minimal terdapat 8 karakter[/color]'
                self.passwrd.text=''
                self.confpasswr.text=''
            else:
                #mengecheck jumlah user yang terdaftar
                rows=JumlahUser
                w_sheet = wb.get_sheet(0)
                w_sheet.write(rows,0,simpanwaktu)
                w_sheet.write(rows,1,namalengkap)
                w_sheet.write(rows,2,addr)
                w_sheet.write(rows,3,nomorHP)
                w_sheet.write(rows,4,gender)
                w_sheet.write(rows,5,emaildata)
                w_sheet.write(rows,6,confPass)
                rows+=1
                wb.save('data.xls')
                info.text='[color=#1764ff]Success Registered!!![/color]'
                print(namalengkap+' '+addr+' '+nomorHP+' '+emaildata+' '+confPass)
                self.usernameku.text=''
                self.namaAwal.text=''
                self.namaAkhir.text=''
                self.nomorTelp.text=''
                self.passwrd.text=''
                self.address.text=''
                self.confpasswr.text=''
                self.ids.info_regist.text=''
                self.manager.current='welcome'#program untuk pindah ke layout yang lain berdasarkan name window
        else:
            print('password anda harus terdiri dari huruf dan angka')
            self.passwrd.text=''
            self.confpasswr.text=''
            info.text='[color=#FF0000]password anda harus terdiri dari huruf dan angka[/color]'
        self.username=[]
        self.nomorHand=[]
        JumlahUser=1
        #print(res)
    def checkboxMale(self,instance,value):
        global gender
        if value is True:
            gender='Male'
        else:
            gender=''
    def checkboxFemale(self,instance,value):
        global gender
        if value is True :
            gender='Female'
        else:
            gender=''  
    

class ForcaPOSApp(App):
    theme_cls = ThemeManager()
    def build(self):

        main_widget = Builder.load_file(
            os.path.join(os.path.dirname(__file__), "./designpos.kv")
        )
        
        self.bottom_navigation_remove_mobile(main_widget)
        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)

 
if __name__ == "__main__":
    ForcaPOSApp().run()
