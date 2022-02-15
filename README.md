<div id="top"></div>

<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="icon.ico" alt="Logo" width="100" height="100">
  </a>
  <h3 align="center">YUV-Observer.exe</h3>
  <p align="center">
    A simple YUV file viewer for Windows 10 System.
    <br />
    Latest version: v0.1.1.0
    <br />
    <a href=""><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>

## Features

* Display YUV444, YUV422, YUV420, YUV400, save as PNG format.
* Display of YUV and RGB layers.
* Zoom in and out of YUV images. (Note: memory limitation).

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

```sh
hogehoge(1024x768,YUV444).yuv
```

or

```sh
fugafuga(1024x768_444).yuv
```

Please change the file name of the YUV format you wish to view to the above format. If you do not use the above format, you can still view the file by specifying the height, width and color space of the YUV format file when viewing.

_For more examples, please refer to the [Documentation]()_

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the 3-clause BSD License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Library

The following libraries are used in this program.

* [NumPy](https://numpy.org/)
* [OpenCV](https://opencv.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

The following is a list of references that were used to create this program. I would like to take this opportunity to express my sincere gratitude.

* [その他の画像変換 — opencv 2.2 documentation](http://opencv.jp/opencv-2svn/c/miscellaneous_image_transformations.html)
* [Recommended 8-Bit YUV Formats for Video Rendering - Win32 apps](https://docs.microsoft.com/en-us/windows/win32/medfound/recommended-8-bit-yuv-formats-for-video-rendering)
* [BT.601 BT.709 BT.2020 BT.2100規格 - 虹色の旋律](http://nijikarasu.cocolog-nifty.com/blog/2017/08/bt601-bt709-bt2.html)
* [RGBからYCbCrへ変換する際の注意 - 虹色の旋律](http://nijikarasu.cocolog-nifty.com/blog/2020/02/post-3c4fbe.html)
* [JPEG のクロマサブサンプリングと YUVabc](http://blog.awm.jp/2016/02/10/yuv/)
* [YUVをちゃんと理解してからRGBにコンバートしましょうね](https://www.klab.com/jp/blog/tech/2016/1054828175.html)
* [YUVフォーマット及び YUVとRGBの変換](https://hk.interaction-lab.org/firewire/yuv.html#packed_format)
* [Processing YUV I420 from framebuffer?](https://stackoverflow.com/questions/69518644/processing-yuv-i420-from-framebuffer)

<p align="right">(<a href="#top">back to top</a>)</p>
