import statics


################################################################################
# Output translation
###############################################################################
def output_translate(engine, mapping_name, os_name, version_engine, location, serialization, de_duplication):
    """
    Orchestrator function that calls the corresponding translation per engine for the Output TML.

    Args:
        engine: one of statics.Engines
        mapping_name: one of statics.MappingLanguages
        os_name: one of statics.OperatingSystems
        version_engine: version of the engine to use for configuration
        location: location coming from TML
        serialization: serialization coming from TML
        de_duplication: de-duplication (True/False) coming from TML

    Returns: Command for command line, configuration file, configuration filename, warnings (if there are any)

    """
    if engine == statics.Engines.ONTOP:
        cli_command, config_file, config_file_name, warnings = output_translate_to_ontop(mapping_name, location,
                                                                                         serialization, de_duplication)
    elif engine == statics.Engines.MORPH_RDB:
        cli_command, config_file, config_file_name, warnings = output_translate_to_morphrdb(mapping_name, os_name,
                                                                                            version_engine, location,
                                                                                            serialization,
                                                                                            de_duplication)
    elif engine == statics.Engines.RMLMAPPER:
        cli_command, config_file, config_file_name, warnings = output_translate_to_rmlmapper(mapping_name, location,
                                                                                             serialization,
                                                                                             de_duplication)
    elif engine == statics.Engines.SDM_RDFIZER:
        cli_command, config_file, config_file_name, warnings = output_translate_to_sdmrdfizer(mapping_name, location,
                                                                                              serialization,
                                                                                              de_duplication)
    elif engine == statics.Engines.RMLSTREAMER:
        cli_command, config_file, config_file_name, warnings = output_translate_to_rmlstreamer(mapping_name,
                                                                                               version_engine, location,
                                                                                               serialization,
                                                                                               de_duplication)
    else:
        cli_command, config_file, config_file_name, warnings = None, None, None, statics.Warnings.NOT_IMPLEMENTED

    return cli_command, config_file, config_file_name, warnings


def output_translate_to_rmlstreamer(mapping_name, version_engine, location, serialization, de_duplication):
    cli_command = 'FLINK_BIN run RMLStreamer-' + version_engine + '.jar'
    cli_command += ' toFile'  # or ToTCPSocket or toKafka, TODO to implement other options
    cli_command += ' --mapping-file ' + mapping_name
    cli_command += ' --output-path ' + location
    if serialization == 'jsonld':
        cli_command += ' --json-ld'

    if de_duplication:
        warnings = statics.Warnings.DEDUPLICATION_UNSUPPORTED
    else:
        warnings = None

    return cli_command, None, None, warnings


def output_translate_to_ontop(mapping_name, location, serialization, de_duplication):
    cli_command = '/.ontop'
    cli_command += ' materialize'
    cli_command += ' --mapping ' + mapping_name
    cli_command += ' --output ' + location
    cli_command += ' --format ' + serialization

    if de_duplication:
        warnings = statics.Warnings.DEDUPLICATION_UNSUPPORTED
    else:
        warnings = None

    return cli_command, None, None, warnings


def output_translate_to_morphrdb(mapping_name, os_name, version_engine, location, serialization, de_duplication):
    if os_name == statics.OperatingSystems.WINDOWS:
        cli_command = 'java -cp .:morph-rdb-dist-' + version_engine + '.jar:dependency/*'
    else:
        cli_command = 'java -cp morph-rdb.jar;lib/*'
    cli_command += 'es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner morph-output config.morph.properties'

    config_file = 'mappingdocument.file.path=' + mapping_name
    config_file += '\n' + 'output.file.path=' + location
    config_file += '\n' + 'output.rdflanguage=' + serialization

    if de_duplication:
        warnings = statics.Warnings.DEDUPLICATION_UNSUPPORTED
    else:
        warnings = None

    return cli_command, config_file, 'config.morph.properties', warnings


def output_translate_to_rmlmapper(mapping_name, location, serialization, de_duplication):
    cli_command = 'java -jar rmlmapper.jar'
    cli_command += ' --mappingfile ' + mapping_name
    cli_command += ' --outputfile ' + location
    cli_command += ' --serialization ' + serialization

    if de_duplication:
        cli_command += ' --duplicates'

    return cli_command, None, None, None


def output_translate_to_sdmrdfizer(mapping_name, location, serialization, de_duplication):
    config_file_name = 'config.ini'
    cli_command = "python3 rdfizer/run_rdfizer.py" + config_file_name

    config_file = '[default]'
    config_file += '\nmain_directory: /'
    config_file += '\n[datasets]'
    config_file += '\nnumber_of_datasets: 1'
    config_file += '\noutput_folder: ${default:main_directory}/' + location
    config_file += '\nall_in_one_file: no'
    if de_duplication:
        config_file += '\nremove_duplicate: yes'
    else:
        config_file += '\nremove_duplicate: no'
    config_file += '\nenrichment: yes'
    config_file += '\nname: output'

    config_file += '\n\n[dataset1]'
    config_file += '\nname: output'
    config_file += '\nmapping: ${default:main_directory}/' + mapping_name

    return cli_command, config_file, config_file_name, None


################################################################################
# Data Access translation
###############################################################################
def data_access_translate(engine, name, url, user, password):
    """
    Translation function for DataAccess per engine.
    Args:
        engine: one of statics.Engines
        name: location name
        url: connection link
        user: username for login
        password: password for login

    Returns: configuration file, configuration filename

    """
    if engine == statics.Engines.ONTOP:
        config_file_name = 'basic.properties'
        config_file = 'jdbc.name=' + name
        config_file += '\njdbc.url=' + url
        config_file += '\njdbc.user=' + user
        config_file += '\njdbc.password=' + password

    elif engine == statics.Engines.MORPH_RDB:
        config_file_name = 'config.morph.properties'
        config_file = 'no_of_database=1'
        config_file += '\ndatabase.name[0]=' + name
        config_file += '\ndatabase.driver[0]=com.mysql.jdbc.Driver'
        config_file += '\ndatabase.url[0]=' + url
        config_file += '\ndatabase.user[0]=' + user
        config_file += '\ndatabase.pwd[0]=' + password
        config_file += '\ndatabase.type[0]=mysql'

    elif engine == statics.Engines.SDM_RDFIZER:
        config_file_name = 'config.ini'
        config_file = 'db: ' + name
        config_file += '\nhost: ' + url
        config_file += '\nuser: ' + user
        config_file += '\npassword: ' + password

    else:
        config_file = None
        config_file_name = None

    return config_file, config_file_name
