from django.shortcuts import render, redirect, HttpResponse

from app1.models import tanks
from django.http import JsonResponse
from app1.models import marker
from app1.models import jw

import json
from django.http import JsonResponse

from django.db.models import Max
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User,auth

from django.shortcuts import render,HttpResponse,redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages


up_index = 0
up_path_id = 0

# to get tank type
marker_type = "";


# Create your views here.
@login_required(login_url='/login')

def index(request):
    
    
    tank = tanks.objects.all()
    # print(tank)
    
    
    data = {
        'tank':tank,
    }
    
    # return render(request, "index.html",data)
    return redirect("/draw_line")



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
            # return redirect('/')
            return redirect("/draw_line")
            
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
    
    from app1.models import jw,marker
    
    tank = tanks.objects.all()
    jw = jw.objects.all()
    
    markers = marker.objects.all()
    
    print(get_markers_by_path_id())
    
    
    
    
    data = {
        'tank':tank,
        'marker':marker,
        'jw':jw,
     
    }
    
    return render(request, "draw_line.html",data)







from django.db.models import Max, Q

from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# def save_markers(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
#         latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
#         new_path_id = latest_path_id + 1 if latest_path_id is not None else 1

#         for index, marker_info in enumerate(markers_data, start=1):
#             lat = marker_info.get('latitude')
#             lon = marker_info.get('longitude')
#             marker_type = marker_info.get('type')
            
#             # Set default marker type if not provided
#             if marker_type is None:
#                 marker_type = 'tank'

#             # Create a new marker
#             new_marker = marker.objects.create(
#                 path_id=new_path_id,
#                 point_id=index,
#                 latitude=lat,
#                 longitude=lon,
#                 type=marker_type,
#                 user_id=request.user.id,
#                 pip_material=pipe_material[index - 1] if index <= len(pipe_material) else None,
#                 pip_diameter=pipe_diameter[index - 1] if index <= len(pipe_diameter) else None,
#                 valve_type=valve_type[index - 1] if index <= len(valve_type) else None,
#                 valve_key_size=valve_key_size[index - 1] if index <= len(valve_key_size) else None,
#                 valve_diameter=valve_diameter[index - 1] if index <= len(valve_diameter) else None,
#             )
#             new_marker.save()

#         # Move success message outside the loop
#         messages.success(request, 'Markers saved successfully')

#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def save_markers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        markers_data = data.get('markers', [])
        
        pipe_material = data.get('pipe_material', [])
        pipe_diameter = data.get('pipe_diameter', [])
        valve_type = data.get('valve_type', [])
        valve_diameter = data.get('valve_diameter', [])
        valve_key_size = data.get('valve_key_size', [])
        
        print(markers_data)
        print(pipe_material,pipe_diameter,valve_type,valve_diameter,valve_key_size)
        
        latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
        new_path_id = latest_path_id + 1 if latest_path_id is not None else 1

        for index, marker_info in enumerate(markers_data, start=1):
            lat = marker_info.get('latitude')
            lon = marker_info.get('longitude')
            marker_type = marker_info.get('type')
            
            # Set default marker type if not provided
            if marker_type is None:
                marker_type = 'start'

            # Check if a marker with the same path_id and point_id already exists
            existing_marker = marker.objects.filter(path_id=new_path_id, point_id=index).first()
            if existing_marker is None:
                # Create a new marker
                new_marker = marker.objects.create(
                    path_id=new_path_id,
                    point_id=index,
                    latitude=lat,
                    longitude=lon,
                    type=marker_type,
                    user_id=request.user.id,
                    
                    pip_material=pipe_material[index - 1] if index <= len(pipe_material) else None,
                    pip_diameter=pipe_diameter[index - 1] if index <= len(pipe_diameter) else None,
                    
                    valve_type=valve_type[index - 1] if index <= len(valve_type) else None,
                    valve_key_size=valve_key_size[index - 1] if index <= len(valve_key_size) else None,
                    valve_diameter=valve_diameter[index - 1] if index <= len(valve_diameter) else None,
                )
                new_marker.save()

        # Move success message outside the loop
        messages.success(request, 'Markers saved successfully')

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



