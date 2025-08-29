The storeConfigure.fksc is a fkWrong! store configure file
Please do not change it easily. This file contains the way of sorting papers by FID.
If you really want to change the sort, you can go to the settings page, instead of messing with these critical files.
The general norm of fksc files is written below. Check it carefully before editing.


"root node FID": {
  "child node FID": {
    "args": [
      {
        "index": number,      <- This indicates where the arg is located.
        "length": number,     <- Length of the arg.
        "name": "xxx"         <- The name must be consistent with the args in the filename.
      }
    ],
    "filename": "filename{xxx}.jpg",     <- If you need to mention an arg in the filename, add a {} outside the name.
    "name": "sub node name",             <- Subdirectory name.
    "subject": 8                         <- Subject ID, 0-5 for Chi-Mat-Eng-Phy-Che-Bio, 8 for Other, and 9 for unknown.
                                         In fact, 9 will never appear in this file. But the python function may return 9 when it is unable to determine.
    "subtypes": {           <- If you have similar subtypes, use this. A perfect example is your Chinese regular homeworks.
        "1": "subA",
        "2": "subB",
        "C": "subC"
      }
  },

  "name": "root name"
}