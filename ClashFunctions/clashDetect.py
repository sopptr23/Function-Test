# Function to determine if two meshes are clashing based on bounding boxes or proximity
def is_clashing(mesh_a, mesh_b, tolerance=0.01):
    """
    Check if two PyMesh objects are clashing.
    This example uses bounding boxes with an optional tolerance to detect proximity-based clashes.
    """
    bbox_a_min, bbox_a_max = mesh_a.bbox[:3], mesh_a.bbox[3:]
    bbox_b_min, bbox_b_max = mesh_b.bbox[:3], mesh_b.bbox[3:]
    
    # Check for overlap in all three dimensions with tolerance
    clash_x = (bbox_a_min[0] <= bbox_b_max[0] + tolerance) and (bbox_a_max[0] >= bbox_b_min[0] - tolerance)
    clash_y = (bbox_a_min[1] <= bbox_b_max[1] + tolerance) and (bbox_a_max[1] >= bbox_b_min[1] - tolerance)
    clash_z = (bbox_a_min[2] <= bbox_b_max[2] + tolerance) and (bbox_a_max[2] >= bbox_b_min[2] - tolerance)
    
    return clash_x and clash_y and clash_z

# Function to perform clash detection on a list of PyMesh objects
def clashDetection(element_data):
    """
    Takes a list of elements with 'element_id' and 'pymesh' as keys.
    Returns a dictionary with clash counts and clashing pairs.
    """
    clashes = []
    clash_count = 0
    num_elements = len(element_data)

    # Nested loop to compare each element with every other element
    for i in range(num_elements):
        for j in range(i + 1, num_elements):
            element_a = element_data[i]
            element_b = element_data[j]
            
            # Check if the two elements are clashing
            if is_clashing(element_a['pymesh'], element_b['pymesh']):
                clash_count += 1
                clashes.append((element_a['element_id'], element_b['element_id']))

    return {"clash_count": clash_count, "clashes": clashes}

# Function to display or store the clash results in a suitable format
def storeResults(clash_data, output_file="clash_results.txt"):
    """
    Stores clash results in a file or database.
    """
    with open(output_file, "w") as f:
        f.write(f"Total Clashes: {clash_data['clash_count']}\n")
        f.write("Clashing Pairs:\n")
        for pair in clash_data["clashes"]:
            f.write(f"{pair[0]} clashes with {pair[1]}\n")
    print(f"Clash results stored in {output_file}")