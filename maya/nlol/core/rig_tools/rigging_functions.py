import re

from maya import cmds


def increment_bracketed_digit_once(text: str = "") -> str:
    """Increment last bracketed number in string by 1.

    Args:
        text: String with bracketed digit like [0] or [1].

    """
    if not text:
        return None

    match = re.search(r"\[(\d+)\](?!.*\[\d+\])", text)
    if not match:
        return None

    return re.sub(
        r"\[(\d+)\](?!.*\[\d+\])",  # find the last bracketed number
        lambda match: f"[{int(match.group(1)) + 1}]",  # increment by 1
        text,
    )


def increment_bracketed_digit_walk(plug: str) -> str:
    """Walk an array plug forward until an unconnected index is found.
    Returns the original plug if it has no bracketed digit or is already free.

    Args:
        plug: Object and attribute such as "main_nucleus.inputActiveStart[0]"
        to increment bracketed digit for.

    """
    while cmds.listConnections(plug):
        next_plug = increment_bracketed_digit_once(plug)
        if next_plug is None:
            break
        plug = next_plug
    return plug


def replace_node_connections(
    old_node: str = "",
    new_node: str = "",
    delete_old_node: bool = False,
    delete_old_node_parent: bool = False,
    increment_output_dest_plug: bool = False,
    increment_output_src_plug: bool = False,
    increment_input_dest_plug: bool = False,
    increment_input_src_plug: bool = False,
    skipped_output_connections: set | list = [],
    skipped_input_connections: set | list = [],
) -> None:
    """Replace old node connections with new node connections.
    If no args, first selected is new node, second selected is old node.

    Args:
        old_node: Old node to get connection data from.
        new_node: New node to replace old node with, keeping same connections.
        delete_old_node: Delete the old node.
        delete_old_node_parent: Useful for deleting parent transform if old node is a shape.
        increment_output_dest_plug, increment_output_src_plug,
        increment_input_dest_plug, increment_input_src_plug:
            Increase plug index by 1. From [0] to [1], for instance.
            "dest" refers to destination or endpoint of connection.
            "src" refers to source or startpoint of connection.
            "output" refers to connections going out from new node.
            "input" refers to connections going into new node.
        skipped_output_connections, skipped_input_connections:
            Skip plug connection if contains string from this list.
            So if the string "inputActive" is included, any plug with that will be skipped.
            "output" and "input" in arg names used in the same way as for the "increment" args.

    """
    if not (new_node and old_node):
        selected = cmds.ls(selection=True)
        new_node = selected[0]
        old_node = selected[1]

    # --- get old node connections ---
    # destination
    old_nd_dest = cmds.listConnections(
        old_node,
        source=False,
        destination=True,
        connections=True,
        plugs=True,
    )
    old_nd_output_pairs = list(zip(old_nd_dest[0::2], old_nd_dest[1::2], strict=False))

    # source
    old_node_src = cmds.listConnections(
        old_node,
        source=True,
        destination=False,
        connections=True,
        plugs=True,
    )
    old_nd_input_pairs = list(zip(old_node_src[1::2], old_node_src[0::2], strict=False))

    # --- replace old node connections with new node ---
    # destination.  output from new node.
    for src, dest in old_nd_output_pairs:
        src = src.replace(old_node, new_node, 1)
        if any(conn in src or conn in dest for conn in skipped_output_connections):
            continue  # skip specified plugs
        if not cmds.isConnected(src, dest):  # avoid warning/ incrementing an existing connection
            if increment_output_dest_plug:
                dest = increment_bracketed_digit_walk(dest)
            if increment_output_src_plug:
                src = increment_bracketed_digit_walk(src)
            cmds.connectAttr(src, dest, force=True)

    # source.  input to new node.
    for src, dest in old_nd_input_pairs:
        dest = dest.replace(old_node, new_node, 1)
        if any(conn in src or conn in dest for conn in skipped_input_connections):
            continue
        if not cmds.isConnected(src, dest):
            if increment_input_dest_plug:
                dest = increment_bracketed_digit_walk(dest)
            if increment_input_src_plug:
                src = increment_bracketed_digit_walk(src)
            cmds.connectAttr(src, dest, force=True)

    # --- delete old node ---
    if delete_old_node:
        cmds.delete(old_node)
    if delete_old_node_parent:  # for deleting shape transforms
        old_node_parent = cmds.listRelatives(old_node, parent=True)[0]
        cmds.delete(old_node_parent)
