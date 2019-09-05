import xml.etree.ElementTree as ET


def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root


def parse_parameters_bounds_xml(xml_path):
    root = parse_xml(xml_path)
    parameters_bounds = dict()
    for parameter in root.findall('parameter'):
        lower_bound = float(parameter.get('lowerBound'))
        upper_bound = float(parameter.get('upperBound'))
        parameter_name = parameter.get('name')
        parameters_bounds[parameter_name] = (lower_bound, upper_bound)

    return parameters_bounds


def parse_abundance_xml(xml_path):
    root = parse_xml(xml_path)
    abundances = dict()
    for protein in root.findall('protein'):
        abundance = float(protein.get('abundance'))
        monitor_variable_name = protein.get('name')
        abundances[monitor_variable_name] = abundance

    return abundances