# def extend(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])  # Retrieve the markers array from the data
#         up_index = data.get('up_index')
#         up_path_id = data.get('up_path_id')
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
        
        
#         print("up_index:",up_path_id, "up_path_id",up_path_id)

#         # Fetch the latest path_id from the database
#         # latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
#         # new_path_id = latest_path_id + 1 if latest_path_id is not None else 1
        
#         latest_path_id = up_path_id
#         new_path_id = up_path_id
        
#         start = int(up_index)
        
#         last_marker = marker.objects.filter(path_id=latest_path_id).last()
        
#         if up_index == last_marker.point_id:

#             # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
#             for index, marker_info in enumerate(markers_data, start=start+1):
#                 lat = marker_info.get('latitude')
#                 lon = marker_info.get('longitude')
#                 marker_type = marker_info.get('type')

#                 # Check if a marker with the same latitude, longitude, and type already exists
#                 existing_marker = marker.objects.filter(
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type
#                 ).first()

#                 if existing_marker:
#                     # Skip saving duplicate data
#                     continue

#                 new_marker = marker.objects.create(
#                     path_id=new_path_id,
#                     point_id=index,  # Use the index variable for sequential point_id
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type,
                    
#                     user_id = request.user.id,
                    
#                     pip_material=pipe_material[index - 1] if index <= len(pipe_material) else None,
#                     pip_diameter=pipe_diameter[index - 1] if index <= len(pipe_diameter) else None,
                    
#                     valve_type=valve_type[index - 1] if index <= len(valve_type) else None,
#                     valve_key_size=valve_key_size[index - 1] if index <= len(valve_key_size) else None,
#                     valve_diameter=valve_diameter[index - 1] if index <= len(valve_diameter) else None,
                    
#                     )
#                 new_marker.save()

            
            
#             return JsonResponse({'success': True})
#         else:
#             messages.error(request, 'selcted point was not last point of line')
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})



# @csrf_exempt
# def extend(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])  # Retrieve the markers array from the data
#         up_index = data.get('up_index')
#         up_path_id = data.get('up_path_id')
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
#         print(markers_data)
#         print(valve_type)
        
#         print("up_index:", up_index, "up_path_id:", up_path_id)

#         # Fetch the latest path_id from the database
#         latest_path_id = up_path_id
#         new_path_id = up_path_id
        
#         start = int(up_index)
        
#         last_marker = marker.objects.filter(path_id=latest_path_id).last()
        
#         if up_index == last_marker.point_id:
#             # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
#             for index, marker_info in enumerate(markers_data, start=start+1):
#                 lat = marker_info.get('latitude')
#                 lon = marker_info.get('longitude')
#                 marker_type = marker_info.get('type')

#                 # Check if a marker with the same latitude, longitude, and type already exists
#                 existing_marker = marker.objects.filter(
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type
#                 ).first()

#                 if existing_marker:
#                     # Skip saving duplicate data
#                     continue

#                 new_marker = marker.objects.create(
#                     path_id=new_path_id,
#                     point_id=index,  # Use the index variable for sequential point_id
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type,
#                     user_id=request.user.id,
#                 )
#                 new_marker.save()

#             return JsonResponse({'success': True})
#         else:
#             messages.error(request, 'Selected point was not the last point of the line')
#             return JsonResponse({'success': False, 'error': 'Selected point was not the last point of the line'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})

# @csrf_exempt
# def extend(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])  # Retrieve the markers array from the data
#         up_index = data.get('up_index')
#         up_path_id = data.get('up_path_id')
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
#         print(markers_data)
#         print(pipe_diameter)
#         print(pipe_material)
        
#         print("up_index:", up_index, "up_path_id:", up_path_id)

#         # Fetch the latest path_id from the database
#         latest_path_id = up_path_id
#         new_path_id = up_path_id
        
#         start = int(up_index)
        
#         last_marker = marker.objects.filter(path_id=latest_path_id).last()
        
