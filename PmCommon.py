
import re, copy
import CliRegProcessor
from Logger import (dbgprint, logprint)

CALSS = ["PmProcessor"]
CONST_PM_GROUP = ["PM_GROUP_TYPE_LIST", "PM_GROUP_MAP_PM_PARAM"]
CONST_ERROR_STRING = ["UNASSIG_PORT_STR"]
CONST_CLI_PARAM_LIST = ["OPIN_PM_CLI_PARAM_LIST",  "OPOUT_PM_CLI_PARAM_LIST",     \
                        "OPR_PM_CLI_PARAM_LIST",   "OPT_PM_CLI_PARAM_LIST",       \
                        "SONET_PM_CLI_PARAM_LIST", "DW_PM_CLI_PARAM_LIST",        \
                        "PCS_PM_CLI_PARAM_LIST",   "ETHERNET_PM_CLI_PARAM_LIST"   \
                        "SDH_PM_CLI_PARAM_LIST",   "OPOCH_PM_CLI_PARAM_LIST"      \
                        "INTERFACE_PM_CLI_PARAM_LIST"]

__all__ = CONST_CLI_PARAM_LIST + CONST_PM_GROUP + CONST_ERROR_STRING + CALSS


INVALID_LIST_INDEX = -1

OPOCH_PM_CLI_PARAM_LIST = ("Min Power",       \
                           "Max Power",       \
                           "Average Power")


OPIN_PM_CLI_PARAM_LIST = ("OPIN Min (dBm)", \
                          "OPIN Max (dBm)", \
                          "OPIN Average (dBm)")


OPOUT_PM_CLI_PARAM_LIST = ("OPOUT Min (dBm)", \
                           "OPOUT Max (dBm)", \
                           "OPOUT Average (dBm)")


OPR_PM_CLI_PARAM_LIST = ("OPR Min (dBm)", \
                         "OPR Max (dBm)", \
                         "OPR Average (dBm)")


OPT_PM_CLI_PARAM_LIST = ("OPT Min (dBm)", \
                         "OPT Max (dBm)", \
                         "OPT Average (dBm)")


SONET_PM_CLI_PARAM_LIST = ("Rx CVS",            \
                           "Rx ESS",            \
                           "Rx SESS",           \
                           "Rx SEFSS",          \
                           "Rx CVL",            \
                           "Rx ESL",            \
                           "Rx SESL",           \
                           "Rx UASL",           \
                           "Rx Far-End  CVL",   \
                           "Rx Far-End  ESL",   \
                           "Rx Far-End  SESL",  \
                           "Rx Far-End  UASL",  \
                           )


SDH_PM_CLI_PARAM_LIST = ("Rx RSEB",     \
                         "Rx RSES",     \
                         "Rx RSSES",    \
                         "Rx RSUAS")


PCS_PM_CLI_PARAM_LIST = ("Rx CV_PCS",     \
                         "Rx ES_PCS",     \
                         "Rx SES_PCS",    \
                         "Rx SEFS_PCS",   \
                         "Tx CV_PCS",     \
                         "Tx ES_PCS",     \
                         "Tx SES_PCS",    \
                         "Tx SEFS_PCS")


DW_PM_CLI_PARAM_LIST = ("Rx RS Corrected Count",                             \
                        "Rx RS Uncorrected Count",                           \
                        "Rx SMBIP8 Error Count",                             \
                        "Rx PMBIP8 Error Count",                             \
                        "Rx SM Errored Seconds",                             \
                        "Rx PM Errored Seconds",                             \
                        "Rx SM Severely Errored Seconds",                    \
                        "Rx PM Severely Errored Seconds",                    \
                        "Rx SM Unavailable Seconds",                         \
                        "Rx PM Unavailable Seconds",                         \
                        "Rx Far End OTUk Background Block Error",            \
                        "Rx Far End ODUk Background Block Error",            \
                        "Rx Far End OTUk Errored Seconds",                   \
                        "Rx Far End ODUk Errored Seconds",                   \
                        "Rx Far End OTUk Severely Errored Seconds",          \
                        "Rx Far End ODUk Severely Errored Seconds",          \
                        "Rx Far End OTUk Unavailable Seconds",               \
                        "Rx Far End ODUk Unavailable Seconds",               \
                        "Rx OTUk Backward Incoming Alignment Error Seconds", \
                        "Rx OTUk Incoming Alignment Errored Seconds",        \
                        "Rx BER to be calculated from FEC-EC and FEC-UBC",   \
                        "Rx BER to be calculated from FEC-UBC")


