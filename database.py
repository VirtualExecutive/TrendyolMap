import mysql.connector
from log import Log
import traceback
import time


class Database():
    Log:Log
    host:str
    user:str
    password:str
    database:str

    minerName=""
    isConnected = False
    
    cursor=None

    def __init__(self) -> None:
        pass

    def Connect(self, check=True):
        if self.isConnected and check:
            return
        self.Log.Write("DEBUG","Database","DatabaseConnecting",self.minerName,"Bağlantı kuruluyor.")
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                self.isConnected=True
                self.cursor = self.connection.cursor()
                self.Log.Write("DEBUG","Database","DatabaseConnected",self.minerName,"Bağlantı kuruldu.")
                                
        except mysql.connector.Error as err:
            self.Log.Write("ERROR","Database","DatabaseConnectError",self.minerName,"Bağlantı kurulamadı.","\nERROR: "+traceback.format_exc())

    def Disconnect(self):
        self.cursor.close()
        self.connection.close()
        self.isConnected=False
        self.Log.Write("DEBUG","Database","DatabaseDisconnected",self.minerName,"Bağlantı sonlandırıldı.")
    
    def Execute(self, cmd,*args,**kargs):
        self.Log.Write("DEBUG", "Database", "DatabaseExecuteUsed", self.minerName, "Execute: " + cmd)
        rows = None
    
        while type(rows)==type(None):
            try:
                self.cursor.execute(cmd,*args,**kargs)

                if self.isCommitNeeded(cmd):
                    self.connection.commit()

                rows = self.cursor.fetchall()
                self.Log.Write("DEBUG", "Database", "DatabaseExecuteResultCount", self.minerName,"Execute sonuç sayısı: " + str(len(rows)))
                    
               
            
            except mysql.connector.errors.IntegrityError as e:
                self.Log.Write("ERROR", "Database", "DatabaseExecuteIntegrityError", self.minerName, "ERROR")
                raise e

            except mysql.connector.errors.InterfaceError as e:
                self.Log.Write("ERROR", "Database", "DatabaseExecuteFetchError", self.minerName, "Sorgu yürütülürken hata oluştu. Fetch hatası verdi.")

            except mysql.connector.errors.ProgrammingError as e:
                self.Log.Write("ERROR", "Database", "DatabaseExecuteProgrammingError", self.minerName, "Sorgu yürütülürken hata oluştu. Programming hatası verdi.\n"+ traceback.format_exc())                try:
                    self.cursor = self.connection.cursor()
                except:
                    if not self.connection.is_connected():
                        time.sleep(1)
                        self.Disconnect()
                        self.Connect()

            except mysql.connector.errors.OperationalError as e:
                self.Log.Write("ERROR", "Database", "DatabaseExecuteOperationalError", self.minerName, "Sorgu yürütülürken hata oluştu. ","\nERROR: " + traceback.format_exc())
                try:
                    self.cursor = self.connection.cursor()
                except:
                    if not self.connection.is_connected():
                        time.sleep(1)
                        self.Disconnect()
                        self.Connect()

            except Exception as e:
                self.Log.Write("ERROR", "Database", "DatabaseExecuteError", self.minerName, "Sorgu yürütülürken hata oluştu.","\nERROR: " + traceback.format_exc())
                
            
        return rows
        
    def ExecuteMany(self, cmd,*args, **kargs):
        self.Log.Write("DEBUG", "Database", "DatabaseExecuteManyUsed", self.minerName, "ExecuteMany: " + cmd)
        try:
            self.cursor.executemany(cmd,*args,**kargs)

            if self.isCommitNeeded(cmd):
                self.connection.commit()

            rows = self.cursor.fetchall()
            self.Log.Write("DEBUG", "Database", "DatabaseExecuteManyResultCount", self.minerName,"ExecuteMany sonuç sayısı: " + str(len(rows)))

            return rows
        
        except mysql.connector.errors.IntegrityError as e:
            self.Log.Write("ERROR", "Database", "DatabaseExecuteIntegrityError", self.minerName, "ERROR")
            raise e
        
        except mysql.connector.errors.InterfaceError as e:
            self.Log.Write("ERROR", "Database", "DatabaseExecuteManyFetchError", self.minerName, "Sorgu yürütülürken hata oluştu. Fetch hatası verdi.")

        except Exception as e:
            self.Log.Write("ERROR", "Database", "DatabaseExecuteManyError", self.minerName, "Sorgu yürütülürken hata oluştu.","\nERROR: " + traceback.format_exc())
            raise e
        
    def isCommitNeeded(self,cmd:str):
            keywords = ["INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME"]
            for keyword in keywords:
                if keyword in cmd.upper():
                    return True
            return False
            