#         if up_index == last_marker.point_id:
#             # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
#             for index, marker_info in enumerate(markers_data, start=start+1):
#                 lat = marker_info.get('latitude')
#                 lon = marker_info.get('longitude')
#                 marker_type = marker_info.get('type')

#                 # Check if a marker with the same latitude, longitude, and type already exists
#                 existing_marker = marker.objects.filter(
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type
#                 ).first()

#                 if existing_marker:
#                     # Skip saving duplicate data
#                     continue

#                 # Calculate index for additional fields data
#                 additional_index = index - start - 1

#                 new_marker = marker.objects.create(
#                     path_id=new_path_id,
#                     point_id=index,  # Use the index variable for sequential point_id
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type,
#                     user_id=request.user.id,
#                     pip_material=pipe_material[additional_index] if additional_index < len(pipe_material) else None,
#                     pip_diameter=pipe_diameter[additional_index] if additional_index < len(pipe_diameter) else None,
#                     valve_type=valve_type[additional_index] if additional_index < len(valve_type) else None,
#                     valve_key_size=valve_key_size[additional_index] if additional_index < len(valve_key_size) else None,
#                     valve_diameter=valve_diameter[additional_index] if additional_index < len(valve_diameter) else None,
#                 )
#                 new_marker.save()

#             return JsonResponse({'success': True})
#         else:
#             messages.error(request, 'Selected point was not the last point of the line')
#             return JsonResponse({'success': False, 'error': 'Selected point was not the last point of the line'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})




#     if request.method == 'POST':
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])  # Retrieve the markers array from the data
#         up_index = data.get('up_index')
#         up_path_id = data.get('up_path_id')
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
#         print(markers_data)
#         print(pipe_diameter)
#         print(pipe_material)
        
#         print("up_index:", up_index, "up_path_id:", up_path_id)

#         # Fetch the latest path_id from the database
#         latest_path_id = up_path_id
#         new_path_id = up_path_id
        
#         start = int(up_index)
        
#         last_marker = marker.objects.filter(path_id=latest_path_id).last()
        
#         if up_index == last_marker.point_id:
#             # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
#             for index, marker_info in enumerate(markers_data, start=start+1):
#                 lat = marker_info.get('latitude')
#                 lon = marker_info.get('longitude')
#                 marker_type = marker_info.get('type')

#                 # Check if a marker with the same latitude, longitude, and type already exists
#                 existing_marker = marker.objects.filter(
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type
#                 ).first()

#                 if existing_marker:
#                     # Skip saving duplicate data
#                     continue

#                 # Calculate index for additional fields data
#                 additional_index = index - start - 1

#                 # Check if the values are empty strings
#                 pip_material_value = pipe_material[additional_index] if additional_index < len(pipe_material) else None
#                 pip_diameter_value = pipe_diameter[additional_index] if additional_index < len(pipe_diameter) else None
#                 valve_type_value = valve_type[additional_index] if additional_index < len(valve_type) else None
#                 valve_key_size_value = valve_key_size[additional_index] if additional_index < len(valve_key_size) else None
#                 valve_diameter_value = valve_diameter[additional_index] if additional_index < len(valve_diameter) else None

#                 # Skip saving if any value is an empty string
#                 if '' in [pip_material_value, pip_diameter_value, valve_type_value, valve_key_size_value, valve_diameter_value]:
#                     continue

#                 new_marker = marker.objects.create(
#                     path_id=new_path_id,
#                     point_id=index,  # Use the index variable for sequential point_id
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type,
#                     user_id=request.user.id,
#                     pip_material=pip_material_value,
#                     pip_diameter=pip_diameter_value,
#                     valve_type=valve_type_value,
#                     valve_key_size=valve_key_size_value,
#                     valve_diameter=valve_diameter_value,
#                 )
#                 new_marker.save()

#             return JsonResponse({'success': True})
#         else:
#             messages.error(request, 'Selected point was not the last point of the line')
#             return JsonResponse({'success': False, 'error': 'Selected point was not the last point of the line'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})

