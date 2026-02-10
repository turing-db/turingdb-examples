import pandas as pd
import networkx as nx
from typing import Union, Dict, List, Optional


def create_graph_from_df(
    df: pd.DataFrame,
    *,
    directed: bool = True,
    source_node_col: Union[str, Dict[str, str]] = "source",
    target_node_col: Union[str, Dict[str, str], None] = None,
    attributes_source_node_cols: Union[str, List[str], None] = None,
    attributes_target_node_cols: Union[str, List[str], None] = None,
    optional_nodes_cols: Optional[
        Dict[str, Dict[str, Union[str, List[str], bool]]]
    ] = None,
    attributes_edges: Union[str, List[str], None] = None,
    edge_col: Optional[str] = None,
    edge_col_label: Optional[str] = None,
    node_attributes_df: Optional[pd.DataFrame] = None,
    node_attributes_key_col: str = "id",
) -> Union[nx.Graph, nx.DiGraph]:
    """
    Create a NetworkX graph from a pandas DataFrame.

    This function converts a DataFrame where each row represents either:
    - An interaction (if target_node_col is provided)
    - A single node (if target_node_col is None)

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame where each row represents a node or an interaction.

    directed : bool, default=True
        Whether to create a directed graph. If True, creates nx.DiGraph, otherwise nx.Graph.

    source_node_col : str or Dict[str, str], default='source'
        Column(s) specifying the source node (or main node when target is None).
        If str: Name of column containing source node IDs.
        If dict: {
            'id': 'column_name',  # Required: Column containing node IDs
            'displayName': 'column_name',  # Optional: Column containing node labels
            'type': value  # Optional: Can be either:
                           # - A column name containing node types
                           # - A constant string value to use as the type for all nodes
        }

    target_node_col : str, Dict[str, str], or None, default=None
        Column(s) specifying the target node. If None, each row creates only a source node.
        Same format as source_node_col when provided.

    attributes_source_node_cols : str, List[str], or None, default=None
        Column(s) containing attributes for source nodes.

    attributes_target_node_cols : str, List[str], or None, default=None
        Column(s) containing attributes for target nodes. Ignored if target_node_col is None.

    optional_nodes_cols : Dict[str, Dict[str, Union[str, List[str], bool]]] or None, default=None
        Specifications for additional node sets in the DataFrame.
        Format: {
            'node_set_name': {
                'id': 'column_name',  # Required: Column containing node IDs
                'displayName': 'column_name',  # Optional: Column containing node labels
                'type': 'column_name',  # Optional: Column containing node types
                'attributes': ['col1', 'col2', ...],  # Optional: Columns for node attributes
                'link_to_source': True,  # Optional: Whether to link to source nodes
                'link_to_target': False,  # Optional: Whether to link to target nodes (ignored if target_node_col is None)
                'edge_attributes': ['col1', 'col2', ...]  # Optional: Edge attribute columns
            },
            ...
        }

    attributes_edges : str, List[str], or None, default=None
        Column(s) containing edge attributes between source and target nodes.
        Ignored if target_node_col is None.


    edge_type_col : str or None, default=None
        Column containing the type/label for edges.
        Ignored if target_node_col is None.

    node_attributes_df : pd.DataFrame or None, default=None
        Optional DataFrame containing additional attributes for nodes.
        Must contain a column specified by node_attributes_key_col to match nodes.

    node_attributes_key_col : str, default='id'
        Column name in node_attributes_df used to match nodes.

    Returns
    -------
    G : nx.DiGraph or nx.Graph
        NetworkX graph with nodes, edges, and attributes as specified.

    Notes
    -----
    - Node IDs must be unique and not NaN
    - If label is not specified, node ID is used as label
    - Node attributes are added as node properties in the graph
    - Edge attributes are added as edge properties in the graph
    - When target_node_col is None, each row creates a standalone node that can be linked to optional nodes

    Examples
    --------
    >>> # Simple example with standalone nodes (no target)
    >>> G = create_graph_from_df(df, source_node_col='person', target_node_col=None)

    >>> # Nodes with optional connections
    >>> G = create_graph_from_df(
    ...     df,
    ...     source_node_col={'id': 'person_id', 'displayName': 'person_name', 'type': 'Person'},
    ...     target_node_col=None,
    ...     optional_nodes_cols={
    ...         'skills': {
    ...             'id': 'skill_id',
    ...             'displayName': 'skill_name',
    ...             'type': 'Skill',
    ...             'link_to_source': True
    ...         }
    ...     }
    ... )

    >>> # Traditional source-target relationship
    >>> G = create_graph_from_df(df, source_node_col='person', target_node_col='movie')
    """
    label_str = "displayName"

    # Strip whitespace from string columns in main DataFrame
    df = df.copy()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # Strip whitespace from node_attributes_df if provided
    if node_attributes_df is not None:
        node_attributes_df = node_attributes_df.copy()
        for col in node_attributes_df.select_dtypes(include=["object"]).columns:
            node_attributes_df[col] = node_attributes_df[col].astype(str).str.strip()

    # Create a directed or undirected graph
    G = nx.DiGraph() if directed else nx.Graph()

    # Helper function to process node columns
    def process_node_info(col_spec):
        if isinstance(col_spec, str):
            return {
                "id": col_spec,
                label_str: None,
                "type": None,
                "is_type_column": False,
            }
        else:
            # Check if 'type' is directly a string (constant type) or a column name
            type_value = col_spec.get("type")
            is_type_column = False

            # If type is specified and is a string that exists as a column, it's a column reference
            # Otherwise, it's treated as a constant value
            if isinstance(type_value, str) and type_value in df.columns:
                is_type_column = True

            return {
                "id": col_spec.get("id"),
                label_str: col_spec.get(label_str),
                "type": type_value,
                "is_type_column": is_type_column,
            }

    # Process node column specifications
    source_info = process_node_info(source_node_col)
    target_info = (
        process_node_info(target_node_col) if target_node_col is not None else None
    )

    # Validate required columns exist in the DataFrame
    required_cols = [source_info["id"]]
    if source_info[label_str]:
        required_cols.append(source_info[label_str])
    if source_info["type"] and source_info["is_type_column"]:
        required_cols.append(source_info["type"])

    # Only add target columns if target is specified
    if target_info:
        required_cols.append(target_info["id"])
        if target_info[label_str]:
            required_cols.append(target_info[label_str])
        if target_info["type"] and target_info["is_type_column"]:
            required_cols.append(target_info["type"])

    # Add attribute columns to required columns if specified
    if attributes_source_node_cols:
        if isinstance(attributes_source_node_cols, str):
            required_cols.append(attributes_source_node_cols)
        else:
            required_cols.extend(attributes_source_node_cols)

    # Only add target attributes if target is specified
    if target_info and attributes_target_node_cols:
        if isinstance(attributes_target_node_cols, str):
            required_cols.append(attributes_target_node_cols)
        else:
            required_cols.extend(attributes_target_node_cols)

    # Only add edge attributes if target is specified
    if target_info and attributes_edges:
        if isinstance(attributes_edges, str):
            required_cols.append(attributes_edges)
        else:
            required_cols.extend(attributes_edges)

    if target_info and edge_col:
        required_cols.append(edge_col)

    # Check for optional node sets
    if optional_nodes_cols:
        for node_set, config in optional_nodes_cols.items():
            required_cols.append(config.get("id", node_set))
            if label_str in config and config[label_str]:
                required_cols.append(config[label_str])
            if "type" in config and config["type"]:
                required_cols.append(config["type"])
            if "attributes" in config and config["attributes"]:
                if isinstance(config["attributes"], str):
                    required_cols.append(config["attributes"])
                else:
                    required_cols.extend(config["attributes"])
            if "edge_attributes" in config and config["edge_attributes"]:
                if isinstance(config["edge_attributes"], str):
                    required_cols.append(config["edge_attributes"])
                else:
                    required_cols.extend(config["edge_attributes"])

    # Check if all required columns exist in DataFrame
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in DataFrame: {missing_cols}")

    # Helper function to normalize attributes to a list
    def normalize_attr(attr):
        if attr is None:
            return []
        elif isinstance(attr, str):
            return [attr]
        return list(attr)

    # Normalize attribute lists
    source_attrs = normalize_attr(attributes_source_node_cols)
    target_attrs = normalize_attr(attributes_target_node_cols) if target_info else []
    edge_attrs = normalize_attr(attributes_edges) if target_info else []

    # Create lookup dict for node attributes if provided
    node_attrs_lookup = {}
    if node_attributes_df is not None:
        # Drop duplicates based on key column to ensure unique index
        unique_node_attrs = node_attributes_df.drop_duplicates(
            subset=[node_attributes_key_col]
        )
        node_attrs_lookup = unique_node_attrs.set_index(
            node_attributes_key_col
        ).to_dict("index")

    # Function to add a node to the graph with its attributes
    def add_node_with_attrs(
        row,
        node_id_col,
        node_label_col,
        node_type_val,
        is_type_column,
        attr_cols,
        node_prefix="",
    ):
        if pd.isna(row[node_id_col]):
            return None

        node_id = row[node_id_col]

        # Skip if node_id is NaN
        if pd.isna(node_id):
            return None

        # Add node if it doesn't exist yet
        if node_id not in G:
            # Set node attributes
            node_attrs = {}

            # Add label if specified
            if node_label_col:
                label = (
                    row[node_label_col] if not pd.isna(row[node_label_col]) else node_id
                )
                node_attrs[label_str] = label
            else:
                node_attrs[label_str] = str(node_id)

            # Add type if specified
            if node_type_val is not None:
                if is_type_column:
                    # Type from column
                    node_type = (
                        row[node_type_val] if not pd.isna(row[node_type_val]) else None
                    )
                    if node_type:
                        node_attrs["type"] = node_type
                else:
                    # Type as constant value
                    node_attrs["type"] = node_type_val

            # Add other attributes from row
            for attr_col in attr_cols:
                if attr_col in row and not pd.isna(row[attr_col]):
                    attr_name = f"{node_prefix}{attr_col}" if node_prefix else attr_col
                    node_attrs[attr_name] = row[attr_col]

            # Add attributes from node_attributes_df if available
            if node_id in node_attrs_lookup:
                for attr_name, attr_value in node_attrs_lookup[node_id].items():
                    if not pd.isna(attr_value):
                        node_attrs[attr_name] = attr_value

            G.add_node(node_id, **node_attrs)

        return node_id

    # Process each row in the DataFrame
    for idx, row in df.iterrows():
        # Add source node (always required)
        source_id = add_node_with_attrs(
            row,
            source_info["id"],
            source_info[label_str],
            source_info["type"],
            source_info["is_type_column"],
            source_attrs,
            node_prefix="",
        )

        # Skip if source is None
        if source_id is None:
            continue

        # Add target node only if target_node_col is specified
        target_id = None
        if target_info:
            target_id = add_node_with_attrs(
                row,
                target_info["id"],
                target_info[label_str],
                target_info["type"],
                target_info["is_type_column"],
                target_attrs,
                node_prefix="",
            )

            # Add edge between source and target with attributes (only if both nodes exist)
            if target_id is not None:
                edge_attributes = {}

                # Add edge type if specified
                if edge_col and edge_col in row and not pd.isna(row[edge_col]):
                    if edge_col_label is None:
                        edge_col_label = edge_col
                    edge_attributes[edge_col_label] = row[edge_col]

                # Add edge attributes
                for attr_col in edge_attrs:
                    if attr_col in row and not pd.isna(row[attr_col]):
                        edge_attributes[attr_col] = row[attr_col]

                G.add_edge(source_id, target_id, **edge_attributes)

        # Process optional node sets
        if optional_nodes_cols:
            for node_set, config in optional_nodes_cols.items():
                # Extract node information - use key name as default for id
                node_id_col = config.get("id", node_set)
                node_label_col = config.get(label_str)

                # Handle node type (column reference or constant value)
                if "type" in config:
                    # Explicitly specified type
                    node_type_val = config["type"]
                    is_type_column = (
                        isinstance(node_type_val, str) and node_type_val in df.columns
                    )
                else:
                    # Default to node_set key as constant type
                    node_type_val = node_set
                    is_type_column = False  # Always treat default as constant

                node_attr_cols = normalize_attr(config.get("attributes", []))

                # Add optional node
                opt_node_id = add_node_with_attrs(
                    row,
                    node_id_col,
                    node_label_col,
                    node_type_val,
                    is_type_column,
                    node_attr_cols,
                    node_prefix="",
                )

                if opt_node_id is None:
                    continue

                # Connect to source if specified
                if config.get("link_to_source", False):
                    edge_attrs_to_source = {}

                    # Add edge type if specified
                    if "edge_type_to_source" in config:
                        edge_attrs_to_source["type"] = config["edge_type_to_source"]

                    # Add edge attributes if specified
                    if "edge_attributes" in config:
                        for attr_col in normalize_attr(config["edge_attributes"]):
                            if attr_col in row and not pd.isna(row[attr_col]):
                                edge_attrs_to_source[attr_col] = row[attr_col]

                    G.add_edge(source_id, opt_node_id, **edge_attrs_to_source)

                # Connect to target if specified (only if target exists)
                if config.get("link_to_target", False) and target_id is not None:
                    edge_attrs_to_target = {}

                    # Add edge type if specified
                    if "edge_type_to_target" in config:
                        edge_attrs_to_target["type"] = config["edge_type_to_target"]

                    # Add edge attributes if specified
                    if "edge_attributes" in config:
                        for attr_col in normalize_attr(config["edge_attributes"]):
                            if attr_col in row and not pd.isna(row[attr_col]):
                                edge_attrs_to_target[attr_col] = row[attr_col]

                    G.add_edge(opt_node_id, target_id, **edge_attrs_to_target)

    return G


