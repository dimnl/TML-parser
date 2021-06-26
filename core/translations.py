def output_translate_to_rmlstreamer(mapping_name, location, serialization, de_duplication=None):
    cli_command = 'FLINK_BIN run RMLStreamer-<version>.jar'
    cli_command += ' toFile'  # or ToTCPSocket or toKafka
    cli_command += ' --mapping-file ' + mapping_name
    cli_command += ' --output-path ' + location
    if serialization == 'jsonld':
        cli_command += ' --json-ld'

    return cli_command, None, None


def output_translate_to_ontop(mapping_name, location, serialization, de_duplication=None):
    cli_command = '/.ontop'
    cli_command += ' materialize'
    cli_command += ' --mapping ' + mapping_name
    cli_command += ' --output ' + location
    cli_command += ' --format ' + serialization

    return cli_command, None, None


def output_translate_to_morphrdb(mapping_name, os_name, location, serialization, de_duplication=None):
    cli_command_windows = 'java -cp .:morph-rdb-dist-3.8.1.jar:dependency/*'
    cli_command_unix = 'java -cp morph-rdb.jar;lib/*'
    if os_name == 'WINDOWS':
        cli_command = cli_command_windows
    else:
        cli_command = cli_command_unix
    cli_command += 'es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner morph-output config.morph.properties'

    config_file = 'mappingdocument.file.path=' + mapping_name
    config_file += '\n' + 'output.file.path=' + location
    config_file += '\n' + 'output.rdflanguage=' + serialization

    return cli_command, config_file, 'config.morph.properties'


def output_translate_to_rmlmapper(mapping_name, location, serialization, de_duplication):
    cli_command = 'java -jar rmlmapper.jar'
    cli_command += ' --mappingfile ' + mapping_name
    cli_command += ' --outputfile ' + location
    cli_command += ' --serialization ' + serialization
    if de_duplication:
        cli_command += ' --duplicates'

    return cli_command, None, None


def output_translate_to_rocketrml(mapping_name, location, serialization, de_duplication):
    # TODO
    cli_command = 'java -jar rmlmapper.jar'
    cli_command += ' --mappingfile ' + mapping_name
    cli_command += ' --outputfile ' + location
    cli_command += ' --serialization ' + serialization
    if de_duplication:
        cli_command += ' --duplicates'

    return cli_command, None, None


def output_translate_to_sdmrdfizer(mapping_name, location, serialization, de_duplication):
    # TODO
    cli_command = 'java -jar rmlmapper.jar'
    cli_command += ' --mappingfile ' + mapping_name
    cli_command += ' --outputfile ' + location
    cli_command += ' --serialization ' + serialization
    if de_duplication:
        cli_command += ' --duplicates'

    return cli_command, None, None
