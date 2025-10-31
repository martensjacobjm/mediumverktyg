#!/usr/bin/env python3
"""
Filter Panel - Interactive filtering controls
Allows user to filter fluids by various criteria
"""

import tkinter as tk
from tkinter import ttk


class FilterPanel(ttk.Frame):
    """Filter panel with sliders and checkboxes"""

    def __init__(self, parent, on_filter_change=None):
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)

        self.on_filter_change = on_filter_change

        # Filter values
        self.bp_min = tk.DoubleVar(value=-50)
        self.bp_max = tk.DoubleVar(value=50)
        self.gwp_max = tk.IntVar(value=2000)
        self.p_min = tk.DoubleVar(value=0)
        self.p_max = tk.DoubleVar(value=20)

        # Safety class checkboxes
        self.safety_vars = {
            'A1': tk.BooleanVar(value=True),
            'A2L': tk.BooleanVar(value=True),
            'A2': tk.BooleanVar(value=True),
            'A3': tk.BooleanVar(value=True),
            'B1': tk.BooleanVar(value=True),
            'B2L': tk.BooleanVar(value=True),
            'B2': tk.BooleanVar(value=False),
            'B3': tk.BooleanVar(value=False),
        }

        self._create_widgets()

    def _create_widgets(self):
        """Create all filter widgets"""

        # Title
        title = ttk.Label(
            self,
            text="FILTER",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10)

        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)

        # Boiling point filter
        self._create_bp_filter()

        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, padx=5, pady=10)

        # GWP filter
        self._create_gwp_filter()

        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, padx=5, pady=10)

        # Pressure filter
        self._create_pressure_filter()

        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, padx=5, pady=10)

        # Safety class filter
        self._create_safety_filter()

        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, padx=5, pady=10)

        # Buttons
        self._create_buttons()

    def _create_bp_filter(self):
        """Boiling point range filter"""
        frame = ttk.LabelFrame(self, text="Kokpunkt @ 1 atm", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)

        # Min slider
        ttk.Label(frame, text="Min [°C]:").pack(anchor=tk.W)
        self.bp_min_scale = tk.Scale(
            frame,
            from_=-50, to=50,
            orient=tk.HORIZONTAL,
            variable=self.bp_min,
            command=self._on_filter_update,
            resolution=5
        )
        self.bp_min_scale.pack(fill=tk.X)

        # Max slider
        ttk.Label(frame, text="Max [°C]:").pack(anchor=tk.W, pady=(10, 0))
        self.bp_max_scale = tk.Scale(
            frame,
            from_=-50, to=100,
            orient=tk.HORIZONTAL,
            variable=self.bp_max,
            command=self._on_filter_update,
            resolution=5
        )
        self.bp_max_scale.pack(fill=tk.X)

        # Current range label
        self.bp_label = ttk.Label(frame, text="")
        self.bp_label.pack(pady=(5, 0))
        self._update_bp_label()

    def _create_gwp_filter(self):
        """GWP maximum filter"""
        frame = ttk.LabelFrame(self, text="Max GWP (Global Warming Potential)", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)

        self.gwp_scale = tk.Scale(
            frame,
            from_=0, to=2000,
            orient=tk.HORIZONTAL,
            variable=self.gwp_max,
            command=self._on_filter_update,
            resolution=50
        )
        self.gwp_scale.pack(fill=tk.X)

        # Preset buttons
        preset_frame = ttk.Frame(frame)
        preset_frame.pack(pady=(5, 0))

        ttk.Button(
            preset_frame,
            text="< 10 (Utmärkt)",
            command=lambda: self.set_gwp(10),
            width=15
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            preset_frame,
            text="< 100 (Bra)",
            command=lambda: self.set_gwp(100),
            width=15
        ).pack(side=tk.LEFT, padx=2)

        # Current value label
        self.gwp_label = ttk.Label(frame, text="")
        self.gwp_label.pack(pady=(5, 0))
        self._update_gwp_label()

    def _create_pressure_filter(self):
        """Pressure range @ 50°C filter"""
        frame = ttk.LabelFrame(self, text="Tryck @ 50°C [bar]", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)

        # Min slider
        ttk.Label(frame, text="Min:").pack(anchor=tk.W)
        self.p_min_scale = tk.Scale(
            frame,
            from_=0, to=20,
            orient=tk.HORIZONTAL,
            variable=self.p_min,
            command=self._on_filter_update,
            resolution=0.5
        )
        self.p_min_scale.pack(fill=tk.X)

        # Max slider
        ttk.Label(frame, text="Max:").pack(anchor=tk.W, pady=(10, 0))
        self.p_max_scale = tk.Scale(
            frame,
            from_=0, to=20,
            orient=tk.HORIZONTAL,
            variable=self.p_max,
            command=self._on_filter_update,
            resolution=0.5
        )
        self.p_max_scale.pack(fill=tk.X)

        # Optimal range hint
        hint = ttk.Label(
            frame,
            text="Optimalt: 2-8 bar",
            font=('Arial', 9, 'italic'),
            foreground='gray'
        )
        hint.pack(pady=(5, 0))

        # Current range label
        self.p_label = ttk.Label(frame, text="")
        self.p_label.pack(pady=(5, 0))
        self._update_pressure_label()

    def _create_safety_filter(self):
        """Safety class checkboxes"""
        frame = ttk.LabelFrame(self, text="ASHRAE Säkerhetsklass", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)

        # Info label
        info = ttk.Label(
            frame,
            text="A = Icke-giftig, 1 = Icke-brandfarlig",
            font=('Arial', 8, 'italic'),
            foreground='gray'
        )
        info.pack(pady=(0, 5))

        # Safe classes (recommended)
        safe_frame = ttk.LabelFrame(frame, text="Säkra klasser (rekommenderade)")
        safe_frame.pack(fill=tk.X, pady=(0, 5))

        for cls in ['A1', 'A2L', 'B1']:
            cb = ttk.Checkbutton(
                safe_frame,
                text=f"{cls} - {'Bäst' if cls == 'A1' else 'Bra'}",
                variable=self.safety_vars[cls],
                command=self._on_filter_update
            )
            cb.pack(anchor=tk.W, padx=5, pady=2)

        # Less safe classes
        other_frame = ttk.LabelFrame(frame, text="Andra klasser")
        other_frame.pack(fill=tk.X)

        for cls in ['A2', 'A3', 'B2L', 'B2', 'B3']:
            cb = ttk.Checkbutton(
                other_frame,
                text=f"{cls}",
                variable=self.safety_vars[cls],
                command=self._on_filter_update
            )
            cb.pack(anchor=tk.W, padx=5, pady=2)

    def _create_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="Återställ filter",
            command=self.reset
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            button_frame,
            text="Applicera",
            command=self._notify_change,
            style='Accent.TButton'
        ).pack(fill=tk.X, pady=2)

    def _update_bp_label(self):
        """Update boiling point range label"""
        self.bp_label.config(
            text=f"Intervall: {self.bp_min.get():.0f} till {self.bp_max.get():.0f} °C"
        )

    def _update_gwp_label(self):
        """Update GWP label"""
        gwp = self.gwp_max.get()
        if gwp < 10:
            rating = "(Utmärkt)"
        elif gwp < 100:
            rating = "(Bra)"
        elif gwp < 500:
            rating = "(Acceptabelt)"
        else:
            rating = "(Högt)"

        self.gwp_label.config(text=f"Max GWP: {gwp} {rating}")

    def _update_pressure_label(self):
        """Update pressure range label"""
        self.p_label.config(
            text=f"Intervall: {self.p_min.get():.1f} - {self.p_max.get():.1f} bar"
        )

    def _on_filter_update(self, event=None):
        """Called when any filter value changes"""
        self._update_bp_label()
        self._update_gwp_label()
        self._update_pressure_label()

        # Auto-apply filters after short delay (debounce)
        if hasattr(self, '_update_timer'):
            self.after_cancel(self._update_timer)

        self._update_timer = self.after(500, self._notify_change)

    def _notify_change(self):
        """Notify parent of filter changes"""
        if self.on_filter_change:
            filters = self.get_filters()
            self.on_filter_change(filters)

    def get_filters(self):
        """Get current filter values"""
        return {
            'bp_range': (self.bp_min.get(), self.bp_max.get()),
            'gwp_max': self.gwp_max.get(),
            'pressure_range': (self.p_min.get(), self.p_max.get()),
            'safety_classes': [
                cls for cls, var in self.safety_vars.items()
                if var.get()
            ]
        }

    def set_gwp(self, value):
        """Set GWP maximum value"""
        self.gwp_max.set(value)
        self._on_filter_update()

    def reset(self):
        """Reset all filters to defaults"""
        self.bp_min.set(-50)
        self.bp_max.set(50)
        self.gwp_max.set(2000)
        self.p_min.set(0)
        self.p_max.set(20)

        # Reset all safety classes to checked except B2, B3
        for cls, var in self.safety_vars.items():
            if cls in ['B2', 'B3']:
                var.set(False)
            else:
                var.set(True)

        self._on_filter_update()


# Test standalone
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Filter Panel Test")

    def on_change(filters):
        print("\nFilters changed:")
        print(f"  BP: {filters['bp_range']}")
        print(f"  GWP max: {filters['gwp_max']}")
        print(f"  Pressure: {filters['pressure_range']}")
        print(f"  Safety: {filters['safety_classes']}")

    panel = FilterPanel(root, on_filter_change=on_change)
    panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()
