from django.shortcuts import render

from app1.models import tanks
from django.http import JsonResponse
from app1.models import marker

import json
from django.http import JsonResponse

from django.db.models import Max
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User,auth

from django.shortcuts import render,HttpResponse,redirect

from django.contrib.auth.decorators import login_required

up_index = 0
up_path_id = 0


# Create your views here.
@login_required(login_url='/login')

def index(request):
    
    
    tank = tanks.objects.all()
    # print(tank)
    
    
    data = {
        'tank':tank,
    }
    
    return render(request, "index.html",data)


def logout(request):
    auth.logout(request)

    return redirect('/')



def login (request):
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')

        
        user = auth.authenticate(username=uname, password=pwd)
            
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return HttpResponse("uname , password invalid ")
    
    return render(request, "login.html")


@login_required(login_url='/login')

def all_tanks(request):
    print(up_index)
    
    tank = tanks.objects.all()
    # print(tank)
    
    
    data = {
        'tank':tank,
    }
    return render(request, "all_tanks.html",data)


@login_required(login_url='/login')

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




def extend(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        markers_data = data.get('markers', [])  # Retrieve the markers array from the data
        up_index = data.get('up_index')
        up_path_id = data.get('up_path_id')
        
        print("up_index:",up_path_id, "up_path_id",up_path_id)

        # Fetch the latest path_id from the database
        # latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
        # new_path_id = latest_path_id + 1 if latest_path_id is not None else 1
        
        latest_path_id = up_path_id
        new_path_id = up_path_id
        
        start = int(up_index)

        # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
        for index, marker_info in enumerate(markers_data, start=start+1):
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





from django.db import transaction

@csrf_exempt
def save_marker_point_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        marker_id = data.get('marker_id')
        new_point_id = data.get('new_point_id')
        path_id = data.get('path_id')
        
        print(marker_id, new_point_id, path_id)  # Check if the marker_id is received
        
        # Check if the marker ID is valid
        if not marker_id:
            return JsonResponse({'success': False, 'error': 'Invalid marker ID'})

        try:
            with transaction.atomic():
                marker_obj = marker.objects.get(id=marker_id)
                marker_obj.point_id = new_point_id
                marker_obj.path_id = path_id
                marker_obj.save()
        except marker.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Marker not found'})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def forextend(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        marker_id = data.get('marker_id')
        new_point_id = data.get('new_point_id')
        path_id = data.get('path_id')
        
        print(marker_id, new_point_id, path_id)  # Check if the marker_id is received
        
        # Check if the marker ID is valid
        
    

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
