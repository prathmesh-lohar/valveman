from django.shortcuts import render

from app1.models import tanks
from django.http import JsonResponse
from app1.models import marker

import json
from django.http import JsonResponse


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
    # print(tank)
    
    
    data = {
        'tank':tank,
        'marker':marker,
    }
    
    return render(request, "draw_line.html",data)








def save_markers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude_list = data.get('latitudeList', [])
        longitude_list = data.get('longitudeList', [])
        marker_type = data.get('type', None)  

        # Print to check if lists are received
        print("Latitude List:", latitude_list)
        print("Longitude List:", longitude_list)
        
        print("Type:", marker_type)

        # Your code to save the lists
        
        # Separate latitude and longitude lists
        
        # for index,value in enumerate(latitude_list):
        #     print(f"lattitude , Index: {index}, Value: {value}")
            
        # for index,value in enumerate(longitude_list):
        #     print(f"longitude , Index: {index}, Value: {value}")
        
        
        
        # # Save latitude and longitude pairs to database
        # for lat, lon in zip(latitude_list, longitude_list):
        #     new_marker = marker.objects.create(latitude=lat, longitude=lon)
        #     new_marker.save()
        
        for seq, (lat, lon) in enumerate(zip(latitude_list, longitude_list), start=1):
            new_marker = marker.objects.create(latitude=lat, longitude=lon, type=marker_type, seq=seq)
            new_marker.save() 
                

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_markers(request):
    
    from app1.models import  marker
    
    markers = marker.objects.all()

    # Serialize marker data
    serialized_markers = []
    for marker in markers:
        serialized_markers.append({
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            'type':marker.type    
            # Add other fields if needed
        })

    # Return serialized marker data as JSON response
    return JsonResponse({'success': True, 'markers': serialized_markers})
        