# @csrf_exempt
# def extend(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])  # Retrieve the markers array from the data
#         up_index = data.get('up_index')
#         up_path_id = data.get('up_path_id')
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
#         print(markers_data)
#         print(pipe_diameter)
#         print(pipe_material)
        
#         print("up_index:", up_index, "up_path_id:", up_path_id)

#         # Fetch the latest path_id from the database
#         latest_path_id = up_path_id
#         new_path_id = up_path_id
        
#         start = int(up_index)
        
#         last_marker = marker.objects.filter(path_id=latest_path_id).last()
        
#         if up_index == last_marker.point_id:
#             # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
#             for index, marker_info in enumerate(markers_data, start=start+1):
#                 lat = marker_info.get('latitude')
#                 lon = marker_info.get('longitude')
#                 marker_type = marker_info.get('type')

#                 # Check if a marker with the same latitude, longitude, and type already exists
#                 existing_marker = marker.objects.filter(
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type
#                 ).first()

#                 if existing_marker:
#                     # Skip saving duplicate data
#                     continue

#                 # Calculate index for additional fields data
#                 additional_index = index - start

#                 # Check if any of the additional fields are None
#                 if (
#                     additional_index >= len(pipe_material) or
#                     additional_index >= len(pipe_diameter) or
#                     additional_index >= len(valve_type) or
#                     additional_index >= len(valve_diameter) or
#                     additional_index >= len(valve_key_size)
#                 ):
#                     continue

#                 new_marker = marker.objects.create(
#                     path_id=new_path_id,
#                     point_id=index,  # Use the index variable for sequential point_id
#                     latitude=lat,
#                     longitude=lon,
#                     type=marker_type,
#                     user_id=request.user.id,
#                     pip_material=pipe_material[additional_index],
#                     pip_diameter=pipe_diameter[additional_index],
#                     valve_type=valve_type[additional_index],
#                     valve_key_size=valve_key_size[additional_index],
#                     valve_diameter=valve_diameter[additional_index],
#                 )
#                 new_marker.save()

#             return JsonResponse({'success': True})
#         else:
#             messages.error(request, 'Selected point was not the last point of the line')
#             return JsonResponse({'success': False, 'error': 'Selected point was not the last point of the line'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def extend(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        markers_data = data.get('markers', [])  # Retrieve the markers array from the data
        up_index = data.get('up_index')
        up_path_id = data.get('up_path_id')
        
        pipe_material = data.get('pipe_material', [])
        pipe_diameter = data.get('pipe_diameter', [])
        valve_type = data.get('valve_type', [])
        valve_diameter = data.get('valve_diameter', [])
        valve_key_size = data.get('valve_key_size', [])
        
        print(markers_data)
        print(pipe_diameter)
        print(pipe_material)
        
        print("up_index:", up_index, "up_path_id:", up_path_id)

        # Fetch the latest path_id from the database
        latest_path_id = up_path_id
        new_path_id = up_path_id
        
        start = int(up_index)
        
        last_marker = marker.objects.filter(path_id=latest_path_id).last()
        
        if up_index == last_marker.point_id:
            # Save latitude, longitude, and type to database with incremented path_id and sequential point_id
            for index, marker_info in enumerate(markers_data, start=start):
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

                # Calculate index for additional fields data
                additional_index = index - start

                # Check if any of the additional fields are None
                if (
                    additional_index >= len(pipe_material) or
                    additional_index >= len(pipe_diameter) or
                    additional_index >= len(valve_type) or
                    additional_index >= len(valve_diameter) or
                    additional_index >= len(valve_key_size)
                ):
                    continue

                new_marker = marker.objects.create(
                    path_id=new_path_id,
                    point_id=index,  # Use the index variable for sequential point_id
                    latitude=lat,
                    longitude=lon,
                    type=marker_type,
                    user_id=request.user.id,
                    pip_material=pipe_material[additional_index],
                    pip_diameter=pipe_diameter[additional_index],
                    valve_type=valve_type[additional_index],
                    valve_key_size=valve_key_size[additional_index],
                    valve_diameter=valve_diameter[additional_index],
                )
                new_marker.save()

            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Selected point was not the last point of the line')
            return JsonResponse({'success': False, 'error': 'Selected point was not the last point of the line'})
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
    
    from app1.models import  marker,tanks,jw,wtp,booster
    
    markers = marker.objects.all()
    
    markers_by_path = get_markers_by_path_id()

    # Serialize marker data
    serialized_markers = []
    
    #tanks
    tanks = tanks.objects.all()
    all_tanks = []
    
    #jws
    jw = jw.objects.all()
    all_jw = []
    #wtp
    wtp=wtp.objects.all()
    all_wtp=[];
    #boster
    booster = booster.objects.all()
    all_booster=[];
    
    
    for marker in tanks:
        all_tanks.append({
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            
            # Add other fields if needed
           
        })
        
    for marker in jw:
        all_jw.append({
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            
            # Add other fields if needed
           
        })
        
    for marker in wtp:
        all_wtp.append({
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            
            # Add other fields if needed
           
        })
        
    
    for marker in booster:
        all_booster.append({
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            
            # Add other fields if needed
           
        })
      
    
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
    return JsonResponse({'success': True, 'markers': serialized_markers, 'markers_by_path':markers_by_path, 'all_tanks':all_tanks,'all_jw':all_jw,'all_wtp':all_wtp,'all_booster':all_booster})
        
        
        
        


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
                marker_obj.user = request.user
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



