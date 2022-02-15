#--------------------------------------#
# yuvObserver_gui.exe v0.1.1.0         #
# Copyright S.Toguchi CIT YYLab 2021   #
#--------------------------------------#
import tkinter as Tk
import tkinter.filedialog as Tkf
import tkinter.messagebox as Tkm
import tkinter.simpledialog as Tks
import numpy as np
import cv2
from PIL import Image, ImageTk
import os
import re
import sys
import webbrowser as web
#--------------------------------------#
# MessageBox Definition                #
#--------------------------------------#
def msg_info_develop():
  # Developer Message
  Tkm.showinfo("Information from Developer", "This feature is under development.\nPlease wait for future updates.")
  
def msg_err_notread():
  # Error Message
  Tkm.showerror('Error','The image has not been loaded.\nPlease load the YUV image from the YUV-File menu.')
  
def msg_err_wrongyuv():
  # Error Message
  Tkm.showerror('Error','The height, width, and color of the image are incorrectly specified.')
  
#--------------------------------------#
# Image Viewer Application Class       #
#--------------------------------------#
class App(Tk.Frame):
  def __init__(self,master=None):
    super().__init__(master)
    # Main Window
    self.master.title('yuvObserver '+version_str) # Global variable
    w, h = 640, 512
    self.master.minsize(w,h)
    sw = self.master.winfo_screenwidth()
    sh = self.master.winfo_screenheight()
    x = (sw//2)-(w//2)
    y = (sh//2)-(h//2)
    self.master.geometry('%dx%d+%d+%d'%(w,h,x,y))
    self.master.rowconfigure(0, weight=1)
    self.master.columnconfigure(0, weight=1)
    # Menubar - declaration
    menubar = Tk.Menu(self)
    # File Menue
    filemenu = Tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label='Open YUV File', command=self.import_yuv)
    filemenu.add_command(label='Save as PNG', command=self.export_png)
    filemenu.add_command(label='Save as MP4', command=lambda:msg_info_develop())
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=self.quit)
    # YUV-Layer Menue
    viewmenu = Tk.Menu(menubar, tearoff=1)
    self.layer_var = 0
    self.view_value = Tk.IntVar(value = self.layer_var)
    target_list = ['Original','YUV Layer','Y Layer','U Layer',
                  'V Layer','RGB Layer','R Layer','G Layer','B Layer']
    for i,lavel_t in enumerate(target_list):
      if i == 1 or i == 5:
        viewmenu.add_separator()
      viewmenu.add_radiobutton(label=lavel_t,variable=self.view_value,value=i,command=lambda arg=i: self.show_Layer(arg))
    # Movie Menue
    moviemenu = Tk.Menu(menubar, tearoff=1)
    self.movie_value = Tk.IntVar(value = 0)
    self.movie_value_ = Tk.IntVar(value = 0)
    movieradio_list = ['Play','Pause','Stop','Play - Repeat']
    movieradio_list1 = ['1 fps','15 fps ','30 fps','60 fps', '120 fps', '240 fps']
    for i,lavel_t in enumerate(movieradio_list):
      moviemenu.add_radiobutton(label=lavel_t,variable=self.movie_value,value=i, command=lambda:msg_info_develop())
    moviemenu.add_separator()
    moviemenu.add_command(label='Advance 1 frame', command=lambda:msg_info_develop())
    moviemenu.add_command(label='Return 1 frame', command=lambda:msg_info_develop())
    moviemenu.add_command(label='Specify frame number', command=lambda:msg_info_develop())
    moviemenu.add_separator()
    for i,lavel_t in enumerate(movieradio_list1):
      moviemenu.add_radiobutton(label=lavel_t,variable=self.movie_value_,value=i, command=lambda:msg_info_develop())
    # Canvas Menue
    canvasmenu = Tk.Menu(menubar, tearoff=1)
    canvasmenu.add_command(label='Set Width x Height _ Color', command=lambda:self.setWxHxC())
    canvasmenu.add_separator()
    self.canvas_value = Tk.IntVar(value = 0)
    canvasradio_list = ['1x - original','2x in','4x in','8x in','16x in','32x in','64x in',
                        '2x out','4x out','8x out','16x out','32x out','64x out']
    for i,lavel_t in enumerate(canvasradio_list):
      if i == 1 or i == 7:
        canvasmenu.add_separator()
      canvasmenu.add_radiobutton(label=lavel_t,variable=self.canvas_value,value=i, command=lambda:msg_info_develop())
    # Help Menue
    helpmenu = Tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label='Version and Copyright', command=self.show_version)
    helpmenu.add_command(label='Update - Open Github Page', command=self.get_update)
    helpmenu.add_command(label='Help - Open Github Page', command=self.get_help)
    # Menuebar - add
    menubar.add_cascade(label='YUV-File', menu=filemenu)
    menubar.add_cascade(label='YUV-Layer', menu=viewmenu)
    menubar.add_cascade(label='YUV-Movie', menu=moviemenu)
    menubar.add_cascade(label='Canvas', menu=canvasmenu)
    menubar.add_cascade(label='Help', menu=helpmenu)
    self.master.config(menu=menubar)
    # Frame and Canvas
    frame1 = Tk.Frame(self.master)
    frame1.rowconfigure(0, weight=1)
    frame1.columnconfigure(0,weight=1)
    self.canvas = Tk.Canvas(self.master, width=500, height=500)
    self.canvas.grid(row=0, column=0)
    # Set Window Icon (base-64)
    ico = '''
          R0lGODlhMgAyAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr
          /wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCq
          mQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMA
          MzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV
          /zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPV
          mTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYr
          M2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA
          /2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/
          mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlV
          M5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq
          /5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswA
          mcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyA
          M8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV
          /8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8r
          mf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+q
          M/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP//
          /wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAAAyADIAAAj/APcJHEiwoMGDCBMqXMiw
          ocOHECM6hKaBiJIidOrU+QTKlDJo0SRKhJaByBKNGkGVAqXMIzSREJVlqKMQ1EuY
          DqNNoCkwWSdPyQaCAoWTHj139Nq1czdsGLFhmQQq2ynQUyc6neYoE/jJlMij7cB9
          yyZNGio/VKioACB1wpt9yn72HLjx61F37c6ZO8fLFi9JKlRIbUATGR19AqE9E1iH
          qESjA/XVK1iFLVwGb30G3dcJE+I3PCPWoyeQbFlp5gTCELwPFIOo0Dx5UvYM0xyB
          SkJHi7bsVKjfd4IfaXKEiUDI+8BJA9eurEAqlpUZeLuv1KU5Vj0hJkJk4LJov0PZ
          /7nTxMgRDh04GDlOOrk00mRJr2Atnfo+aMmg6du6T4PuZQlFY8F6+yCnXDZkTSOQ
          FtEZgIZCIHS3D3g3BWfhQBYAIdBoAn0jjYfSILZPYAIRY8ABYvigoorccZeBBgOF
          EtI+6NV4x4QVFMGeQMrhtZxAlUkFAAAGFMkAAw0kOcEEJQkEXigCoSdQBx0I9MAP
          O+5DVjv7lEXaagNFgxiAk4k44ZkC2QHlPlTWeIqVWO7DYUJBShRNHG/ucx55VArk
          QJzIFViPZISSaCeeU1ZJo6IO5DBQXmKRhcpZaa0FExNr1kglgQ7gwJ5S4ET6yiuF
          bLFFDCItc8SaFt6xZjQHeP+KU0PRHGGHQrF+Nc+u88jjqzzrxBPsOk5y0MQdcCQL
          xxtvpJHGDwHc8JU+9OjD66++qhOPQMu0yYEFFTzwAAIOHHBAAAdItJ+ZB8Ujz0Cn
          LLOMMtEow5Iy+OYrUT3KTJaQPNvO2hAxIgIskK+I+SowQ/oQw5/C+0CMzLsiKTMv
          MZlkPEkaaIjh8YbEtAcxxL2KFA09ymCcySQdh3FDDAZYRo8mxBxMscH77JqYHXaY
          0lFHH9V7H0H8yQkNv/wqE4Nly/jy8M0U6zxhCEssYUcddvxskzIoD1T0QUsfR0nN
          EcszTz4Q0zOPVFZHA5LbQyfWHlxwSRLVPmlMIlDY+yz/0wh/aP+aj1SDT7iEYwgN
          055kAnEskCQP7nODZfo4QrZA7O5DrZOHC8TEEp6DDld7Qu8jxiQpo3E3335bTszr
          DhOzDMrIQdOzQBqEINAGuu/TzjAbDlQPGmiw7C/rh4zRiCONUKKJL7C7w7WTdWwV
          De8ChbCBQEthXvTKaFzOd9/1nBwNh5lTn2cIukOzQRQCDcMltwQRT9DkIkHDkkCm
          bGAHEyFwjFK8JrziEWR8EImGTQbCvg2Ibh+8mN8y2IWvA1pGIgvkH+9uso9zzA8u
          9YBGvhyWCYwh8CH64+A+bjeQvXgtZSubhMdetrQLRkSEmBuUoIzCi9RsCBqzG2EJ
          LjN2t4jMCxooI8Y8fteOvZgDHOdYGENeUi3aIYUpSvmgFLfIxS568YtgDCNMAgIA
          Ow==
          '''
    self.master.iconphoto(True, Tk.PhotoImage(data=ico))
    # Make Status Bar
    self.statusbar = Tk.Frame(self.master, relief = Tk.GROOVE)
    self.rights_info = Tk.Label(self.statusbar, relief = Tk.SUNKEN, text="Produced by Yashima-Lab CIT")
    self.image_info = Tk.Label(self.statusbar, relief = Tk.SUNKEN, text="Hello Observer! Please open the YUV-file! :)")
    self.rights_info.grid(row=0, column=0,sticky=Tk.W,ipadx=10,)
    self.image_info.grid(row=0, column=1,sticky=Tk.E,ipadx=10)
    self.statusbar.grid(row=2, column=0,sticky=Tk.E+Tk.W)
    self.statusbar.rowconfigure(2, weight=1)
    self.statusbar.columnconfigure(0,weight=1)
  
  def import_yuv(self):
    file_path = Tkf.askopenfilename(filetypes=[('YUV files','*.yuv')],initialdir=os.getcwd())
    if len(file_path) != 0:
      self.file_read_path = file_path
      data = read_img(file_path)
      self.show_img(*data)
    else:
      return
  
  def export_png(self):
    try:
      if keep_imgfile is None: # Global variable
        print('ok')
    except:
      msg_err_notread()
      return
    file_path = Tkf.asksaveasfilename(title = "Save as PNG",
    filetypes = [("PNG", ".png")],
    initialdir = image_path, # Global variable
    defaultextension = "png")
    if len(file_path) != 0:
      image_rgb = cv2.cvtColor(keep_imgfile, cv2.COLOR_BGR2RGB)
      image_pil = Image.fromarray(image_rgb)
      image_pil.save(file_path)
    else:
      return
    
  def arg_imgread(self,arg):
    file_path = arg
    if len(file_path) != 0:
      self.file_read_path = file_path
      data = read_img(file_path)
      if data is None:
        msg_err_wrongyuv()
        self.master.destroy()
        sys.exit()
      else:
        self.show_img(*data)
    else:
      self.master.destroy()
      sys.exit()
      
  def setWxHxC(self):
    try:
      path = self.file_read_path
    except:
      msg_err_notread()
      return
    if len(path) != 0:
      data = read_img_whc(path)
      if data is None:
        msg_err_wrongyuv()
        return
      else:
        self.show_img(*data)
    else:
      return
  
  def show_img(self,img,w,h,path,c):
    self.master.title('yuvObserver '+version_str+' - '+os.path.basename(path))
    self.view_value.set(0)
    self.width_status = w
    self.height_status = h
    self.color_status = c
    if c != 400:
      try:
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      except:
        msg_err_wrongyuv()
        return
      image_pil = Image.fromarray(image_rgb)
    else:
      image_pil = img
    self.image_info['text'] = 'View mode: %dx%dp,YUV%d'%(w,h,c)
    self.image_tk = ImageTk.PhotoImage(image_pil)
    self.canvas.delete('img')
    self.canvas.create_image(0, 0, image=self.image_tk, anchor=Tk.NW, tag='img')
    self.canvas.grid(sticky=Tk.W+Tk.E+Tk.N+Tk.S)
    self.canvas.configure(scrollregion=(0,0,w,h))
    xbar = Tk.Scrollbar(self.master,orient=Tk.HORIZONTAL,)
    ybar = Tk.Scrollbar(self.master,orient=Tk.VERTICAL,)
    xbar.grid(row=1, column=0,sticky=Tk.W+Tk.E)
    ybar.grid(row=0, column=1,sticky=Tk.N+Tk.S)
    xbar.config(command=self.canvas.xview)
    ybar.config(command=self.canvas.yview)
    self.canvas.config(xscrollcommand=xbar.set)
    self.canvas.config(yscrollcommand=ybar.set)
    self.master.update()
  
  def show_Layer(self,arg):
    try:
      data = YUVappendArray(arg)
      if data is None: # Under Develop
        self.view_value.set(self.layer_var)
        return
    except:
      msg_err_notread()
      self.view_value.set(self.layer_var)
      return
    self.layer_var = arg
    w,h = data.size
    self.image_info['text'] = 'View mode: %dx%dp,YUV%d'%(self.width_status,self.height_status,self.color_status)
    self.image_tk = ImageTk.PhotoImage(data)
    self.canvas.delete('img')
    self.canvas.create_image(0, 0, image=self.image_tk, anchor=Tk.NW, tag='img')
    self.canvas.grid(sticky=Tk.W+Tk.E+Tk.N+Tk.S)
    self.canvas.configure(scrollregion=(0,0,w,h))
    xbar = Tk.Scrollbar(self.master,orient=Tk.HORIZONTAL,)
    ybar = Tk.Scrollbar(self.master,orient=Tk.VERTICAL,)
    xbar.grid(row=1, column=0,sticky=Tk.W+Tk.E)
    ybar.grid(row=0, column=1,sticky=Tk.N+Tk.S)
    xbar.config(command=self.canvas.xview)
    ybar.config(command=self.canvas.yview)
    self.canvas.config(xscrollcommand=xbar.set)
    self.canvas.config(yscrollcommand=ybar.set)
    self.master.update()
  
  def show_version(self):
    sub_win = Tk.Toplevel(master=self.master)
    sub_win.title('yuvObserver '+version_str+' - Version and Copyright') # Global variable
    w, h = 350, 110
    sw = sub_win.winfo_screenwidth()
    sh = sub_win.winfo_screenheight()
    x = (sw//2)-(w//2)
    y = (sh//2)-(h//2)
    sub_win.geometry('%dx%d+%d+%d'%(w,h,x,y))
    sub_win.resizable(width=False, height=False)
    label = Tk.Label(sub_win,
    text='yuvObserverGUI.exe '+version_str+'\nCopyright (c) S.Toguchi CIT YYLab B4 2021\nAll rights reserved.', # Global variable
    font=('System', 10))
    label.place(x=25, y=10)
    button = Tk.Button(sub_win, text='OK', command=sub_win.destroy)
    button.place(x=160, y=70)
    button.focus_set()
    sub_win.transient(self.master)
    sub_win.grab_set()
  
  def get_update(self):
    web.open_new_tab('https://github.com/nkgw-marronnier/yuvObserver_GUI_test/releases')

  def get_help(self):
    web.open_new_tab('https://github.com/nkgw-marronnier/yuvObserver_GUI_test')

  def quit(self):
    self.master.destroy()
    sys.exit()

#--------------------------------------#
# Definition Image Processing Code     #
#--------------------------------------#
def read_img(path):
  global keep_imgfile, save_imgfile, image_path # Keep save imgfile
  image_path = path
  path_str = str(image_path)
  size_p = str(re.findall('\((.*)\)', path_str))
  size_s = size_p.split('x')
  w = size_s[0].strip("[']")
  h = ''
  width = height = color = 0
  if len(size_s) == 2:
    h = size_s[1].strip("[']")
  else:
    wxh = None
    while wxh == None:
      wxh = Tks.askstring('yuvObserer - Open YUV file','Please enter the YUV width, height and color.\nex) 1024x640_444\nex) 1024x640,YUV444')
    try:
      size_s = wxh.split('x')
      w = size_s[0].strip("[']")
      h = size_s[1].strip("[']")
    except:
      msg_err_wrongyuv()
      return
  if ',YUV' in h:
    size_c = h.split(',YUV')
    width = int(w)
    height = int(size_c[0])
    color = int(size_c[1])
  elif '_' in h:
    size_c = h.split('_')
    width = int(w)
    height = int(size_c[0])
    color = int(size_c[1])
  else:
    int_color = None
    while int_color == None:
      int_color = Tks.askinteger('yuvObserer - Open YUV file','Please enter the YUV color format.\nex) 444\nex) 420')
    width = int(w)
    height = int(h)
    color = int_color
  data = np.fromfile(image_path, dtype=np.uint8)
  data = np.ravel(data)
  if color == 444:
    if len(data) == width*height*3:
      rgb = YUV444toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width*3)
      rgb = YUV444toRGB(data_,width,height)
  elif color == 422:
    if len(data) == width*height*2:
      rgb = YUV422toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width*2)
      rgb = YUV422toRGB(data_,width,height)
  elif color == 420:
    if len(data) == width*height*3//2:
      rgb = YUV420toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width*3//2)
      rgb = YUV420toRGB(data_,width,height)
  elif color == 400:
    if len(data) == width*height:
      rgb = YUV400toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width)
      rgb = YUV400toRGB(data_,width,height)
  else:
    msg_err_wrongyuv()
    return
  keep_imgfile = rgb
  return [rgb,width,height,path_str,color]