ETHERNET_PM_CLI_PARAM_LIST = ( "Rx Drop Events",                \
                               "Rx Octets",                     \
                               "Rx Packets",                    \
                               "Rx Broadcast Packets",          \
                               "Rx Multicast Packets",          \
                               "Rx CRC Alignment Errors",       \
                               "Rx Undersized Packets",         \
                               "Rx Oversized Packets",          \
                               "Rx Fragments",                  \
                               "Rx Jabbers",                    \
                               "Rx Collisions",                 \
                               "Rx Packets 64 Bytes",           \
                               "Rx Packets 65 to 127 Bytes",    \
                               "Rx Packets 128 to 255 Bytes",   \
                               "Rx Packets 256 to 511 Bytes",   \
                               "Rx Packets 512 to 1023 Bytes",  \
                               "Rx Packets 1024 to 1518 Bytes", \
                               "Rx Jumbo Packets",              \
                               "Rx Packet Error Ratio",         \
                               "Tx DropEvents",                 \
                               "Tx Octets",                     \
                               "Tx Packets",                    \
                               "Tx Broadcast Packets",          \
                               "Tx Multicast Packets",          \
                               "Tx CRC Alignment Errors",       \
                               "Tx Undersized Packets",         \
                               "Tx Oversized Packets",          \
                               "Tx Fragments",                  \
                               "Tx Jabbers",                    \
                               "Tx Collisions",                 \
                               "Tx Packets 64 Bytes",           \
                               "Tx Packets 65 to 127 Bytes",    \
                               "Tx Packets 128 to 255 Bytes",   \
                               "Tx Packets 256 to 511 Bytes",   \
                               "Tx Packets 512 to 1023 Bytes",  \
                               "Tx Packets 1024 to 1518 Bytes", \
                               "Tx Jumbo Packets",              \
                               "Tx Packet Error Ratio")

INTERFACE_PM_CLI_PARAM_LIST = ( "In Octets",                \
                                "In Unicast Packets",       \
                                "In Discards",              \
                                "In Errors",                \
                                "In Unknown Protocols",     \
                                "In Multicast Packets",     \
                                "In Broadcast Packets",     \
                                "In Packets Not Classified",\
                                "Out Octets",               \
                                "Out Unicast Packets",      \
                                "Out Discards",             \
                                "Out Errors",               \
                                "Out Multicast Packets",    \
                                "Out Broadcast Packets")


OTU_PM_CLI_PARAM_LIST = ( "Rx RS Corrected Count",                          \
                          "Rx RS Uncorrected Count",                        \
                          "Rx BER to be calculated from FEC-EC and FEC-UBC",\
                          "Rx BER to be calculated from FEC-UBC",           \
                          "Rx SM BIP8 Error Count",                         \
                          "Rx SM Errored Seconds",                          \
                          "Rx SM Severely Errored Seconds",                 \
                          "Rx SM Unavailable Seconds",                      \
                          "Rx SM Incoming Alignment Error Seconds",         \
                          "Rx SM FarEnd BIP8 Error Count",                  \
                          "Rx SM FarEnd Errored Seconds",                   \
                          "Rx SM FarEnd Severely Errored Seconds",          \
                          "Rx SM FarEnd Unavailable Seconds",               \
                          "Rx SM FarEnd Incoming Alignment Error Seconds")


FOFF_PM_CLI_PARAM_LIST = ("FOFF Min (GHz)",     \
                          "FOFF Max (GHz)",     \
                          "FOFF Average (GHz)")


DGD_PM_CLI_PARAM_LIST = ("DGD Min (ps)",     \
                         "DGD Max (ps)",     \
                         "DGD Average (ps)")


CD_PM_CLI_PARAM_LIST = ("CD Min (ps/nm)",       \
                        "CD Max (ps/nm)",       \
                        "CD Average (ps/nm)")


PREFECBITS_PM_CLI_PARAM_LIST = ("PreFEC Min (bits/per-second)",     \
                                "PreFEC Max (bits/per-second)",     \
                                "PreFEC Average(bits/per-second)")


FEC_PM_CLI_PARAM_LIST = ("Rx BER to be calculated from FEC-EC and FEC-UBC",)


PREFEC_PM_CLI_PARAM_LIST = ("Rx BER to be calculated from FEC-EC and FEC-UBC",)


PM_GROUP_TYPE_LIST = ("OPR", "OPT", "OPIN", "OPOUT",    \
                      "OPOCHIN", "OPOCHOUT",            \
                      "PCS", "ETHERNET", "DW",          \
                      "SONET", "SDH", "INTERFACE",      \
                      "FOFF", "CD", "DGD", "OTU",       \
                      "PREFECBITS", "FEC", "PREFEC")


