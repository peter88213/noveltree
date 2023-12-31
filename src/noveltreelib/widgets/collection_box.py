"""Provide a widget for displaying and modifying a collection of list items.

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import ttk

from novxlib.novx_globals import _
import tkinter as tk


class CollectionBox(ttk.Frame):
    """A frame with a listbox and control buttons.
    
    Public instance variables:
        cList: tk.strVar -- Holds a list representing the collection.
        cListbox: tk.Listbox -- Displays the collection.
        btnOpen: ttk.Button -- Activatable button, not intended to modify the collection.
        btnAdd: ttk.Button -- Input widget, always active by default.
        btnRemove: ttk.Button -- Activatable input widget.
        inputWidgets -- List with references to the input widgets.
        
    The inputWidgets list can be used to lock the application, deactivating the input widgets.
    The activate_buttons() and deactivate_buttons() methods are intended for setting the 
    buttons' status from outsides, dependent on the list content and selection. So "Add" is always 
    meant to be active, whereas "Open" and "Remove" is only to be active when a list item is selected.
    """

    def __init__(
            self, master,
            cmdAdd=None, lblAdd=None,
            cmdOpen=None, lblOpen=None,
            cmdRemove=None, lblRemove=None,
            cmdActivate=None,
            **kw
            ):
        """Set up the listbox and the buttons.
        
        Optional arguments:
            cmdAdd -- Reference to the callback routine for the "Add" button.
                      If not set, the "Add" button is not available.
            lblAdd --  Optional alternative text on the "Add" button.
            cmdOpen -- Reference to the callback routine for the "Open" button.
                       Bound to the "Return" key and left mouse button doublecklick.
                       If not set, the "Add" button is not available.
            lblOpen -- Optional alternative text on the "Open" button.
            cmdRemove -- Reference to the callback routine for the "Remove" button.
                         Bound to the "Delete" key.
                         If not set, the "Remove" button is not available.
            lblRemove -- Optional alternative text on the "Remove" button.
            cmdActivate -- Reference to an external callback routine (optional)
                           Bound to listbox focus and selection.
        
        Extends the superclass constructor.
        """
        super().__init__(master, **kw)
        if cmdActivate is None:
            cmdActivate = self.activate_buttons

        buttonbar = ttk.Frame(self)
        buttonbar.pack(anchor='n', side='left', fill='x', padx=5)

        # Listbox.
        listFrame = ttk.Frame(self)
        listFrame.pack(side='right', fill='both', expand=True)
        self.cList = tk.StringVar()
        self.cListbox = tk.Listbox(listFrame, listvariable=self.cList, selectmode='single')
        vbar = ttk.Scrollbar(listFrame, orient='vertical', command=self.cListbox.yview)
        vbar.pack(side='right', fill='y')
        self.cListbox.pack(side='left', fill='both', expand=True)
        self.cListbox.config(yscrollcommand=vbar.set)

        self.cListbox.bind('<FocusIn>', cmdActivate)
        self.cListbox.bind('<<ListboxSelect>>', cmdActivate)

        # Buttons.
        self.inputWidgets = []

        # "Open" command.
        if lblOpen is None:
            label = _('Open')
        else:
            label = lblOpen
        self.btnOpen = ttk.Button(buttonbar, text=label, command=cmdOpen)
        if cmdOpen is not None:
            self.btnOpen.pack(fill='x', expand=True)
            self.cListbox.bind('<Double-1>', cmdOpen)
            self.cListbox.bind('<Return>', cmdOpen)

        # "Add" command.
        if lblAdd is None:
            label = _('Add')
        else:
            label = lblAdd
        self.btnAdd = ttk.Button(buttonbar, text=label, command=cmdAdd)
        if cmdAdd is not None:
            self.btnAdd.pack(fill='x', expand=True)
            self.inputWidgets.append(self.btnAdd)

        # "Remove" command.
        if lblRemove is None:
            label = _('Remove')
        else:
            label = lblRemove
        self.btnRemove = ttk.Button(buttonbar, text=label, command=cmdRemove)
        if cmdRemove is not None:
            self.btnRemove.pack(fill='x', expand=True)
            self.inputWidgets.append(self.btnRemove)
            self.cListbox.bind('<Delete>', cmdRemove)

    def activate_buttons(self, event=None):
        """Activate the group of activatable buttons."""
        self.btnOpen.config(state='normal')
        self.btnRemove.config(state='normal')

    def deactivate_buttons(self, event=None):
        """Deactivate the group of activatable buttons."""
        self.btnOpen.config(state='disabled')
        self.btnRemove.config(state='disabled')

