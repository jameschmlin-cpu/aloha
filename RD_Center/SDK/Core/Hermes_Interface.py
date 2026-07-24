import sqlite3

class HermesInterface:

    def sync_data(self):

        with sqlite3.connect(r'C:\Genesis\Genesis_Core\Data\Unified_Empire_Memory.db') as conn:

            return conn.execute('SELECT 1').fetchone() is not None