"""
================================================================================
MANUFACTURING QUALITY COMPARISON ANALYZER
F-Test Statistical Analysis Application
================================================================================

REQUIRED LIBRARIES:
    pip install customtkinter pandas matplotlib scipy numpy

DESCRIPTION:
    This is a professional desktop application for comparing the quality 
    (variance/consistency) of two manufacturing plants using statistical F-Test.
    It provides a modern GUI, data upload, statistical calculations, 
    visualizations, and PDF export functionality.

FEATURES:
    - Modern CustomTkinter GUI with dark mode
    - CSV data upload for two plants
    - F-Test statistical analysis
    - Publication-quality visualizations (boxplot + histograms)
    - PDF export of results
    - Comprehensive error handling
    - Reset functionality

AUTHOR: Manufacturing Quality Analysis Team
VERSION: 1.0.0
DATE: 2025

================================================================================
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from datetime import datetime
import threading
from pathlib import Path


# ============================================================================
# GLOBAL CONFIGURATION
# ============================================================================

class Config:
    """Global configuration constants"""
    SIGNIFICANCE_LEVEL = 0.05
    APP_WIDTH = 1400
    APP_HEIGHT = 900
    BG_COLOR = "#212121"
    FG_COLOR = "#FFFFFF"
    ACCENT_COLOR = "#2E7D32"
    ERROR_COLOR = "#D32F2F"
    SUCCESS_COLOR = "#388E3C"


# ============================================================================
# DATA HANDLING FUNCTIONS
# ============================================================================

def load_data(file_path):
    """
    Load and validate CSV data from file.
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        tuple: (pandas.Series, str or None) - Series containing measurements and error message
        
    Raises:
        Exception: If file format is invalid or required column missing
    """
    try:
        # Load CSV file
        df = pd.read_csv(file_path)
        
        # Check if file is empty
        if df.empty:
            return None, "Error: CSV file is empty. Please provide a file with data."
        
        # Check if 'Measurement' column exists
        if 'Measurement' not in df.columns:
            columns = ', '.join(df.columns)
            return None, (f"Error: 'Measurement' column not found.\n"
                         f"Available columns: {columns}\n"
                         f"Please ensure your CSV has a 'Measurement' column.")
        
        # Extract measurement column
        measurements = pd.to_numeric(df['Measurement'], errors='coerce')
        
        # Check for non-numeric values
        if measurements.isna().any():
            invalid_count = measurements.isna().sum()
            return None, (f"Error: Found {invalid_count} non-numeric values in 'Measurement' column.\n"
                         f"Please ensure all measurements are numeric.")
        
        # Remove any NaN values
        measurements = measurements.dropna()
        
        # Check if we have enough data points
        if len(measurements) < 2:
            return None, "Error: Need at least 2 data points per plant."
        
        return measurements, None
        
    except FileNotFoundError:
        return None, "Error: File not found. Please check the file path."
    except pd.errors.EmptyDataError:
        return None, "Error: CSV file is empty or corrupted."
    except Exception as e:
        return None, f"Error reading file: {str(e)}"


# ============================================================================
# STATISTICAL ANALYSIS FUNCTIONS
# ============================================================================

def perform_f_test(data1, data2):
    """
    Perform F-Test to compare variances of two samples.
    
    F-Test hypothesis:
    - H0: σ1² = σ2² (variances are equal)
    - H1: σ1² ≠ σ2² (variances are not equal - two-tailed test)
    
    Args:
        data1 (pandas.Series): Measurements from Plant 1
        data2 (pandas.Series): Measurements from Plant 2
        
    Returns:
        dict: Dictionary containing all statistical results
    """
    # Calculate descriptive statistics
    mean1 = data1.mean()
    mean2 = data2.mean()
    
    var1 = data1.var(ddof=1)  # Sample variance (unbiased)
    var2 = data2.var(ddof=1)
    
    std1 = data1.std(ddof=1)  # Sample standard deviation
    std2 = data2.std(ddof=1)
    
    n1 = len(data1)
    n2 = len(data2)
    
    # Degrees of freedom
    df1 = n1 - 1  # df for numerator
    df2 = n2 - 1  # df for denominator
    
    # Calculate F-statistic
    # F = var_larger / var_smaller (always >= 1 for one-tailed equivalent)
    if var1 >= var2:
        f_statistic = var1 / var2
        df_num = df1
        df_den = df2
        larger_var_plant = 1
    else:
        f_statistic = var2 / var1
        df_num = df2
        df_den = df1
        larger_var_plant = 2
    
    # Calculate p-value for two-tailed test
    # For two-tailed: p = 2 * P(F > f_stat)
    p_value = 2 * (1 - stats.f.cdf(f_statistic, df_num, df_den))
    
    # Ensure p-value doesn't exceed 1 (due to two-tailed nature)
    p_value = min(p_value, 1.0)
    
    # Hypothesis test conclusion
    reject_null = p_value < Config.SIGNIFICANCE_LEVEL
    
    # Determine which plant has better consistency (lower variance)
    if var1 < var2:
        better_consistency_plant = 1
        consistency_improvement = ((var2 - var1) / var2) * 100
    else:
        better_consistency_plant = 2
        consistency_improvement = ((var1 - var2) / var1) * 100
    
    return {
        'n1': n1,
        'n2': n2,
        'mean1': mean1,
        'mean2': mean2,
        'var1': var1,
        'var2': var2,
        'std1': std1,
        'std2': std2,
        'f_statistic': f_statistic,
        'df_numerator': df_num,
        'df_denominator': df_den,
        'p_value': p_value,
        'significance_level': Config.SIGNIFICANCE_LEVEL,
        'reject_null': reject_null,
        'better_consistency_plant': better_consistency_plant,
        'consistency_improvement': consistency_improvement,
        'larger_var_plant': larger_var_plant,
        'data1': data1,
        'data2': data2
    }


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def generate_graphs(results, fig_canvas_widget):
    """
    Generate publication-quality boxplot and histograms for both plants.
    
    Args:
        results (dict): Statistical results dictionary from perform_f_test()
        fig_canvas_widget: tkinter widget to embed matplotlib figure in
    """
    data1 = results['data1']
    data2 = results['data2']
    
    # Create figure with 3 subplots
    fig = Figure(figsize=(14, 5), dpi=100, facecolor='#212121')
    
    # -------- Subplot 1: Boxplot Comparison --------
    ax1 = fig.add_subplot(131)
    bp = ax1.boxplot([data1, data2], 
                      labels=['Plant 1', 'Plant 2'],
                      patch_artist=True,
                      widths=0.6,
                      notch=False,
                      showmeans=True,
                      meanprops=dict(marker='D', markerfacecolor='red', 
                                   markeredgecolor='red', markersize=8))
    
    # Style boxplot
    for patch in bp['boxes']:
        patch.set_facecolor('#2E7D32')
        patch.set_alpha(0.7)
        patch.set_edgecolor('#FFFFFF')
        patch.set_linewidth(1.5)
    
    for whisker in bp['whiskers']:
        whisker.set_color('#FFFFFF')
        whisker.set_linewidth(1.5)
    
    for cap in bp['caps']:
        cap.set_color('#FFFFFF')
        cap.set_linewidth(1.5)
    
    for median in bp['medians']:
        median.set_color('#FFEB3B')
        median.set_linewidth(2)
    
    ax1.set_ylabel('Measurement Value', color='#FFFFFF', fontsize=11, fontweight='bold')
    ax1.set_title('Quality Comparison\n(Boxplot)', color='#FFFFFF', 
                  fontsize=12, fontweight='bold', pad=10)
    ax1.tick_params(colors='#FFFFFF')
    ax1.grid(True, alpha=0.3, color='#FFFFFF')
    ax1.set_facecolor('#2C2C2C')
    
    # -------- Subplot 2: Plant 1 Histogram --------
    ax2 = fig.add_subplot(132)
    ax2.hist(data1, bins='auto', color='#2E7D32', alpha=0.7, edgecolor='#FFFFFF', linewidth=1.2)
    ax2.axvline(data1.mean(), color='#FF9800', linestyle='--', linewidth=2.5, 
               label=f'Mean: {data1.mean():.4f}')
    ax2.set_xlabel('Measurement Value', color='#FFFFFF', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Frequency', color='#FFFFFF', fontsize=10, fontweight='bold')
    ax2.set_title('Plant 1 Distribution\n(Histogram)', color='#FFFFFF', 
                 fontsize=12, fontweight='bold', pad=10)
    ax2.tick_params(colors='#FFFFFF')
    ax2.legend(facecolor='#2C2C2C', edgecolor='#FFFFFF', labelcolor='#FFFFFF')
    ax2.grid(True, alpha=0.3, color='#FFFFFF', axis='y')
    ax2.set_facecolor('#2C2C2C')
    
    # -------- Subplot 3: Plant 2 Histogram --------
    ax3 = fig.add_subplot(133)
    ax3.hist(data2, bins='auto', color='#1976D2', alpha=0.7, edgecolor='#FFFFFF', linewidth=1.2)
    ax3.axvline(data2.mean(), color='#FF9800', linestyle='--', linewidth=2.5,
               label=f'Mean: {data2.mean():.4f}')
    ax3.set_xlabel('Measurement Value', color='#FFFFFF', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Frequency', color='#FFFFFF', fontsize=10, fontweight='bold')
    ax3.set_title('Plant 2 Distribution\n(Histogram)', color='#FFFFFF', 
                 fontsize=12, fontweight='bold', pad=10)
    ax3.tick_params(colors='#FFFFFF')
    ax3.legend(facecolor='#2C2C2C', edgecolor='#FFFFFF', labelcolor='#FFFFFF')
    ax3.grid(True, alpha=0.3, color='#FFFFFF', axis='y')
    ax3.set_facecolor('#2C2C2C')
    
    plt.tight_layout()
    
    # Embed figure in tkinter
    canvas = FigureCanvasTkAgg(fig, master=fig_canvas_widget)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    return canvas


# ============================================================================
# PDF EXPORT FUNCTIONS
# ============================================================================

def generate_pdf_report(results, filename):
    """
    Generate a comprehensive PDF report of the F-Test analysis.
    
    Args:
        results (dict): Statistical results dictionary
        filename (str): Output PDF filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        
        # Create PDF
        pdf_file = SimpleDocTemplate(filename, pagesize=letter,
                                     rightMargin=0.75*inch,
                                     leftMargin=0.75*inch,
                                     topMargin=0.75*inch,
                                     bottomMargin=0.75*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1B5E20'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2E7D32'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        story.append(Paragraph("Manufacturing Quality Comparison Report", title_style))
        story.append(Paragraph(f"F-Test Statistical Analysis", styles['Heading3']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                             styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        
        better_plant = results['better_consistency_plant']
        improvement = results['consistency_improvement']
        conclusion = "REJECT NULL HYPOTHESIS" if results['reject_null'] else "FAIL TO REJECT NULL HYPOTHESIS"
        conclusion_text = ("The two plants have SIGNIFICANTLY different variance levels (quality consistency) " 
                          if results['reject_null'] 
                          else "The two plants have SIMILAR variance levels (quality consistency) ")
        
        summary_text = (
            f"<b>Conclusion:</b> {conclusion}<br/>"
            f"{conclusion_text}at {results['significance_level']*100:.1f}% significance level.<br/>"
            f"<b>Plant with Better Consistency:</b> Plant {better_plant} "
            f"({improvement:.2f}% lower variance)<br/>"
            f"<b>P-Value:</b> {results['p_value']:.6f}"
        )
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Statistical Results Table
        story.append(Paragraph("Statistical Results", heading_style))
        
        results_data = [
            ['Metric', 'Plant 1', 'Plant 2'],
            ['Sample Size (n)', f"{results['n1']}", f"{results['n2']}"],
            ['Mean', f"{results['mean1']:.6f}", f"{results['mean2']:.6f}"],
            ['Variance (s²)', f"{results['var1']:.6f}", f"{results['var2']:.6f}"],
            ['Std. Deviation (s)', f"{results['std1']:.6f}", f"{results['std2']:.6f}"],
        ]
        
        results_table = Table(results_data, colWidths=[2*inch, 2*inch, 2*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 0.2*inch))
        
        # F-Test Results
        story.append(Paragraph("F-Test Results", heading_style))
        
        f_test_data = [
            ['Parameter', 'Value'],
            ['F-Statistic', f"{results['f_statistic']:.6f}"],
            ['Degrees of Freedom (numerator)', f"{results['df_numerator']}"],
            ['Degrees of Freedom (denominator)', f"{results['df_denominator']}"],
            ['P-Value (two-tailed)', f"{results['p_value']:.6f}"],
            ['Significance Level (α)', f"{results['significance_level']}"],
            ['Test Conclusion', conclusion],
        ]
        
        f_test_table = Table(f_test_data, colWidths=[3*inch, 2*inch])
        f_test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(f_test_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Interpretation
        story.append(Paragraph("Interpretation", heading_style))
        
        interpretation = (
            "<b>Null Hypothesis (H₀):</b> The variances of Plant 1 and Plant 2 are equal (σ₁² = σ₂²)<br/>"
            "<b>Alternative Hypothesis (H₁):</b> The variances are not equal (σ₁² ≠ σ₂²)<br/><br/>"
            f"<b>Test Result:</b> {conclusion_text}at α = {results['significance_level']} significance level.<br/>"
            f"<b>Plant with Better Consistency:</b> Plant {better_plant} has lower variance, indicating "
            f"higher consistency in quality measurements ({improvement:.2f}% improvement)."
        )
        story.append(Paragraph(interpretation, styles['Normal']))
        
        # Build PDF
        pdf_file.build(story)
        return True
        
    except ImportError:
        return False
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


# ============================================================================
# GUI APPLICATION CLASS
# ============================================================================

class ManufacturingQualityApp(ctk.CTk):
    """
    Main application class for Manufacturing Quality Comparison Analyzer.
    Handles all GUI components, data management, and analysis workflows.
    """
    
    def __init__(self):
        """Initialize the application window and components."""
        super().__init__()
        
        # Window configuration
        self.title("Manufacturing Quality Comparison - F-Test Analyzer")
        self.geometry(f"{Config.APP_WIDTH}x{Config.APP_HEIGHT}")
        self.resizable(True, True)
        
        # Configure dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Application state
        self.plant1_data = None
        self.plant2_data = None
        self.analysis_results = None
        self.canvas_widget = None
        self.canvas = None
        
        # Build UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Create and configure all UI components."""
        
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color=Config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # -------- HEADER --------
        header = ctk.CTkFrame(main_container, fg_color=Config.ACCENT_COLOR, height=60)
        header.pack(fill=tk.X, pady=(0, 10))
        header.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header,
            text="Manufacturing Quality Comparison Analyzer",
            font=("Arial", 20, "bold"),
            text_color=Config.FG_COLOR
        )
        title_label.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            header,
            text="F-Test Statistical Analysis for Plant Consistency Comparison",
            font=("Arial", 11),
            text_color=Config.FG_COLOR
        )
        subtitle.pack()
        
        # -------- CONTENT AREA --------
        content = ctk.CTkFrame(main_container, fg_color=Config.BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (Controls)
        left_panel = ctk.CTkFrame(content, fg_color="#2C2C2C", corner_radius=8)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        left_panel.pack_propagate(False)
        left_panel.configure(width=300)
        
        self._create_control_panel(left_panel)
        
        # Right panel (Results and Graphs)
        right_panel = ctk.CTkFrame(content, fg_color="#2C2C2C", corner_radius=8)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=0)
        
        self._create_results_panel(right_panel)
        
    def _create_control_panel(self, parent):
        """Create the left control panel with file upload and analysis buttons."""
        
        # Title
        title = ctk.CTkLabel(
            parent,
            text="Data Input & Analysis",
            font=("Arial", 14, "bold"),
            text_color=Config.FG_COLOR
        )
        title.pack(pady=15, padx=15)
        
        # -------- PLANT 1 SECTION --------
        plant1_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A", corner_radius=6)
        plant1_frame.pack(padx=10, pady=10, fill=tk.X)
        
        ctk.CTkLabel(
            plant1_frame,
            text="Plant 1 Data",
            font=("Arial", 12, "bold"),
            text_color="#4CAF50"
        ).pack(pady=(10, 5), padx=10, anchor="w")
        
        self.plant1_button = ctk.CTkButton(
            plant1_frame,
            text="📁 Upload CSV",
            command=self._load_plant1_data,
            font=("Arial", 11),
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            text_color=Config.FG_COLOR,
            corner_radius=6
        )
        self.plant1_button.pack(padx=10, pady=5, fill=tk.X)
        
        self.plant1_label = ctk.CTkLabel(
            plant1_frame,
            text="No file loaded",
            font=("Arial", 9),
            text_color="#B0BEC5"
        )
        self.plant1_label.pack(padx=10, pady=(0, 10))
        
        # -------- PLANT 2 SECTION --------
        plant2_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A", corner_radius=6)
        plant2_frame.pack(padx=10, pady=10, fill=tk.X)
        
        ctk.CTkLabel(
            plant2_frame,
            text="Plant 2 Data",
            font=("Arial", 12, "bold"),
            text_color="#2196F3"
        ).pack(pady=(10, 5), padx=10, anchor="w")
        
        self.plant2_button = ctk.CTkButton(
            plant2_frame,
            text="📁 Upload CSV",
            command=self._load_plant2_data,
            font=("Arial", 11),
            fg_color="#1976D2",
            hover_color="#1565C0",
            text_color=Config.FG_COLOR,
            corner_radius=6
        )
        self.plant2_button.pack(padx=10, pady=5, fill=tk.X)
        
        self.plant2_label = ctk.CTkLabel(
            plant2_frame,
            text="No file loaded",
            font=("Arial", 9),
            text_color="#B0BEC5"
        )
        self.plant2_label.pack(padx=10, pady=(0, 10))
        
        # -------- SEPARATOR --------
        ctk.CTkFrame(parent, height=2, fg_color="#404040").pack(
            padx=10, pady=15, fill=tk.X
        )
        
        # -------- ANALYSIS BUTTON --------
        self.analyze_button = ctk.CTkButton(
            parent,
            text="🔬 Analyze Data",
            command=self._perform_analysis,
            font=("Arial", 12, "bold"),
            fg_color=Config.ACCENT_COLOR,
            hover_color="#1B5E20",
            text_color=Config.FG_COLOR,
            corner_radius=6,
            height=40,
            state=tk.DISABLED
        )
        self.analyze_button.pack(padx=10, pady=10, fill=tk.X)
        
        # -------- EXPORT BUTTON --------
        self.export_button = ctk.CTkButton(
            parent,
            text="📊 Export as PDF",
            command=self._export_pdf,
            font=("Arial", 11),
            fg_color="#F57C00",
            hover_color="#E65100",
            text_color=Config.FG_COLOR,
            corner_radius=6,
            state=tk.DISABLED
        )
        self.export_button.pack(padx=10, pady=5, fill=tk.X)
        
        # -------- RESET BUTTON --------
        self.reset_button = ctk.CTkButton(
            parent,
            text="🔄 Reset All",
            command=self._reset_application,
            font=("Arial", 11),
            fg_color="#455A64",
            hover_color="#37474F",
            text_color=Config.FG_COLOR,
            corner_radius=6
        )
        self.reset_button.pack(padx=10, pady=5, fill=tk.X)
        
        # -------- FOOTER INFO --------
        footer = ctk.CTkLabel(
            parent,
            text="Significance Level: α = 0.05\n\nEnsure CSVs have a\n'Measurement' column",
            font=("Arial", 9),
            text_color="#78909C",
            justify="center"
        )
        footer.pack(padx=10, pady=(20, 10), fill=tk.X)
        
    def _create_results_panel(self, parent):
        """Create the right panel for displaying results and visualizations."""
        
        # Create a notebook (tabbed interface)
        self.notebook = ctk.CTkTabview(parent, fg_color="#2C2C2C")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Statistics Results
        self.stats_tab = self.notebook.add("Statistics Results")
        self._create_stats_tab(self.stats_tab)
        
        # Tab 2: Visualizations
        self.viz_tab = self.notebook.add("Visualizations")
        self.viz_container = ctk.CTkFrame(self.viz_tab, fg_color="#2C2C2C")
        self.viz_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def _create_stats_tab(self, parent):
        """Create the statistics results display tab."""
        
        # Create scrollable text widget for results
        self.results_text = tk.Text(
            parent,
            bg="#1A1A1A",
            fg="#FFFFFF",
            font=("Courier New", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Configure text tags for formatting
        self.results_text.tag_configure("title", font=("Arial", 14, "bold"), 
                                       foreground="#4CAF50", spacing1=10, spacing3=10)
        self.results_text.tag_configure("section", font=("Arial", 12, "bold"), 
                                       foreground="#2196F3", spacing1=10, spacing3=5)
        self.results_text.tag_configure("key", font=("Courier New", 10, "bold"), 
                                       foreground="#FFD54F")
        self.results_text.tag_configure("value", font=("Courier New", 10), 
                                       foreground="#81C784")
        self.results_text.tag_configure("conclusion", font=("Arial", 11, "bold"), 
                                       foreground="#FF9800", spacing1=10, spacing3=10)
        
        # Display initial placeholder
        self._display_placeholder_results()
        
    def _display_placeholder_results(self):
        """Display placeholder text before analysis is performed."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        placeholder = """
ANALYSIS RESULTS
────────────────────────────────────────────────────

Status: Ready for Analysis

Steps to Proceed:
1. Upload CSV file for Plant 1 (must have 'Measurement' column)
2. Upload CSV file for Plant 2 (must have 'Measurement' column)
3. Click "Analyze Data" button to perform F-Test
4. View results in this tab
5. View visualizations in the "Visualizations" tab
6. Export results as PDF

About F-Test:
The F-Test compares the variances (consistency) of two data sets.
A low p-value suggests the plants have significantly different 
consistency levels in quality measurements.

CSV Format:
Your CSV file should contain a column named "Measurement" with 
numeric values representing quality measurements from each plant.
        """
        
        self.results_text.insert(tk.END, placeholder, "value")
        self.results_text.config(state=tk.DISABLED)
        
    def _load_plant1_data(self):
        """Load Plant 1 data from CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select Plant 1 CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            data, error = load_data(file_path)
            if error:
                messagebox.showerror("Data Loading Error", error)
                self.plant1_data = None
                self.plant1_label.configure(text="❌ Error loading file")
            else:
                self.plant1_data = data
                filename = os.path.basename(file_path)
                self.plant1_label.configure(
                    text=f"✓ {filename}\n({len(data)} measurements)",
                    text_color="#81C784"
                )
                self._update_analyze_button()
                
    def _load_plant2_data(self):
        """Load Plant 2 data from CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select Plant 2 CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            data, error = load_data(file_path)
            if error:
                messagebox.showerror("Data Loading Error", error)
                self.plant2_data = None
                self.plant2_label.configure(text="❌ Error loading file")
            else:
                self.plant2_data = data
                filename = os.path.basename(file_path)
                self.plant2_label.configure(
                    text=f"✓ {filename}\n({len(data)} measurements)",
                    text_color="#81C784"
                )
                self._update_analyze_button()
                
    def _update_analyze_button(self):
        """Enable analyze button if both data sets are loaded."""
        if self.plant1_data is not None and self.plant2_data is not None:
            self.analyze_button.configure(state=tk.NORMAL)
        else:
            self.analyze_button.configure(state=tk.DISABLED)
            
    def _perform_analysis(self):
        """Perform F-Test analysis in a separate thread."""
        self.analyze_button.configure(state=tk.DISABLED, text="⏳ Analyzing...")
        
        # Run analysis in background thread to prevent GUI freezing
        analysis_thread = threading.Thread(target=self._analysis_worker)
        analysis_thread.daemon = True
        analysis_thread.start()
        
    def _analysis_worker(self):
        """Worker thread for statistical analysis."""
        try:
            # Perform F-Test
            self.analysis_results = perform_f_test(self.plant1_data, self.plant2_data)
            
            # Update GUI in main thread
            self.after(0, self._display_results)
            self.after(0, self._generate_visualizations)
            self.after(0, lambda: self.analyze_button.configure(
                state=tk.NORMAL, text="✓ Analysis Complete"
            ))
            
            # Re-enable buttons
            self.after(0, lambda: self.export_button.configure(state=tk.NORMAL))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Analysis Error", f"An error occurred during analysis:\n{str(e)}"
            ))
            self.after(0, lambda: self.analyze_button.configure(
                state=tk.NORMAL, text="🔬 Analyze Data"
            ))
            
    def _display_results(self):
        """Display statistical results in the results text widget."""
        if not self.analysis_results:
            return
            
        r = self.analysis_results
        
        # Format results text
        results_output = f"""
{'='*70}
MANUFACTURING QUALITY COMPARISON - F-TEST ANALYSIS
{'='*70}

EXECUTIVE SUMMARY
────────────────────────────────────────────────────
Plant with Better Consistency: Plant {r['better_consistency_plant']}
Improvement in Variance: {r['consistency_improvement']:.2f}%
Test Conclusion: {'REJECT NULL HYPOTHESIS' if r['reject_null'] else 'FAIL TO REJECT NULL HYPOTHESIS'}
P-Value: {r['p_value']:.8f}

INTERPRETATION
────────────────────────────────────────────────────
The two plants have {'SIGNIFICANTLY DIFFERENT' if r['reject_null'] else 'SIMILAR'} variance levels 
(quality consistency) at the {r['significance_level']*100:.1f}% significance level.

{'Plant ' + str(r['better_consistency_plant']) + ' demonstrates superior consistency in quality.' if r['reject_null'] else 'Both plants demonstrate similar consistency in quality.'}

DESCRIPTIVE STATISTICS
────────────────────────────────────────────────────
Metric                    Plant 1              Plant 2
{'─'*65}
Sample Size (n)           {r['n1']:<20} {r['n2']}
Mean (μ)                  {r['mean1']:<20.8f} {r['mean2']:.8f}
Variance (s²)             {r['var1']:<20.8f} {r['var2']:.8f}
Std. Deviation (s)        {r['std1']:<20.8f} {r['std2']:.8f}

F-TEST RESULTS
────────────────────────────────────────────────────
F-Statistic:              {r['f_statistic']:.8f}
Degrees of Freedom (num): {r['df_numerator']}
Degrees of Freedom (den): {r['df_denominator']}
P-Value (two-tailed):     {r['p_value']:.8f}
Significance Level (α):   {r['significance_level']}

HYPOTHESIS TEST
────────────────────────────────────────────────────
H₀ (Null):     σ₁² = σ₂² (Equal variances)
H₁ (Alt):      σ₁² ≠ σ₂² (Unequal variances)

Decision: {'REJECT H₀' if r['reject_null'] else 'FAIL TO REJECT H₀'}
          (p-value {'<' if r['reject_null'] else '≥'} {r['significance_level']})

QUALITY CONSISTENCY RANKING
────────────────────────────────────────────────────
Plant {r['better_consistency_plant']:<70} ⭐ BETTER CONSISTENCY
Plant {3 - r['better_consistency_plant']:<70} LOWER CONSISTENCY

{'='*70}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
        """
        
        # Display results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results_output, "value")
        self.results_text.config(state=tk.DISABLED)
        
    def _generate_visualizations(self):
        """Generate and display visualizations."""
        if not self.analysis_results:
            return
        
        # Clear previous canvas if exists
        for widget in self.viz_container.winfo_children():
            widget.destroy()
        
        # Generate graphs
        self.canvas = generate_graphs(self.analysis_results, self.viz_container)
        
    def _export_pdf(self):
        """Export analysis results as PDF."""
        if not self.analysis_results:
            messagebox.showwarning("No Analysis", "Please perform analysis first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"quality_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if file_path:
            success = generate_pdf_report(self.analysis_results, file_path)
            if success:
                messagebox.showinfo("Success", f"Report exported to:\n{file_path}")
            else:
                messagebox.showwarning(
                    "PDF Export",
                    "reportlab library not installed.\n"
                    "Install with: pip install reportlab\n\n"
                    "Alternatively, results are displayed in the application."
                )
                
    def _reset_application(self):
        """Reset the application to initial state."""
        confirm = messagebox.askyesno(
            "Reset Application",
            "Are you sure you want to reset all data and results?"
        )
        
        if confirm:
            # Clear data
            self.plant1_data = None
            self.plant2_data = None
            self.analysis_results = None
            
            # Reset UI
            self.plant1_label.configure(text="No file loaded", text_color="#B0BEC5")
            self.plant2_label.configure(text="No file loaded", text_color="#B0BEC5")
            self.analyze_button.configure(state=tk.DISABLED, text="🔬 Analyze Data")
            self.export_button.configure(state=tk.DISABLED)
            
            # Clear results
            self._display_placeholder_results()
            
            # Clear visualizations
            for widget in self.viz_container.winfo_children():
                widget.destroy()
            
            messagebox.showinfo("Reset", "Application has been reset.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    app = ManufacturingQualityApp()
    app.mainloop()
