"""
PDF Report Generation Utility
Generates health report PDFs with user data
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class HealthReportPDF:
    """Generate health report PDFs from user data."""
    
    def __init__(self, user):
        self.user = user
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(self.buffer, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=6
        )
    
    def add_header(self, start_date, end_date):
        """Add report header with user and date information."""
        self.story.append(Paragraph("SMART HEALTH MANAGEMENT SYSTEM", self.title_style))
        self.story.append(Paragraph("Health Report", self.styles['Heading2']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # User and date info
        info_data = [
            ['Patient Name:', self.user.get_full_name() or self.user.email],
            ['Email:', self.user.email],
            ['Report Date:', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Period:', f"{start_date} to {end_date}"],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ]))
        
        self.story.append(info_table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_blood_pressure_section(self, bp_data):
        """Add blood pressure data section."""
        if not bp_data:
            return
        
        self.story.append(Paragraph("Blood Pressure", self.heading_style))
        
        table_data = [['Date & Time', 'Systolic (mmHg)', 'Diastolic (mmHg)', 'Status']]
        
        for bp in bp_data:
            date_str = bp.timestamp.strftime('%Y-%m-%d %H:%M')
            systolic = bp.systolic_blood_pressure
            diastolic = bp.diastolic_blood_pressure
            
            # Determine BP status
            if systolic < 120 and diastolic < 80:
                status = "Normal"
            elif systolic < 130 and diastolic < 80:
                status = "Elevated"
            elif systolic < 140 or diastolic < 90:
                status = "High BP Stage 1"
            else:
                status = "High BP Stage 2"
            
            table_data.append([date_str, str(systolic), str(diastolic), status])
        
        bp_table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        bp_table.setStyle(self._get_table_style())
        
        self.story.append(bp_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_blood_sugar_section(self, sugar_data):
        """Add blood sugar data section."""
        if not sugar_data:
            return
        
        self.story.append(Paragraph("Blood Sugar", self.heading_style))
        
        table_data = [['Date & Time', 'Reading (mg/dL)', 'Type', 'Status']]
        
        for sugar in sugar_data:
            date_str = sugar.timestamp.strftime('%Y-%m-%d %H:%M')
            reading = sugar.blood_sugar_reading_mgdl
            reading_type = "Fasting" if sugar.reading_type == 'F' else "Random"
            
            # Determine status
            if reading_type == 'Fasting':
                if reading < 100:
                    status = "Normal"
                elif reading < 126:
                    status = "Prediabetes"
                else:
                    status = "Diabetes"
            else:
                if reading < 140:
                    status = "Normal"
                elif reading < 200:
                    status = "Prediabetes"
                else:
                    status = "Diabetes"
            
            table_data.append([date_str, str(reading), reading_type, status])
        
        sugar_table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        sugar_table.setStyle(self._get_table_style())
        
        self.story.append(sugar_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_weight_section(self, weight_data):
        """Add weight data section."""
        if not weight_data:
            return
        
        self.story.append(Paragraph("Weight", self.heading_style))
        
        table_data = [['Date & Time', 'Weight (kg)']]
        
        for weight in weight_data:
            date_str = weight.timestamp.strftime('%Y-%m-%d %H:%M')
            table_data.append([date_str, f"{weight.weight_in_kg:.2f}"])
        
        weight_table = Table(table_data, colWidths=[3*inch, 2*inch])
        weight_table.setStyle(self._get_table_style())
        
        self.story.append(weight_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_temperature_section(self, temp_data):
        """Add temperature data section."""
        if not temp_data:
            return
        
        self.story.append(Paragraph("Temperature", self.heading_style))
        
        table_data = [['Date & Time', 'Temperature (°C)', 'Status']]
        
        for temp in temp_data:
            date_str = temp.timestamp.strftime('%Y-%m-%d %H:%M')
            reading = temp.temperature_reading_celsius
            
            status = "Normal" if 36.1 <= reading <= 37.2 else "Abnormal"
            
            table_data.append([date_str, f"{reading:.2f}", status])
        
        temp_table = Table(table_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        temp_table.setStyle(self._get_table_style())
        
        self.story.append(temp_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_pulse_section(self, pulse_data):
        """Add pulse data section."""
        if not pulse_data:
            return
        
        self.story.append(Paragraph("Pulse/Heart Rate", self.heading_style))
        
        table_data = [['Date & Time', 'Pulse (bpm)', 'Status']]
        
        for pulse in pulse_data:
            date_str = pulse.timestamp.strftime('%Y-%m-%d %H:%M')
            reading = pulse.pulse_reading
            
            if 60 <= reading <= 100:
                status = "Normal"
            elif reading < 60:
                status = "Low"
            else:
                status = "High"
            
            table_data.append([date_str, str(reading), status])
        
        pulse_table = Table(table_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        pulse_table.setStyle(self._get_table_style())
        
        self.story.append(pulse_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_exercise_section(self, exercise_data):
        """Add exercise data section."""
        if not exercise_data:
            return
        
        self.story.append(Paragraph("Exercise", self.heading_style))
        
        table_data = [['Date', 'Duration', 'Type']]
        
        for exercise in exercise_data:
            date_str = exercise.timestamp.strftime('%Y-%m-%d')
            duration = f"{exercise.exercise_duration_in_minutes} minutes"
            exercise_type = exercise.get_type_display()
            
            table_data.append([date_str, duration, exercise_type])
        
        exercise_table = Table(table_data, colWidths=[2*inch, 2*inch, 2.5*inch])
        exercise_table.setStyle(self._get_table_style())
        
        self.story.append(exercise_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_sleep_section(self, sleep_data):
        """Add sleep data section."""
        if not sleep_data:
            return
        
        self.story.append(Paragraph("Sleep", self.heading_style))
        
        table_data = [['Date', 'Duration (Hours)', 'Status']]
        
        for sleep in sleep_data:
            date_str = sleep.timestamp.strftime('%Y-%m-%d')
            duration = f"{sleep.sleep_duration_hours:.2f}"
            
            status = "Good" if 6 <= sleep.sleep_duration_hours <= 8 else "Needs Improvement"
            
            table_data.append([date_str, duration, status])
        
        sleep_table = Table(table_data, colWidths=[2*inch, 2*inch, 2.5*inch])
        sleep_table.setStyle(self._get_table_style())
        
        self.story.append(sleep_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_stress_section(self, stress_data):
        """Add stress data section."""
        if not stress_data:
            return
        
        self.story.append(Paragraph("Stress Level", self.heading_style))
        
        table_data = [['Date', 'Level', 'Status']]
        
        for stress in stress_data:
            date_str = stress.timestamp.strftime('%Y-%m-%d')
            level = stress.level
            
            # Map CharField choices to display values
            if level == 'L':
                status = "Low"
                level_display = "Low"
            elif level == 'M':
                status = "Moderate"
                level_display = "Medium"
            else:  # 'H'
                status = "High"
                level_display = "High"
            
            table_data.append([date_str, level_display, status])
        
        stress_table = Table(table_data, colWidths=[2*inch, 2*inch, 2.5*inch])
        stress_table.setStyle(self._get_table_style())
        
        self.story.append(stress_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_health_profile_section(self, profile):
        """Add health profile summary section."""
        if not profile:
            return
        
        self.story.append(Paragraph("Health Profile Summary", self.heading_style))
        
        profile_data = [
            ['Gender:', profile.get_gender_display()],
            ['Height:', f"{profile.height_in_meters} m"],
            ['Smoker:', 'Yes' if profile.is_smoker else 'No'],
            ['Disabled:', 'Yes' if profile.is_disabled else 'No'],
        ]
        
        profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ]))
        
        self.story.append(profile_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def _get_table_style(self):
        """Get standard table style."""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ])
    
    def generate(self):
        """Build and return the PDF."""
        self.doc.build(self.story)
        self.buffer.seek(0)
        return self.buffer
