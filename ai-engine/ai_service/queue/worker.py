from ai_service.service_factory import get_ticket_pipeline
from ai_service.queue.retryableJobError import RetryableJobError
from ai_service.queue.nonRetryableJobError import NonRetryableJobError

pipeline = get_ticket_pipeline()

def process_ticket(ticket_text: str):

    result = pipeline.run(ticket_text)

    if "error" in result:
        error_message = result["error"]

        if "Invalid response from LLM client - response was not valid JSON" in error_message:
            raise NonRetryableJobError(error_message)
        else:
            raise RetryableJobError(error_message)

    return result

 