PM_GROUP_MAP_PM_PARAM = { "OPR":        OPR_PM_CLI_PARAM_LIST,       \
                          "OPT":        OPT_PM_CLI_PARAM_LIST,       \
                          "OPIN":       OPIN_PM_CLI_PARAM_LIST,      \
                          "OPOUT":      OPOUT_PM_CLI_PARAM_LIST,     \
                          "PCS":        PCS_PM_CLI_PARAM_LIST,       \
                          "ETHERNET":   ETHERNET_PM_CLI_PARAM_LIST,  \
                          "DW":         DW_PM_CLI_PARAM_LIST,        \
                          "SONET":      SONET_PM_CLI_PARAM_LIST,     \
                          "SDH":        SDH_PM_CLI_PARAM_LIST,       \
                          "OPOCHIN":    OPOCH_PM_CLI_PARAM_LIST,     \
                          "OPOCHOUT":   OPOCH_PM_CLI_PARAM_LIST,     \
                          "INTERFACE":  INTERFACE_PM_CLI_PARAM_LIST, \
                          "OTU":        OTU_PM_CLI_PARAM_LIST,       \
                          "FOFF":       FOFF_PM_CLI_PARAM_LIST,      \
                          "CD":         CD_PM_CLI_PARAM_LIST,        \
                          "DGD":        DGD_PM_CLI_PARAM_LIST,       \
                          "PREFECBITS": PREFECBITS_PM_CLI_PARAM_LIST,\
                          "FEC":        FEC_PM_CLI_PARAM_LIST,       \
                          "PREFEC":     PREFEC_PM_CLI_PARAM_LIST,    \
                        }


    

BIN_STATUS_LIST = ("Adjusted", "Complete", "DSBLD", "LONG", "NA", " ", \
                   "PRTL", "OFF", "ALL", "Not Available", "Valid")

BIN_INTERVAL_LIST = ("0", "1", "RAW")

#BIN_INTERVAL_LIST = ("15MIN", "1DAY", "RAW")


INVALID_GROUP = -1
UNKNOWN_BIN_STATUS = -1
INVALID_BIN_INTERVAL = -1
UNKNOWN_STR = "unkown"


LIMIT_NUM_15MIN_BINS = 33
LIMIT_NUM_DAY_BINS = 8
LIMIT_NUM_INTERVAL = 2
INVALID_PM_DATA = -9999
UNASSIG_PORT_STR = "Port is unassigned"
INVALID_PORT = "Invalid Port"
ERROR_CLI_CMD = "CLI Commd Error"

PARAM_NAME_COL  = 0
PARAM_VALUE_COL = 1

# No Data Reason
ERROR_CLI_CMD = "CLI Commd Error"
UNSUPPORT_GRP = "Unsupported Group"