# to delete marker


def delete_marker(request,path_id,point_id):
    
    from app1.models import marker
    
    obj = marker.objects.filter(path_id=path_id,point_id=point_id)
    
    
    obj.delete()
    
    messages.error(request, 'marker deleted')
    
    return redirect(request.META.get('HTTP_REFERER'))




    if request.method == 'POST':
        data = json.loads(request.body)
        marker_data = data.get('marker')
        line_data = data.get('line')

        # Save the marker
        marker = marker.objects.create(
            latitude=marker_data['latitude'],
            longitude=marker_data['longitude'],
            type=marker_data['type'],
            path_id=marker_data['path_id'],
            point_id=marker_data['point_id'],
        )
        marker.save()

        # Save the line
        line = Line.objects.create(
            path_id=line_data['path_id'],
            point_ids=json.dumps(line_data['point_ids']),
        )
        line.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    
 
@csrf_exempt
# def save_branch(request):
#     if request.method == 'POST':
#         # Read the JSON data from the request body
#         data = json.loads(request.body)
#         markers_data = data.get('markers', [])
        
#         pipe_material = data.get('pipe_material', [])
#         pipe_diameter = data.get('pipe_diameter', [])
#         valve_type = data.get('valve_type', [])
#         valve_diameter = data.get('valve_diameter', [])
#         valve_key_size = data.get('valve_key_size', [])
        
        
#         # Find the latest path_id
#         latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
#         new_path_id = latest_path_id + 1 if latest_path_id is not None else 1

#         # Get up_index and up_path_id
#         up_index = data.get('up_index')
#         up_path_id = data.get('up_path_id')
#         print('up_index', up_index, 'up_path', up_path_id)
        
#         # Find the branch_point
#         branch_point = marker.objects.filter(path_id=up_path_id, point_id=up_index).first()
#         if branch_point is None:
#             return JsonResponse({'success': False, 'error': 'Branch point not found'})

#         # Extract latitude and longitude of the branch point
#         first_point_lat = branch_point.latitude
#         first_point_long = branch_point.longitude

#         print("First point:", first_point_lat, first_point_long)

#         # Insert the first marker with branch point's coordinates and type 'branch'
#         new_marker = marker.objects.create(
#             path_id=new_path_id,
#             point_id=1,  # Assuming this is the first marker in the new path
#             latitude=first_point_lat,
#             longitude=first_point_long,
#             type='branch',  # Assuming 'branch' is the type for the first marker
            
#             pip_material=pipe_material[index - 1] if index <= len(pipe_material) else None,
#             pip_diameter=pipe_diameter[index - 1] if index <= len(pipe_diameter) else None,
                    
