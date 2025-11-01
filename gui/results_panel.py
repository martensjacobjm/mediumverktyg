#!/usr/bin/env python3
"""
Results Panel - Sortable table of ranked fluids
Displays scored and ranked fluids with detailed information
"""

import tkinter as tk
from tkinter import ttk
from gui.fluid_detail_dialog import FluidDetailDialog


class ResultsPanel(ttk.Frame):
    """Results panel with sortable treeview table"""

    def __init__(self, parent, on_selection_change=None, on_sort=None, db=None):
        super().__init__(parent)

        self.on_selection_change = on_selection_change
        self.on_sort = on_sort
        self.db = db  # Database reference for detail dialog

        self.current_scores = []
        self.sort_column = None
        self.sort_reverse = False
        self.checked_fluids = set()  # Track checked fluids

        self._create_widgets()

    def _create_widgets(self):
        """Create table and controls"""

        # Title and info frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        title = ttk.Label(
            header_frame,
            text="RESULTAT",
            font=('Arial', 12, 'bold')
        )
        title.pack(side=tk.LEFT)

        # Selection buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Button(
            btn_frame,
            text="Välj alla",
            command=self._select_all,
            width=10
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            btn_frame,
            text="Avmarkera alla",
            command=self._deselect_all,
            width=12
        ).pack(side=tk.LEFT, padx=2)

        self.count_label = ttk.Label(
            header_frame,
            text="",
            font=('Arial', 10)
        )
        self.count_label.pack(side=tk.RIGHT)

        # Create treeview with scrollbars
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Define columns
        columns = (
            'select', 'rank', 'fluid', 'total', 'thermo', 'env', 'safety', 'econ',
            'gwp', 'ashrae', 'T_boil', 'p_50', 'hfg', 'pr'
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            selectmode='extended',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Define column headings and widths
        column_config = {
            'select': ('☐', 30),
            'rank': ('#', 40),
            'fluid': ('Fluid', 120),
            'total': ('Total', 60),
            'thermo': ('Termo', 60),
            'env': ('Miljö', 60),
            'safety': ('Säker', 60),
            'econ': ('Ekon', 60),
            'gwp': ('GWP', 60),
            'ashrae': ('Klass', 60),
            'T_boil': ('Tb@1atm', 70),
            'p_50': ('P@50°C', 70),
            'hfg': ('hfg', 70),
            'pr': ('PR', 60)
        }

        for col, (heading, width) in column_config.items():
            self.tree.heading(
                col,
                text=heading,
                command=lambda c=col: self._sort_by_column(c)
            )
            self.tree.column(col, width=width, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Bind click event for checkbox toggling
        self.tree.bind('<Button-1>', self._on_click)

        # Bind double-click to show detail dialog
        self.tree.bind('<Double-Button-1>', self._on_double_click)

        # Bind right-click to show detail dialog
        self.tree.bind('<Button-3>', self._on_right_click)

        # Instructions
        info = ttk.Label(
            self,
            text="Klicka på checkbox för att välja | Dubbelklick/högerklick på rad för FULL info | Klicka på kolumnrubrik för sortering",
            font=('Arial', 9, 'italic'),
            foreground='gray'
        )
        info.pack(pady=2)

    def update_results(self, scores):
        """Update table with new scores"""
        self.current_scores = scores

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add new items
        for score in scores:
            # Determine row tag based on total score
            if score.total_score >= 90:
                tag = 'excellent'
            elif score.total_score >= 80:
                tag = 'good'
            elif score.total_score >= 70:
                tag = 'moderate'
            else:
                tag = 'poor'

            # Format stars
            stars = '⭐' * min(5, int(score.total_score / 20) + 1)

            # Checkbox symbol
            checkbox = '☑' if score.fluid in self.checked_fluids else '☐'

            values = (
                checkbox,
                score.rank or '',
                f"{score.fluid} {stars}",
                f"{score.total_score:.1f}",
                f"{score.thermo_score:.1f}",
                f"{score.env_score:.1f}",
                f"{score.safety_score:.1f}",
                f"{score.econ_score:.1f}",
                score.gwp or '-',
                score.ashrae_class or '-',
                f"{score.T_boiling_1atm:.1f}" if score.T_boiling_1atm else '-',
                f"{score.pressure_50C:.2f}" if score.pressure_50C else '-',
                f"{score.hfg_50C:.1f}" if score.hfg_50C else '-',
                f"{score.pressure_ratio:.2f}" if score.pressure_ratio else '-'
            )

            self.tree.insert('', 'end', values=values, tags=(tag,))

        # Configure tags for coloring
        self.tree.tag_configure('excellent', background='#c8e6c9')  # Light green
        self.tree.tag_configure('good', background='#fff9c4')      # Light yellow
        self.tree.tag_configure('moderate', background='#ffe0b2')  # Light orange
        self.tree.tag_configure('poor', background='#ffccbc')      # Light red

        # Update count
        self.count_label.config(text=f"{len(scores)} medier")

    def _sort_by_column(self, col):
        """Sort table by column"""
        # Toggle sort direction if same column
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False

        # Get column index
        col_idx = self.tree['columns'].index(col)

        # Get all items with their values
        items = [
            (self.tree.set(item, col), item)
            for item in self.tree.get_children('')
        ]

        # Sort items
        def sort_key(x):
            val = x[0]
            # Try numeric sort first
            try:
                # Remove stars and extra characters
                val = val.split()[0].replace('⭐', '')
                return float(val)
            except:
                return val

        items.sort(key=sort_key, reverse=self.sort_reverse)

        # Rearrange items
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)

        # Update column heading to show sort direction
        for c in self.tree['columns']:
            heading = self.tree.heading(c)['text']
            # Remove existing arrows
            heading = heading.replace(' ▲', '').replace(' ▼', '')
            if c == col:
                heading += ' ▼' if self.sort_reverse else ' ▲'
            self.tree.heading(c, text=heading)

        if self.on_sort:
            self.on_sort(col)

    def _on_select(self, event):
        """Handle selection change - now uses checked fluids"""
        # Selection is now handled by checkboxes, not tree selection
        # Notify parent of checked fluids
        if self.on_selection_change:
            self.on_selection_change(list(self.checked_fluids))

    def get_selected_fluids(self):
        """Get list of currently checked fluids"""
        return list(self.checked_fluids)

    def _on_click(self, event):
        """Handle click on checkbox column"""
        region = self.tree.identify_region(event.x, event.y)
        if region != 'cell':
            return

        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)

        # Check if clicked on select column (column #0 = #1 in identify_column)
        if column == '#1' and item:
            values = self.tree.item(item)['values']
            fluid_with_stars = values[2]  # Column 2 is fluid name (after select and rank)
            fluid = fluid_with_stars.split()[0]

            # Toggle checkbox
            if fluid in self.checked_fluids:
                self.checked_fluids.remove(fluid)
            else:
                self.checked_fluids.add(fluid)

            # Update display
            self.update_results(self.current_scores)

            # Notify parent
            if self.on_selection_change:
                self.on_selection_change(list(self.checked_fluids))

    def _select_all(self):
        """Select all fluids"""
        for score in self.current_scores:
            self.checked_fluids.add(score.fluid)

        self.update_results(self.current_scores)

        if self.on_selection_change:
            self.on_selection_change(list(self.checked_fluids))

    def _deselect_all(self):
        """Deselect all fluids"""
        self.checked_fluids.clear()
        self.update_results(self.current_scores)

        if self.on_selection_change:
            self.on_selection_change(list(self.checked_fluids))

    def _on_double_click(self, event):
        """Handle double-click to show fluid details"""
        self._show_fluid_detail(event)

    def _on_right_click(self, event):
        """Handle right-click to show fluid details"""
        self._show_fluid_detail(event)

    def _show_fluid_detail(self, event):
        """Show detailed fluid information dialog"""
        # Check if database is available
        if not self.db:
            print("Warning: Database not available for detail view")
            return

        # Get clicked item
        item = self.tree.identify_row(event.y)
        if not item:
            return

        # Get fluid name from item
        values = self.tree.item(item)['values']
        if len(values) < 3:
            return

        fluid_with_stars = values[2]  # Column 2 is fluid name (after select and rank)
        fluid = fluid_with_stars.split()[0]  # Remove stars

        # Show detail dialog
        try:
            dialog = FluidDetailDialog(self, fluid, self.db)
            dialog.focus_set()
        except Exception as e:
            print(f"Error showing fluid details for {fluid}: {e}")


