class Base_Vendor_Interface:
    """SDK 標準介面，確保五大廠商邏輯能直接對接系統核心"""
    def compute_matrix(self, payload):
        """強制實作：矩陣運算邏輯"""
        raise NotImplementedError("實體運算節點未實作")