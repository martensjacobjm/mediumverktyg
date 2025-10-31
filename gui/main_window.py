#!/usr/bin/env python3
"""
Main Window - ORC Fluid Analysis Tool
Coordinates all GUI panels and application logic
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gui.filter_panel import FilterPanel
from gui.results_panel import ResultsPanel
from gui.plot_panel import PlotPanel
from core.fluid_database import FluidDatabase
from core.scoring import FluidScorer, ScoringWeights
from export.pdf_generator import PDFReportGenerator
from export.csv_exporter import CSVExporter
from export.plot_exporter import PlotExporter
import threading
import os


class MainWindow:
    """Main application window coordinating all panels"""

    def __init__(self, root):
        self.root = root

        # Initialize backend
        print("Initializing database...")
        self.db = FluidDatabase(metadata_file='data/fluid_metadata_manual.json')

        print("Initializing scorer...")
        self.scorer = FluidScorer(T_hot=50, T_cold=20)

        # Current state
        self.current_scores = []
        self.selected_fluids = []  # For plotting

        # Create UI
        self._create_menu()
        self._create_layout()
        self._create_status_bar()

        # Initial load
        self.refresh_results()

        print("✓ GUI initialized successfully")

    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fil", menu=file_menu)
        file_menu.add_command(label="Exportera PDF rapport...", command=self.export_pdf)
        file_menu.add_command(label="Exportera CSV data...", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Avsluta", command=self.root.quit)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visa", menu=view_menu)
        view_menu.add_command(label="Återställ filter", command=self.reset_filters)
        view_menu.add_command(label="Uppdatera resultat", command=self.refresh_results)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hjälp", menu=help_menu)
        help_menu.add_command(label="Användarguide", command=self.show_user_guide)
        help_menu.add_command(label="Om programmet", command=self.show_about)

    def _create_layout(self):
        """Create main layout with panels"""

        # Create main container with horizontal panes
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left side: Filter panel
        self.filter_panel = FilterPanel(main_paned, on_filter_change=self.on_filter_change)
        main_paned.add(self.filter_panel, weight=1)

        # Right side: Vertical panes for results and plots
        right_paned = ttk.PanedWindow(main_paned, orient=tk.VERTICAL)
        main_paned.add(right_paned, weight=4)

        # Top right: Results panel
        self.results_panel = ResultsPanel(
            right_paned,
            on_selection_change=self.on_selection_change,
            on_sort=self.on_sort
        )
        right_paned.add(self.results_panel, weight=2)

        # Bottom right: Plot panel
        self.plot_panel = PlotPanel(right_paned)
        right_paned.add(self.plot_panel, weight=3)

    def _create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(
            self.status_bar,
            text="Klar",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.fluid_count_label = ttk.Label(
            self.status_bar,
            text="",
            relief=tk.SUNKEN,
            anchor=tk.E
        )
        self.fluid_count_label.pack(side=tk.RIGHT)

    def set_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def on_filter_change(self, filters):
        """Called when filters are changed"""
        self.set_status("Applicerar filter...")

        # Run filtering in background to keep UI responsive
        def filter_task():
            try:
                # Apply filters through database
                filtered_fluids = self.db.filter_fluids(
                    bp_range=filters.get('bp_range'),
                    gwp_max=filters.get('gwp_max'),
                    safety_classes=filters.get('safety_classes'),
                    pressure_range=filters.get('pressure_range'),
                    pressure_temp=50.0
                )

                # Score and rank
                if filtered_fluids:
                    self.current_scores = self.scorer.rank_fluids(filtered_fluids)
                else:
                    self.current_scores = []

                # Update UI (must be done in main thread)
                self.root.after(0, self._update_results_display)

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Filter Error",
                    f"Ett fel uppstod vid filtrering:\n{str(e)}"
                ))

        thread = threading.Thread(target=filter_task, daemon=True)
        thread.start()

    def _update_results_display(self):
        """Update results panel with current scores"""
        self.results_panel.update_results(self.current_scores)

        # Update status
        count = len(self.current_scores)
        total = len(self.db.get_all_fluids())
        self.fluid_count_label.config(text=f"{count} av {total} medier")
        self.set_status(f"Visning {count} medier")

    def on_selection_change(self, selected_fluids):
        """Called when fluid selection changes in results panel"""
        self.selected_fluids = selected_fluids

        if len(selected_fluids) > 0:
            self.set_status(f"{len(selected_fluids)} medier valda för jämförelse")
            # Update plots
            self.plot_panel.plot_comparison(selected_fluids, self.db)
        else:
            self.set_status("Ingen fluid vald")

    def on_sort(self, sort_column):
        """Called when results table is sorted"""
        # Results panel handles sorting internally
        pass

    def refresh_results(self):
        """Refresh all results (no filters)"""
        self.set_status("Laddar alla medier...")

        def load_task():
            try:
                all_fluids = self.db.get_all_fluids()
                self.current_scores = self.scorer.rank_fluids(all_fluids)
                self.root.after(0, self._update_results_display)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Load Error",
                    f"Kunde inte ladda medier:\n{str(e)}"
                ))

        thread = threading.Thread(target=load_task, daemon=True)
        thread.start()

    def reset_filters(self):
        """Reset all filters to defaults"""
        self.filter_panel.reset()
        self.refresh_results()

    def export_pdf(self):
        """Export results to PDF"""
        if not self.current_scores:
            messagebox.showwarning("Export PDF", "Inga resultat att exportera!")
            return

        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="orc_fluid_report.pdf"
        )

        if not filename:
            return  # User cancelled

        self.set_status("Genererar PDF-rapport...")

        def export_task():
            try:
                # Generate plots if fluids are selected
                plot_files = None
                if self.selected_fluids:
                    plot_exporter = PlotExporter()
                    base_name = filename.replace('.pdf', '')
                    plot_files = plot_exporter.export_all_plots(
                        self.selected_fluids,
                        self.db,
                        base_name
                    )

                # Generate PDF
                pdf_gen = PDFReportGenerator()
                pdf_gen.generate_report(
                    self.current_scores,
                    filename,
                    selected_fluids=self.selected_fluids,
                    plot_files=plot_files
                )

                self.root.after(0, lambda: messagebox.showinfo(
                    "Export klar",
                    f"PDF-rapport sparad:\n{filename}"
                ))
                self.root.after(0, lambda: self.set_status("PDF-export klar"))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Export fel",
                    f"Kunde inte skapa PDF:\n{str(e)}"
                ))
                self.root.after(0, lambda: self.set_status("Export misslyckades"))

        thread = threading.Thread(target=export_task, daemon=True)
        thread.start()

    def export_csv(self):
        """Export results to CSV"""
        if not self.current_scores:
            messagebox.showwarning("Export CSV", "Inga resultat att exportera!")
            return

        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="orc_fluid_data.csv"
        )

        if not filename:
            return  # User cancelled

        self.set_status("Exporterar till CSV...")

        try:
            # Export to CSV
            exporter = CSVExporter()
            exporter.export_scores(self.current_scores, filename)

            messagebox.showinfo(
                "Export klar",
                f"CSV-fil sparad:\n{filename}\n\n"
                f"Kan öppnas i Excel/LibreOffice"
            )
            self.set_status("CSV-export klar")

        except Exception as e:
            messagebox.showerror(
                "Export fel",
                f"Kunde inte skapa CSV:\n{str(e)}"
            )
            self.set_status("Export misslyckades")

    def show_user_guide(self):
        """Show user guide"""
        guide_text = """ORC FLUID ANALYSIS TOOL - ANVÄNDARGUIDE

