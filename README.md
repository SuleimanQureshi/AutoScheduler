# AutoScheduler
This is a script to automatically find the aggregate schedule of students in a particular group. The objective is to see the common slots to schedule an industry visit.
HOW TO USE:
The only parameter to change would be the drop_EDI parameter given at the start of the script. This hides or shows Engineering Design and Innovation's timings in the final schedule. The option to hide it comes from the fact that students are allowed to miss class in the case that they have an industry visit scheduled.
The directory needs to be set up as follows:

'''bash
Main folder/
├── script.py
├── Project 1/
│   ├── Student1_sched.csv
│   ├── Student2_sched.csv
│   └── ...
├── Project 2/
│   ├── StudentN_sched.csv
│   └── ...
└── ...
'''

The images for every project (with the folder/project name) will be given in the main folder where the script is. The student schedules have to be exported from UniTime.
Steps:
1. Step up the main folder and download the script. 
2. Add folders for every project.
3. To the relevant folders, export the .csv schedule from UniTime of the relevant students.
4. Run the script.
5. All group schedules will be visible in the main folder.

Features to be added:
See the Ramadan Schedule of students too.
