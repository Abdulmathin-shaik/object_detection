from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DefectDetection
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
from django.core.files.base import ContentFile
import io
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Define MODELS dictionary at module level
MODELS = {}

def get_model(model_type):
    """Get or load YOLO model"""
    if model_type not in MODELS:
        logger.info(f"Loading model: {model_type}")
        MODELS[model_type] = YOLO(f'{model_type}.pt')
    return MODELS[model_type]

def inspection_page(request):
    return render(request, 'defect_app/inspect.html')

@csrf_exempt
def analyze_defect(request):
    if request.method == 'POST':
        try:
            logger.info("Received POST request for defect analysis")
            
            # Get form data
            name = request.POST.get('name')
            serial = request.POST.get('serial')
            model_type = request.POST.get('model')
            image_file = request.FILES.get('image')

            logger.info(f"Received data - Name: {name}, Serial: {serial}, Model: {model_type}")

            if not all([name, serial, model_type, image_file]):
                logger.error("Missing required fields")
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields'
                })

            try:
                # Load image
                logger.info("Loading image")
                image = Image.open(image_file)
                
                # Convert PIL Image to CV2 format
                logger.info("Converting image to OpenCV format")
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # Get model and run inference
                logger.info("Running model inference")
                model = get_model(model_type)
                results = model(opencv_image)
                
                # Process detection results
                logger.info("Processing detection results")
                detection_counts = {}
                for r in results:
                    for c in r.boxes.cls:
                        class_name = model.names[int(c)]
                        detection_counts[class_name] = detection_counts.get(class_name, 0) + 1

                # Plot results
                logger.info("Plotting results")
                plotted_image = results[0].plot()
                
                # Convert back to PIL Image
                logger.info("Converting back to PIL Image")
                plotted_image_rgb = cv2.cvtColor(plotted_image, cv2.COLOR_BGR2RGB)
                annotated_image = Image.fromarray(plotted_image_rgb)

                # Save to bytes
                logger.info("Saving image to bytes")
                img_byte_arr = io.BytesIO()
                annotated_image.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)

                # Create Django image file
                image_content = ContentFile(img_byte_arr.getvalue())

                # Save to database
                logger.info("Saving to database")
                detection = DefectDetection.objects.create(
                    name=name,
                    serial_number=serial,
                    model_type=model_type,
                    defect_results=detection_counts
                )
                
                # Save annotated image
                logger.info("Saving annotated image")
                detection.image.save(
                    f'annotated_{serial}.jpg',
                    image_content,
                    save=True
                )

                logger.info("Successfully processed defect detection")
                return JsonResponse({
                    'success': True,
                    'results': detection_counts,
                    'image_url': detection.image.url
                })

            except Exception as e:
                logger.error(f"Error during image processing: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': f'Error processing image: {str(e)}'
                })

        except Exception as e:
            logger.error(f"Error in analyze_defect view: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    logger.warning("Invalid request method")
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def inspection_history(request):
    inspections = DefectDetection.objects.all().order_by('-inspection_date')
    return render(request, 'defect_app/history.html', {'inspections': inspections})

