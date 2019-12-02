## 使用方法
------
1.  使用精灵标注助手进行标注，并最后生成JSON格式的文件(注意：图片名中不得包含下划线、空格等特殊字符，tools文件夹下有一个delete_x_in_batches.bat工具，和图片放在同一文件夹中，双击即可。当set "str=_"时，清除图片下划线；set "str= "清除图片空格。)

2. 将精灵标注助手生成output文件夹下的JSON文件全部放在data/annotations文件夹下

3. 图片将标注的图片放在data/imgs下。为确保找到准确的数据，请忽随意修改图片文件名

4. 完成上述步骤

5. 生成初步的TXT文件
    ```python
    python 1.json2TXT.py
    ```
    (此时，你可以在data\labeledimgs文件夹下看到你标注的图片)

6. 生成anchors文件
    ```python
    python 2.get_kmeans.py
    ```
   

7. 得到最后所需要的文件
    ```python
   python 3.final_get_useful_data.py
    ```
8. 在OUT_PUT文件夹下可以看到yolo训练程序所需要的Annotations.txt、names.txt、yolo_anchors.txt


## 数据增强
------
**确定你运行了'3.final_get_useful_data.py'**
- 4.data_enhance_resize.py 主要进行缩放，每张图片都会进行缩放，范围定义在(0.3，0.8),生成的data_enhance_resize.txt把其中的数据按格式粘贴添加到
'data\data_configs\annotations.txt'中。把'OUT_PUT\data_enhance_resize\data'下的img，粘贴到'data\data_configs\imgs'中。再执行5,6,7步骤即可.
    ```python
   python 4.data_enhance_resize.py
    ```

- 5.data_enhance_crop.py 主要进行随机剪裁，按左上角、右上角、左下角、右下角进行剪裁，图片中所有需要被识别的物体都会被包含在内。
    ```python
   python 5.data_enhance_crop.py
    ```

- 6.data_enhance_Increase_noise.py 主要用于给图片增加噪声，默认为高斯噪声，此方法比较耗时，量力而行。
    ```python
   python 6.data_enhance_Increase_noise.py
    ```

- 7.data_enhance_Change_Bright.py,主要是用来改变图片的明暗程度的。
  

## 注意
------
- 如果你想使用某个单独步骤，请查看1.dataTXT.py、2.get_kmeans.py、3.filay_get_useful_data.py代码，单独运行即可