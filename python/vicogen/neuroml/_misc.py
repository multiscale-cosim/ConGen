
neuroml_namespace = {'nml': "http://morphml.org/neuroml/schema",
                     'xsi': "http://www.w3.org/2001/XMLSchema-instance",
                     'net2': "http://morphml.org/networkml/schema",
                     'net': "http://www.neuroml.org/schema/neuroml2",
                     'cg': "./NetworkML_ViCoGen_file_format.xsd",
                     'mml': "http://morphml.org/morphml/schema",
                     'meta': "http://morphml.org/metadata/schema",
                     'bio': "http://morphml.org/biophysics/schema",
                     'cml': "http://morphml.org/channelml/schema"}


class NetworkMLParsingError(Exception):
    def __init__(self, xmlElement, msg=None):
        """:type xmlElement: xml.etree.ElementTree.Element
        :type msg: str"""
        self.xmlElement = xmlElement
        self.message = msg

    def __str__(self):
        if self.message:
            return "Exception while parsing NetworkML file: " + self.message + "\n" + str(self.xmlElement)
        else:
            return "Exception while parsing NetworkML file:\n" + str(self.xmlElement)
