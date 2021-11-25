from .fixtures_edge import *  # noqa
from .fixtures_graph import *  # noqa
from .fixtures_vertex import *  # noqa
from .fixtures import *  # noqa

from be.tile_creator_2.gtm_args import GtmArgs

class TestGtmArgs():

    def test_build_from_final_configs_dictionary(self, configurations):
        assert configurations != None, "The configuraiton fixture is none"
        gtm_args = GtmArgs(configurations)
        assert gtm_args.get_name() == configurations['graph_name']
        assert gtm_args.get_source_file() != None