1. FILTER (vänster panel)
   - Justera kokpunkt, GWP, tryck med sliders
   - Välj säkerhetsklasser (A1, A2L, B1, etc.)
   - Resultat uppdateras automatiskt

2. RESULTAT (övre höger panel)
   - Sorterbara kolumner (klicka på rubrik)
   - Välj flera medier för jämförelse (Ctrl+klick)
   - Färgkodning: Grön = bra, Röd = dålig

3. DIAGRAM (nedre höger panel)
   - Välj diagramtyp från dropdown
   - Visar jämförelse för valda medier
   - Kan exporteras som PNG

4. EXPORT
   - Fil → Exportera PDF för komplett rapport
   - Fil → Exportera CSV för Excel-analys

TIPS:
- R1233zd(E) är det bästa valet för hemmainstallation
- A1/A2L är säkraste klasserna
- GWP < 10 är miljövänligt
"""

        messagebox.showinfo("Användarguide", guide_text)

    def show_about(self):
        """Show about dialog"""
        about_text = """ORC WORKING FLUID ANALYSIS TOOL
Version 0.5.0

Dynamiskt verktyg för jämförelse av 79+ arbetsmedier
för Tesla-turbin ORC-system.

Features:
✓ 79 fluider från CoolProp-databasen
✓ Automatiska termodynamiska beräkningar
✓ TesTur-validerad turbindesign
✓ Intelligent rankingsystem
✓ Interaktiva filter och diagram

Utvecklad för:
- Examensarbeten
- Forskning inom ORC-system
- Industriella projekt
- Utbildning i termodynamik

Baserad på:
- CoolProp 7.1.0
- TesTur experimentdata
- ASHRAE säkerhetsstandarder

© 2025 - MIT License
"""

        messagebox.showinfo("Om programmet", about_text)


if __name__ == "__main__":
    # Test window standalone
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