class PmProcessor(CliRegProcessor.CliRegProcessor):
    def __init__(self):
        super(PmProcessor, self).__init__()
    
    #def Show(self, shelf, slot, port, grp_name, bin_type, bin_num=0):
    #    grp = PmGroup()
    #    grp.name = grp_name
    #    if not grp.isvalid: return None
    #    shslprt = self.shelf_slot_port(shelf, slot, port)
    #    
    #    #show interface 1/2/Line pm opochin 0 0
    #    if not bin_type == "raw":
    #        cmd = "show interface %s pm %s %s %s"%(shslprt, grp.name, bin_type, bin_num)
    #    else:
    #        cmd = "show interface %s pm %s raw"%(shslprt, grp.name)
    #    (pm_res, noerr) = self.send(cmd)
    #    if noerr is False: return None
    #    #print [pm_res]
    #    pmbin = self.Parse(pm_res)
    #    pmbin.Dump()
    #    return pmbin
    
    def Parse(self, raw_string):
        """
        PM Info Case 1:
        Group: OPOUT  Interval: 0  Bin: 0  Location: 1/4/LINE  ==> bin info
        -------------------------------------------------------------------------------
        Start Time                     : 2017/03/02 22:30:00 (UTC)
        Bin Status                     : Valid
        OPOUT Min (dBm)                :                13.01
        OPOUT Max (dBm)                :                13.03
        OPOUT Average (dBm)            :                13.02

        PM Info Case 2:
        Group: OPR  Interval: 0  Bin: 0  Location: 1/4/LINE
        -------------------------------------------------------------------------------
        Port is unassigned
        
        PM Info Case 3: raw bin
        Group: OPR  Location: 1/1/P1
        -------------------------------------------------------------------------------
        Port is unassigned
        
        """
        pm_bin = PmBin()
        raw_bin_item_nums = 2
        bin_item_nums = 4
        
        group_col = 0
        raw_bin_port_col = 1
        interval_col = 1
        unit_col = 2
        port_col = 3
        value_col = 1
        
        #print "raw string:\n", raw_string
        pm_info_str   = self.filter_line_break(raw_string)
        pm_info_list  = re.split(self.REG_SPLIT_LINE, pm_info_str, maxsplit=1)
        if len(pm_info_list) == 1 :
            if re.search(r"Error\:", pm_info_list[0]):
                pm_bin.data = None
                pm_bin.nodata_reason = ERROR_CLI_CMD
                return pm_bin
        
        bin_info_str  = self.filter_begin_or_end_enter(pm_info_list[0])
        #print "bin_info_str: ", bin_info_str
        bin_info_list = re.split(r"\s{2,}", bin_info_str)
        #print "bin_info_list: ", bin_info_list
        bin_info_item_nums = len(bin_info_list)
        if bin_info_item_nums == 0 or  bin_info_item_nums > 4:
            # process error
            logprint.warn("Can't get bin info from the PM info.")
            return 
        else:
            # [ Group: OPT,  Interval: 0,  Bin: 2,  Location: 1/2/OSC ]
            #print bin_info_list
            #get pm group name
            pm_bin.group = re.split(self.REG_COLON_SPLIT, bin_info_list[group_col])[value_col]
            if bin_info_item_nums == raw_bin_item_nums:
                # For raw Bin
                pm_bin.port   = re.split(self.REG_COLON_SPLIT, bin_info_list[raw_bin_port_col])[value_col]
                pm_bin.interval = "raw"
            elif bin_info_item_nums == bin_item_nums:
                # For 15min/1day Bin
                pm_bin.interval  = re.split(self.REG_COLON_SPLIT, bin_info_list[interval_col])[value_col]
                pm_bin.unit      = re.split(self.REG_COLON_SPLIT, bin_info_list[unit_col])[value_col]
                pm_bin.port      = re.split(self.REG_COLON_SPLIT, bin_info_list[port_col])[value_col]
        
        #Process channel bins
        if pm_bin.group == PmGroup().opochin or \
           pm_bin.group == PmGroup().opochout:
            bin_data_str  = self.filter_split_line(pm_info_list[1])
            pm_bin.data= self._parase_opoch(bin_data_str)
            return pm_bin
          
        bin_data_str  = self.filter_begin_or_end_enter(pm_info_list[1])            
        # Process "Port is unassigned" case
        if bin_data_str == UNASSIG_PORT_STR:
            pm_bin.data = None
            pm_bin.nodata_reason = UNASSIG_PORT_STR
            return pm_bin
        
        pm_bin = copy.deepcopy(self._handle_bin_data(pm_bin, bin_data_str))
        return pm_bin
    
    def _handle_bin_data(self, pmbin_obj, bin_data_str):
        if pmbin_obj is None: return None
        
        pm_bin = pmbin_obj
        if pm_bin.group == PmGroup().opr:
            pm_bin.data = self._parse_opr(bin_data_str)
        elif pm_bin.group == PmGroup().opt:
            pm_bin.data = self._parse_opt(bin_data_str)
        elif pm_bin.group == PmGroup().opin:
            pm_bin.data = self._parse_opin(bin_data_str)
        elif pm_bin.group == PmGroup().opout:
            pm_bin.data = self._parse_opout(bin_data_str)
        elif pm_bin.group == PmGroup().pcs:
            pm_bin.data = self._parse_pcs(bin_data_str)
        elif pm_bin.group == PmGroup().dw:
            bin_data_str = re.sub(self.REG_SPLIT_LINE, "", bin_data_str)
            pm_bin.data = self._parse_dw(bin_data_str)
        elif pm_bin.group == PmGroup().sonet:
            pm_bin.data = self._parse_sonet(bin_data_str)
        elif pm_bin.group == PmGroup().sdh:
            pm_bin.data = self._parse_sdh(bin_data_str)
        elif pm_bin.group == PmGroup().ethernet:
            pm_bin.data = self._parse_ethernet(bin_data_str)
        elif pm_bin.group == PmGroup().interface:
            pm_bin.data = self._parse_interface(bin_data_str)
        elif pm_bin.group == PmGroup().cd:
            pm_bin.data = self._parse_cd(bin_data_str)
        elif pm_bin.group == PmGroup().dgd:
            pm_bin.data = self._parse_dgd(bin_data_str)
        elif pm_bin.group == PmGroup().foff:
            pm_bin.data = self._parse_foff(bin_data_str)
        else:
            pm_bin.nodata_reason = UNSUPPORT_GRP
            pm_bin.data =  None
        return pm_bin
    
    def _parse_opr(self, bin_data_string):
        opr_data = OprData()
        self._parse_case_1(bin_data_string, opr_data)
        return opr_data
        
    def _parse_opt(self, bin_data_string):
        opt_data = OptData()
        self._parse_case_1(bin_data_string, opt_data)
        return opt_data
    
    def _parse_opin(self, bin_data_string):
        opin_data = OpinData()
        self._parse_case_1(bin_data_string, opin_data)
        return opin_data
    
    def _parse_opout(self, bin_data_string):
        opout_data = OpoutData()
        self._parse_case_1(bin_data_string, opout_data)
        return opout_data
    
    def _parse_pcs(self, bin_data_string):
        pcs_data = PcsData()
        self._parse_case_1(bin_data_string, pcs_data)
        return pcs_data
    
    def _parse_dw(self, bin_data_string):
        dw_data = DwData()
        self._parse_case_1(bin_data_string, dw_data)
        return dw_data
    
    def _parse_sonet(self, bin_data_string):
        sonet_data = SonetData()
        self._parse_case_1(bin_data_string, sonet_data)
        return sonet_data
    
    def _parse_sdh(self, bin_data_string):
        sdh_data = SdhData()
        self._parse_case_1(bin_data_string, sdh_data)
        return sdh_data
    
    def _parse_ethernet(self, bin_data_string):
        ethernet_data = EthernetData()
        self._parse_case_1(bin_data_string, ethernet_data)
        return ethernet_data
    
    def _parse_interface(self, bin_data_string):
        intf_data = InterfaceData()
        self._parse_case_1(bin_data_string, intf_data)
        return intf_data
    
    def _parse_cd(self, bin_data_string):
        cd_data = CdData()
        self._parse_case_1(bin_data_string, cd_data)
        return cd_data
    
    def _parse_dgd(self, bin_data_string):
        dgd_data = DgdData()
        self._parse_case_1(bin_data_string, dgd_data)
        return dgd_data
    
    def _parse_foff(self, bin_data_string):
        foff_data = FoffData()
        self._parse_case_1(bin_data_string, foff_data)
        return foff_data
    
    def _parse_otu(self, bin_data_string):
        otu_data = OtuData()
        self._parse_case_1(bin_data_string, otu_data)
        return otu_data
    
    def _parse_fec(self, bin_data_string):
        fec_data = FecData()
        self._parse_case_1(bin_data_string, fec_data)
        return fec_data
    
    def _parse_prefec(self, bin_data_string):
        prefec_data = PrefecData()
        self._parse_case_1(bin_data_string, prefec_data)
        return prefec_data
    
    def _parse_prefecbits(self, bin_data_string):
        prefecbits_data = PrefecBitsData()
        self._parse_case_1(bin_data_string, prefecbits_data)
        return prefecbits_data
    
    def _parase_opoch(self, bin_data_string):
        return self._parse_case_opchannel(bin_data_string)
    
    def _parse_case_1(self, bin_data_string, bin_data_obj):
        """
        Case 1:
        Start Time                    : 2017/03/27 00:00:00 (UTC)
        Bin Status                    : Valid
        OPR Min (dBm)                 :               -20.06
        OPR Max (dBm)                 :               -19.86
        OPR Average (dBm)             :               -19.99
        """
        bin_data_list = re.split(self.REG_ENTER, bin_data_string)
        if not len(bin_data_list): return None
        for bin_data in bin_data_list:
            if not len(bin_data): continue
            item_list  = re.split(self.REG_COLON_SPLIT, bin_data)
            #print item_list
            item_name  = self.filter_begin_or_end_space(item_list[PARAM_NAME_COL])
            item_value = self.filter_begin_or_end_space(item_list[PARAM_VALUE_COL])
            rtr = bin_data_obj.Write(item_name, item_value)
            if not rtr: return None
            
    def _parse_case_opchannel(self, bin_data_string):
        """
        Case 2:
        Start Time                    : 2017/03/27 06:00:00 (UTC)
        Bin Status                    : Valid
        Channel      Min Power       Max Power       Average Power
        -----------------------------------------------------------
        9180.000     -22.05          -21.98          -22.02
        9450.000     -22.48          -22.32          -22.40
        9575.000     -22.78          -22.71          -22.75
        9585.000     -23.71          -23.64          -23.67
        9595.000     -22.94          -22.88          -22.91
        9605.000     -22.45          -22.38          -22.41
        """
        opch_bin = OpoChBinData()
        bin_data_list = re.split(self.REG_ENTER, bin_data_string)
        ch_index = 0
        min_power_index = 1
        max_power_index = 2
        avg_power_index = 3
        opch_min_name = OPOCH_PM_CLI_PARAM_LIST[0]
        opch_max_name = OPOCH_PM_CLI_PARAM_LIST[1]
        opch_avg_name = OPOCH_PM_CLI_PARAM_LIST[2]
        startime = ""
        status = UNKNOWN_STR

        if not len(bin_data_list): return None
        for bin_data in bin_data_list:
            if not len(bin_data): continue
            if re.search(r"^\d{4}", bin_data):
                item_list  = re.split(self.REG_SPACE, bin_data)
                item_num = len(item_list)
                if item_num == 4:
                    min_power = item_list[min_power_index]
                    max_power = item_list[max_power_index]
                    avg_power = item_list[avg_power_index]               
                elif item_num > 0 and item_num < 4:
                    min_power = max_power = avg_power = INVALID_PM_DATA
                
                channel= item_list[ch_index]
                opch_bin.Write(channel, opch_min_name, min_power)
                opch_bin.Write(channel, opch_max_name, max_power)
                opch_bin.Write(channel, opch_avg_name, avg_power)
                opch_bin.SetStartTime(channel, startime)
                opch_bin.SetBinStatus(channel, status)
                    
            elif re.search(r"\s+:\s+", bin_data):
                item_list  = re.split(self.REG_COLON_SPLIT, bin_data)
                item_name  = self.filter_begin_or_end_space(item_list[PARAM_NAME_COL])
                item_value = self.filter_begin_or_end_space(item_list[PARAM_VALUE_COL])
                if item_name == opch_bin.param_startime:
                    startime = item_value
                elif item_name == opch_bin.param_binstatus:
                    status = item_value
            elif re.search(r"Channel\s+", bin_data):
                continue
        return opch_bin
    
    
