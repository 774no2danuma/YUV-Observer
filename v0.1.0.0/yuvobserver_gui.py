import numpy as np
import os
import re
import sys
import cv2
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import Image, ImageTk

def import_yuv():
    # ファイル選択ダイアログの表示
    file_path = tkinter.filedialog.askopenfilename()

    if len(file_path) != 0:
        # ファイルが選択された場合
        data = file_path
        read_img(data)
    else:
        data = ''

def get_help():
    print('menu2!')

def quit():
  sys.exit()
  
def show_version():
    u""" Tk() と同じような感じで使える """
    sub_win = Toplevel(master = root.master)
    sub_win.title('yuvObserver v0.1.0.0 - Version')
    sub_win.geometry('350x100')
    sub_win.resizable(width=False, height=False)
    label = tkinter.Label(sub_win,
    text='yuvObserverGUI.exe v0.1.0.0\nCopyright (c) S Toguchi. CIT YYLab B4 2021\nAll rights reserved.',
    font=('System', 10))
    label.place(x=15, y=10)
    button = Button(sub_win, text = 'OK', command = sub_win.destroy)
    button.place(x=160, y=70)
    u""" フォーカス移動 """
    button.focus_set()
    sub_win.transient(root.master)
    sub_win.grab_set()

def read_img(path):
  global u_img, v_img
  image_path = path
  fr = open(image_path, 'rb')
  path_str = str(image_path)
  size_p = str(re.findall('\((.*)\)', path_str))
  size_s = size_p.split('x')
  w = size_s[0].strip("[']")
  h = size_s[1].strip("[']")
  size_c = h.split(',YUV')
  width = int(w)
  height = int(size_c[0])
  color = int(size_c[1])
  print(width,height,color)
  data = np.fromfile(fr, dtype=np.uint8)
  data = np.ravel(data)
  fr.close()

  print('data len', len(data))
  
  #rgb_arr = np.array([[1.164, 0, 1.596],
  #                    [1.164,0.391, 0.813],
  #                    [1.164, 2.018, 0]])

  if color == 444:
    wxh = width*height
    y = np.array(data[:wxh])
    u = np.array(data[wxh:wxh*2])
    v = np.array(data[wxh*2:])
    y = y.reshape(height,width)
    u = u.reshape(height,width)
    v = v.reshape(height,width)
    yuv = np.stack([y,u,v],axis=2)
    #r = np.array(rgb_arr[0,0]*(y)+rgb_arr[0,2]*(v)).astype(np.uint8)
    #g = np.array(rgb_arr[1,0]*(y)-rgb_arr[1,1]*(u)-rgb_arr[1,2]*(v)).astype(np.uint8)
    #b = np.array(rgb_arr[2,0]*(y)+rgb_arr[2,2]*(u)).astype(np.uint8)
    #rgb = np.stack([r,g,b],axis=2)
    rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

  elif color == 422:
    wxh = width*height
    wxh_ = (width//2)*height
    y = np.array(data[:wxh])
    u = np.array(data[wxh:wxh+wxh_])
    v = np.array(data[wxh+wxh_:])
    y = y.reshape(height,width)
    u = u.reshape(height,width//2)
    v = v.reshape(height,width//2)
    y0 = np.expand_dims(y[:,::2], axis=2)
    u = np.expand_dims(u, axis=2)
    y1 = np.expand_dims(y[:,1::2], axis=2)
    v = np.expand_dims(v, axis=2)
    img_yuv = np.concatenate((y0, u, y1, v), axis=2)
    img_yuv_cvt = img_yuv.reshape(img_yuv.shape[0], img_yuv.shape[1] * 2, int(img_yuv.shape[2] / 2))
    rgb = cv2.cvtColor(img_yuv_cvt, cv2.COLOR_YUV2BGR_YUYV)
    #r = np.array(rgb_arr[0,0]*(y-16)+rgb_arr[0,2]*(v_-128)).astype(np.uint8)
    #g = np.array(rgb_arr[1,0]*(y-16)-rgb_arr[1,1]*(u_-128)-rgb_arr[1,2]*(v_-128)).astype(np.uint8)
    #b = np.array(rgb_arr[2,0]*(y-16)+rgb_arr[2,2]*(u_-128)).astype(np.uint8)
    #rgb = np.stack([r,g,b],axis=2).astype(np.uint8)
    #rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_YUY2)

  elif color == 420:
    f = open(path,'rb')
    yuv = np.frombuffer(f.read(width*height*3//2), dtype=np.uint8).reshape((height*3//2, width))
    rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
    f.close()
    
  elif color == 400:
    wxh = width*height
    y = np.array(data[:wxh])
    y = y.reshape(height,width)
    rgb = Image.fromarray(y,'L')
    
  show_img(rgb,width,height,path_str,color)
  
def show_img(data,w,h,path,c):
  global canvas, u_img, v_img
  root.title('yuvObserver v0.1.0.0 - '+path)
  if c != 400:
    image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb) # RGBからPILフォーマットへ変換
  else:
    image_pil = data
  image_tk  = ImageTk.PhotoImage(image_pil) # ImageTkフォーマットへ変換
  
  canvas.delete('img')
  print(canvas)
  canvas.create_image(0, 0, image=image_tk, anchor='nw', tag='img') # ImageTk 画像配置
  canvas.grid(sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)
  #root.geometry("{0}x{1}".format(w,h))
  canvas.configure(scrollregion=(0,0,w,h))
  
  app = root
  xbar = tkinter.Scrollbar(
  app,  # 親ウィジェット
  orient=tkinter.HORIZONTAL,  # バーの方向
  )

# 垂直方向のスクロールバーを作成
  ybar = tkinter.Scrollbar(
  app,  # 親ウィジェット
  orient=tkinter.VERTICAL,  # バーの方向
  )

# キャンバスの下に水平方向のスクロールバーを配置
  xbar.grid(
  row=1, column=0,  # キャンバスの下の位置を指定
  sticky=tkinter.W + tkinter.E  # 左右いっぱいに引き伸ばす
  )

  # キャンバスの右に垂直方向のスクロールバーを配置
  ybar.grid(
  row=0, column=1,  # キャンバスの右の位置を指定
  sticky=tkinter.N + tkinter.S  # 上下いっぱいに引き伸ばす
  )


  # キャンバスをスクロールするための設定

  # スクロールバーのスライダーが動かされた時に実行する処理を設定
  xbar.config(
  command=canvas.xview
  )
  ybar.config(
  command=canvas.yview
  )

  # キャンバススクロール時に実行する処理を設定
  canvas.config(
  xscrollcommand=xbar.set
  )
  canvas.config(
  yscrollcommand=ybar.set
  )
  
  root.mainloop()

def main():
  read_img('bird-20(1024x672,YUV422).yuv')

if __name__ == '__main__':
  root = Tk()

  menubar = Menu(root)
    # File Menu
  filemenu = Menu(menubar, tearoff=0)
  filemenu.add_command(label='YUV File Open', command=import_yuv)
  filemenu.add_separator()
  filemenu.add_command(label='Exit', command=quit)
    # Help
  helpmenu = Menu(menubar, tearoff=0)
  helpmenu.add_command(label='Version', command=show_version)
  helpmenu.add_command(label='Help', command=get_help)
    
    # Add
  menubar.add_cascade(label='File', menu=filemenu)
  menubar.add_cascade(label='Help', menu=helpmenu)
    
  root.config(menu=menubar)

  root.title('yuvObserverGUI v0.1.0.0')
  root.minsize(640,512)
  root.rowconfigure(0, weight=1)
  root.columnconfigure(0, weight=1)
    
  frame1 = ttk.Frame(root)
  frame1.rowconfigure(0, weight=1)
  frame1.columnconfigure(0,weight=1)
  
  canvas = tkinter.Canvas(root, width=500, height=500) # Canvas作成
  canvas.grid()
  
  if len(sys.argv) > 1:
    read_img(sys.argv[1])
  
  root.mainloop()
  #main()
