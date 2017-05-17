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
import os
#################################################################################################################################### ########## Classi e Funzioni #################################################################################################### #################################################################################################################################
class Database:
############## membri ##########################################################################################################
################################################################################################################################
#################################################################################################################################
	# lista di variabili che rappresentano il numero di paper per ogni tipo di misura (si aggiorna ad ogni aggiunta)
	number_of_papers_list = [0,0,0,0,0,0,0,0,0,0]
	# liste degli entries
	entry_list = []
	entry_list_stat = []
	entry_list_sys = []
	# lista coi nomi delle misure
	measures_names = ['GAhh','ggsz','GAhhhh','ADhhPi0','GLS','GAKPiPiDhh','BsDsK','GABDK*','ggszDKPi','ggszDK*0']
	# lista coi nomi delle osservabili
	observables_names = [[],[],[],[],[],[],[],[],[],[]]
	observables_names[0] =  ['a_ADS_K_KPi','a_CP_DK_KK','a_CP_DK_PiPi','a_fav_DK_KPi','r_ADS_K_KPi','r_CP_KK','r_CP_PiPi']
	observables_names[1] = ['X+','X-','Y+','Y-']		
	observables_names[2] = ['a_ADS_K_K3Pi','a_CP_DK_4Pi','a_fav_DK_K3Pi','r_ADS_K_K3Pi','r_CP_4Pi']
	observables_names[3] = ['a_ADS_DK_KPiPi0','a_CP_DK_KKPi0','a_CP_DK_PiPiPi0','a_fav_DK_KPiPi0', 'r_ADS_K_KPiPi0','r_CP_KKPi0','r_CP_PiPiPi0']
	observables_names[4] = ['r_DK_fos_Ks_KPi','a_fav_DK_KsKPi','a_sup_DK_KsKPi']
	observables_names[5] = ['r_CP_DKPiPi','a_fav_DKPiPi_KPi','a_CP_DKPiPi_KK','a_CP_DKPiPi_PiPi','r_plus_DKPiPi_KPi','r_minus_DKPiPi_KPi']
	observables_names[6] = ['C','D_f','D_bar_f','S_f','S_bar_f']
	observables_names[7] = ['a_fav_DK*0_KPi','r_plus_DK*0_KPi','r_minus_DK*0_KPi']
	observables_names[8] = ['X+','X-','Y+','Y-']
	observables_names[9] = ['X+','X-','Y+','Y-']
	# dictionary dei dieci tipi di misure
	measures = {}
	for measure_name in measures_names:
		measures[measure_name] = {}
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

		for name in self.measures_names :
			self.tree_master.insert('','end',iid=name,text=name)

		self.tree_master.pack(fill=BOTH,expand=1)
#####################################################################################################################################
#####################################################################################################################################
	# crea il popup menu e lo associa al pulsante destro del mouse
	def make_popup(self,parent):
		# Crea il popup menu che si apre quando seleziono un elemento del tree
		self.popup = Menu(parent, tearoff=0)
		self.popup.add_command(label='Delete paper',command=self.delete_paper)
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
		self.menu_actions.add_command(label='Import JSON file',command=self.import_data)
		self.menu_actions.add_command(label='Save all as JSON',command=self.export_as_json)
		self.menu_actions.add_command(label='Create your JSON file',command=self.create_custom_file)
		self.menu_actions.add_command(label='Quit',command=parent.destroy)

		for meas in self.measures_names:
			self.menu_add.add_command(label=meas,command=lambda meas=meas:self.add_paper(meas))

		parent.config(menu=self.barra_menu)