# Test standalone
if __name__ == "__main__":
    from core.scoring import FluidScore

    root = tk.Tk()
    root.title("Results Panel Test")
    root.geometry("1000x600")

    # Create test data
    test_scores = [
        FluidScore(
            fluid='R1233zd(E)', rank=1,
            thermo_score=100, env_score=100, safety_score=100, econ_score=64,
            total_score=96.4, gwp=7, ashrae_class='A1',
            T_boiling_1atm=18.3,
            pressure_50C=2.93, hfg_50C=177.3, pressure_ratio=2.71
        ),
        FluidScore(
            fluid='R245fa', rank=2,
            thermo_score=100, env_score=43, safety_score=80, econ_score=75,
            total_score=76.4, gwp=1030, ashrae_class='B1',
            T_boiling_1atm=15.1,
            pressure_50C=3.44, hfg_50C=175.9, pressure_ratio=2.80
        ),
        FluidScore(
            fluid='Isopentane', rank=3,
            thermo_score=100, env_score=100, safety_score=40, econ_score=90,
            total_score=87.0, gwp=5, ashrae_class='A3',
            T_boiling_1atm=27.8,
            pressure_50C=2.06, hfg_50C=325.3, pressure_ratio=2.06
        ),
    ]

    def on_select(fluids):
        print(f"Selected: {fluids}")

    panel = ResultsPanel(root, on_selection_change=on_select)
    panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    panel.update_results(test_scores)

    root.mainloop()
