def updateColor(client, stream_id, clashing_pairs, automate_context):
    """
    Updates the color of clashing elements to red.

    Args:
        client: The Speckle client instance.
        stream_id: The ID of the Speckle stream.
        clashing_pairs: A list of tuples with clashing element IDs.
        automate_context: The Speckle automation context for error reporting.
    """
    # Collect unique element IDs from clashing pairs
    clashing_element_ids = {element_id for pair in clashing_pairs for element_id in pair}

    for element_id in clashing_element_ids:
        # Retrieve each element, update its color property, and send it back to Speckle
        element = client.object.get(stream_id, element_id)
        element["color"] = {"r": 255, "g": 0, "b": 0}  # Set color to red

        # Update the element back to Speckle
        client.object.update(stream_id, element_id, element)
