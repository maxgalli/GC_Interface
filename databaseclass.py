from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile
import json
#################################################################################################################################### ########## Classi e Funzioni #################################################################################################### #################################################################################################################################
class Database:
############## membri ##########################################################################################################
################################################################################################################################
#################################################################################################################################
	# variabile che si aggiorna ogni volta che viene aggiunta una misura (numero complessivo di paper)
	number_mes = 0
	# lista di variabili che rappresentano il numero di paper per ogni tipo di misura (si aggiorna ad ogni aggiunta)
	n_papers_list = [0,0,0,0,0,0,0,0,0,0]
	# lista di costanti che indicano il numero di osservabili di ogni tipo di misura
	n_obs_list = [7,4,5,7,3,6,5,3,4,4]
	# lista di costanti che indicano il numero di elementi nelle matrici di correlazione di ogni tipo di misura
	n_matrix_elements_list = [49,16,25,49,9,36,25,9,16,16]
	# lista degli entries
	entry_list = []
	# dictionary dei dieci tipi di misure
	measures = {}
	measures['m0'] = {}					# GAhh
	measures['m1'] = {}					# ggsz
	measures['m2'] = {}					# GAhhhh
	measures['m3'] = {}					# ADhhPi0
	measures['m4'] = {}					# GLS
	measures['m5'] = {}					# GAKKPiPiDhh
	measures['m6'] = {}					# BsDsK
	measures['m7'] = {}					# GABDK*
	measures['m8'] = {}					# ggszDKPi
	measures['m9'] = {}					# ggszDK*0
	# measure_type definita successivamente
############## metodi ###########################################################################################################
################################################################################################################################
#################################################################################################################################
	# costruttore
	def __init__(self,parent):
		self.make_tree(parent)
		self.make_popup(parent)
		self.make_menu(parent)
###################################################################################################################################
###################################################################################################################################
	# crea il tree di visualizzazione
	def make_tree(self,parent):
		self.tree_master = ttk.Treeview(parent,columns='Values',selectmode='extended')
		self.tree_master.column('#0',stretch=True,width=350)
		self.tree_master.column('Values',stretch=True,width=150)
		self.tree_master.heading('#0',text='Measures/Years/Observables and Uncertainties')
		self.tree_master.heading('Values',text="Values")

		self.tree_master.insert('',0,iid='m0',text='GAhh')
		self.tree_master.insert('',1,iid='m1',text='ggsz')
		self.tree_master.insert('',2,iid='m2',text='GAhhhh')
		self.tree_master.insert('',3,iid='m3',text='ADhhPi0')
		self.tree_master.insert('',4,iid='m4',text='GLS')
		self.tree_master.insert('',5,iid='m5',text='GAKPiPiDhh')
		self.tree_master.insert('',6,iid='m6',text='BsDsK')
		self.tree_master.insert('',7,iid='m7',text='GABDK*')
		self.tree_master.insert('',8,iid='m8',text='ggszDKPi')
		self.tree_master.insert('',9,iid='m9',text='ggszDK*0')

		self.tree_master.pack(fill=BOTH,expand=1)
#####################################################################################################################################
#####################################################################################################################################
	# crea il popup menu e lo associa al pulsante destro del mouse
	def make_popup(self,parent):
		# Crea il popup menu che si apre quando seleziono un elemento del tree
		self.popup = Menu(parent, tearoff=0)
		self.popup.add_command(label='Print')
		self.popup.add_command(label='Delete paper',command=self.delete_item)
		self.popup.add_separator()
		self.popup.add_command(label='Back')
		
		def do_popup(measure):
			# apre il popup menu
			try:
				# variabile che assume il valore dell'iid dell'item selezionato
				self.item_identified = self.tree_master.identify_row(measure.y)

				self.popup.post(measure.x_root, measure.y_root)
			# rilascio del tasto
			finally:
				self.popup.grab_release()
		
		# associo l'apertura del popup menu al tasto destro del mouse
		self.tree_master.bind("<Button-3>", do_popup)