#######################################################################################################################################
########################################################################################################################################
########################################################################################################################################
## da qui tutti i metodi che non compaiono nel costruttore, ma solo come comandi o simili ##############################################
########################################################################################################################################
#########################################################################################################################################
########################################################################################################################################
	# reinserisce i dati inseriti precedentemente a partire da all_measures.json
	def import_data(self):
		# finestra di dialogo per far scegliere il file da aprire
		json_file = askopenfile(mode='r',defaultextension='.json',filetypes=[("JSON Files", "*.json")],title='Import')
		# ricostruisce il dizionario measures, con la condizione che il file json non sia vuoto
		if os.stat('all_measures.json').st_size > 0:
			self.measures = json.load(json_file)
			# aggiorna il numero di paper per ogni misura (elementi di number_of_papers_list)
			for measure in self.measures_names:
				self.number_of_papers_list[self.measures_names.index(measure)] = len(self.measures[measure])
			# scrive nel tree
			for name in self.measures_names:
				count_paper = 0
				while count_paper <= self.number_of_papers_list[self.measures_names.index(name)]:
					if '%s_paper_%i'%(name,count_paper) in self.measures[name]:
						self.update_only_tree (self.measures_names.index(name),count_paper)
					count_paper=count_paper+1
		json_file.close()

		#print (self.number_of_papers_list[0:11])
		#print (self.measures)
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
	# esporta il dictionary con le misure nel file JSON
	def export_as_json (self):
		json_file = asksaveasfile(mode='w',defaultextension='.json',filetypes=[("JSON Files", "*.json")],title='Save as')
		json.dump(self.measures,json_file,sort_keys = True,indent = 4)
		json_file.close()	
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
	# cancella l'elemento solo se è una misura, non un'osservabile (tasto "Delete paper" del popup menu)
	def delete_paper(self):
		check_variable = False
		for name in self.measures_names:
			if self.tree_master.parent(self.item_identified) == name:
				check_variable = True
		if check_variable == True:
			self.tree_master.delete(self.item_identified)
			del self.measures[self.tree_master.parent(self.item_identified)][self.item_identified]
			self.number_of_papers_list[j] = self.number_of_papers_list[j]-1
		else:
			messagebox.showerror("Error", "You can't delete this item")
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
	# apre finestra per aggiungere un paper (tasto "Add paper")
	def add_paper(self,name):
		self.glob_var_name = name # variabile globale che assume il valore del nome della misura, per utilizzo in altre funzioni
		# finestra
		self.add_paper_window = Tk()											
		self.add_paper_window.geometry('+700+200')									
		self.add_paper_window.title(name)
		# etichette ed entries
		self.labels(self.measures_names.index(name))
		# bottone di inserimento
		self.add_paper_button()

		self.add_paper_window.mainloop()
#######################################################################################################################################
	# carica quanto scritto nel tree (bottone "ENTER")
	def update_tree_and_dictionary(self): 
		# ciclo che controlla se tutti i campi sono stati riempiti
		field_variable = TRUE
		for s in self.entry_list:
			if s.get() == '':
				field_variable = FALSE 

		# se anche solo un campo è vuoto si apre la finestra di errore, altrimenti reiempie il tree (e aggiorna il dict)
		if field_variable == FALSE:
			messagebox.showerror("Error", "You didn't fill all the fields")	
			
		else:
			self.update_dict_measures(self.measures_names.index(self.glob_var_name),self.number_of_papers_list[self.measures_names.index(self.glob_var_name)])
			self.update_only_tree(self.measures_names.index(self.glob_var_name),self.number_of_papers_list[self.measures_names.index(self.glob_var_name)])

			self.number_of_papers_list[self.measures_names.index(self.glob_var_name)] = self.number_of_papers_list[self.measures_names.index(self.glob_var_name)]+1
			#print (self.number_of_papers_list[self.measures_names.index(self.glob_var_name)])
			del self.entry_list[:]		# svuota entry_list in vista del prossimo utilizzo
			del self.entry_list_stat[:]
			del self.entry_list_sys[:] 
			self.add_paper_window.destroy()
