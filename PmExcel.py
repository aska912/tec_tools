
import OpenPyExcel
import PmCommon
import copy
from Logger import (dbgprint, logprint)

SHEET_TITLE = ("Export Time", "Card Name", "Port", "Group", "Bin Start Time", "Bin Status", "Interval", "Bin Unit")

exportime_index = SHEET_TITLE.index("Export Time")
cardname_index  = SHEET_TITLE.index("Card Name")
port_index      = SHEET_TITLE.index("Port")
group_index     = SHEET_TITLE.index("Group")
startime_index  = SHEET_TITLE.index("Bin Start Time")
binstatus_index = SHEET_TITLE.index("Bin Status")
interval_index  = SHEET_TITLE.index("Interval")
binunit_index   = SHEET_TITLE.index("Bin Unit")


SHEET_TITLE_COL_DICT = {exportime_index: "A",   \
                        cardname_index:  "B",   \
                        port_index:      "C",   \
                        group_index:     "D",   \
                        startime_index:  "E",   \
                        binstatus_index: "F",   \
                        interval_index:  "G",   \
                        binunit_index:   "H"}

TITLE_ROW = 1
PM_PARAM_TITLE_COLUMN = len(SHEET_TITLE) + 1
PM_RECORD_FIRST_ROW = 2




