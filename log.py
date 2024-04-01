
import datetime
import os
import json

@staticmethod
class Log():
    filename:str
    logsFolder="logs"

    settingsFile="settings.json"
    settings={}


    def __init__(self) -> None:
        self.filename =f"{self.GetCurrentDate('%Y%m%d%H%M%S')}.log"
        self.IfNotExistsFolderCreateLogsFolder()
        self.IfNotExistsFileCreateSettingsFile()
        self.ReadSettingsFile()
 
    def Write(self, *node):
        self.ReadSettingsFile()
        self.AddToSettings(*node[:3])
        if self.GetPermitFromSettings(*node[:3]):
            with self.OpenFile("a") as f:
                f.write(f'{self.GetCurrentDate("%Y.%m.%d %H:%M:%S.%f")} | {" | ".join(node)}\n')

    def OpenFile(self, mode,encoding="utf-8"):
        return open(os.path.join(self.logsFolder,self.filename),mode,encoding=encoding)
    
    def GetCurrentDate(self, format):
        return datetime.datetime.now().strftime(format)
    
    def IfNotExistsFolderCreateLogsFolder(self):
        if not os.path.exists(self.logsFolder):
            os.mkdir(self.logsFolder)

    def IfNotExistsFileCreateSettingsFile(self):
        try:
            with open(self.settingsFile,"r"):
                pass
        except FileNotFoundError:
            with open(self.settingsFile,"w") as f:
                json.dump(self.settings, f)

    def ReadSettingsFile(self):
        try:
            with open(self.settingsFile,"r",encoding="utf-8") as f:
                    self.settings = json.load(f)
        except:
            pass

    def WriteSettingsFile(self):
        with open(self.settingsFile,"w",encoding="utf-8") as f:
            json.dump(self.settings,f,indent=4)

    def AddToSettings(self,*states):
        statesDict = self.settings
        for state in states[:2]:
            if state  not in statesDict.keys():
                statesDict[state] = {
                    "all":True
                }

            statesDict = statesDict[state]
        
        if states[2] not in statesDict.keys():
            statesDict[states[2]] = True
            self.WriteSettingsFile()

    def GetPermitFromSettings(self, *states):
        statesDict = self.settings
        for state in states[:2]:
            if not statesDict[state]["all"]:
                return False
            else:
                statesDict = statesDict[state]
        return statesDict[states[2]]
            
