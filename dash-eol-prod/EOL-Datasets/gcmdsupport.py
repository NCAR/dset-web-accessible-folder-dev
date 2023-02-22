import xmltodict
import pprint

def getGCMDfromXML(filename):
    with open(filename) as fd:
        doc = xmltodict.parse(fd.read())

    pp = pprint.PrettyPrinter(indent=1)

    #print(doc['gmd:MD_Metadata']['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:descriptiveKeywords'])
    try:
        gcmd_ref = doc['gmd:MD_Metadata']['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:descriptiveKeywords'][2]['gmd:MD_Keywords']['gmd:keyword']
    except IndexError:
        pass
    except KeyError:
        gcmd_ref = doc['gmd:MD_Metadata']['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:descriptiveKeywords']

    is_local = "gcmd_ref" in locals()

    keywords = []

    if is_local:
        for elem in gcmd_ref:
            try:
                keywords.append(elem['gco:CharacterString'])
            except TypeError:
                try:
                    keywords.append(gcmd_ref['gco:CharacterString'])
                except KeyError:
                    keywords.append("no keywords")
            except KeyError:
                keywords.append("no keywords")
    else:
        keywords.append("no keywords")
    
    return keywords