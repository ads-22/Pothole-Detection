import subprocess
# !pip install nbimporter
# from nbimporter import coordinates_sandbox.ipynb
import coordinates_sandbox as cs
# import_notebook('coordinates_sandbox.ipynb')
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import os
import re
import json,sys
import torch,glob
from IPython.display import Image
import google_streetview.api



def solve(src,dest):
    s_lat,s_lng=cs.location(src)
    d_lat,d_lng=cs.location(dest)
    routes,routes_data = cs.getroutes(s_lat,s_lng,d_lat,d_lng)

    URL = "https://overpass-api.de/api/interpreter/" 

    coordinates = []

    prev_count = []

    for i in routes:

      param = cs.make_url_body(i['nodes'])

      # print(param)

      r = requests.post(url = URL, data = param)

      data = r.json()

      data = data['elements']

      curr_coordinates = []

      curr_prev_count = 0

      i_lat = 0
      i_lon = 0

      for j in data:
        i_lat = j['lat']
        i_lon = j['lon']
        s = str(i_lat) + "," + str(i_lon)
        ans = cs.find_in_prev(s)
        if(not ans):
          curr_coordinates.append(s)
        else:
          pthlcnt = int(ans[0][ans[0].find('"count":') + 9 : ans[0].find('}')])
          curr_prev_count  = curr_prev_count + pthlcnt
      coordinates.append(curr_coordinates)
      prev_count.append(curr_prev_count)
    print(len(coordinates[0]))
    
    
    gsv_path = r"/gsv_images/"

    if not os.path.exists(gsv_path):
      os.makedirs(gsv_path)

    gsv_files = list(glob.glob(gsv_path + "*"))

    gsv_files_len = len(gsv_files)

    k = gsv_files_len + 1

    for i in range(len(coordinates)):

      api_list=[]
      image_links = []
      api_results=[]

      n = len(coordinates[i])


      for j in range(n):
        params = {
        'size': '600x600', # max 640x640 pixels
        'location': coordinates[i][j],
        'heading': '45;90;-90', #indicates the compass heading of the camera. Accepted values are from 0 to 360
        'pitch': '-0.76', #(default is 0) specifies the up or down angle of the camera relative to the Street View vehicle.
        'key': 'AIzaSyC9Q1u6PExObkUUWKFDcWlXTf0S34niKTM',
        'return_error_code': 'true'
      }
        api = google_streetview.helpers.api_list(params)
        api_list.append(api)


      for j in range(n):
        api_result = google_streetview.api.results(api_list[j])
        api_results.append(api_result)

      for j in range(n):
        link = api_results[j].links
        image_links.append(link)

      for j in range(n):
        req = requests.get(image_links[j][0])
        if (req.status_code == 200):
          img_data = req.content
          if not os.path.exists('/gsv_images/gsv'+str(k)+'/'):
           os.makedirs('/gsv_images/gsv'+str(k)+'/')
          with open('/gsv_images/gsv'+str(k)+'/google_view_image_GA' + str(j)+ '-co-'+ str(coordinates[i][j]) + '.jpeg', 'wb+') as handler:
              handler.write(img_data)
      k = k + 1
    

    k = gsv_files_len + 1
    
    
  
    
    for i in range(len(coordinates)):
      if os.path.exists('/gsv_images/gsv'+str(k)+'/'):
            command = 'python C:/Users/aditr/Downloads/Major_trial/yolov5/detect.py --weights C:/Users/aditr/Downloads/Major_trial/yolov5/runs/train/exp8/weights/best.pt --img 600 --conf 0.25 --source "/gsv_images/gsv"'+str(k)+'"/" --save-txt'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)  
#         !python C:/Users/aditr/Downloads/Major_trial/yolov5/detect.py --weights C:/Users/aditr/Downloads/Major_trial/yolov5/runs/train/exp8/weights/best.pt --img 600 --conf 0.25 --source {"/gsv_images/gsv"+str(k)+"/"} --save-txt

      k = k + 1
    
    
    basepath = r"yolov5/runs/detect/"

    files = list(glob.glob(basepath + "*"))

    #files.sort(key = os.path.getctime)

    files = files[::-1]

    print(len(files))

    j = 0

    potholes_in_route = []

    for i in range(len(coordinates)):
      print(files[j]) 
      s = cs.get_pothole_count(files[j])
      cs.push_no_pothole(files[j])
      s = s + prev_count[i]
      potholes_in_route.append(s)
      j = j + 1

    potholes_in_route = potholes_in_route[::-1]

    for i in potholes_in_route:
      print(i)


    min = sys.maxsize
    min_index = -1

    for i in range(len(potholes_in_route)):

      if potholes_in_route[i]<min:

        min = potholes_in_route[i]

        min_index = i

    best_route = routes_data['routes'][min_index]['geometry']
    # json_file = cs.get_route(best_route,s_lat,s_lng,d_lat,d_lng,min_index)
    folium_map = cs.get_map(cs.get_route(best_route,s_lat,s_lng,d_lat,d_lng,min_index,routes_data))
    return folium_map
    
# solve('anand vihar delhi','sector 128 noida')