#######################################################################################################################################
	def create_custom_file (self):
		messagebox.showinfo("Add papers", "Double-click the papers you want in your JSON file, then press the Enter key")
		self.custom_measures = {} # dizionario custom sulla falsa riga di self.measures{}
		for measure_name in self.measures_names:
			self.custom_measures[measure_name] = {}
		self.custom_number_of_papers_list = [0,0,0,0,0,0,0,0,0,0]


		self.double_to_add = self.tree_master.bind("<Double-Button-1>", self.add_to_custom_dict)
		self.enter_to_save = self.tree_master.bind("<Return>",self.export_custom_json)

	def add_to_custom_dict (self, measure):
		self.item_identified = self.tree_master.identify_row(measure.y)
		check_variable = False
		for name in self.measures_names:
			if self.tree_master.parent(self.item_identified) == name:
				check_variable = True
		if check_variable == True:
			#copia il paper con tutti gli attributi dal dizionario principale a quello custom
			self.custom_measures[self.tree_master.parent(self.item_identified)]['%s_paper_%i'%(self.tree_master.parent(self.item_identified),self.custom_number_of_papers_list[self.measures_names.index(self.tree_master.parent(self.item_identified))])] = self.measures[self.tree_master.parent(self.item_identified)].get(self.item_identified)
			print (self.custom_measures[self.tree_master.parent(self.item_identified)]['%s_paper_%i'%(self.tree_master.parent(self.item_identified),self.custom_number_of_papers_list[self.measures_names.index(self.tree_master.parent(self.item_identified))])])
			self.custom_number_of_papers_list[self.measures_names.index(self.tree_master.parent(self.item_identified))] = self.custom_number_of_papers_list[self.measures_names.index(self.tree_master.parent(self.item_identified))]+1
		else:
			messagebox.showerror("Error", "You can choose only papers")

	def export_custom_json (self, event=None):
		json_file = asksaveasfile(mode='w',defaultextension='.json',filetypes=[("JSON Files", "*.json")],title='Save as')
		json.dump(self.custom_measures,json_file,sort_keys = True,indent = 4)
		json_file.close()
		for measure_name in self.measures_names:
			self.custom_measures[measure_name].clear()
		self.tree_master.unbind("<Double-Button-1>",self.double_to_add)
		self.tree_master.unbind("<Return>",self.enter_to_save)

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
	# metodo chiamato in add_paper per aggiungere labels ed entries
	def labels (self,a): # a è il numero corrispondente alla misura
		del self.entry_list[:]
		del self.entry_list_stat[:]
		del self.entry_list_sys[:]
		# etichette 
		Label(self.add_paper_window,text="Date").grid(row=0,sticky=E)
		Label(self.add_paper_window,text='Statistical correlation matrix').grid(row=0,column=2,columnspan=8)
		Label(self.add_paper_window,text='Systematic correlation matrix').grid(row=11,column=2,columnspan=8)

		count_entry1 = 0
		count_entry2 = 0
		for observable in self.observables_names[a] :
			Label(self.add_paper_window,text="%s"%(observable)).grid(row=count_entry1+1,sticky=E)
			count_entry1=count_entry1+1
			Label(self.add_paper_window,text="%s statistical uncertainty"%(observable)).grid(row=count_entry1+1, sticky=E)
			count_entry1=count_entry1+1
			Label(self.add_paper_window,text="%s systematic uncertainty"%(observable)).grid(row=count_entry1+1, sticky=E)
			count_entry1=count_entry1+1
			Label(self.add_paper_window,text="%s"%(observable)).grid(row=1,column=(count_entry2)+3)
			Label(self.add_paper_window,text="%s"%(observable)).grid(row=(count_entry2)+2,column=2)
			Label(self.add_paper_window,text="%s"%(observable)).grid(row=12,column=(count_entry2)+3)
			Label(self.add_paper_window,text="%s"%(observable)).grid(row=(count_entry2)+13,column=2)
			count_entry2=count_entry2+1
			
		# entries per permettere all'utente di digitare
		i=0
		while i<(count_entry1+1):
			self.entry_list.append(Entry(self.add_paper_window,width=13))
			self.entry_list[i].grid(row=i,column=1)
			i=i+1
		i=0
		for j in range(0,len(self.observables_names[a])):
			for k in range(0,len(self.observables_names[a])):
				self.entry_list_stat.append(Entry(self.add_paper_window,width=13))
				self.entry_list_stat[i].grid(row=j+2,column=k+3)
				self.entry_list_sys.append(Entry(self.add_paper_window,width=13))					
				self.entry_list_sys[i].grid(row=j+13,column=k+3)
				i=i+1
########################################################################################################################################
	# pulsante parametrico della finestra add_paper
	def add_paper_button (self):
		enter_button1=Button(self.add_paper_window,text='ENTER',command=self.update_tree_and_dictionary).grid(row=len(self.entry_list)+3, columnspan=2,rowspan=5,pady=10)
#########################################################################################################################################
	# come dice il nome, funzione chiamata da update_tree_and_dictionary per aggiornare contemporaneamente dizionario delle misure e tree
	def update_dict_measures (self,a,b): # a numero di misura, b numero di paper
		count_entry = 1
		
		self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)] = {}
		self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['corr_Stat_paper_%i'%(b)] = []
		self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['corr_Sys_paper_%i'%(b)] = [] 
		self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['%s_paper_%i_date'%(self.measures_names[a],b)] = self.entry_list[0].get()

		for observable in self.observables_names[a]:
			self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable] = {}
			self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['value'] = self.entry_list[count_entry].get()
			count_entry = count_entry+1
			#print (self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['value'])
			self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['stat'] = self.entry_list[count_entry].get()
			count_entry = count_entry+1
			#print (self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['stat'])		
			self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['sys'] = self.entry_list[count_entry].get()
			count_entry = count_entry+1
			#print (self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['sys'])

		for entry in self.entry_list_stat:
			self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['corr_Stat_paper_%i'%(b)].append(entry.get())
		#for element in self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['corr_Stat_paper_%i'%(b)]:
			#print (element) 

		for entry in self.entry_list_sys:
			self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['corr_Sys_paper_%i'%(b)].append(entry.get())
		#for element in self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['corr_Sys_paper_%i'%(b)]:
			#print (element) 
#########################################################################################################################################
	def update_only_tree (self,a,b): # a numero di misura, b numero di paper
		self.tree_master.insert(self.measures_names[a],'end',iid='%s_paper_%i'%(self.measures_names[a],b),text=self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)]['%s_paper_%i_date'%(self.measures_names[a],b)])
		for observable in self.observables_names[a]:
			self.tree_master.insert('%s_paper_%i'%(self.measures_names[a],b),'end',text=observable,values=self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['value'])
			self.tree_master.insert('%s_paper_%i'%(self.measures_names[a],b),'end',text='Statistical Uncertainty',values=self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['stat'])
			self.tree_master.insert('%s_paper_%i'%(self.measures_names[a],b),'end',text='Systematic Uncertainty',values=self.measures[self.measures_names[a]]['%s_paper_%i'%(self.measures_names[a],b)][observable]['sys'])
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
