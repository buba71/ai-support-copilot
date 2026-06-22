from ai_service.tools.base_tool import BaseTool

class CustomerHistoryTool(BaseTool):

    def execute(self, customer_id: str):

        return {
            "customer_id": customer_id,
            "tickets_count": 12,
            "vip": True,
            "last_ticket_days": 3,
        }