def read_img_whc(path):
  global keep_imgfile, save_imgfile, image_path # Keep save imgfile
  image_path = path
  path_str = str(image_path)
  width = height = color = 0
  wxh = None
  while wxh == None:
    wxh = Tks.askstring('yuvObserer - Open YUV file','Please enter the YUV width, height and color.\nex) 1024x640_444\nex) 1024x640,YUV444')
  try:
    size_s = wxh.split('x')
    w = size_s[0].strip("[']")
    h = size_s[1].strip("[']")
  except:
    return
  print(w,h)
  if ',YUV' in h:
    size_c = h.split(',YUV')
    width = int(w)
    height = int(size_c[0])
    color = int(size_c[1])
  elif '_' in h:
    size_c = h.split('_')
    width = int(w)
    height = int(size_c[0])
    color = int(size_c[1])
  else:
    int_color = None
    while int_color == None:
      int_color = Tks.askinteger('yuvObserer - Open YUV file','Please enter the YUV color format.\nex) 444\nex) 420')
    width = int(w)
    height = int(h)
    color = int_color
  data = np.fromfile(image_path, dtype=np.uint8)
  data = np.ravel(data)
  if color == 444:
    if len(data) == width*height*3:
      rgb = YUV444toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width*3)
      rgb = YUV444toRGB(data_,width,height)
  elif color == 422:
    if len(data) == width*height*2:
      rgb = YUV422toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width*2)
      rgb = YUV422toRGB(data_,width,height)
  elif color == 420:
    if len(data) == width*height*3//2:
      rgb = YUV420toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width*3//2)
      rgb = YUV420toRGB(data_,width,height)
  elif color == 400:
    if len(data) == width*height:
      rgb = YUV400toRGB(data,width,height)
    else:
      data_ = np.resize(data,height*width)
      rgb = YUV400toRGB(data_,width,height)
  else:
    return
  keep_imgfile = rgb
  return [rgb,width,height,path_str,color]

