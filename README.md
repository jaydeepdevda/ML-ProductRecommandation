# ML-ProductRecommandation
Product Recommandation
Folder Description:
helper -> in helper folder GUIClass contains which is helper class for GUI using tkinter library

screen_shot -> two screen shot contains of result of this script for each GUI and Non-GUI
![Alt text](screen_shot/screen_shot_gui.png?raw=true "Output GUI")

File Description:
`data_order.json`  (Private Data) -> data set of transaction history for building model as JSON Format

`script_main_gui.py` -> GUI Version

`script_simple.py` -> runs in Command Prompt

(in both script file functionality is same)

after running any of this script (code) following files will be created for saving object as Model:</br>
	1. `obj_item_dict.pkl`</br>
	2. `obj_list_pair.pkl`</br>
	3. `obj_pair_dict.pkl`</br>
in case if delete any file, will be generated again after run code again.

all `data.txt` -> is item id and its name, it is just for references, It is not used in code.
