'''Class that performs the parsing.'''
'''Todo: need to verify the parsing of flat functions.'''

import xml.etree.ElementTree as ET
import re
import datetime

class JSParser():
    def __init__(self):
        self.state = "new"
        self.namespacelist = []
        self.objectlist = []
        self.functionlist = []
        self.paramlist = []
        self.comment = ""
        self.commentstate = False

    def fileopen(self, filename):
        try:
            fh = filename
            JSbody = open(fh)
            return JSbody
        except:
            messsage = "Not able to open file."
            print (messsage)
            return messsage

    def getcomment_slash(self, line):
        '''With a line and comment variable, will add the comment line to the comment variable.'''
        if re.search('//', line):
            obpara = line.find('/')+2
            commentline = line[obpara:]
            commentline = commentline.strip()
            self.comment = self.comment + commentline
            self.commentstate = True

    def getcomment_hash(self, line):
        '''With a line and comment variable, will add the comment line to the comment varaible.'''
        if re.search('#', line):
            obpara = line.find('#')+1
            commentline = line[obpara:]
            commentline = commentline.strip()
            self.comment = self.comment + commentline
            self.commentstate = True

    def jstoXML(self, filename):

        JSbody = self.fileopen(filename)

        # variables

        linecounter = 0
        comment = ""
        commentstate = False
        filenameroot = filename[:-3]
        filenameout = filenameroot + ".xml"
        timestamp = str(datetime.date.today())

        # build XML tree
        root = ET.Element('root')
        root.attrib['file'] = filename
        root.attrib['date'] = timestamp
        jsnamespaces = ET.SubElement(root,"namespaces")

        # the line reader

        for line in JSbody:
            line = line.rstrip()
            linecounter += 1
            print (linecounter)

            # parse namespace following Type declratoin and create root of the tree

            self.getcomment_slash(line)
            self.getcomment_hash(line)

            if re.search('Type\.registerNamespace', line):
                obpara = line.find('(')+1
                clpara = line.find(')')
                fnamespace = line[obpara:clpara]
                fnamespace = fnamespace.strip("\'")
                fnamespace = fnamespace.strip()

                # add subnodes: 'namespace' and sibling 'name'
                jsnamespace = ET.SubElement(jsnamespaces, "namespace")
                self.namespacelist.append(jsnamespace)
                jsnamespacename = ET.SubElement(jsnamespace, "name")
                jsnamespacename.text = fnamespace

                # add comment node for namespace
                if self.commentstate == True:
                    lastnode = len(self.namespacelist)
                    jsnamespacename_com = ET.SubElement(self.namespacelist[lastnode-2], "comment")
                    jsnamespacename_com.text = self.comment
                    self.comment = ""
                    selfcommentstate = False

            # parse objects

            if re.search(' = function ()', line):
                obterminal = line.find('=')
                hereObject = line[0:obterminal]
                hereObject = hereObject.strip()

                # add subnodes: 'object' and sibling 'name'
                try:
                    jsnamespace
                except:
                    jsnamespace = ET.SubElement(jsnamespaces, "namespace")
                jsobject = ET.SubElement(jsnamespace, "object")
                self.objectlist.append(jsobject)
                jsobjectname = ET.SubElement(jsobject,"name")
                jsobjectname.text = hereObject

                #add comment node for object
                if self.commentstate == True:
                    lastnode = len(self.objectlist)
                    jsobjectname_com = ET.SubElement(self.objectlist[lastnode-2], "comment")
                    jsobjectname_com.text = self.comment
                    self.comment = ""
                    self.commentstate = False

            # parse functions structure 1 - 'CancelAttach: function () { '

            if re.search(': function', line):
                atcolon = line.find(':')
                jsfunc = line[0:atcolon]
                jsfunc = jsfunc.strip()

                # add subnodes: 'function' and sibling 'name'
                try:
                    jsobject
                except:
                    jsobject = ET.SubElement(jsnamespace, "object")
                jsfunction1 = ET.SubElement(jsobject,"function")
                self.functionlist.append(jsfunction1)
                jsfunctionname1 = ET.SubElement(jsfunction1,"name")
                jsfunctionname1.text = jsfunc

                # add comment node for function
                if self.commentstate == True:
                    lastnode = len(self.functionlist)
                    jsfunction_com1 = ET.SubElement(self.functionlist[lastnode-2], "comment")
                    jsfunction_com1.text = self.comment
                    self.comment = ""
                    self.commentstate = False

            # parse functions structure 2 - 'NWF.RuntimeFunctions.max = function(controlValues) { '

            if re.search('= function\(', line):
                atequal = line.find('=')
                jsfunc = line[0:atequal]
                jsfunc = jsfunc.strip()
                

                # add subnodes: 'function' and sibling 'name'
                try:
                    jsobject
                except:
                    jsobject = ET.SubElement(jsnamespace,"object")
                jsfunction2 = ET.SubElement(jsobject,"function")
                self.functionlist.append(jsfunction2)
                jsfunctionname2 = ET.SubElement(jsfunction2,"name")
                jsfunctionname2.text = jsfunc

                # add comment node for function
                if self.commentstate == True:
                    lastnode = len(self.functionlist)
                    jsfunction_com2 = ET.SubElement(self.functionlist[lastnode-2], "comment")
                    jsfunction_com2.text = self.comment
                    self.comment = ""
                    self.commentstate = False

            # parse parameters structure 1 - - 'CancelAttach: function () { '

            if re.search(': function', line):
                obpara = line.find('(')+1
                clpara = line.find(')')
                parameters = line[obpara:clpara]
                parameters = parameters.strip()
                parametersList = parameters.split(",")

                # add subnodes: 'parameter'
                for p in parametersList:
                    param = p.strip()
                    jsparameter1 = ET.SubElement(jsfunction1,"parameter")
                    self.paramlist.append(jsparameter1)
                    jsparameter1.text = param

                    # add comment node for parameter
                    if self.commentstate == True:
                        lastnode = len(self.paramlist)
                        jsparameter_com1 = ET.SubElement(self.paramlist[lastnode-2], "comment")
                        jsparameter_com1.text = self.comment
                        self.comment = ""
                        self.commentstate = False
            
            # parse parameters structure 2 - 'NWF.RuntimeFunctions.max = function(controlValues) { '

            if re.search('= function\(', line):
                obpara = line.find('(')+1
                clpara = line.find(')')
                parameters = line[obpara:clpara]
                parameters = parameters.strip()
                parametersList = parameters.split(",")

                # add subnodes: 'parameter'
                for p in parametersList:
                    param = p.strip()
                    jsparameter2 = ET.SubElement(jsfunction2,"parameter")
                    self.paramlist.append(jsparameter2)
                    jsparameter2.text = param

                    # add comment node for parameter
                    if self.commentstate == True:
                        lastnode = len(self.paramlist)
                        jsparameter_com2 = ET.SubElement(self.paramlist[lastnode-2], "comment")
                        jsparameter_com2.text = self.comment
                        self.comment = ""
                        self.commentstate = False
            
              # Console Out

        ET.dump(root)
        totalline = str(linecounter+1)
        root.attrib['lines'] = totalline
        print ("total lines: " + totalline)
        print ("Saved file to " + filenameout)

        #XML File Out

        tree = ET.ElementTree(root)
        tree.write(filenameout)