#------------------------------------------------------------------------------
#
#
#
#------------------------------------------------------------------------------
class PmBin(object):
    def __init__(self):
        """
        Property: 
            group, 
            interval, 
            status, 
            unit,
            port,
            data, (BinData class)
        """
        # The unit is the collected data for the specified bin
        self.unit = 0 
        self.port = INVALID_PORT
        self.data = None
        self.nodata_reason = UNKNOWN_STR
        
        self._bingrp_obj = PmGroup()
        self._binintvl_obj = BinInterval()
        
    def GetBinData(self, param_name):
        if self.data is None:
            return INVALID_PM_DATA
        return self.data.Read(param_name)
    
    @property
    def datanums(self):
        if self.data is None: return 0
        return self.data.maxdata
        
    @property
    def startime(self):
        if self.data is not None:
            return self.data.startime
        else:
            return "No time"
        
    @property
    def status(self):
        if self.data is not None:
            return self.data.binstatus
        else:
            return " "
        
    @property
    def group(self):
        return self._bingrp_obj.name
    
    @group.setter
    def group(self, grp_name):
        self._bingrp_obj.name = grp_name
        
    @property
    def interval(self):
        return self._binintvl_obj.interval
    
    @interval.setter
    def interval(self, bin_interval):
        self._binintvl_obj.interval = bin_interval
            
    def Dump(self):
        print "Group:    ", self.group
        print "Interval: ", self.interval
        print "Bin:      ", self.unit
        print "Port:     ", self.port
        if not self.data is None:
            self.data.Dump()
        else:
            print "No data Reason: ", self.nodata_reason
        
