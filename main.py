from specklepy.api.client import SpeckleClient
from speckle_automate import AutomationContext, execute_automate_function, AutomationStatus
from ClashFunctions.element import getElement, pymeshLocation
from ClashFunctions.clashDetect import clashDetection, storeResults
from ClashFunctions.colorUpdate import updateColor

def automate_function(automate_context: AutomationContext) -> None:
    """Main function to perform clash detection using Speckle Automate context."""

    # Access the stream ID from the automation context
    stream_id = automate_context.stream_id  # Use stream_id directly if available
    version_root_object = automate_context.receive_version()

    # Initialize the Speckle client using the token provided in the GitHub Secrets
    speckle_token = automate_context.token  # Automate provides the token
    speckle_server_url = automate_context.server_url  # Automate provides the server URL
    client = SpeckleClient(host=speckle_server_url)
    client.authenticate(speckle_token)

    try:
        # Set the initial status to "RUNNING" if it's not already set
        if automate_context.status != AutomationStatus.RUNNING:
            automate_context.report_run_status(status=AutomationStatus.RUNNING)

        # Retrieve element data
        branch_name = "main"  # You can change this if needed
        element_ids = getElement(client, stream_id, branch_name)
        element_data = pymeshLocation(client, stream_id, element_ids)

        # Perform clash detection
        clash_data = clashDetection(element_data)

        if clash_data["clash_count"] > 0:
            # Attach clash error details to the context
            automate_context.attach_error_to_objects(
                category="Clash Detection",
                object_ids=[pair for pair in clash_data["clashes"]],
                message="Detected clashes between elements."
            )

            # Store clash results in a file (optional)
            storeResults(clash_data)

            # Update color of clashing elements to red
            updateColor(client, stream_id, clash_data["clashes"], automate_context)

            # Mark the automation run as failed due to detected clashes
            automate_context.mark_run_failed(f"Automation failed: Found {clash_data['clash_count']} clashes.")
        else:
            # Mark as successful if no clashes are detected
            automate_context.mark_run_success("No clashes detected.")
    
    except Exception as e:
        # If an error occurs, mark the run as failed and log the error
        automate_context.mark_run_failed(f"Automation failed due to an error: {str(e)}")

if __name__ == "__main__":
    execute_automate_function(automate_function)
