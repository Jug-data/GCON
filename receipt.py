"""
GCON Receipt - Execution receipt data structures and storage.

The receipt system:
1. Stores execution proofs
2. Manages receipt lifecycle
3. Provides receipt retrieval
4. Validates receipt authenticity
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ReceiptManager:
    """Manages execution receipts."""
    
    def __init__(self, storage_dir: str = "./receipts"):
        """
        Initialize ReceiptManager.
        
        Args:
            storage_dir: Directory to store receipt files
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
        logger.info(f"ReceiptManager initialized with storage: {storage_dir}")
    
    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def save_receipt(self, receipt: Dict[str, Any]) -> bool:
        """
        Save receipt to storage.
        
        Args:
            receipt: Receipt dictionary to save
            
        Returns:
            True if successful
        """
        try:
            receipt_id = receipt.get("receipt_id", "unknown")
            filepath = os.path.join(self.storage_dir, f"{receipt_id}.json")
            
            with open(filepath, 'w') as f:
                json.dump(receipt, f, indent=2)
            
            logger.info(f"Receipt saved: {receipt_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save receipt: {e}")
            return False
    
    def load_receipt(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        """
        Load receipt from storage.
        
        Args:
            receipt_id: Receipt identifier
            
        Returns:
            Receipt dictionary or None if not found
        """
        try:
            filepath = os.path.join(self.storage_dir, f"{receipt_id}.json")
            if not os.path.exists(filepath):
                logger.warning(f"Receipt not found: {receipt_id}")
                return None
            
            with open(filepath, 'r') as f:
                receipt = json.load(f)
            
            logger.info(f"Receipt loaded: {receipt_id}")
            return receipt
        except Exception as e:
            logger.error(f"Failed to load receipt {receipt_id}: {e}")
            return None
    
    def list_receipts(self, job_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all receipts, optionally filtered by job_id.
        
        Args:
            job_id: Optional job identifier to filter by
            
        Returns:
            List of receipt dictionaries
        """
        receipts = []
        try:
            for filename in os.listdir(self.storage_dir):
                if not filename.endswith('.json'):
                    continue
                
                filepath = os.path.join(self.storage_dir, filename)
                with open(filepath, 'r') as f:
                    receipt = json.load(f)
                
                if job_id is None or receipt.get("job_id") == job_id:
                    receipts.append(receipt)
            
            logger.info(f"Listed {len(receipts)} receipts")
            return receipts
        except Exception as e:
            logger.error(f"Failed to list receipts: {e}")
            return []
    
    def delete_receipt(self, receipt_id: str) -> bool:
        """
        Delete receipt from storage.
        
        Args:
            receipt_id: Receipt identifier
            
        Returns:
            True if successful
        """
        try:
            filepath = os.path.join(self.storage_dir, f"{receipt_id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Receipt deleted: {receipt_id}")
                return True
            else:
                logger.warning(f"Receipt not found for deletion: {receipt_id}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete receipt {receipt_id}: {e}")
            return False


class ReceiptFormatter:
    """Formats receipts for display and export."""
    
    @staticmethod
    def to_json_string(receipt: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert receipt to JSON string.
        
        Args:
            receipt: Receipt dictionary
            pretty: If True, use pretty printing
            
        Returns:
            JSON string representation
        """
        if pretty:
            return json.dumps(receipt, indent=2)
        else:
            return json.dumps(receipt)
    
    @staticmethod
    def to_summary(receipt: Dict[str, Any]) -> str:
        """
        Create human-readable summary of receipt.
        
        Args:
            receipt: Receipt dictionary
            
        Returns:
            Formatted summary string
        """
        summary = f"""
╔════════════════════════════════════════════════════════���═══╗
║                  GCON EXECUTION RECEIPT                    ║
╠════════════════════════════════════════════════════════════╣
║ Receipt ID:      {receipt.get("receipt_id", "N/A"):<38} ║
║ Job ID:          {receipt.get("job_id", "N/A"):<38} ║
║ Status:          {receipt.get("status", "N/A"):<38} ║
║ Issued At:       {receipt.get("issued_at", "N/A"):<38} ║
╠════════════════════════════════════════════════════════════╣
║ Input Hash:      {receipt.get("input_hash", "N/A")[:40]:<40} ║
║ Output Hash:     {receipt.get("output_hash", "N/A")[:40]:<40} ║
╠════════════════════════════════════════════════════════════╣
║ GPU:             {receipt.get("proof", {}).get("gpu", "N/A"):<38} ║
║ Runtime:         {str(receipt.get("proof", {}).get("runtime_seconds", "N/A")) + "s":<38} ║
║ Verified:        {str(receipt.get("proof", {}).get("verified", False)):<38} ║
╚════════════════════════════════════════════════════════════╝
"""
        return summary.strip()
    
    @staticmethod
    def to_csv(receipts: List[Dict[str, Any]]) -> str:
        """
        Convert receipts to CSV format.
        
        Args:
            receipts: List of receipt dictionaries
            
        Returns:
            CSV formatted string
        """
        if not receipts:
            return ""
        
        # Extract headers from first receipt
        headers = ["receipt_id", "job_id", "status", "gpu", "runtime_seconds", "verified", "issued_at"]
        
        lines = [".".join(headers)]
        
        for receipt in receipts:
            proof = receipt.get("proof", {})
            row = [
                receipt.get("receipt_id", ""),
                receipt.get("job_id", ""),
                receipt.get("status", ""),
                proof.get("gpu", ""),
                str(proof.get("runtime_seconds", "")),
                str(proof.get("verified", "")),
                receipt.get("issued_at", "")
            ]
            lines.append(",".join(row))
        
        return "\
".join(lines)