class BinData(object):
    def __init__(self):
        self.start_time = " "
        self.bin_param_list = []
        self._binstat_obj = BinStatus()
        self.invalid_index = -1
        self.bin_data_dict = {}
        
    def Write(self, param_name, param_value):
        if param_name == self.param_startime:
            self.start_time = param_value
            return True
        elif param_name == self.param_binstatus:
            self.binstatus = param_value
            return True
            
        if not len(self.bin_param_list): return False
        param_index = self.StrMapIndex(param_name)
        if param_index == self.invalid_index: return False
        self.bin_data_dict.update( {param_index: param_value} )
        return True
    
    def Read(self, param_name):
        if not len(self.bin_param_list): return INVALID_PM_DATA
        param_index = self.StrMapIndex(param_name)
        if param_index == self.invalid_index: return INVALID_PM_DATA
        return self.bin_data_dict.get(param_index, INVALID_PM_DATA)
    
    def Dump(self):
        if not len(self.bin_param_list) or \
           not len(self.bin_data_dict):
                print "No such as data in BinData"
                return
        print "Start Time:  ", self.start_time
        print "Bin Status:  ", self.binstatus
        for param_index in self.bin_data_dict.keys():
            param_name  = self.IndexMapStr(param_index)
            param_value = self.bin_data_dict.get(param_index)
            print "%s:    %-15s"%(param_name, param_value)
        
        
    def StrMapIndex(self, param_name):
        """
        Return the index of name string
        """
        if param_name in self.bin_param_list:
            return self.bin_param_list.index(param_name)
        else:
            return self.invalid_index
        
    def IndexMapStr(self, param_index):
        if param_index == self.invalid_index or \
           param_index >= len(self.bin_param_list):
            return ""
        else:
            return self.bin_param_list[param_index]
        
    @property
    def maxdata(self):
        return len(self.bin_data_dict)
    
    @property
    def startime(self):
        return self.start_time
    
    @startime.setter
    def startime(self, start_time):
        self.start_time = start_time
    
    @property
    def binstatus(self):
        return self._binstat_obj.status
    
    @binstatus.setter
    def binstatus(self, bin_status):
        self._binstat_obj.status = bin_status
    
    @property
    def param_startime(self):
        return "Start Time"
    
    @property
    def param_binstatus(self):
        return "Bin Status"
 
 
class OpinData(BinData):
    def __init__(self):
        super(OpinData, self).__init__()
        self.bin_param_list = OPIN_PM_CLI_PARAM_LIST
        

class OpoutData(BinData):
    def __init__(self):
        super(OpoutData, self).__init__()
        self.bin_param_list = OPOUT_PM_CLI_PARAM_LIST

        
class OprData(BinData):
    def __init__(self):
        super(OprData, self).__init__()
        self.bin_param_list = OPR_PM_CLI_PARAM_LIST


