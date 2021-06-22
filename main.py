import base64
import re
import uuid

import streamlit as st

from TMLParserEnvironment import TMLParserEnvironment

################################################################################
# Website structure
###############################################################################
st.set_page_config(page_title="TML Parser", page_icon=":open_book:", layout="wide",
                   initial_sidebar_state="expanded")

# Make website sidebar
st.sidebar.title("Configurations")
st.sidebar.subheader('Engine')
ENGINE_CHOSEN = st.sidebar.selectbox("Choose a KGC engine", ['Ontop', 'Morph-RDB', 'RMLMapper', 'RMLStreamer', 'RocketRML'])
st.sidebar.subheader('Input')
MAPPING_LANGUAGE_IN = st.sidebar.selectbox("Choose the language of the input mapping",
                                           ['R2RML', 'RML', 'SPARQL-Generate', 'ShExML'])
st.sidebar.subheader('Output')
MAPPING_LANGUAGE_OUT = st.sidebar.selectbox("Choose the language of the output mapping",
                                            ['R2RML', 'RML', 'SPARQL-Generate', 'ShExML'])


st.sidebar.markdown(
    """
    ## Additional information
    
    Source code freely available at [GitHub](https://github.com/dimnl/TML-parser).
    
    Made at :house: by [Dim Hoogeveen](https://www.linkedin.com/in/dimhoogeveen/?locale=en_US) 
    as part of his Master Thesis. 
    
    The involved parties of this thesis are [OEG](https://oeg.fi.upm.es/) 
    (part of [fi](http://fi.upm.es/) within [UPM](https://www.upm.es/))
    and [TUe](https://www.tue.nl/en/).
    
    """
)

# Make website main page
st.title('Templated Mapping Language (TML) Parser :open_book:')

INPUT_CONTAINER = st.beta_container()
OUTPUT_CONTAINER = st.beta_container()
FOOTER_CONTAINER = st.beta_container()

# Put logic in containers
INPUT_CONTAINER.header('Input')
FILE_UPLOADED = INPUT_CONTAINER.file_uploader('Choose a TML file to parse',
                                              help='The filename extension does not matter')

with INPUT_CONTAINER.beta_expander('Alternatively, click here to write or paste TML mapping directly'):
    FILE_PASTED = st.text_area('Mapping textual input',
                               help='If a file is uploaded, delete that first to parse the pasted TML.')
    FILENAME_PASTED = st.text_input('Optionally, specify mapping name to be used for creating the output',
                                    value='example-mapping.ttl')

OUTPUT_CONTAINER.header('Output')
OUTPUT_CONTAINER.markdown(f'Generated for the **{ENGINE_CHOSEN}** knowledge graph construction engine. '
                          f'The original mapping uses  **{MAPPING_LANGUAGE_IN}** as mapping language, '
                          f'while the outputted mapping language is **{MAPPING_LANGUAGE_OUT}**. ')

OUTPUT_MAPPING, OUTPUT_CONFIG = OUTPUT_CONTAINER.beta_columns(2)
OUTPUT_MAPPING.subheader('Mapping')
OUTPUT_CONFIG.subheader('Configurations')

FOOTER_CONTAINER.markdown('------')
sidebar_col_oeg, sidebar_col_fi, sidebar_col_upm, sidebar_col_tue = FOOTER_CONTAINER.beta_columns(4)
with sidebar_col_oeg:
    st.image('./img/oeg.png', width=150)
    # st.markdown("[OEG](https://oeg.fi.upm.es/)")
with sidebar_col_fi:
    st.image('./img/fi.png', width=120)
    # st.markdown("[fi](http://fi.upm.es/)")
with sidebar_col_upm:
    st.image('./img/upm.png', width=150)
    # st.markdown("[UPM](https://www.upm.es/)")
with sidebar_col_tue:
    st.image('./img/TUe.png', width=150)


################################################################################
# Main logic
###############################################################################
def main():
    Observer.clear()  # Prevent build-up of multiple TML files at the same time.
    content_parsed = None

    if FILE_UPLOADED is not None:
        content_parsed = get_environment().load_file(FILE_UPLOADED)
        mapping_name = FILE_UPLOADED.name

    elif FILE_PASTED.strip() != '':
        content_parsed = get_environment().from_string(FILE_PASTED)
        mapping_name = FILENAME_PASTED

    if content_parsed is not None:
        OUTPUT_MAPPING.markdown(generate_download_link(content_parsed.render(), mapping_name), unsafe_allow_html=True)
        OUTPUT_MAPPING.code(content_parsed.render())

        for (output_id, output) in Observer.output.items():
            if ENGINE_CHOSEN == 'Ontop':
                config_cli = output.translate_to_ontop(mapping_name)
            elif ENGINE_CHOSEN == 'Morph-RDB':
                config_cli = output.translate_to_rmlmapper(mapping_name)  # TODO
            elif ENGINE_CHOSEN == 'RMLMapper':
                config_cli = output.translate_to_rmlmapper(mapping_name)
            elif ENGINE_CHOSEN == 'RMLStreamer':
                config_cli = output.translate_to_rmlstreamer(mapping_name)
            elif ENGINE_CHOSEN == 'RocketRML':
                config_cli = output.translate_to_rmlmapper(mapping_name)  # TODO

            OUTPUT_CONFIG.write('Command for command line interface')
            OUTPUT_CONFIG.code(config_cli)


