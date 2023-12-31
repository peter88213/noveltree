"""Provide a class for viewing and editing "Todo" chapter properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from noveltreelib.view.properties_window.basic_view import BasicView
from noveltreelib.widgets.label_entry import LabelEntry
from noveltreelib.widgets.my_string_var import MyStringVar
from novxlib.novx_globals import _


class ArcView(BasicView):
    """Class for viewing and editing arc properties.
    
    Adds to the right pane:
    - A "Short name" entry.
    - The number of normal sections assigned to this arc.
    - A button to remove all section assigments to this arc.
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            view: NoveltreeUi -- Reference to the user interface.
            parent -- Parent widget to display this widget.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        self._lastSelected = ''

        # 'Short name' entry.
        self._shortName = MyStringVar()
        self._shortNameEntry = LabelEntry(self._elementInfoWindow, text=_('Short name'), textvariable=self._shortName, lblWidth=22)
        self._shortNameEntry.pack(anchor='w')
        inputWidgets.append(self._shortNameEntry)
        self._shortNameEntry.entry.bind('<Return>', self.apply_changes)

        # Frame for arc specific widgets.
        self._arcFrame = ttk.Frame(self._elementInfoWindow)
        self._arcFrame.pack(fill='x')
        self._nrSections = ttk.Label(self._arcFrame)
        self._nrSections.pack(side='left')
        self._clearButton = ttk.Button(self._arcFrame, text=_('Clear section assignments'), command=self._remove_sections)
        self._clearButton.pack(padx=1, pady=2)
        inputWidgets.append(self._clearButton)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()

        # 'Short name' entry.
        self._element.shortName = self._shortName.get()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.arcs[elementId]
        super().set_data(elementId)

        # 'Arc name' entry.
        self._shortName.set(self._element.shortName)

        # Frame for arc specific widgets.
        if self._element.sections is not None:
            self._nrSections['text'] = f'{_("Number of sections")}: {len(self._element.sections)}'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_button_bar()

    def _remove_sections(self):
        """Remove all section references.
        
        Remove also all section associations from the children points.
        """
        if self._ui.ask_yes_no(f'{_("Remove all sections from the story arc")} "{self._element.shortName}"?'):
            # Remove section back references.
            if self._element.sections:
                self.doNotUpdate = True
                for scId in self._element.sections:
                    self._mdl.novel.sections[scId].scArcs.remove(self._elementId)
                for tpId in self._mdl.novel.tree.get_children(self._elementId):
                    scId = self._mdl.novel.turningPoints[tpId].sectionAssoc
                    if scId is not None:
                        del(self._mdl.novel.sections[scId].scTurningPoints[tpId])
                        self._mdl.novel.turningPoints[tpId].sectionAssoc = None
                self._element.sections = []
                self.set_data(self._elementId)
                self.doNotUpdate = False