class OptData(BinData):
    def __init__(self):
        super(OptData, self).__init__()
        self.bin_param_list = OPT_PM_CLI_PARAM_LIST


class SonetData(BinData):
    def __init__(self):
        super(SonetData, self).__init__()
        self.bin_param_list = SONET_PM_CLI_PARAM_LIST
        
        
class SdhData(BinData):
    def __init__(self):
        super(SdhData, self).__init__()
        self.bin_param_list = SDH_PM_CLI_PARAM_LIST


class PcsData(BinData):
    def __init__(self):
        super(PcsData, self).__init__()        
        self.bin_param_list = PCS_PM_CLI_PARAM_LIST

    
class DwData(BinData):
    def __init__(self):
        super(DwData, self).__init__()
        self.bin_param_list = DW_PM_CLI_PARAM_LIST


class InterfaceData(BinData):
    def __init__(self):
        super(InterfaceData, self).__init__()
        self.bin_param_list = INTERFACE_PM_CLI_PARAM_LIST
    
    
class EthernetData(BinData):
    def __init__(self):
        super(EthernetData, self).__init__()
        self.bin_param_list = ETHERNET_PM_CLI_PARAM_LIST
        

class CdData(BinData):
    def __init__(self):
        super(CdData, self).__init__()
        self.bin_param_list = CD_PM_CLI_PARAM_LIST
        

class FoffData(BinData):
    def __init__(self):
        super(FoffData, self).__init__()
        self.bin_param_list = FOFF_PM_CLI_PARAM_LIST


class DgdData(BinData):
    def __init__(self):
        super(DgdData, self).__init__()
        self.bin_param_list = DGD_PM_CLI_PARAM_LIST

 
class OtuData(BinData):
    def __init__(self):
        super(OtuData, self).__init__()
        self.bin_param_list = OTU_PM_CLI_PARAM_LIST
        

class FecData(BinData):
    def __init__(self):
        super(FecData, self).__init__()
        self.bin_param_list = FEC_PM_CLI_PARAM_LIST
        

class PrefecData(BinData):
    def __init__(self):
        super(PrefecData, self).__init__()
        self.bin_param_list = PREFEC_PM_CLI_PARAM_LIST
        

class PrefecBitsData(BinData):
    def __init__(self):
        super(PrefecBitsData, self).__init__()
        self.bin_param_list = PREFECBITS_PM_CLI_PARAM_LIST       


class OpoChBinData():
    def __init__(self):
        #super(OpChBinData, self).__init__()
        self._channel_bin_data = {}
        
    def Write(self, channel, param_name, param_value):
        if channel in self.GetChannels():
            self._channel_bin_data[channel].Write(param_name, param_value)
        else:
            bindata = BinData()
            bindata.bin_param_list = OPOCH_PM_CLI_PARAM_LIST
            bindata.Write(param_name, param_value)
            self._channel_bin_data.update({channel: bindata}) 
        
    def Read(self, channel, param_name):
        if channel in self.GetChannels():
            bindata = self._channel_bin_data[channel]
            if bindata is not None:
                return bindata.Read(param_name)
            
    def Dump(self):
        print self._channel_bin_data.keys()
        for ch in self._channel_bin_data.keys():
            print "Channel: ", ch
            self._channel_bin_data[ch].Dump()
        
    def GetChannels(self):
        return self._channel_bin_data.keys()
    
    def GetStartTime(self, channel):
        if channel in self.GetChannels():
            bindata = self._channel_bin_data[channel]
            if bindata is not None:
                return bindata.startime
        return ""
    
    def GetBinStatus(self, channel):
        if channel in self.GetChannels():
            bindata = self._channel_bin_data[channel]
            if bindata is not None:
                return bindata.binstatus
        return UNKNOWN_STR


    def SetBinStatus(self, channel, bin_status):
        if channel in self.GetChannels():
            bindata = self._channel_bin_data[channel]
            if bindata is not None:
                bindata.binstatus = bin_status


    def SetStartTime(self, channel, start_time):
        if channel in self.GetChannels():
            bindata = self._channel_bin_data[channel]
            if bindata is not None:
                bindata.startime = start_time
    
    @property
    def param_startime(self):
        return "Start Time"
    
    @property
    def param_binstatus(self):
        return "Bin Status"
        

