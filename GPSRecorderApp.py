#\input texinfo
#coding: utf-8

# Put your script (and all resources that it needs for running) in this folder.
# The filename of the main script should be "main.py".

import ui, location, dialogs, time, console, math, urllib, requests
stop = True
lastloc = None
curloc = None
debug = False





view = ui.View()
view=ui.View()
view.frame = (0, 0, 320, 430)
view.name = 'GPS RECORDER'
view.enabled = True
view.tint_color = (0.000000,0.478000,1.000000,1.000000)
view.border_color = (0.000000,0.000000,0.000000,1.000000)
view.background_color = (1.000000,1.000000,1.000000,1.000000)
view.flex = 'LR'





# start the GPS in the device.
# want this was a button because running the gps uses a lot of battery life

def button_startgps(sender):
  location.start_updates()


  if location.is_authorized():
      location.start_updates()
      dialogs.hud_alert('GPS Started', 'success', 1)
  else:
      dialogs.alert('App not authorized to use GPS. Enable GPS in system preferences.', 'Plz fix', 'Oh rats... gonna fix that now', hide_cancel_button=True)


def clear(sender):
  console.clear()

# allow user to stop the gps receiver to save battery
def button_stopgps(sender):
  location.stop_updates()
  dialogs.hud_alert('GPS stopped','success', 1)

# print the current location
def button_print_pos(sender):
  global debug, v
  debug = not debug

  if debug:
      v['button_position'].background_color = 'white'
      v['button_position'].title='Turn Debug Off'
  else:
      v['button_position'].background_color = 'white'
      v['button_position'].title='Turn Debug On'

# record the gps signal to a file and warn if the accuracy is poor
def button_record(sender):
  # code here
  global curloc, lastloc
  lastloc=curloc
  curloc = location.get_location()
  name=dialogs.input_alert("Enter Name", "Name:","John Doe", hide_cancel_button=False)
  curloc = location.get_location()
  if curloc['horizontal_accuracy']>5:
      dialogs.hud_alert("Poor GPS accuracy", 'error', 1)
      count=0
      while count<10 and curloc["horizontal_accuracy"]>5:
          curloc=location.get_location()
          count+=1
      dialogs.hud_alert('Location Recorded', 'success', 1)
  else:
      dialogs.hud_alert('Location Recorded', 'success', 1)


  form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeYmR_PSpxeeE1pJEP83Ui_eqz4OA6tqqx35cfPX1VL2mfd0g/formResponse'

  form_postbody = {'entry.598678340':str(curloc['longitude']), 'entry.1352477612':str(curloc['latitude']), 'entry.1482071151':str(curloc['horizontal_accuracy']), 'entry.1391268977':urllib.parse.quote(str(name)), 'draftResponse':[], 'pageHistory':0}

  form_headers = {'Referer':'https://docs.google.com/forms/d/e/1FAIpQLSeYmR_PSpxeeE1pJEP83Ui_eqz4OA6tqqx35cfPX1VL2mfd0g/viewform'}

  try:
      val = requests.post(form_url, data=form_postbody, headers=form_headers)
  except:
      console.hud_alert('Error on upload', 'failure', 1)


# stop the program WORKS
def button_stop(sender):
  global stop
  #alertval = dialogs.alert('Press cancel to stop', '', '', 'Keep Going', hide_cancel_button=True)
  stop=False


def gpsdistance(lat1, lng1, lat2, lng2):
  #return distance as meter if you want km distance, remove "* 1000"
  radius = 6371 * 1000

  dLat = (lat2-lat1) * math.pi / 180
  dLng = (lng2-lng1) * math.pi / 180

  lat1 = lat1 * math.pi / 180
  lat2 = lat2 * math.pi / 180

  val = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLng/2) * math.sin(dLng/2) * math.cos(lat1) * math.cos(lat2)
  ang = 2 * math.atan2(math.sqrt(val), math.sqrt(1-val))
  return radius * ang