##################################################################################################################################
##################################################################################################################################
	# crea il menu a barra principale in alto
	def make_menu(self,parent):
		self.barra_menu = Menu(parent)
		
		self.menu_actions = Menu(self.barra_menu,tearoff=0)
		self.barra_menu.add_cascade(label='Actions',menu=self.menu_actions)

		self.menu_add = Menu(self.menu_actions,tearoff=0)
		self.menu_actions.add_cascade(label='Add paper',menu=self.menu_add)
		self.menu_actions.add_command(label='Quit',command=parent.destroy)
		
		self.menu_add.add_command(label='GAhh',command=lambda:self.add_measure(0))
		self.menu_add.add_command(label='ggsz',command=lambda:self.add_measure(1))
		self.menu_add.add_command(label='GAhhhh',command=lambda:self.add_measure(2))
		self.menu_add.add_command(label='ADhhpi0',command=lambda:self.add_measure(3))
		self.menu_add.add_command(label='GLS',command=lambda:self.add_measure(4))
		self.menu_add.add_command(label='GAKPiPiDhh',command=lambda:self.add_measure(5))
		self.menu_add.add_command(label='BsDsK',command=lambda:self.add_measure(6))
		self.menu_add.add_command(label='GABDK*',command=lambda:self.add_measure(7))
		self.menu_add.add_command(label='ggszDKPi',command=lambda:self.add_measure(8))
		self.menu_add.add_command(label='ggszDK*0',command=lambda:self.add_measure(9))

		parent.config(menu=self.barra_menu)
#######################################################################################################################################
########################################################################################################################################
########################################################################################################################################
## da qui tutti i metodi che non compaiono nel costruttore, ma solo come comandi o simili ##############################################
########################################################################################################################################
#########################################################################################################################################
########################################################################################################################################
	# salva quanto scritto in un file di testo (tasto "Save as")