def build_create_command_from_networkx(G, node_type_key=None, edge_type_key=None):
    """Build CREATE command from NetworkX object"""

    def escape_value(value):
        """Escape quotes and special characters in property values"""
        import re

        value_str = str(value)
        # Replace problematic characters
        value_str = value_str.replace('"', '\\"')
        value_str = value_str.replace("\n", " ")
        value_str = value_str.replace("\r", " ")
        value_str = value_str.replace("\t", " ")
        value_str = value_str.replace("\\", "")
        # Remove or replace other problematic characters
        value_str = re.sub(
            r"[^\w\s\-\.\,\:\;\(\)\[\]\{\}\/\@\#\$\%\&\*\+\=\<\>\?\!\~\`\|\\]",
            " ",
            value_str,
        )
        # Clean up multiple spaces
        value_str = re.sub(r"\s+", " ", value_str).strip()
        return value_str

    # Collect all unique nodes
    all_nodes = {}
    for node_id, attrs in G.nodes(data=True):
        all_nodes[node_id] = attrs

    commands = []

    # TODO: Set properties type to correct one depending on one in networkx graph
    # ...

    def format_prop_key(k):
        if " " in k:
            return f"`{k}`"
        return k

    def format_prop_val(v):
        if isinstance(v, str):
            return f'"{escape_value(v)}"'
        return v

    # Create nodes first
    node_parts = []
    for i, (node_id, attrs) in enumerate(all_nodes.items()):
        props = []
        for k, v in attrs.items():
            prop = f"{format_prop_key(k)}: {format_prop_val(v)}"
            props.append(prop)
        props = ", ".join(props)

        node_type = attrs.get(
            node_type_key, node_type_key if node_type_key is not None else "Node"
        )
        # Convert node_type to PascalCase to avoid issues with spaces in queries
        node_type = (
            "".join(x.title() for x in node_type.replace("_", " ").split())
            if " " in node_type or "_" in node_type
            else node_type[0].upper() + node_type[1:]
        )
        node_id_val = f'"{node_id}"'
        node_parts.append(
            f'(:{node_type} {{id: {node_id_val}{", " + props if props else ""}}})'
        )

    if node_parts:
        commands.append("CREATE " + ",\n".join(node_parts))

    # Create edges using MATCH ... CREATE ...
    for source, target, edge_attrs in G.edges(data=True):
        # Extract relationship type from specified key
        relationship_type = edge_attrs.get(
            edge_type_key, edge_type_key if edge_type_key is not None else "CONNECTED"
        )

        # Remove the type key from properties to avoid duplication
        filtered_edge_attrs = {
            k: v for k, v in edge_attrs.items() if k != edge_type_key
        }

        # Build edge properties string
        edge_props = (
            ", ".join(
                [
                    f"{format_prop_key(k)}:{format_prop_val(v)}"
                    for k, v in filtered_edge_attrs.items()
                ]
            )
            if filtered_edge_attrs
            else ""
        )
        edge_props_str = f" {{{edge_props}}}" if edge_props else ""

        # Convert relationship type to uppercase for Cypher convention
        relationship_type = str(relationship_type).upper()

        source_id = f'"{source}"'
        target_id = f'"{target}"'

        edge_command = (
            f"MATCH (source {{id: {source_id}}}), (target {{id: {target_id}}}) "
            f"CREATE (source)-[:{relationship_type}{edge_props_str}]->(target)"
        )
        commands.append(edge_command)

    print(
        f"Cypher query will create graph with {G.number_of_nodes():,} nodes and {G.number_of_edges():,} edges"
    )

    return "\n".join(commands) if commands else ""