def YUV444toRGB(data,width,height):
  global yuv_l, y_l, u_l, v_l
  wxh = width*height
  y = (np.array(data[:wxh])).reshape(height,width)
  u = (np.array(data[wxh:wxh*2])).reshape(height,width)
  v = (np.array(data[wxh*2:])).reshape(height,width)
  yuv = np.stack([y,u,v],axis=2)
  rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
  # YUV444 Layer
  yuv_l = np.c_["1",y,u,v]
  y_l, u_l, v_l = y, u, v
  return rgb

def YUV422toRGB(data,width,height):
  global yuv_l, y_l, u_l, v_l
  wxh = width*height
  wxh_ = (width//2)*height
  y = (np.array(data[:wxh])).reshape(height,width)
  u = (np.array(data[wxh:wxh+wxh_])).reshape(height,width//2)
  v = (np.array(data[wxh+wxh_:])).reshape(height,width//2)
  y0 = np.expand_dims(y[:,::2], axis=2)
  u = np.expand_dims(u, axis=2)
  y1 = np.expand_dims(y[:,1::2], axis=2)
  v = np.expand_dims(v, axis=2)
  img_yuv = np.concatenate((y0, u, y1, v), axis=2)
  img_yuv_cvt = img_yuv.reshape(img_yuv.shape[0], img_yuv.shape[1] * 2, int(img_yuv.shape[2] / 2))
  rgb = cv2.cvtColor(img_yuv_cvt, cv2.COLOR_YUV2BGR_YUYV)
  # YUV422 Layer 
  zeros_arr = np.zeros((height,width//2),dtype=np.uint8)
  u_l = (np.c_[u.reshape(height,width//2),zeros_arr]).reshape(height,width)
  v_l = (np.c_[v.reshape(height,width//2),zeros_arr]).reshape(height,width)
  y_l = y
  yuv_l = np.c_[y_l,u_l,v_l]
  return rgb

def YUV420toRGB(data,width,height):
  global yuv_l, y_l, u_l, v_l
  wxh = width*height
  wxh_ = (width*height)//4
  y = (np.array(data[:wxh])).reshape(height,width)
  u = (np.array(data[wxh:wxh+wxh_])).reshape(height//2,width//2)
  v = (np.array(data[wxh+wxh_:])).reshape(height//2,width//2)
  y0 = np.expand_dims(y, axis=2)
  u = np.expand_dims(u, axis=2)
  v = np.expand_dims(v, axis=2)
  img_yuv = np.concatenate([y0.flat, u.flat, v.flat])
  img_yuv_cvt = img_yuv.reshape(height*3//2,width)
  rgb = cv2.cvtColor(img_yuv_cvt, cv2.COLOR_YUV2BGR_I420)
  # YUV420 Layer 
  zeros_arr = np.zeros((height//2,width//2),dtype=np.uint8)
  zeros_arr1 = np.zeros((height//2,width),dtype=np.uint8)
  u_ = (np.c_[u.reshape(height//2,width//2),zeros_arr]).reshape(height//2,width)
  v_ = (np.c_[v.reshape(height//2,width//2),zeros_arr]).reshape(height//2,width)
  u_l = (np.r_[u_.reshape(height//2,width),zeros_arr1]).reshape(height,width)
  v_l = (np.r_[v_.reshape(height//2,width),zeros_arr1]).reshape(height,width)
  y_l = y
  yuv_l = np.c_[y_l,u_l,v_l]
  return rgb

def YUV400toRGB(data,width,height):
  global yuv_l, y_l, u_l, v_l, keep_imgfile
  wxh = width*height
  y = (np.array(data[:wxh])).reshape(height,width)
  rgb = Image.fromarray(y,'L')
  # YUV 400 Layer
  yuv_l = y_l = keep_imgfile = y
  u_l = v_l = None
  return rgb

def YUVappendArray(arg):
  if arg == 0:
    img = IMG2ORIGIN()
    return img
  elif arg == 1:
    img = IMG2YUV()
    return img
  elif arg == 2:
    img = IMG2Y()
    return img
  elif arg == 3:
    img = IMG2U()
    return img
  elif arg == 4:
    img = IMG2V()
    return img
  elif arg == 5:
    img = IMG2RGB()
    return img
  elif arg == 6:
    img = IMG2R()
    return img
  elif arg == 7: 
    img = IMG2G()
    return img
  elif arg == 8:
    img = IMG2B()
    return img

def IMG2ORIGIN():
  data = keep_imgfile # Global variable
  try:
    rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    pil_img_RGB = Image.fromarray(rgb)
  except: # YUV 400
    pil_img_RGB = data
  return pil_img_RGB

def IMG2YUV():
  pil_img_RGB = Image.fromarray(yuv_l)
  return pil_img_RGB

def IMG2Y():
  pil_img_RGB = Image.fromarray(y_l)
  return pil_img_RGB

def IMG2U():
  pil_img_RGB = Image.fromarray(u_l)
  return pil_img_RGB

def IMG2V():
  pil_img_RGB = Image.fromarray(v_l)
  return pil_img_RGB

def IMG2RGB():
  data = keep_imgfile # Global variable
  im = np.array(data)
  im_R = im.copy()
  im_R[:, :, (1, 2)] = 0
  im_G = im.copy()
  im_G[:, :, (0, 2)] = 0
  im_B = im.copy()
  im_B[:, :, (0, 1)] = 0
  im_RGB = np.c_['1', im_R, im_G, im_B]
  pil_img_RGB = Image.fromarray(im_RGB)
  return pil_img_RGB

def IMG2R():
  data = keep_imgfile # Global variable
  im = np.array(data)
  im_R = im.copy()
  im_R[:, :, (1, 2)] = 0
  pil_img_RGB = Image.fromarray(im_R)
  return pil_img_RGB

def IMG2G():
  data = keep_imgfile # Global variable
  im = np.array(data)
  im_G = im.copy()
  im_G[:, :, (0, 2)] = 0
  pil_img_RGB = Image.fromarray(im_G)
  return pil_img_RGB

def IMG2B():
  data = keep_imgfile # Global variable
  im = np.array(data)
  im_B = im.copy()
  im_B[:, :, (0, 1)] = 0
  pil_img_RGB = Image.fromarray(im_B)
  return pil_img_RGB

#--------------------------------------#
# Defining Main Function               #
#--------------------------------------#
if __name__ == '__main__':
  global version_str
  version_str = 'v0.1.1.0' # Version String
  app = App()
  app.grid()
  if len(sys.argv) > 1:
    App.arg_imgread(app,sys.argv[1])
  app.mainloop()
