## How to use
------
1. use Colabeler(Chinese name:精灵标注助手) to annotate your data,finally ,create JSON files.(Warning:The name of Picture can't Contain 'Blank space','Underline'.you can use 'tools/delete_x_in_batches.bat' to solve this problem.Put this file to your picture,and double-click)

2. Put all the json files(not 'output' folder.) in  'data/annotations'.

3. Put all the pictures in 'data/imgs',don't change pictre's name.

4. Complete the above steps

5. create embryo TXT file.
    ```python
    python 1.json2TXT.py
    ```

6. create anchors TXT
    ```python
    python 2.get_kmeans.py
    ```
7. Get finaly files you need
   ```python
   python 3.final_get_useful_data.py
   ```

8. in the 'OUT_PUT' files ,you can get the required documents: Annotations.txt、names.txt、yolo_anchors.txt


## DATA ENHANCE
------
**make sure you run the '3.final_get_useful_data.py'**
- '4.data_enhance_resize.py' this file will resize all pictures，scale range(0.3 0.8).Copy content from 'OUT_PUT/data_enhance_resize/data_enhance_resize.txt' file to 'data\data_configs\annotations.txt'(add ,not cover).Copy all pictures from 'OUT_PUT\data_enhance_resize\data' to 'data\data_configs\imgs',than perform 5,6,7 step
    ```python
   python 4.data_enhance_resize.py
    ```

- 5.data_enhance_crop.py  Same method to use.Random clipping of pictures

- 6.data_enhance_Increase_noise.py Same method to use.Add noise to picture,The default noise is Gaussian.This script will consume a lot of time,Do according to your PC ability.Please read this script if you want to add other noise,it won't take long
  
- 7.data_enhance_Change_Bright.py,this script will change the bright of pitcure.