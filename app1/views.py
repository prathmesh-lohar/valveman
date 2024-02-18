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








# def save_markers(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         latitude_list = data.get('latitudeList', [])
#         longitude_list = data.get('longitudeList', [])
#         marker_type = data.get('type', None)  

#         # Print to check if lists are received
#         print("Latitude List:", latitude_list)
#         print("Longitude List:", longitude_list)
        
#         print("Type:", marker_type)

        
#         # Save latitude and longitude pairs to database
#         for  lat, lon in zip(latitude_list, longitude_list):
#             new_marker = marker.objects.create(latitude=lat, longitude=lon)
#             new_marker.save()
                   

#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.db.models import Max

def save_markers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude_list = data.get('latitudeList', [])
        longitude_list = data.get('longitudeList', [])
        marker_type = data.get('type', None)  

        # Fetch the latest path_id from the database
        latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
        new_path_id = latest_path_id + 1 if latest_path_id is not None else 1

        # Save latitude and longitude pairs to database with incremented path_id and sequential point_id
        for index, (lat, lon) in enumerate(zip(latitude_list, longitude_list), start=1):
            new_marker = marker.objects.create(
                path_id=new_path_id, 
                point_id=index,
                latitude=lat, 
                longitude=lon,
                type=marker_type
            )
            new_marker.save()
                   
        return JsonResponse({'success': True})
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
            'type':marker.type  
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

