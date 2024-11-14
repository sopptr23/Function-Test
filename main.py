import os
from dotenv import load_dotenv
from speckle_automate import AutomateBase, AutomationContext, execute_automate_function
from ClashFunctions.element import getElement, pymeshLocation
from ClashFunctions.clashDetect import clashDetection, storeResults
from ClashFunctions.colorUpdate import updateColor
from specklepy.api.client import SpeckleClient

# Load environment variables from .env
load_dotenv()

# Retrieve secrets and settings from environment variables
SPECKLE_TOKEN = os.getenv("SPECKLE_TOKEN")
SPECKLE_SERVER_URL = os.getenv("SPECKLE_SERVER_URL")
SPECKLE_PROJECT_ID = os.getenv("SPECKLE_PROJECT_ID")
SPECKLE_AUTOMATION_ID = os.getenv("SPECKLE_AUTOMATION_ID")

# Initialize Speckle client with the token and server URL
client = SpeckleClient(host=SPECKLE_SERVER_URL)
client.authenticate(SPECKLE_TOKEN)

class FunctionInputs(AutomateBase):
    """Function inputs for Speckle automation."""
    # Define additional inputs as needed, based on automation requirements

def automate_function(automate_context: AutomationContext, function_inputs: FunctionInputs) -> None:
    """Main function to perform clash detection and handle Speckle automation."""
    # Use the project ID as stream ID and specify branch name
    stream_id = SPECKLE_PROJECT_ID
    branch_name = "main"  # Adjust branch name as necessary

    # Step 1: Retrieve element IDs
    element_ids = getElement(client, stream_id, branch_name)
    # Step 2: Retrieve PyMesh data for each element
    element_data = pymeshLocation(client, stream_id, element_ids)

    # Step 3: Perform clash detect  ion
    clash_data = clashDetection(element_data)
    
    if clash_data["clash_count"] > 0:
        # Attach clash error details to the context
        automate_context.attach_error_to_objects(
            category="Clash Detection",
            object_ids=[pair for pair in clash_data["clashes"]],
            message="Detected clashes between elements.",
        )
        
        # Store clash results in a file
        storeResults(clash_data)

        # Step 4: Update color of clashing elements to red
        updateColor(client, stream_id, clash_data["clashes"], automate_context)

        # Mark the automation run as failed due to detected clashes
        automate_context.mark_run_failed(f"Automation failed: Found {clash_data['clash_count']} clashes.")
    else:
        # Mark as successful if no clashes are detected
        automate_context.mark_run_success("No clashes detected.")

if __name__ == "__main__":
    execute_automate_function(automate_function, FunctionInputs)
