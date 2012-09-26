#    Back In Time
#    Copyright (C) 2008-2009 Oprea Dan
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import os
import os.path
import sys
import copy
import pygtk
pygtk.require("2.0")
import gtk
import gobject
import datetime
import gettext

import config
import snapshots
import tools
import gnometools


_=gettext.gettext


def restore( parent, snapshot_id, what, where = '' ):
	RestoreDialog(parent, snapshot_id, what, where).run()


class RestoreDialog(object):
	
	def __init__( self, parent, snapshot_id, what, where = '' ):
		self.parent = parent
		self.config = parent.config
		self.snapshots = parent.snapshots
		self.snapshot_id = snapshot_id
		self.what = what
		self.where = where
		
		builder = gtk.Builder()
		self.builder = builder
		
		glade_file = os.path.join(self.config.get_app_path(), 'gnome', 'logviewdialog.glade')
		
		builder.add_from_file(glade_file)
		
		get = builder.get_object
		
		self.dialog = get('LogViewDialog')
		self.dialog.set_transient_for( parent.window )

		#log view
		self.txt_log_view = get( 'txt_log_view' )
		#self.txt_log_view.set_sensitive(False)

		#hide unused items 
		get('lbl_profile').hide()
		get('combo_profiles').hide()
		get('lbl_filter').hide()
		get('combo_filter').hide()
		get('hbox1').hide()
		get('label1').hide()
	
		#update title
		self.dialog.set_title( _('Restore') )

		#disable close
		self.btn_close = get('button3')	
		self.btn_close.set_sensitive(False)

		#
		self.buffer = ''
	
	def callback(self, line, *params ):
		self.buffer = self.buffer + line + "\n"
		self.txt_log_view.get_buffer().set_text(self.buffer)
        	gnometools.run_gtk_update_loop()

	def run( self ):
        	self.dialog.show()
        	gnometools.run_gtk_update_loop()
		self.snapshots.restore( self.snapshot_id, self.what, self.callback, self.where )
		self.btn_close.set_sensitive(True)
		self.dialog.run()
		self.dialog.destroy()