################################################################################
# Helper functions
###############################################################################
@st.cache(hash_funcs={TMLParserEnvironment: id})
def get_environment():
    """
    Get the current environment or create one if it doesn't exist yet.
    Because of the defined cache with custom hashing, it will not recalculate; except when cache is cleared.

    Returns: TMLParserEnvironment

    """
    return TMLParserEnvironment(autoescape='')


def template_callable(obj):
    """
    Decorator to use for objects that should be called directly from template; using '@template_callable'.
    """
    get_environment().add_object_to_globals(obj)
    return obj


@st.cache
def generate_download_link(file, filename):
    """
    Generates a download link for the given string; filename is what the output filename will be.
    This is made ad Streamlit does not support a download button natively.
    An adaption of https://discuss.streamlit.io/t/a-download-button-with-custom-css/4220

    Args:
        file (str):  file to download
        filename (str): filename including extension as output

    Returns: download link to be used in st.markdown with unsafe_allow_html=True)

    """
    # Some encoding/decoding magic to create download
    b64 = base64.b64encode(file.encode()).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub(r'\d+', '', button_uuid)

    # Custom CSS to match style of Streamlit
    custom_css = f""" 
            <style>
                #{button_id} {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    background-color: rgb(255, 255, 255);
                    color: rgb(38, 39, 48);
                    padding: .25rem .75rem;
                    position: relative;
                    text-decoration: none;
                    border-radius: 4px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: rgb(230, 234, 241);
                    border-image: initial;
                }} 

                #{button_id}:hover {{
                    border-color: rgb(246, 51, 102);
                    color: rgb(246, 51, 102);
                }}
                #{button_id}:active {{
                    box-shadow: none;
                    background-color: rgb(246, 51, 102);
                    color: white;
                    }}
            </style> """

    dl_link = custom_css + f'<a download="{filename}" id="{button_id}" href="data:file/txt;base64,{b64}">' \
                           f'Download {filename}</a><br></br>'

    return dl_link


################################################################################
# Translation classes (TML to engine-specific command/file)
###############################################################################
@template_callable
class Output(object):
    """
    Output class that exactly specifies the output dimension of the resulting knowledge graph from the mapping.
    Callable directly from template in TML.
    """

    def __init__(self, output_id='output', location='internal', serialization='turtle', de_duplication=False):
        self.output_id = output_id
        self.location = location
        self.serialization = serialization
        self.de_duplication = de_duplication
        Observer.output.update({output_id: self})

    def __repr__(self):
        return ''  # This is output printed to mapping in the place where the function was called

    def translate_to_ontop(self, mapping_name):
        cli_command = '/.ontop'
        cli_command += ' materialize'
        cli_command += ' --mapping ' + mapping_name
        cli_command += ' --output ' + self.location
        cli_command += ' --format ' + self.serialization

        return cli_command

    def translate_to_rmlmapper(self, mapping_name):
        cli_command = 'java -jar rmlmapper.jar'
        cli_command += ' --mappingfile ' + mapping_name
        cli_command += ' --outputfile ' + self.location
        cli_command += ' --serialization ' + self.serialization
        if self.de_duplication:
            cli_command += ' --duplicates'

        return cli_command

    def translate_to_rmlstreamer(self, mapping_name):
        cli_command = 'FLINK_BIN run RMLStreamer-<version>.jar'
        cli_command += ' toFile'  # or ToTCPSocket or toKafka
        cli_command += ' --mapping-file ' + mapping_name
        cli_command += ' --output-path ' + self.location
        if self.serialization == 'jsonld':
            cli_command += ' --json-ld'

        return cli_command


@template_callable
class DataAccess(object):
    """
    DataAccess class with credentials to get/put data from/in a certain location.
    Callable directly from template in TML.
    """

    def __init__(self, name='postgresDB', url='', user='admin', password='admin'):
        self.name = name
        self.url = url
        self.user = user
        self.password = password
        Observer.data_access[name] = self

    def __repr__(self):
        return ''

    def print_name(self):
        print(self.name)


class Observer(object):
    """
    Observer class to aggregate all classes created from within TML parsing.
    """
    output: {str: Output} = {}
    data_access: {str: DataAccess} = {}

    @staticmethod
    def clear():
        Observer.output = {}
        Observer.data_access = {}


################################################################################
# Start running file (if not part of an import)
###############################################################################
if __name__ == '__main__':
    main()
