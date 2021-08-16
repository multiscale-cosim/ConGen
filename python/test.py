import neuroml


def main():
    xmlfilename = "../script/CompleteNetwork.xml"
    xmlfilename = "potjans_diesmann.xml"
    xmlfilename = "simple_network.xml"
    with open(xmlfilename) as xmlfile:
        network = neuroml.read_xml(xmlfile)
    print("\n".join(str(p) for p in network.populations))
    print("\n".join(str(p) for p in network.projections))

if __name__ == "__main__":
    main()
