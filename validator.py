class ReceiptValidator:
    """Validates verified GCON execution receipts."""

    def __init__(self):
        pass

    def validate_receipt_id(self, receipt):
        """Validate that the receipt contains a receipt ID."""

        if receipt.get("receipt_id"):
            return True, "Receipt ID present"

        return False, "Receipt ID missing"

    def validate_job_id(self, receipt):
        """Validate that the receipt contains a job ID."""

        if receipt.get("job_id"):
            return True, "Job ID present"

        return False, "Job ID missing"

    def validate_agent_id(self, receipt):
        """Validate that the receipt contains an agent ID."""

        if receipt.get("agent_id"):
            return True, "Agent ID present"

        return False, "Agent ID missing"

    def validate_proof(self, receipt):
        """Validate that the receipt contains a proof."""

        proof = receipt.get("proof")

        if proof is None:
            return False, "Proof missing"

        if not isinstance(proof, dict):
            return False, "Proof is invalid"

        return True, "Proof present"

    def validate(self, receipt):
        """
        Validate a receipt and return a validation report.
        """

        report = {
            "valid": True,
            "checks": []
        }

        checks = [
            ("Receipt ID", self.validate_receipt_id),
            ("Job ID", self.validate_job_id),
            ("Agent ID", self.validate_agent_id),
            ("Proof", self.validate_proof),
        ]

        for name, check in checks:
            passed, message = check(receipt)

            report["checks"].append({
                "name": name,
                "passed": passed,
                "message": message
            })

            if not passed:
                report["valid"] = False

        return report