#             valve_type=valve_type[index - 1] if index <= len(valve_type) else None,
#             valve_key_size=valve_key_size[index - 1] if index <= len(valve_key_size) else None,
#             valve_diameter=valve_diameter[index - 1] if index <= len(valve_diameter) else None,
#         )
#         new_marker.save()

#         # Iterate through the remaining markers data and save each marker to the database
#         for index, marker_info in enumerate(markers_data, start=2):  # Start from 2 as the first marker is already inserted
#             lat = marker_info.get('latitude')
#             lon = marker_info.get('longitude')
#             marker_type = marker_info.get('type')
            
#             pipe_material = data.get('pipe_material', [])
#             pipe_diameter = data.get('pipe_diameter', [])
#             valve_type = data.get('valve_type', [])
#             valve_diameter = data.get('valve_diameter', [])
#             valve_key_size = data.get('valve_key_size', [])
            
            
            
#             # Check if a marker with the same latitude, longitude, and type already exists
#             existing_marker = marker.objects.filter(
#                 latitude=lat,
#                 longitude=lon,
#                 type=marker_type
#             ).first()

#             if existing_marker:
#                 # Skip saving duplicate data
#                 continue

#             # Save the marker to the database
#             new_marker = marker.objects.create(
#                 path_id=new_path_id,
#                 point_id=index,
#                 latitude=lat,
#                 longitude=lon,
#                 type=marker_type,
                
#             )
#             new_marker.save()
 
#         # Return a JSON response indicating success
#         return JsonResponse({'success': True, 'message': 'Branch markers saved successfully'})
#     else:
#         # If the request method is not POST, return an error response
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    
    
@csrf_exempt
def save_branch(request):
    if request.method == 'POST':
        # Read the JSON data from the request body
        data = json.loads(request.body)
        markers_data = data.get('markers', [])
        
        pipe_material = data.get('pipe_material', [])
        pipe_diameter = data.get('pipe_diameter', [])
        valve_type = data.get('valve_type', [])
        valve_diameter = data.get('valve_diameter', [])
        valve_key_size = data.get('valve_key_size', [])
        
        # Find the latest path_id
        latest_path_id = marker.objects.aggregate(Max('path_id'))['path_id__max']
        new_path_id = latest_path_id + 1 if latest_path_id is not None else 1

        # Get up_index and up_path_id
        up_index = data.get('up_index')
        up_path_id = data.get('up_path_id')
        print('up_index', up_index, 'up_path', up_path_id)
        
        # Find the branch_point
        branch_point = marker.objects.filter(path_id=up_path_id, point_id=up_index).first()
        if branch_point is None:
            return JsonResponse({'success': False, 'error': 'Branch point not found'})

        # Extract latitude and longitude of the branch point
        first_point_lat = branch_point.latitude
        first_point_long = branch_point.longitude

        print("First point:", first_point_lat, first_point_long)

        # Insert the first marker with branch point's coordinates and type 'branch'
        new_marker = marker.objects.create(
            path_id=new_path_id,
            point_id=1,  # Assuming this is the first marker in the new path
            latitude=first_point_lat,
            longitude=first_point_long,
            type='branch',  # Assuming 'branch' is the type for the first marker
        )
        new_marker.save()

        # Iterate through the remaining markers data and save each marker to the database
        for index, marker_info in enumerate(markers_data, start=2):  # Start from 2 as the first marker is already inserted
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

            # Save the marker to the database
            new_marker = marker.objects.create(
                path_id=new_path_id,
                point_id=index,
                latitude=lat,
                longitude=lon,
                type=marker_type,
                
                pip_material=pipe_material[index - 2] if index - 2 < len(pipe_material) else None,
                pip_diameter=pipe_diameter[index - 2] if index - 2 < len(pipe_diameter) else None,
                valve_type=valve_type[index - 2] if index - 2 < len(valve_type) else None,
                valve_key_size=valve_key_size[index - 2] if index - 2 < len(valve_key_size) else None,
                valve_diameter=valve_diameter[index - 2] if index - 2 < len(valve_diameter) else None,
            )
            new_marker.save()
 
        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'message': 'Branch markers saved successfully'})
    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
# alerts