record_button = ui.Button()
record_button.frame = (74, 155, 180, 180)
record_button.flex = 'LR'
record_button.corner_radius = 90
record_button.background_color = (0.000000,0.742925,0.000000,1.000000)
record_button.border_color = (1.000000,0.000000,0.000000,1.000000)
record_button.border_width = 5
record_button.title = 'RECORD'
record_button.action = button_record
record_button.font_bold = True
record_button.name = 'record_button'
record_button.font_size = 30

dist_label = ui.Label()
dist_label.frame = (74, 57, 180, 70)
dist_label.font_size = 18
dist_label.corner_radius = 10
dist_label.number_of_lines = 2
dist_label.border_width = 2
dist_label.alignment = ui.ALIGN_CENTER
dist_label.text = 'Feet Since Last Measurement'
dist_label.font_name = '<System>'
dist_label.name = 'distance'
dist_label.flex = 'LR'


startgps_button = ui.Button()
startgps_button.frame = (22, 356, 131, 50)
startgps_button.font_size = 15
startgps_button.corner_radius = 17
startgps_button.background_color = (0.563837,0.768868,0.563837,1.000000)
startgps_button.border_width = 0
startgps_button.title = 'Start GPS'
startgps_button.action = button_startgps
startgps_button.alpha = 1
startgps_button.font_bold = True
startgps_button.name = 'startgps'
startgps_button.flex = 'LR'



stopgps_button = ui.Button()
stopgps_button.frame = (174, 356, 131, 50)
stopgps_button.font_size = 15
stopgps_button.corner_radius = 17
stopgps_button.background_color = (1.000000,0.633333,0.633333,1.000000)
stopgps_button.border_width = 0
stopgps_button.title = 'Stop GPS'
stopgps_button.action = button_stopgps
stopgps_button.alpha = 1
stopgps_button.font_bold = True
stopgps_button.name = 'stopgps'
stopgps_button.flex = 'LR'


stop_button = ui.Button()
stop_button.frame = (174, 424, 114, 50)
stop_button.border_width = 0
stop_button.flex = 'LR'
stop_button.action = button_stop
stop_button.title = 'STOP'
stop_button.corner_radius = 10
stop_button.background_color = (1.000000,0.000000,0.000000,1.000000)
stop_button.name = 'button_stop'
stop_button.font_size = 36

stop_button_2 = ui.Button()
stop_button_2.frame = (39, 424, 114, 50)
stop_button_2.border_width = 0
stop_button_2.action = clear
stop_button_2.title = 'CLEAR'
stop_button_2.corner_radius = 10
stop_button_2.background_color = (1.000000,0.000000,0.000000,1.000000)
stop_button_2.name = 'button_stop'
stop_button_2.font_size = 36



debug_button = ui.Button()
debug_button.frame = (97, 6, 127, 50)
debug_button.border_width = 0
debug_button.action = button_print_pos
debug_button.title = 'Debug Mode'
debug_button.corner_radius = 10
debug_button.background_color = (1.000000,1.000000,1.000000,1.000000)
debug_button.name = 'button_position'
debug_button.font_size = 18






#v = ui.load_view()
#v.present('Full_Screen', hide_title_bar=False,animated=False)

recbutton = v['record_button']
distance = v['distance']

lastloc=location.get_location()

# main loop
# repeatedly get a new location and show
# the user if the gps is accurate enough
# yay the break works
while stop:
  if not stop:
      console.hud_alert('Stopped!')
      break
  curloc = location.get_location()
  accuracy=curloc['horizontal_accuracy']

  if accuracy>5:
      recbutton.background_color='red'
  else:
      recbutton.background_color='green'

  curlong=curloc['longitude']
  curlat=curloc['latitude']
  lastlong=lastloc['longitude']
  lastlat=lastloc['latitude']

  distance.text = 'Distance since last record: ' + str(round(gpsdistance(lastlat,lastlong, curlat, curlong))) + ' meters'

  if debug:
      console.alert(str(curloc), "", "OK", hide_cancel_button=True)

      console.alert(str('Postion: '+str(curloc['latitude'])+' '+str(curloc['longitude'])), "", "OK", hide_cancel_button=True)

      console.alert(str('Distance since last record: ' + str(gpsdistance(lastlat,lastlong, curlat, curlong)) + ' meters'), "", "OK", hide_cancel_button=True)

  time.sleep(5)
