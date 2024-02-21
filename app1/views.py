from django.shortcuts import render

from app1.models import tanks
from django.http import JsonResponse
from app1.models import marker

import json
from django.http import JsonResponse

from django.db.models import Max
from django.db.models import F

# Create your views here.
def index(request):
    tank = tanks.objects.all()
    # print(tank)
    
    
    data = {
        'tank':tank,
    }
    
    return render(request, "index.html",data)

def all_tanks(request):
    tank = tanks.objects.all()
    # print(tank)
    
    
    data = {
        'tank':tank,
    }
    return render(request, "all_tanks.html",data)

def draw_line(request):
    
    tank = tanks.objects.all()
    
    markers = marker.objects.all()
    
    print(get_markers_by_path_id())
    
    
    
    
    data = {
        'tank':tank,
        'marker':marker,
     
    }
    
    return render(request, "draw_line.html",data)







from django.db.models import Max, Q

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def save_markers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        markers_data = data.get('markers', [])  # Retrieve the markers array from the data

        # Fetch the latest path_id from the database
        latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
        new_path_id = latest_path_id + 1 if latest_path_id is not None else 1

        # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
        for index, marker_info in enumerate(markers_data, start=1):
            lat = marker_info.get('latitude')
            lon = marker_info.get('longitude')
            marker_type = marker_info.get('type')

            # Check if a marker with the same latitude, longitude, and type already exists
            existing_marker = marker.objects.filter(
                latitude=lat,
                longitude=lon,
                type=marker_type
            ).first()

            if existing_marker:
                # Skip saving duplicate data
                continue

            new_marker = marker.objects.create(
                path_id=new_path_id,
                point_id=index,  # Use the index variable for sequential point_id
                latitude=lat,
                longitude=lon,
                type=marker_type
            )
            new_marker.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_existing_marker(request):
    from app1.models import marker
    if request.method == 'POST':
        data = json.loads(request.body)
        path_id = data.get('path_id')
        point_id = data.get('point_id')

        last_point = marker.objects.filter(path_id=path_id).last()
        all_markers = marker.objects.filter(path_id=path_id)

        serialized_markers = []
        
        
        
        if last_point==point_id:
            
            for marker in all_markers:
                serialized_markers.append({
                    'latitude': marker.latitude,
                    'longitude': marker.longitude,
                    'type':marker.type ,
                    'path_id': marker.path_id,
                    'point_id': marker.point_id
                    # Add other fields if needed
                
                })
      

     
        return JsonResponse({'success': True, 'markers': serialized_markers})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



    
def get_markers(request):
    
    from app1.models import  marker
    
    markers = marker.objects.all()
    markers_by_path = get_markers_by_path_id()

    # Serialize marker data
    serialized_markers = []
    for marker in markers:
        serialized_markers.append({
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            'type':marker.type ,
            'path_id': marker.path_id,
            'point_id': marker.point_id
            # Add other fields if needed
           
        })
        
        
    # Create a dictionary to store markers by sequence number

    
    

    # Return serialized marker data as JSON response
    return JsonResponse({'success': True, 'markers': serialized_markers, 'markers_by_path':markers_by_path})
        
        
        
        


# Assuming you have imported the marker model and other necessary modules

def get_markers_by_path_id():
    # Get distinct path_ids
    path_ids = marker.objects.values_list('path_id', flat=True).distinct()

    markers_by_path = {}
    for path_id in path_ids:
        # Filter markers by path_id and order them by point_id
        markers = marker.objects.filter(path_id=path_id).order_by('point_id')

        # Retrieve latitude and longitude pairs for the current path_id
        latitude_longitude_pairs = [(marker.latitude, marker.longitude) for marker in markers]

        # Store latitude and longitude pairs in the dictionary with path_id as key
        markers_by_path[path_id] = latitude_longitude_pairs

    return markers_by_path



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_marker_point(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        marker_id = data.get('marker_id')
        path_id = data.get('path_id')
        
        try:
            # Fetch the latest point_id for the given path_id
            latest_point_id = marker.objects.filter(path_id=path_id).latest('point_id').point_id
            # Update the marker's point_id
            marker_obj = marker.objects.get(point_id=marker_id)
            marker_obj.point_id = latest_point_id + 1  # Increment the point_id
            marker_obj.save()
            return JsonResponse({'success': True})
        except marker.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Marker not found'})
        except marker.MultipleObjectsReturned:
            return JsonResponse({'success': False, 'error': 'Multiple markers found for the same path'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})