def split_cypher_commands(cypher_commands, max_size_mb=1, progress_bar=False):
    """
    Split Cypher commands into chunks to avoid size limits.
    Separates node creation from edge creation.

    Args:
        cypher_commands: Full Cypher command string
        max_size_mb: Maximum size in MB per chunk (default 1MB)
        progress_bar: Show progress bars (default False)

    Returns:
        Dictionary with format:
        {
            "node_chunks": list of node creation chunks,
            "edge_chunks": list of edge creation chunks
        }
    """
    if progress_bar:
        from tqdm.auto import tqdm

    max_bytes = max_size_mb * 1000 * 1000 * 0.9999
    lines = cypher_commands.strip().split("\n")

    # Collect the full CREATE block and separate edges
    create_block = []
    edge_lines = []
    in_create = False

    lines_iter = tqdm(lines, desc="Iterate lines") if progress_bar else lines
    for line in lines_iter:
        line = line.strip()
        if not line:
            continue

        if line.startswith("CREATE"):
            in_create = True
            create_block.append(line[7:].strip())  # Remove 'CREATE ' prefix
        elif line.startswith("MATCH"):
            in_create = False
            edge_lines.append(line)
        elif in_create:
            create_block.append(line)

    # Parse individual nodes from the CREATE block
    full_create = " ".join(create_block)
    nodes = []
    current_node = ""
    paren_count = 0

    full_create = (
        tqdm(full_create, desc="Iterate create characters")
        if progress_bar
        else full_create
    )
    for char in full_create:
        if char == "(":
            paren_count += 1
            current_node += char
        elif char == ")":
            current_node += char
            paren_count -= 1
            if paren_count == 0 and current_node.strip():
                nodes.append(current_node.strip().rstrip(",").strip())
                current_node = ""
        elif paren_count > 0:
            current_node += char

    # Chunk nodes by size
    node_chunks = []
    current_chunk = []
    current_size = len("CREATE ".encode("utf-8"))

    nodes_iter = tqdm(nodes, desc="Split nodes into chunks") if progress_bar else nodes
    for node in nodes_iter:
        node_size = len(node.encode("utf-8")) + 2  # +2 for ",\n"

        if current_size + node_size > max_bytes and current_chunk:
            node_chunks.append("CREATE " + ",\n".join(current_chunk))
            current_chunk = []
            current_size = len("CREATE ".encode("utf-8"))

        current_chunk.append(node)
        current_size += node_size

    if current_chunk:
        node_chunks.append("CREATE " + ",\n".join(current_chunk))

    return {"node_chunks": node_chunks, "edge_chunks": edge_lines}