###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
	# cancella l'elemento solo se è una misura, non un'osservabile (tasto "Delete paper" del popup menu)
	def delete_item(self):
		j = 0
		lenght = len(self.item_identified)
		while j<10:
			if self.tree_master.parent(self.item_identified) == 'm%i'%(j) :
				self.tree_master.delete(self.item_identified)
				if lenght == 4 :
					letter = self.item_identified[3]
					del self.measures['m%i'%(j)]['p%s'%(letter)]
				if lenght == 5 :
					letter1 = self.item_identified[3]
					letter2 = self.item_identified[4]
					del self.measures['m%i'%(j)]['p%s%s'%(letter1,letter2)]

				self.n_papers_list[j] = self.n_papers_list[j]-1

			else:
				messagebox.showerror("Error", "You can't delete this item")
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
	# aggiunge una misura (tasto "Add measure")
	def add_measure(self,n):
		# GAhh
		if n == 0 :
			self.measure_type = 0
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('GAhh')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="a_ADS_K_KPi:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="a_ADS_K_KPi statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="a_ADS_K_KPi systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_KK:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_KK statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_KK systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_PiPi:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_PiPi statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_PiPi systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KPi:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KPi statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KPi systematic uncertainty:").grid(row=12,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_KPi:").grid(row=13,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_KPi statistical uncertainty:").grid(row=14,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_KPi systematic uncertainty:").grid(row=15,sticky=E)
			Label(self.add_measure_window,text="r_CP_KK :").grid(row=16,sticky=E)
			Label(self.add_measure_window,text="r_CP_KK statistical uncertainty:").grid(row=17,sticky=E)
			Label(self.add_measure_window,text="r_CP_KK systematic uncertainty:").grid(row=18,sticky=E)
			Label(self.add_measure_window,text="r_CP_PiPi:").grid(row=19,sticky=E)
			Label(self.add_measure_window,text="r_CP_PiPi statistical uncertainty:").grid(row=20,sticky=E)
			Label(self.add_measure_window,text="r_CP_PiPi systematic uncertainty:").grid(row=21,sticky=E)

			Label(self.add_measure_window,text='Statistical correlation matrix').grid(row=0,column=2,columnspan=8)
			Label(self.add_measure_window,text="a_ADS_K_KPi").grid(row=1,column=3)
			Label(self.add_measure_window,text="a_CP_DK_KK").grid(row=1,column=4)
			Label(self.add_measure_window,text="a_CP_DK_KPi").grid(row=1,column=5)
			Label(self.add_measure_window,text="a_fav_DK_KPi").grid(row=1,column=6)
			Label(self.add_measure_window,text="r_ADS_K_KPi").grid(row=1,column=7)
			Label(self.add_measure_window,text="r_CP_KK").grid(row=1,column=8)
			Label(self.add_measure_window,text="r_CP_PiPi").grid(row=1,column=9)
			Label(self.add_measure_window,text="a_ADS_K_KPi").grid(row=2,column=2)
			Label(self.add_measure_window,text="a_CP_DK_KK").grid(row=3,column=2)
			Label(self.add_measure_window,text="a_CP_DK_KPi").grid(row=4,column=2)
			Label(self.add_measure_window,text="a_fav_DK_KPi").grid(row=5,column=2)
			Label(self.add_measure_window,text="r_ADS_K_KPi").grid(row=6,column=2)
			Label(self.add_measure_window,text="r_CP_KK").grid(row=7,column=2)
			Label(self.add_measure_window,text="r_CP_PiPi").grid(row=8,column=2)
			Label(self.add_measure_window,text='Systematic correlation matrix').grid(row=11,column=2,columnspan=8)
			Label(self.add_measure_window,text="a_ADS_K_KPi").grid(row=12,column=3)
			Label(self.add_measure_window,text="a_CP_DK_KK").grid(row=12,column=4)
			Label(self.add_measure_window,text="a_CP_DK_KPi").grid(row=12,column=5)
			Label(self.add_measure_window,text="a_fav_DK_KPi").grid(row=12,column=6)
			Label(self.add_measure_window,text="r_ADS_K_KPi").grid(row=12,column=7)
			Label(self.add_measure_window,text="r_CP_KK").grid(row=12,column=8)
			Label(self.add_measure_window,text="r_CP_PiPi").grid(row=12,column=9)
			Label(self.add_measure_window,text="a_ADS_K_KPi").grid(row=13,column=2)
			Label(self.add_measure_window,text="a_CP_DK_KK").grid(row=14,column=2)
			Label(self.add_measure_window,text="a_CP_DK_KPi").grid(row=15,column=2)
			Label(self.add_measure_window,text="a_fav_DK_KPi").grid(row=16,column=2)
			Label(self.add_measure_window,text="r_ADS_K_KPi").grid(row=17,column=2)
			Label(self.add_measure_window,text="r_CP_KK").grid(row=18,column=2)
			Label(self.add_measure_window,text="r_CP_PiPi").grid(row=19,column=2)
			# entries per permettere all'utente di digitare
			i=0
			j=0
			k=0
			l=0
			m=0
			while i<22:
				self.entry_list.append(Entry(self.add_measure_window,width=10))
				self.entry_list[i].grid(row=i,column=1)
				i=i+1
			while j<7:
				while k<7:
					self.entry_list.append(Entry(self.add_measure_window,width=10))
					self.entry_list[i].grid(row=j+2,column=k+3)
					i=i+1
					k=k+1
				k=0
				j=j+1
			while l<7:
				while m<7:
					self.entry_list.append(Entry(self.add_measure_window,width=10))					
					self.entry_list[i].grid(row=l+13,column=m+3)
					i=i+1
					m=m+1
				m=0
				l=l+1
			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=24,columnspan=2,rowspan=5,pady=10)


		# ggsz
		if n == 1 :
			self.measure_type = 1
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('ggsz')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="X+:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="X+ statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="X+ systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="X-:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="X- statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="X- systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="Y+:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="Y+ statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="Y+ systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="Y-:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="Y- statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="Y- systematic uncertainty:").grid(row=12,sticky=E)

			Label(self.add_measure_window,text='Statistical correlation matrix').grid(row=0,column=2,columnspan=8)
			Label(self.add_measure_window,text="X+").grid(row=1,column=3)
			Label(self.add_measure_window,text="X-").grid(row=1,column=4)
			Label(self.add_measure_window,text="Y+").grid(row=1,column=5)
			Label(self.add_measure_window,text="Y-").grid(row=1,column=6)
			Label(self.add_measure_window,text="X+").grid(row=2,column=2)
			Label(self.add_measure_window,text="X-").grid(row=3,column=2)
			Label(self.add_measure_window,text="Y+").grid(row=4,column=2)
			Label(self.add_measure_window,text="Y-").grid(row=5,column=2)
			Label(self.add_measure_window,text='Systematic correlation matrix').grid(row=11,column=2,columnspan=8)
			Label(self.add_measure_window,text="X+").grid(row=12,column=3)
			Label(self.add_measure_window,text="X-").grid(row=12,column=4)
			Label(self.add_measure_window,text="Y+").grid(row=12,column=5)
			Label(self.add_measure_window,text="Y-").grid(row=12,column=6)
			Label(self.add_measure_window,text="X+").grid(row=13,column=2)
			Label(self.add_measure_window,text="X-").grid(row=14,column=2)
			Label(self.add_measure_window,text="Y+").grid(row=15,column=2)
			Label(self.add_measure_window,text="Y-").grid(row=16,column=2)
			# entries per permettere all'utente di digitare
			i=0
			j=0
			k=0
			l=0
			m=0
			while i<13:
				self.entry_list.append(Entry(self.add_measure_window,width=10))
				self.entry_list[i].grid(row=i,column=1)
				i=i+1
			while j<4:
				while k<4:
					self.entry_list.append(Entry(self.add_measure_window,width=10))
					self.entry_list[i].grid(row=j+2,column=k+3)
					i=i+1
					k=k+1
				k=0
				j=j+1
			while l<4:
				while m<4:
					self.entry_list.append(Entry(self.add_measure_window,width=10))					
					self.entry_list[i].grid(row=l+13,column=m+3)
					i=i+1
					m=m+1
				m=0
				l=l+1
			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=15,columnspan=2,rowspan=5,pady=10)


		# GAhhhh
		if n == 2 :
			self.measure_type = 2
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('GAhhhh')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_4Pi:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_4Pi statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_4Pi systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi systematic uncertainty:").grid(row=12,sticky=E)
			Label(self.add_measure_window,text="r_CP_4Pi:").grid(row=13,sticky=E)
			Label(self.add_measure_window,text="r_CP_4Pi statistical uncertainty:").grid(row=14,sticky=E)
			Label(self.add_measure_window,text="r_CP_4Pi systematic uncertainty:").grid(row=15,sticky=E)

			Label(self.add_measure_window,text='Statistical correlation matrix').grid(row=0,column=2,columnspan=8)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi").grid(row=1,column=3)
			Label(self.add_measure_window,text="a_CP_DK_4Pi").grid(row=1,column=4)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi").grid(row=1,column=5)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi").grid(row=1,column=6)
			Label(self.add_measure_window,text="r_CP_4Pi").grid(row=1,column=7)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi").grid(row=2,column=2)
			Label(self.add_measure_window,text="a_CP_DK_4Pi").grid(row=3,column=2)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi").grid(row=4,column=2)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi").grid(row=5,column=2)
			Label(self.add_measure_window,text="r_CP_4Pi").grid(row=6,column=2)
			Label(self.add_measure_window,text='Systematic correlation matrix').grid(row=11,column=2,columnspan=8)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi").grid(row=12,column=3)
			Label(self.add_measure_window,text="a_CP_DK_4Pi").grid(row=12,column=4)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi").grid(row=12,column=5)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi").grid(row=12,column=6)
			Label(self.add_measure_window,text="r_CP_4Pi").grid(row=12,column=7)
			Label(self.add_measure_window,text="a_ADS_K_K3Pi").grid(row=13,column=2)
			Label(self.add_measure_window,text="a_CP_DK_4Pi").grid(row=14,column=2)
			Label(self.add_measure_window,text="a_fav_DK_K3Pi").grid(row=15,column=2)
			Label(self.add_measure_window,text="r_ADS_K_K3Pi").grid(row=16,column=2)
			Label(self.add_measure_window,text="r_CP_4Pi").grid(row=17,column=2)
			# entries per permettere all'utente di digitare
			i=0
			j=0
			k=0
			l=0
			m=0
			while i<16:
				self.entry_list.append(Entry(self.add_measure_window,width=10))
				self.entry_list[i].grid(row=i,column=1)
				i=i+1
			while j<5:
				while k<5:
					self.entry_list.append(Entry(self.add_measure_window,width=10))
					self.entry_list[i].grid(row=j+2,column=k+3)
					i=i+1
					k=k+1
				k=0
				j=j+1
			while l<5:
				while m<5:
					self.entry_list.append(Entry(self.add_measure_window,width=10))					
					self.entry_list[i].grid(row=l+13,column=m+3)
					i=i+1
					m=m+1
				m=0
				l=l+1
			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=18,columnspan=2,rowspan=5,pady=10)


		# ADhhpi0
		if n == 3 :
			self.measure_type = 3
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('ADhhpi0')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="a_ADS_DK_KPiPi0:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="a_ADS_DK_KPiPi0 statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="a_ADS_DK_KPiPi0 systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_KKPi0:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_KKPi0 statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_KKPi0 systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_PiPiPi0:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_PiPiPi0 statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="a_CP_DK_PiPiPi0 systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KPiPi0:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KPiPi0 statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KPiPi0 systematic uncertainty:").grid(row=12,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_KPiPi0:").grid(row=13,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_KPiPi0 statistical uncertainty:").grid(row=14,sticky=E)
			Label(self.add_measure_window,text="r_ADS_K_KPiPi0 systematic uncertainty:").grid(row=15,sticky=E)
			Label(self.add_measure_window,text="r_CP_KKPi0:").grid(row=16,sticky=E)
			Label(self.add_measure_window,text="r_CP_KKPi0 statistical uncertainty:").grid(row=17,sticky=E)
			Label(self.add_measure_window,text="r_CP_KKPi0 systematic uncertainty:").grid(row=18,sticky=E)
			Label(self.add_measure_window,text="r_CP_PiPiPi0:").grid(row=19,sticky=E)
			Label(self.add_measure_window,text="r_CP_PiPiPi0 statistical uncertainty:").grid(row=20,sticky=E)
			Label(self.add_measure_window,text="r_CP_PiPiPi0 systematic uncertainty:").grid(row=21,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=24,columnspan=2,rowspan=5,pady=10)


		# GLS
		if n == 4 :
			self.measure_type = 4
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('GLS')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="r_DK_fos_Ks_KPi:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="r_DK_fos_Ks_KPi statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="r_DK_fos_Ks_KPi systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KsKPi:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KsKPi statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK_KsKPi systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="a_sup_DK_KsKPi:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="a_sup_DK_KsKPi statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="a_sup_DK_KsKPi systematic uncertainty:").grid(row=9,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=12,columnspan=2,rowspan=5,pady=10)


		# GAKPiPiDhh
		if n == 5 :
			self.measure_type = 5
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('GAKPiPiDhh')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="r_CP_DKPiPi:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="r_CP_DKPiPi statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="r_CP_DKPiPi systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="a_fav_DKPiPi_KPi:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="a_fav_DKPiPi_KPi statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="a_fav_DKPiPi_KPi systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="a_CP_DKPiPi_KK:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="a_CP_DKPiPi_KK statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="a_CP_DKPiPi_KK systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="a_CP_DKPiPi_PiPi:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="a_CP_DKPiPi_PiPi statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="a_CP_DKPiPi_PiPi systematic uncertainty:").grid(row=12,sticky=E)
			Label(self.add_measure_window,text="r_plus_DKPiPi_KPi:").grid(row=13,sticky=E)
			Label(self.add_measure_window,text="r_plus_DKPiPi_KPi statistical uncertainty:").grid(row=14,sticky=E)
			Label(self.add_measure_window,text="r_plus_DKPiPi_KPi systematic uncertainty:").grid(row=15,sticky=E)
			Label(self.add_measure_window,text="r_minus_DKPiPi_KPi:").grid(row=16,sticky=E)
			Label(self.add_measure_window,text="r_minus_DKPiPi_KPi statistical uncertainty:").grid(row=17,sticky=E)
			Label(self.add_measure_window,text="r_minus_DKPiPi_KPi systematic uncertainty:").grid(row=18,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=21,columnspan=2,rowspan=5,pady=10)


		# BsDsK
		if n == 6 :
			self.measure_type = 6
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('BsDsK')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="C:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="C statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="C systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="D_f:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="D_f statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="D_f systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="D_bar_f:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="D_bar_f statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="D_bar_f systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="S_f:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="S_f statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="S_f systematic uncertainty:").grid(row=12,sticky=E)
			Label(self.add_measure_window,text="S_bar_f:").grid(row=13,sticky=E)
			Label(self.add_measure_window,text="S_bar_f statistical uncertainty:").grid(row=14,sticky=E)
			Label(self.add_measure_window,text="S_bar_f systematic uncertainty:").grid(row=15,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=18,columnspan=2,rowspan=5,pady=10)


		# GABDK*
		if n == 7 :
			self.measure_type = 7
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('GABDK*')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK*0_KPi:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK*0_KPi statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="a_fav_DK*0_KPi systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="r_plus_DK*0_KPi:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="r_plus_DK*0_KPi statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="r_plus_DK*0_KPi systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="r_minus_DK*0_KPi:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="r_minus_DK*0_KPi statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="r_minus_DK*0_KPi systematic uncertainty:").grid(row=9,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=12,columnspan=2,rowspan=5,pady=10)


		# ggszDKPi
		if n == 8 :
			self.measure_type = 8
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('ggszDKPi')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="X+:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="X+ statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="X+ systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="X-:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="X- statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="X- systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="Y+:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="Y+ statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="Y+ systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="Y-:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="Y- statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="Y- systematic uncertainty:").grid(row=12,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=15,columnspan=2,rowspan=5,pady=10)


		# ggszDK*0
		if n == 9 :
			self.measure_type = 9
			# finestra
			self.add_measure_window = Tk()											
			self.add_measure_window.geometry('+700+200')									
			self.add_measure_window.title('ggszDK*0')
			# etichette
			Label(self.add_measure_window,text="Year:").grid(row=0,sticky=E)
			Label(self.add_measure_window,text="X+:").grid(row=1,sticky=E)
			Label(self.add_measure_window,text="X+ statistical uncertainty:").grid(row=2,sticky=E)
			Label(self.add_measure_window,text="X+ systematic uncertainty:").grid(row=3,sticky=E)
			Label(self.add_measure_window,text="X-:").grid(row=4,sticky=E)
			Label(self.add_measure_window,text="X- statistical uncertainty:").grid(row=5,sticky=E)
			Label(self.add_measure_window,text="X- systematic uncertainty:").grid(row=6,sticky=E)
			Label(self.add_measure_window,text="Y+:").grid(row=7,sticky=E)
			Label(self.add_measure_window,text="Y+ statistical uncertainty:").grid(row=8,sticky=E)
			Label(self.add_measure_window,text="Y+ systematic uncertainty:").grid(row=9,sticky=E)
			Label(self.add_measure_window,text="Y-:").grid(row=10,sticky=E)
			Label(self.add_measure_window,text="Y- statistical uncertainty:").grid(row=11,sticky=E)
			Label(self.add_measure_window,text="Y- systematic uncertainty:").grid(row=12,sticky=E)
			# entries per permettere all'utente di digitare

			# bottone di inserimento
			enter_button1=Button(self.add_measure_window,text='ENTER',command=self.update_tree_mes).grid(row=15,columnspan=2,rowspan=5,pady=10)




		self.add_measure_window.mainloop()
