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

        # Check if it's an AJAX request (XMLHttpRequest)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response with redirect URL for AJAX
            from django.urls import reverse
            viewer_url = reverse('rf_analyzer:viewer', kwargs={'session_id': session.id})
            return JsonResponse({
                'success': True,
                'redirect_url': viewer_url,
                'session_id': session.id
            })
        else:
            # Normal form submission - redirect
            return redirect('rf_analyzer:viewer', session_id=session.id)
    except Exception as e:
        session.delete()

        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        else:
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
    import time
    from .progress_tracker import ProgressTracker
    
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
    total_combinations = combinations.count()

    # Initialize progress tracker
    tracker = ProgressTracker(session_id)
    tracker.start(total_combinations, f'Full Report PDF - {session.name}')

    # Log start
    print()
    print("=" * 60)
    print(f"[Full Report PDF] Starting generation for session: {session.name}")
    print(f"[Full Report PDF] Total combinations to process: {total_combinations}")
    print(f"[Full Report PDF] Estimated time: {total_combinations * 2}-{total_combinations * 4} seconds")
    print("=" * 60)
    print()

    start_time = time.time()

    # Generate PDF for each combination
    for idx, combo in enumerate(combinations, 1):
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

        # Check if task was cancelled
        if tracker.is_cancelled():
            print(f"[Full Report PDF] Task cancelled by user at {idx}/{total_combinations}")
            tracker.complete(success=False, message=f'Task cancelled after processing {idx}/{total_combinations} pages')
            return JsonResponse({'error': 'Task cancelled by user'}, status=400)

        # Update progress tracker and log
        current_item = f'{band} {lna} {port}'
        tracker.update(idx, current_item)
        
        elapsed = time.time() - start_time
        avg_time_per_page = elapsed / idx
        remaining_pages = total_combinations - idx
        estimated_remaining = avg_time_per_page * remaining_pages
        print(f"[Full Report PDF] Progress: {idx}/{total_combinations} - {current_item} - Elapsed: {elapsed:.1f}s - ETA: {estimated_remaining:.1f}s")

    # Write merged PDF to output
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    # Calculate total time
    total_time = time.time() - start_time

    # Mark progress as complete
    tracker.complete(success=True, message=f'Generated {total_pages} pages in {int(total_time)}s')

    # Log completion
    print()
    print("=" * 60)
    print(f"[Full Report PDF] Generation complete!")
    print(f"[Full Report PDF] Total pages: {total_pages}")
    print(f"[Full Report PDF] Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print(f"[Full Report PDF] Average time per page: {total_time/total_pages:.1f} seconds")
    print("=" * 60)
    print()

    # Return as downloadable file
    filename = f'full_report_{session.name}_{total_pages}pages.pdf'
    response = HttpResponse(output.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response




def cancel_task(request, session_id):
    """
    API endpoint: Cancel ongoing PDF generation task
    """
    from .progress_tracker import ProgressTracker
    
    tracker = ProgressTracker(session_id)
    tracker.cancel()
    
    return JsonResponse({
        'success': True,
        'message': 'Task cancellation requested'
    })

def progress_stream(request, session_id):
    """
    SSE endpoint for real-time progress updates
    Returns Server-Sent Events stream
    """
    from django.http import StreamingHttpResponse
    from .progress_tracker import ProgressTracker
    import json
    import time

    def event_stream():
        """Generator function that yields SSE formatted messages"""
        tracker = ProgressTracker(session_id)

        # Keep streaming until task completes or times out
        max_duration = 3600  # 1 hour maximum
        check_interval = 0.5  # Check every 0.5 seconds
        elapsed = 0

        while elapsed < max_duration:
            progress_data = tracker.get_progress()

            if progress_data:
                # Format as SSE message
                yield f"data: {json.dumps(progress_data)}\n\n"

                # Check if task is complete
                if progress_data['status'] in ['completed', 'failed']:
                    break
            else:
                # No progress data yet, send waiting message
                yield f"data: {json.dumps({'status': 'waiting', 'message': 'Waiting for task to start...'})}\n\n"

            time.sleep(check_interval)
            elapsed += check_interval

        # Send final completion message
        yield f"data: {json.dumps({'status': 'done', 'message': 'Stream closed'})}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # Disable nginx buffering
    return response


def delete_session(request, session_id):
    """Delete a measurement session"""
    try:
        session = MeasurementSession.objects.get(id=session_id)
        session_name = session.name
        session.delete()  # Cascade delete will handle related files and data
        
        if request.htmx:
            # HTMX request - return success message
            return HttpResponse(f'<div class="alert alert-success">Session "{session_name}" deleted successfully</div>')
        else:
            # Regular request - redirect to index
            return redirect('rf_analyzer:index')
    except MeasurementSession.DoesNotExist:
        if request.htmx:
            return HttpResponse('<div class="alert alert-danger">Session not found</div>', status=404)
        else:
            return redirect('rf_analyzer:index')


def update_session(request, session_id):
    """Update session name and/or description"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    try:
        session = MeasurementSession.objects.get(id=session_id)

        # Get new values from request
        new_name = request.POST.get('name', '').strip()
        new_description = request.POST.get('description', '').strip()

        # Validate name
        if not new_name:
            return JsonResponse({'success': False, 'error': 'Name cannot be empty'}, status=400)

        # Update fields
        session.name = new_name
        session.description = new_description
        session.save()

        return JsonResponse({
            'success': True,
            'name': session.name,
            'description': session.description
        })
    except MeasurementSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def export_full_report_ppt(request, session_id):
    """
    API endpoint: Export full report PPT with all Band/LNA/Port combinations
    """
    import time
    import tempfile
    import shutil
    from .progress_tracker import ProgressTracker
    
    session = get_object_or_404(MeasurementSession, id=session_id)

    # Import PPT generator from prototype
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'prototype'))
    from utils.ppt_generator import PptGenerator
    from utils.chart_generator import ChartGenerator

    # Get all available combinations from database
    combinations = MeasurementData.objects.filter(
        session=session
    ).values('cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1').distinct().order_by(
        'cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1'
    )

    if not combinations.exists():
        return JsonResponse({'error': 'No data available'}, status=404)

    total_combinations = combinations.count()

    # Initialize progress tracker
    tracker = ProgressTracker(session_id)
    tracker.start(total_combinations, f'Full Report PPT - {session.name}')

    # Log start
    print()
    print("=" * 60)
    print(f"[Full Report PPT] Starting generation for session: {session.name}")
    print(f"[Full Report PPT] Total combinations to process: {total_combinations}")
    print(f"[Full Report PPT] Estimated time: {total_combinations * 3}-{total_combinations * 5} seconds")
    print("=" * 60)
    print()

    start_time = time.time()

    # Create temporary directory for PNG files
    temp_dir = Path(tempfile.mkdtemp(prefix='ppt_export_'))
    
    try:
        # Initialize PPT generator (no template for now)
        ppt_gen = PptGenerator(template_path=None)
        
        # Generate PNG and add slide for each combination
        for idx, combo in enumerate(combinations, 1):
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

            # Export to PNG (PPT requires PNG)
            png_filename = f'{band}_{lna}_{port}.png'
            png_path = temp_dir / png_filename
            png_bytes = fig.to_image(format='png', width=1920, height=1200)
            
            with open(png_path, 'wb') as f:
                f.write(png_bytes)

            # Add slide to PPT
            title = f'{band} {lna} {port} LNA Gain'
            ppt_gen.add_slide_with_image(title, png_path)

            # Check if task was cancelled
            if tracker.is_cancelled():
                print(f"[Full Report PPT] Task cancelled by user at {idx}/{total_combinations}")
                tracker.complete(success=False, message=f'Task cancelled after processing {idx}/{total_combinations} slides')
                shutil.rmtree(temp_dir)
                return JsonResponse({'error': 'Task cancelled by user'}, status=400)

            # Update progress tracker and log
            current_item = f'{band} {lna} {port}'
            tracker.update(idx, current_item)
            
            elapsed = time.time() - start_time
            avg_time_per_slide = elapsed / idx
            remaining_slides = total_combinations - idx
            estimated_remaining = avg_time_per_slide * remaining_slides
            print(f"[Full Report PPT] Progress: {idx}/{total_combinations} - {current_item} - Elapsed: {elapsed:.1f}s - ETA: {estimated_remaining:.1f}s")

        # Save PPT to temporary file
        output_ppt_path = temp_dir / 'full_report.pptx'
        ppt_gen.save(output_ppt_path)

        # Calculate total time
        total_time = time.time() - start_time

        # Mark progress as complete
        tracker.complete(success=True, message=f'Generated {total_combinations} slides in {int(total_time)}s')

        # Log completion
        print()
        print("=" * 60)
        print(f"[Full Report PPT] Generation complete!")
        print(f"[Full Report PPT] Total slides: {total_combinations}")
        print(f"[Full Report PPT] Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"[Full Report PPT] Average time per slide: {total_time/total_combinations:.1f} seconds")
        print("=" * 60)
        print()

        # Read PPT file
        with open(output_ppt_path, 'rb') as f:
            ppt_data = f.read()

        # Cleanup temporary directory
        shutil.rmtree(temp_dir)

        # Return as downloadable file
        filename = f'full_report_{session.name}_{total_combinations}slides.pptx'
        response = HttpResponse(ppt_data, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        # Cleanup on error
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        tracker.complete(success=False, message=f'Error: {str(e)}')
        print(f"[Full Report PPT] Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
