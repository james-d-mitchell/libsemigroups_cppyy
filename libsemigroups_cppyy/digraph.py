"""
This file contains the interface to libsemigroups digraph; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__actiondigraph.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail


def ActionDigraph(nr_verts):
    int_type = cppyy.gbl.libsemigroups.SmallestInteger(nr_verts).type
    action_digraph_type = cppyy.gbl.libsemigroups.ActionDigraph(int_type)
    detail.unwrap_return_value_to_int(action_digraph_type, action_digraph_type.scc_id)
    detail.unwrap_return_value_to_int(action_digraph_type, action_digraph_type.nr_nodes)
    detail.unwrap_return_value_to_int(action_digraph_type, action_digraph_type.nr_edges)
    detail.unwrap_return_value_to_int(
        action_digraph_type, action_digraph_type.out_degree
    )
    detail.unwrap_return_value_to_int(action_digraph_type, action_digraph_type.nr_nodes)
    detail.unwrap_return_value_to_int(action_digraph_type, action_digraph_type.neighbor)
    action_digraph_type.__repr__ = (
        lambda x: "<ActionDigraph: %d nodes and %d edges>"
        % (x.nr_nodes(), x.nr_edges())
    )
    D = action_digraph_type()
    D.add_nodes(nr_verts)
    return D