class PmExcel():
    def __init__(self, filename):
        self.excel_filename = filename
        self.sheet_list = []
        self.invalid_index = -1
        self._pmexcel = OpenPyExcel.OpenPyExcel(self.excel_filename)
        
    
    def OpenWorkbook(self):
        if not self._pmexcel.load_workbook():
            logprint.warning("Can't open %s\n"%self.excel_filename)
            return False
        else:
            return True
        
        
    def GetPmGrpSheetName(self, group, interval):
        sheetname = "%s-%s"%(group, PmCommon.BinInterval().MapIntervalToString(interval) )
        return sheetname
        
    
    def OpenPmGrpSheet(self, group, interval):
        if interval == PmCommon.BinInterval().raw:
            return False
        sheetname = self.GetPmGrpSheetName(group, interval)
        if sheetname in self.GetSheets():
            return self._pmexcel.open_sheet(sheetname)
        else:
            return self.AddPmGrpSheet(group, interval)
        
        
    def AddPmGrpSheet(self, group, interval):
        sheetname = self.GetPmGrpSheetName(group, interval)
        if not self._pmexcel.add_sheet(sheetname):
            logprint.warning("Can't add %s into %s\n"%(sheetname, self.excel_filename))
            return False
        if not self.InitGroupSheet(group, sheetname): 
            logprint.warning("Can't init %s\n"%(sheetname))
            return False
        if not self._pmexcel.open_sheet(sheetname): 
            logprint.warning("Can't open %s\n"%(sheetname))
            return False
        return True
        

    def InitGroupSheet(self, group, sheetname):
        grp = group.upper()
        if not self._pmexcel.open_sheet(sheetname):
            logprint.warning("Can't open %s of %s\n"%(sheetname, self.excel_filename))
            return False
        
        for title_index in SHEET_TITLE_COL_DICT.keys():
            self._pmexcel.write_cell_by_coordinate('%s%s'%(SHEET_TITLE_COL_DICT[title_index], TITLE_ROW),\
                                                   SHEET_TITLE[title_index])
            
        col = PM_PARAM_TITLE_COLUMN
        row = TITLE_ROW
        if not grp in PmCommon.PM_GROUP_MAP_PM_PARAM.keys(): return False
        for param in PmCommon.PM_GROUP_MAP_PM_PARAM[grp]:
            self._pmexcel.write_cell(row, col, param)
            col += 1
        return True
        
            
    def GetOpenedSheet(self):
        pass

    def GetSheets(self):
        return self._pmexcel.get_sheet_names()
    
    
    def GetRows(self):
        return self._pmexcel.get_rows()
    
        
    def GetColumns(self):
        return self._pmexcel.get_columns()
        
        
    def OpenGroupSheet(self, group):
        sheet_name = group
        if not sheet_name in self._pmexcel.get_sheet_names():
            if not self.AddSheet(sheet_name):
                return False
            else:
                self.InitGroupSheet(sheet_name)
                
        self._pmexcel.open_sheet(sheet_name)
    
        
    def AppendPmData(self, pmbin_obj=None, exportime=""):
        if pmbin_obj is None:
            return False
        
        pmbin = copy.deepcopy(pmbin_obj)
        row = self.GetRows() + 1
        grp = pmbin.group
        
        if grp == "OPOCHIN" or grp == "OPOCHOUT":
            return self.AppendOpoChPmData(pmbin_obj, exportime)
            
        
        coordinate = self._get_coordinate_for_title("Export Time", row)
        self.WriteDataByCoordinate(coordinate, exportime)
        
        coordinate = self._get_coordinate_for_title("Port", row)
        self.WriteDataByCoordinate(coordinate, pmbin.port)
        
        coordinate = self._get_coordinate_for_title("Group", row)
        self.WriteDataByCoordinate(coordinate, pmbin.group)
        
        coordinate = self._get_coordinate_for_title("Bin Start Time", row)
        if not pmbin.nodata_reason == PmCommon.UNASSIG_PORT_STR:
            self.WriteDataByCoordinate(coordinate, pmbin.startime)
        else:
            self.WriteDataByCoordinate(coordinate, pmbin.nodata_reason)
            return True
        
        coordinate = self._get_coordinate_for_title("Bin Status", row)
        self.WriteDataByCoordinate(coordinate, pmbin.status)
        
        coordinate = self._get_coordinate_for_title("Interval", row)
        self.WriteDataByCoordinate(coordinate, pmbin.interval)
        
        coordinate = self._get_coordinate_for_title("Bin Unit", row)
        self.WriteDataByCoordinate(coordinate, pmbin.unit)
        
        col = PM_PARAM_TITLE_COLUMN
        if not grp in PmCommon.PM_GROUP_MAP_PM_PARAM.keys():
            return False
        for param_name in PmCommon.PM_GROUP_MAP_PM_PARAM[grp]:
            param_value = pmbin.GetBinData(param_name)
            self._pmexcel.write_cell(row, col, param_value)
            col += 1
        return True
            
            
    def AppendOpoChPmData(self, pmbin_obj=None, exportime=""):
        if pmbin_obj is None:
            return False
        
        pmbin = copy.deepcopy(pmbin_obj)
        row = self.GetRows() + 1
        grp = pmbin.group
        
        channels = pmbin.data.GetChannels()
        if len(channels): 
            channels.sort()
        else:
            return False
        
        for ch in channels:
            coordinate = self._get_coordinate_for_title("Export Time", row)
            self.WriteDataByCoordinate(coordinate, exportime)
            
            coordinate = self._get_coordinate_for_title("Port", row)
            self.WriteDataByCoordinate(coordinate, "%s-%s"%(pmbin.port, ch))
            
            coordinate = self._get_coordinate_for_title("Group", row)
            self.WriteDataByCoordinate(coordinate, pmbin.group)
            
            coordinate = self._get_coordinate_for_title("Bin Start Time", row)
            if not pmbin.nodata_reason == PmCommon.UNASSIG_PORT_STR:
                self.WriteDataByCoordinate(coordinate, pmbin.data.GetStartTime(ch))
            else:
                self.WriteDataByCoordinate(coordinate, pmbin.nodata_reason)
                return True
            
            coordinate = self._get_coordinate_for_title("Bin Status", row)
            self.WriteDataByCoordinate(coordinate, pmbin.data.GetBinStatus(ch))
            
            coordinate = self._get_coordinate_for_title("Interval", row)
            self.WriteDataByCoordinate(coordinate, pmbin.interval)
            
            coordinate = self._get_coordinate_for_title("Bin Unit", row)
            self.WriteDataByCoordinate(coordinate, pmbin.unit)
            
            col = PM_PARAM_TITLE_COLUMN
            if not grp in PmCommon.PM_GROUP_MAP_PM_PARAM.keys():
                return False
            for param_name in PmCommon.PM_GROUP_MAP_PM_PARAM[grp]:
                param_value = pmbin.data.Read(ch, param_name)
                self._pmexcel.write_cell(row, col, param_value)
                col += 1
            row += 1
        return True

    def WriteDataByCoordinate(self, coordinate, data):
        try:
            self._pmexcel.write_cell_by_coordinate(coordinate, data)
            return True
        except:
            return False
        
    
    def CloseWithSave(self):
        self._pmexcel.del_sheet("Sheet")
        self._pmexcel.close_save()
        
        
    def StrMapIndex(self, param_list, param_name):
        """
        Return the index of name string
        """
        if param_name in param_list:
            return param_list.index(param_name)
        else:
            return self.invalid_index
        
        
    def IndexMapStr(self, param_list, param_index):
        if param_index == self.invalid_index or \
           param_index >= len(param_list):
            return ""
        else:
            return param_list[param_index]
        
    
    def _get_ordinate_name_for_title(self, title_name):
        index = self.StrMapIndex(SHEET_TITLE, title_name)
        return SHEET_TITLE_COL_DICT[index]
    
    
    def _get_coordinate_for_title(self, title_name, row):
        ordinate_name = self._get_ordinate_name_for_title(title_name)
        return '%s%s'%(ordinate_name, row)
        

            
            
            
            
            
            
            
            
            
            
            
            
            
            
    