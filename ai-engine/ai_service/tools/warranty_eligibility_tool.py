# Warranty Eligibility Tool
# This tool checks if a product is still under warranty based on its purchase date and the warranty period.
class InMemoryWarrantyEligibilityTool:

    def execute(self, product_id: str) -> dict:
        return {
            "product_id": product_id,
            "under_warranty": False,
            "months_since_purchase": 30,
            "coverage_limit_months": 24,
        }