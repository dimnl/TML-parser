class Engines:
    ONTOP = 'Ontop'
    MORPH_RDB = 'Morph-RDB'
    RMLMAPPER = 'RMLMapper'
    ROCKETRML = 'RocketRML'
    SDM_RDFIZER = 'SDM-RDFizer'
    RMLSTREAMER = 'RMLStreamer'

    @staticmethod
    def get_all():
        return [Engines.ONTOP, Engines.MORPH_RDB, Engines.RMLMAPPER, Engines.ROCKETRML, Engines.SDM_RDFIZER,
                Engines.RMLSTREAMER]


class MappingLanguages:
    R2RML = 'R2RML'
    RML = 'RML'
    YARRRML = 'YARRRML'
    SPARQL_GENERATE = 'SPARQL-Generate'
    SHEXML = 'ShExML'

    @staticmethod
    def get_all():
        return [MappingLanguages.R2RML, MappingLanguages.RML, MappingLanguages.YARRRML,
                MappingLanguages.SPARQL_GENERATE, MappingLanguages.SHEXML]


class OperatingSystems:
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MACOS = 'MacOS'

    @staticmethod
    def get_all():
        return [OperatingSystems.WINDOWS, OperatingSystems.LINUX, OperatingSystems.MACOS]


class Warnings:
    DEDUPLICATION_UNSUPPORTED = """
        WARNING: De-duplication is not supported by this engine! 
        The generated configurations to run the engine could return duplicates.
        """

    NOT_IMPLEMENTED = """
        This Knowledge Graph Construction engine is not implemented yet!
        If you would like to have this engine too, please contribute: https://github.com/dimnl/TML-parser
        """

    VERSION_NOT_SPECIFIED = """
        WARNING: Version of Engine is not specified!
        The generated configuration may not work.
        """
