#!/usr/bin/env python3
"""
PDF Report Generator - Professional PDF reports with ReportLab
Creates comprehensive reports with rankings, diagrams, and calculations
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import List
from datetime import datetime
from core.scoring import FluidScore
import tempfile
import os


class PDFReportGenerator:
    """Generate professional PDF reports for ORC fluid analysis"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """Create custom paragraph styles"""

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=12,
            spaceBefore=12
        ))

        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            spaceAfter=12
        ))

    def generate_report(self, scores: List[FluidScore], filename: str,
                       selected_fluids: List[str] = None,
                       plot_files: dict = None):
        """
        Generate complete PDF report

        Args:
            scores: List of FluidScore objects
            filename: Output PDF filename
            selected_fluids: List of fluids to highlight (optional)
            plot_files: Dictionary of plot filenames (optional)
        """

        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Story (content elements)
        story = []

        # Title page
        story.extend(self._create_title_page(scores))
        story.append(PageBreak())

        # Executive summary
        story.extend(self._create_executive_summary(scores))
        story.append(Spacer(1, 1*cm))

        # Top 10 fluids
        story.extend(self._create_top_fluids_section(scores[:10]))
        story.append(PageBreak())

        # Complete ranking table
        story.extend(self._create_complete_ranking(scores))

        # Add plots if provided
        if plot_files:
            story.append(PageBreak())
            story.extend(self._create_plots_section(plot_files))

        # Build PDF
        doc.build(story)

        print(f"✓ Generated PDF report: {filename}")
        return filename

    def _create_title_page(self, scores):
        """Create title page"""
        elements = []

        # Title
        title = Paragraph(
            "ORC WORKING FLUID ANALYSIS REPORT",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 1*cm))

        # Subtitle
        subtitle = Paragraph(
            "Tesla Turbine ORC System<br/>Dynamic Fluid Comparison Tool",
            self.styles['CustomHeading']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 2*cm))

        # Summary box
        summary_data = [
            ['Total Fluids Analyzed:', str(len(scores))],
            ['Top Ranked Fluid:', scores[0].fluid if scores else 'N/A'],
            ['Best Score:', f"{scores[0].total_score:.1f}/100" if scores else 'N/A'],
            ['Report Date:', datetime.now().strftime('%Y-%m-%d %H:%M')],
        ]

        summary_table = Table(summary_data, colWidths=[8*cm, 6*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 2*cm))

        # Evaluation criteria
        criteria = Paragraph(
            "<b>Evaluation Criteria:</b><br/>"
            "• Thermodynamic Performance: 40%<br/>"
            "• Environmental Impact: 30%<br/>"
            "• Safety: 20%<br/>"
            "• Economic Factors: 10%",
            self.styles['CustomBody']
        )
        elements.append(criteria)

        return elements

    def _create_executive_summary(self, scores):
        """Create executive summary"""
        elements = []

        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['CustomHeading']))

        # Top 3 recommendations
        if len(scores) >= 3:
            summary_text = f"""
            <b>Top Recommendations:</b><br/><br/>

            <b>1. {scores[0].fluid} (Score: {scores[0].total_score:.1f}/100)</b><br/>
            GWP: {scores[0].gwp}, Safety: {scores[0].ashrae_class or 'N/A'}<br/>
            {self._get_recommendation_text(scores[0])}<br/><br/>

            <b>2. {scores[1].fluid} (Score: {scores[1].total_score:.1f}/100)</b><br/>
            GWP: {scores[1].gwp}, Safety: {scores[1].ashrae_class or 'N/A'}<br/>
            {self._get_recommendation_text(scores[1])}<br/><br/>

            <b>3. {scores[2].fluid} (Score: {scores[2].total_score:.1f}/100)</b><br/>
            GWP: {scores[2].gwp}, Safety: {scores[2].ashrae_class or 'N/A'}<br/>
            {self._get_recommendation_text(scores[2])}
            """

            elements.append(Paragraph(summary_text, self.styles['CustomBody']))

        return elements

    def _get_recommendation_text(self, score):
        """Get recommendation text for a fluid"""
        if score.total_score >= 95:
            return "Excellent choice for all applications."
        elif score.total_score >= 85:
            return "Very good choice, suitable for most applications."
        elif score.total_score >= 75:
            return "Good choice with some considerations."
        else:
            return "Consider alternatives if possible."

    def _create_top_fluids_section(self, top_scores):
        """Create top fluids detailed section"""
        elements = []

        elements.append(Paragraph("TOP 10 FLUIDS - DETAILED ANALYSIS", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.5*cm))

        # Create table data
        data = [['Rank', 'Fluid', 'Total', 'Thermo', 'Env', 'Safety', 'Econ', 'GWP', 'Class']]

        for score in top_scores:
            data.append([
                str(score.rank or ''),
                score.fluid,
                f"{score.total_score:.1f}",
                f"{score.thermo_score:.1f}",
                f"{score.env_score:.1f}",
                f"{score.safety_score:.1f}",
                f"{score.econ_score:.1f}",
                str(score.gwp or '-'),
                score.ashrae_class or '-'
            ])

        # Create table
        table = Table(data, colWidths=[1.2*cm, 3.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm])

        # Style table
        style = TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),

            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),

            # Padding
            ('PADDING', (0, 0), (-1, -1), 6),
        ])

        # Highlight top 3
        for i in range(1, min(4, len(data))):
            style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#c8e6c9'))

        table.setStyle(style)
        elements.append(table)

        return elements

    def _create_complete_ranking(self, scores):
        """Create complete ranking table"""
        elements = []

        elements.append(Paragraph(
            f"COMPLETE RANKING - ALL {len(scores)} FLUIDS",
            self.styles['CustomHeading']
        ))
        elements.append(Spacer(1, 0.5*cm))

        # Split into multiple tables if too many fluids
        chunk_size = 30
        for i in range(0, len(scores), chunk_size):
            chunk = scores[i:i+chunk_size]

            data = [['Rank', 'Fluid', 'Score', 'GWP', 'Class', 'P@50°C', 'hfg']]

            for score in chunk:
                data.append([
                    str(score.rank or ''),
                    score.fluid,
                    f"{score.total_score:.1f}",
                    str(score.gwp or '-'),
                    score.ashrae_class or '-',
                    f"{score.pressure_50C:.1f}" if score.pressure_50C else '-',
                    f"{score.hfg_50C:.0f}" if score.hfg_50C else '-'
                ])

            table = Table(data, colWidths=[1.2*cm, 4*cm, 1.8*cm, 1.5*cm, 1.8*cm, 2*cm, 2*cm])

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('PADDING', (0, 0), (-1, -1), 4),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 0.5*cm))

            # Page break between chunks
            if i + chunk_size < len(scores):
                elements.append(PageBreak())

        return elements

    def _create_plots_section(self, plot_files):
        """Add plots to report"""
        elements = []

        elements.append(Paragraph("THERMODYNAMIC COMPARISON PLOTS", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.5*cm))

        # Add each plot
        for plot_type, filename in plot_files.items():
            if os.path.exists(filename):
                # Add image
                img = Image(filename, width=15*cm, height=9*cm)
                elements.append(img)
                elements.append(Spacer(1, 0.5*cm))

                # Caption
                caption = Paragraph(
                    f"<i>Figure: {plot_type.replace('_', ' ').title()}</i>",
                    self.styles['CustomBody']
                )
                elements.append(caption)
                elements.append(Spacer(1, 1*cm))

        return elements


# Test
if __name__ == "__main__":
    from core.scoring import FluidScorer

    print("="*70)
    print("PDF GENERATOR - Testing")
    print("="*70)

    # Create test data
    scorer = FluidScorer(T_hot=50, T_cold=20)
    scores = scorer.rank_fluids()

    # Generate report
    generator = PDFReportGenerator()
    generator.generate_report(scores, 'test_orc_report.pdf')

    print("\n✓ Test completed. Check test_orc_report.pdf")
