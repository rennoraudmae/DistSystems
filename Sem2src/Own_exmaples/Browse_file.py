#Information from: https://codeyarns.com/2014/02/25/how-to-use-file-open-dialog-to-get-file-path-in-python/

import Tkinter
import tkFileDialog

def main():

    Tkinter.Tk().withdraw() #close the root window
    in_path = tkFileDialog.askopenfilename()
    print in_path

if __name__=="__main__":
    main()

