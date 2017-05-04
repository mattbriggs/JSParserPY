# JSParserPY
# python3
# Matt Briggs
# This file parse will convert JS into an XML file to use in creating
# an JS object reference.
# 2016.10.19 (See the notes for current information)

import cmd
import datetime
import class_parseJS_v2 as PJS
import class_filewalker as FW

appversion = "JSParserPY Version 0.3 201610210000\n Type \'help\' for documentation.\n"
'''This is the command line interface to the base application.'''

class TagTerminal(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = "> "

    def do_parse(self, line):
        '''Type the filename of the JavaScript to parse. The parser will save an XML represenation alongside your file.'''
        try:
            Par = PJS.JSParser()
            Par.jstoXML(line)
        except:
            print ("Unable to process the file.")
        return
        
    def do_batchparse(self,line):
        '''Type a path name to a directory of JavaScript files to parse them.'''
        timestamp = str(datetime.date.today())
        errorlog = "Error log for " + timestamp + ".\nFiles unable to parse:\n"
        filelist = []
        try: 
            Dirt = FW.filewalker()
            filelist = Dirt.gettargetfiles(line)
        except:
            print ("Unable to process the files at the indicated path.")
        for f in filelist:
            try:
                Par = PJS.JSParser()
                Par.jstoXML(f)
            except:
                errorlog = errorlog + f + "\n"
                print ("Unable to parse: ",f)
            filename = "Error log" + timestamp + ".txt"
            file_ = open(filename, 'w')
            file_.write(errorlog)
            file_.close()  
            print ("Done with batch parsing.")
        return
    
    def do_quit(self, line):
        '''Type quiet to exit the application.'''
        return True

    def do_exit(self, line):
        '''Type exit to exit the application.'''
        return True

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    TagTerminal().cmdloop(appversion)
