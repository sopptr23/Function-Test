import pymesh

# Function to retrieve element IDs from Speckle
def getElement(client, stream_id, branch_name):
    commit = client.branch.get(stream_id, branch_name).commits.items[0]
    commit_id = commit.id

    # Retrieve object data associated with the commit
    element_ids = []
    elements = client.object.get(stream_id, commit_id)
    for element in elements:
        element_ids.append(element.id)
    return element_ids

# Function to convert element IDs into PyMesh objects and get location data
def pymeshLocation(client, stream_id, element_ids):
    element_data = []
    for element_id in element_ids:
        mesh_data = client.object.get(stream_id, element_id)
        vertices = mesh_data.get("vertices")
        faces = mesh_data.get("faces")
        pymesh_obj = pymesh.form_mesh(vertices, faces)
        
        # Store the pymesh object and element ID in a dictionary
        element_data.append({"element_id": element_id, "pymesh": pymesh_obj})
    
    return element_data
