## **Flatcam-to-Aerotech G-code Conversion**

Flatcam-to-Aerotech G-code Conversion was created to translate the g-code generated by _FlatCam_, an open-source PCB CAD milling software, to a code that could be interpreted by _Aerotech Motion Composer_ software.

## **Introduction**

This project was created while working in Nanoengineered Systems Laboratory at UCL, where a significant portion lab members work on hybrid 3D-printed flexible electronics. This work is underpinned by the use of a high-resolution 3D printer, which utilises nanopositioning stages manufactured by _Aerotech_. These stages are controlled by a proprietary _Aerotech Motion Composer_ software.

This 3D printer is mostly used for fabrication of flexible PCBs. Consequently, the PCB design had to take into account the physical dimensions of various electronic components, resulting in the use of various component libraries. The initial workflow for the PCB design involved using a PCB CAD software _Autodesk Eagle_ (now integrated into _Autodesk Fusion 360_) to develop the design, then exporting a _Gerber_ of the board design. This file could then be imported into _FlatCam_ and a g-code could be generated as if for milling around the designed interconnects and component mounting points. By utilising a very small milling tool diameter in _FlatCam_, it is possible to arrive at g-code that mimics the pattern of the designed PCB fairly well. 

Nevertheless, _FlatCam_ generated g-code that is to be used by milling machines, therefore, a number of instructions provided, such as M-codes, some G-codes, numerous F-codes, are either not necessary when performing printing using _Aerotech Motion Composer_ or cannot be interpreted by this piece of software. This project was completed for the simple reason of translating the _FlatCam_ generated g-code into _Aerotech Motion Composer_ readable g-code without needing to do a lot of manual editing.

The different files in the repo serve the following purposes:

- [conversion_v2.py](conversion_v2.py) is a Python script that was written to perform the translation and works by asking the user on whether the g-code supplied is in metric on imperial units, and later asking for inputs for the printing speed as well as high and low positions of the printing nozzle. If no input is provided, metric units are assumed and the default high and low positions are inserted. Only one printing speed F-code is inserted in the converted file (at the beginning), therefore, if different printing speeds throughout the printing pattern are required, the users are encouraged to contribute/modify the project.
- [example_unedited.txt](example_unedited.txt) and [converted.txt](converted.txt) are the example pre- and post-conversion g-code text files, respectively.
- [multilayer_printing.py](multilayer_printing.py) is a Python script to multiply the g-code of the designed printing pattern for multilayer printing. This is useful if you want to perform printing of the same pattern multiple times without running the printing programme on _Aerotech Motion Composer_ every single time. This also enabled 3D (more like 2.5D) printing of some shapes, such as moulds as the g-code of the pattern can be multiplied with a Z-axis offset.
- [3d_printing.txt](3d_printing.txt) is a 50-layer, 0.012 mm Z-offset printing programme of the [converted.txt](converted.txt) printing pattern.

__N.B.__ This workflow might be obsolete for most readers as similar results can be achieved by mastering the slicing software included in _Autodesk Fusion 360_.


## **Installation and Usage**

To install and use Flatcam-to-Aerotech G-code Conversion, follow these steps:

1. Clone the repository: **`git clone https://github.com/mpetreikis/aerotech-gcode.git`**
2. Navigate to the project directory: **`cd aerotech-gcode`**
3. (Optional) Create a new python environment using conda: **`conda env create -f environment.yml`**
4. (Optional) Activate the environment: **`conda activate aerotech`**
5. (Optional) Install the required packages in the environment: **`pip install -r requirements.txt`**
6. Open the project in your favorite code editor
7. Modify [conversion_v2.py](conversion_v2.py) and [multilayer_printing.py](multilayer_printing.py) to fit your needs
8. Use the project as desired

## **Contributing**

If you'd like to contribute to Flatcam-to-Aerotech G-code Conversion, feel free to email me (mpetreikis@tutanota.com) or simply, fork the repo, create a new branch for your changes and eventually submit a pull request.

## **License**

Flatcam-to-Aerotech G-code Conversion is released under the MIT License. See the **[LICENSE](LICENSE)** file for details.

## **Authors and Acknowledgment**

Flatcam-to-Aerotech G-code Conversion was created by **[Matas Petreikis](https://github.com/mpetreikis)**.