#######################################################################################################################################
	# carica quanto scritto nel tree (bottone "ENTER")
	def update_tree_mes(self):
		# ciclo che controlla se tutti i campi sono stati riempiti
		field_variable = TRUE
		for s in self.entry_list:
			if s.get() == '':
				field_variable = FALSE 

		# se anche solo un campo è vuoto si apre la finestra di errore, altrimenti reiempie il tree (e aggiorna il dict)
		if field_variable == FALSE:
			messagebox.showerror("Error", "You didn't fill all the fields")	
			
		else:
			ob_local = 0
			# GAhh
			if self.measure_type == 0 :
				# aggiorna il dict
				self.update_dict_measures(0,self.n_papers_list[0])

				# aggiorna il tree
				self.tree_master.insert('m0','end',iid='m0p%i'%(self.n_papers_list[0]),text='%s'%(self.measures['m0']['p%i'%(self.n_papers_list[0])]['date']))

				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='a_ADS_K_KPi',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])
				ob_local = ob_local+1
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='a_CP_DK_KK',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])
				ob_local = ob_local+1
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='a_CP_DK_PiPi',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])
				ob_local = ob_local+1
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='a_fav_DK_KPi',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])
				ob_local = ob_local+1
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='r_ADS_K_KPi',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])
				ob_local = ob_local+1
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='r_CP_KK',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])
				ob_local = ob_local+1
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='r_CP_PiPi',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['value'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Statistical Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['stat'])
				self.tree_master.insert('m0p%i'%(self.n_papers_list[0]),'end',text='Systematic Uncertainty',values=self.measures['m0']['p%i'%(self.n_papers_list[0])]['ob%i'%(ob_local)]['sys'])



				

			ob_local = 0
			self.n_papers_list[self.measure_type] = self.n_papers_list[self.measure_type]+1
			self.number_mes = self.number_mes+1
			del self.entry_list[:]		# svuota entry_list in vista del prossimo utilizzo
			self.add_measure_window.destroy()			
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
	# funzione che aggiorna il dizionario (di dizionari) python contenente misure, paper, obs ecc.
	def update_dict_measures(self,a,b) : # a numero di misura, b numero di paper //// n_paper_b
		count1 = 1
		count2 = 0
		count3 = 0
		count4 = 0
		n_obs_local = self.n_obs_list[a]
		n_matrix_elements_local = self.n_matrix_elements_list[a]
		
		self.measures['m%i'%(a)]['p%i'%(b)] = {}
		self.measures['m%i'%(a)]['p%i'%(b)]['corrStatp%i'%(b)] = []
		self.measures['m%i'%(a)]['p%i'%(b)]['corrSysp%i'%(b)] = [] 
		self.measures['m%i'%(a)]['p%i'%(b)]['date'] = self.entry_list[0].get()

		while count2 < n_obs_local :
			self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)] = {}
			self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)]['value'] = self.entry_list[count1].get()
			count1 = count1+1
			#print (self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)]['value'])
			self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)]['stat'] = self.entry_list[count1].get()
			count1 = count1+1
			#print (self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)]['stat'])		
			self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)]['sys'] = self.entry_list[count1].get()
			count1 = count1+1
			#print (self.measures['m%i'%(a)]['p%i'%(b)]['ob%i'%(count2)]['sys'])

			count2 = count2+1

			
		while count3 < n_matrix_elements_local :
			self.measures['m%i'%(a)]['p%i'%(b)]['corrStatp%i'%(b)].append(self.entry_list[count1].get())
			#print (self.measures['m%i'%(a)]['p%i'%(b)]['corrStatp%i'%(b)][count3]) 
			count3 = count3+1
			count1 = count1+1
				

		while count4 < n_matrix_elements_local :
			self.measures['m%i'%(a)]['p%i'%(b)]['corrSysp%i'%(b)].append(self.entry_list[count1].get())
			#print (self.measures['m%i'%(a)]['p%i'%(b)]['corrSysp%i'%(b)][count4]) 
			count4 = count4+1
			count1 = count1+1
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
