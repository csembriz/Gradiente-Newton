#!/usr/bin/py
# -*- coding: UTF-8 -*-
from gi.repository import Gtk

from Parse import *
from Ascenso import *
from conjugados import *

global builder, method

class Handler:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def Metodo(self, radiobutton):
		global method
		if radiobutton.get_active():
			method = Gtk.Buildable.get_name(radiobutton)

	def on_button1_clicked(self, button):
		global method
		
		texto_Entrada = builder.get_object("textview1").get_buffer().get_text(builder.get_object("textview1").get_buffer().get_start_iter(), builder.get_object("textview1").get_buffer().get_end_iter(),"\n")
		arg_Entrada = parseProblem(texto_Entrada)

		if method == "radiobutton1":
			try:
				Ascenso(arg_Entrada[0], arg_Entrada[1], arg_Entrada[2], arg_Entrada[3])
				arg_Salida = getDataSalida()
			except Exception as e:
				arg_Salida = "El programa tronó"
				print(e)

			builder.get_object("textview2").get_buffer().set_text(arg_Salida)
		elif method=="radiobutton2":
			try:
				conjugados(arg_Entrada[0], arg_Entrada[1], arg_Entrada[2], arg_Entrada[3])
				arg_Salida = getDataSalida()
			except Exception as e:
				arg_Salida = "El programa tronó"
				print(e)

			builder.get_object("textview2").get_buffer().set_text(arg_Salida)

	def on_button3_clicked(self, button):
		builder.get_object("textview1").get_buffer().set_text("")
		builder.get_object("textview2").get_buffer().set_text("")

	def on_button2_clicked(self, button):
		example = "Maximizar\n\
f(x1,x2) = -(x1-3)^2-5*(x2-2)^2\n\
p=(0,0)"
		builder.get_object("textview1").get_buffer().set_text(example)

builder = Gtk.Builder()
builder.add_from_file("vista.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()
method = "radiobutton1"


Gtk.main()