class PmGroup(object):
    def __init__(self, grp_name=''):
        self.supported_grp_list = PM_GROUP_TYPE_LIST
        self._grp_id = INVALID_GROUP
                
    @property
    def name(self):
        if not self._grp_id == INVALID_GROUP:
            return self.supported_grp_list[self._grp_id]
        else:
            return UNKNOWN_STR
        
    @name.setter
    def name(self, grp_name):
        if grp_name == "Physical Code Sub Layer":
            grp_name = "PCS"
        elif grp_name == "Digital Wrapper":
            grp_name = "DW"
        elif grp_name == "OTU Stats":
            grp_name = "OTU"
        elif grp_name == "Forward Error Correction Performance Monitoring Group":
            grp_name = "FEC"
        elif grp_name == "Pre Forward Error Correction BER Performance Monitoring Group":
            grp_name = "PREFEC"
        self._grp_id = self.map_name_to_id(grp_name)
        #print "In PmGroup: grp_name: ", grp_name, "grp_id: ", self._grp_id
            
    @property
    def isvalid(self):
        if not self._grp_id == INVALID_GROUP:
            return True
        else:
            return False
        
    def map_name_to_id(self, grp_name):
        grp_name = grp_name.upper()
        if grp_name in self.supported_grp_list:
            return self.supported_grp_list.index(grp_name)
        else:
            return INVALID_GROUP
    
    # Define the internal Group ID
    @property
    def opr(self):
        return self.supported_grp_list[self.supported_grp_list.index("OPR")]
    
    @property
    def opt(self):
        return self.supported_grp_list[self.supported_grp_list.index("OPT")]
    
    @property
    def opin(self):
        return self.supported_grp_list[self.supported_grp_list.index("OPIN")]
    
    @property
    def opout(self):
        return self.supported_grp_list[self.supported_grp_list.index("OPOUT")]
    
    @property
    def opochin(self):
        return self.supported_grp_list[self.supported_grp_list.index("OPOCHIN")]
    
    @property
    def opochout(self):
        return self.supported_grp_list[self.supported_grp_list.index("OPOCHOUT")]    

    @property
    def pcs(self):
        return self.supported_grp_list[self.supported_grp_list.index("PCS")]
    
    @property
    def dw(self):
        return self.supported_grp_list[self.supported_grp_list.index("DW")]
    
    @property
    def ethernet(self):
        return self.supported_grp_list[self.supported_grp_list.index("ETHERNET")]
    
    @property
    def sdh(self):
        return self.supported_grp_list[self.supported_grp_list.index("SDH")]
    
    @property
    def sonet(self):
        return self.supported_grp_list[self.supported_grp_list.index("SONET")]
    
    @property
    def interface(self):
        return self.supported_grp_list[self.supported_grp_list.index("INTERFACE")]
    
    @property
    def cd(self):
        return self.supported_grp_list[self.supported_grp_list.index("CD")]
    
    @property
    def dgd(self):
        return self.supported_grp_list[self.supported_grp_list.index("DGD")]
    
    @property
    def foff(self):
        return self.supported_grp_list[self.supported_grp_list.index("FOFF")]
    
    @property
    def fec(self):
        return self.supported_grp_list[self.supported_grp_list.index("FEC")]
    
    @property
    def prefec(self):
        return self.supported_grp_list[self.supported_grp_list.index("PREFEC")]
    
    @property
    def prefecbits(self):
        return self.supported_grp_list[self.supported_grp_list.index("PREFECBITS")]
    
    @property
    def otu(self):
        return self.supported_grp_list[self.supported_grp_list.index("OTU")]

class BinStatus(object):
    def __init__(self):
        self.supported_bin_status_list = BIN_STATUS_LIST
        self._status = UNKNOWN_BIN_STATUS
    
    @property
    def status(self):
        if not self._status == UNKNOWN_BIN_STATUS:
            return self.supported_bin_status_list[self._status]
        else:
            return UNKNOWN_STR
    
    @status.setter
    def status(self, bin_status):
        if bin_status in self.supported_bin_status_list:
            self._status = self.supported_bin_status_list.index(bin_status)
        else:
            self._status = UNKNOWN_BIN_STATUS

            
            
class BinInterval(object):
    def __init__(self):
        self.supported_bin_interval_list = BIN_INTERVAL_LIST
        self._interval = INVALID_BIN_INTERVAL
        
    def MapIntervalToString(self, interval):
        if interval == "0":
            return "15MIN"
        elif interval == "1":
            return "1DAY"
        elif interval == "RAW":
            return "RAW"
        else:
            return UNKNOWN_STR
        
    @property
    def interval(self):
        if not self._interval == INVALID_BIN_INTERVAL:
            return self.supported_bin_interval_list[self._interval]
        else:
            return UNKNOWN_STR
        
    @interval.setter
    def interval(self, bin_intvl):
        bin_intvl = bin_intvl.upper()
        if bin_intvl in self.supported_bin_interval_list:
            self._interval = self.supported_bin_interval_list.index(bin_intvl)
        else:
            self._interval = INVALID_BIN_INTERVAL

            
    @property
    def raw(self):
        return self.supported_bin_interval_list[self.supported_bin_interval_list.index("RAW")]
    
    @property
    def interval_15min(self):
        return self.supported_bin_interval_list[self.supported_bin_interval_list.index("0")]
    
    @property
    def interval_1day(self):
        return self.supported_bin_interval_list[self.supported_bin_interval_list.index("1")]
        
        
        
        
        
        
