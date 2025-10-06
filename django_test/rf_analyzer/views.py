"""
RF Analyzer Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import pandas as pd
from pathlib import Path
import sys

from .models import MeasurementSession, MeasurementFile, MeasurementData
from .forms import CsvUploadForm

# Add prototype to path for CSV parser
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'prototype'))
from parsers.csv_parser import CsvParser


def index(request):
    """Home page - CSV upload form"""
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            return handle_csv_upload(request, form)
    else:
        form = CsvUploadForm()

    recent_sessions = MeasurementSession.objects.all()[:5]
    context = {'form': form, 'recent_sessions': recent_sessions}
    return render(request, 'rf_analyzer/index.html', context)


def handle_csv_upload(request, form):
    """Handle CSV file upload and parsing"""
    session = MeasurementSession.objects.create(
        name=form.cleaned_data['session_name'],
        description=form.cleaned_data['description'],
        user=None
    )

    csv_file = form.cleaned_data['csv_file']
    measurement_file = MeasurementFile.objects.create(
        session=session,
        file=csv_file,
        filename=csv_file.name,
        file_type='csv',
        file_size=csv_file.size
    )

    try:
        parse_csv_to_database(measurement_file)
        measurement_file.is_parsed = True
        measurement_file.save()
        return redirect('rf_analyzer:viewer', session_id=session.id)
    except Exception as e:
        session.delete()
        form.add_error('csv_file', f'Error parsing CSV: {str(e)}')
        return render(request, 'rf_analyzer/index.html', {'form': form})


def parse_csv_to_database(measurement_file):
    """Parse CSV file and save data to database"""
    file_path = Path(measurement_file.file.path)
    parser = CsvParser(file_path)
    parser.load_consolidated()
    df = parser.data

    batch_size = 1000
    data_points = []

    for index, row in df.iterrows():
        data_point = MeasurementData(
            session=measurement_file.session,
            cfg_band=row['Cfg Band'],
            cfg_lna_gain_state=row['cfg-lna_gain_state'],
            cfg_active_port_1=row['cfg-active_port_1'],
            cfg_active_port_2=row['cfg-active_port_2'],
            debug_nplexer_bank=row['debug-nplexer_bank'],
            active_rf_path=row['Active RF Path'],
            frequency_mhz=row['Frequency'],
            gain_db=row['Gain (dB)']
        )
        data_points.append(data_point)

        if len(data_points) >= batch_size:
            MeasurementData.objects.bulk_create(data_points)
            data_points = []

    if data_points:
        MeasurementData.objects.bulk_create(data_points)


def viewer(request, session_id):
    """Grid viewer page"""
    session = get_object_or_404(MeasurementSession, id=session_id)

    bands = MeasurementData.objects.filter(session=session).values_list('cfg_band', flat=True).distinct().order_by('cfg_band')
    lna_states = MeasurementData.objects.filter(session=session).values_list('cfg_lna_gain_state', flat=True).distinct().order_by('cfg_lna_gain_state')
    input_ports = MeasurementData.objects.filter(session=session).values_list('cfg_active_port_1', flat=True).distinct().order_by('cfg_active_port_1')

    selected_band = request.GET.get('band', bands[0] if bands else None)
    selected_lna = request.GET.get('lna', lna_states[0] if lna_states else None)
    selected_port = request.GET.get('port', input_ports[0] if input_ports else None)

    context = {
        'session': session,
        'bands': bands,
        'lna_states': lna_states,
        'input_ports': input_ports,
        'selected_band': selected_band,
        'selected_lna': selected_lna,
        'selected_port': selected_port,
    }
    return render(request, 'rf_analyzer/viewer.html', context)


def get_chart_data(request, session_id):
    """
    API endpoint: Get chart data as JSON
    """
    session = get_object_or_404(MeasurementSession, id=session_id)
    
    band = request.GET.get('band')
    lna = request.GET.get('lna')
    port = request.GET.get('port')
    
    if not all([band, lna, port]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    # Get grid data from database
    from utils.chart_generator import ChartGenerator
    
    # Query data points
    data_points = MeasurementData.objects.filter(
        session=session,
        cfg_band=band,
        cfg_lna_gain_state=lna,
        cfg_active_port_1=port
    ).order_by('debug_nplexer_bank', 'cfg_active_port_2', 'frequency_mhz')
    
    # Organize into grid structure
    grid_data = {}
    for point in data_points:
        ca_combo = point.debug_nplexer_bank
        output_port = point.cfg_active_port_2
        
        if ca_combo not in grid_data:
            grid_data[ca_combo] = {}
        
        if output_port not in grid_data[ca_combo]:
            grid_data[ca_combo][output_port] = {
                'frequency': [],
                'gain_db': [],
                'count': 0
            }
        
        grid_data[ca_combo][output_port]['frequency'].append(float(point.frequency_mhz))
        grid_data[ca_combo][output_port]['gain_db'].append(float(point.gain_db))
        grid_data[ca_combo][output_port]['count'] += 1
    
    # Generate Plotly figure
    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band=band,
        lna_gain_state=lna,
        input_port=port,
        compact_size=(300, 200)
    )
    
    # Return as JSON
    return JsonResponse({
        'success': True,
        'chart': fig.to_json(),
        'data_points': sum(d[p]['count'] for d in grid_data.values() for p in d)
    })


def export_pdf(request, session_id):
    """
    API endpoint: Export current chart as PDF
    """
    session = get_object_or_404(MeasurementSession, id=session_id)

    band = request.GET.get('band')
    lna = request.GET.get('lna')
    port = request.GET.get('port')

    if not all([band, lna, port]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Get grid data (same as get_chart_data)
    from utils.chart_generator import ChartGenerator

    data_points = MeasurementData.objects.filter(
        session=session,
        cfg_band=band,
        cfg_lna_gain_state=lna,
        cfg_active_port_1=port
    ).order_by('debug_nplexer_bank', 'cfg_active_port_2', 'frequency_mhz')

    # Organize into grid structure
    grid_data = {}
    for point in data_points:
        ca_combo = point.debug_nplexer_bank
        output_port = point.cfg_active_port_2

        if ca_combo not in grid_data:
            grid_data[ca_combo] = {}

        if output_port not in grid_data[ca_combo]:
            grid_data[ca_combo][output_port] = {
                'frequency': [],
                'gain_db': [],
                'count': 0
            }

        grid_data[ca_combo][output_port]['frequency'].append(float(point.frequency_mhz))
        grid_data[ca_combo][output_port]['gain_db'].append(float(point.gain_db))
        grid_data[ca_combo][output_port]['count'] += 1

    # Generate Plotly figure
    fig = ChartGenerator.create_compact_grid(
        grid_data=grid_data,
        band=band,
        lna_gain_state=lna,
        input_port=port,
        compact_size=(300, 200)
    )

    # Export to PDF using kaleido
    pdf_bytes = fig.to_image(format='pdf', width=1920, height=1200)

    # Return PDF as downloadable file
    filename = f'chart_{band}_{lna}_{port}.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def export_full_report_pdf(request, session_id):
    """
    API endpoint: Export full report PDF with all Band/LNA/Port combinations
    """
    session = get_object_or_404(MeasurementSession, id=session_id)

    # Get all available combinations from database
    from django.db.models import Q
    from utils.chart_generator import ChartGenerator
    import io
    from PyPDF2 import PdfMerger

    # Get unique combinations that have data
    combinations = MeasurementData.objects.filter(
        session=session
    ).values('cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1').distinct().order_by(
        'cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1'
    )

    if not combinations.exists():
        return JsonResponse({'error': 'No data available'}, status=404)

    # Create PDF merger
    merger = PdfMerger()
    total_pages = 0

    # Generate PDF for each combination
    for combo in combinations:
        band = combo['cfg_band']
        lna = combo['cfg_lna_gain_state']
        port = combo['cfg_active_port_1']

        # Get grid data for this combination
        data_points = MeasurementData.objects.filter(
            session=session,
            cfg_band=band,
            cfg_lna_gain_state=lna,
            cfg_active_port_1=port
        ).order_by('debug_nplexer_bank', 'cfg_active_port_2', 'frequency_mhz')

        # Organize into grid structure
        grid_data = {}
        for point in data_points:
            ca_combo = point.debug_nplexer_bank
            output_port = point.cfg_active_port_2

            if ca_combo not in grid_data:
                grid_data[ca_combo] = {}

            if output_port not in grid_data[ca_combo]:
                grid_data[ca_combo][output_port] = {
                    'frequency': [],
                    'gain_db': [],
                    'count': 0
                }

            grid_data[ca_combo][output_port]['frequency'].append(float(point.frequency_mhz))
            grid_data[ca_combo][output_port]['gain_db'].append(float(point.gain_db))
            grid_data[ca_combo][output_port]['count'] += 1

        # Generate Plotly figure
        fig = ChartGenerator.create_compact_grid(
            grid_data=grid_data,
            band=band,
            lna_gain_state=lna,
            input_port=port,
            compact_size=(300, 200)
        )

        # Export to PDF
        pdf_bytes = fig.to_image(format='pdf', width=1920, height=1200)

        # Append to merger
        pdf_stream = io.BytesIO(pdf_bytes)
        merger.append(pdf_stream)
        total_pages += 1

    # Write merged PDF to output
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    # Return as downloadable file
    filename = f'full_report_{session.name}_{total_pages}pages.pdf'
    response = HttpResponse(output.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
