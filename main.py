
import sys, re, datetime, time, os, os.path
import FileProcessor
import PmCommon
import PmExcel
import copy
from Logger import (dbgprint, logprint)

OUTPUT_FILE_DIR = "executor_output"

def current_second():
    return time.time()

def format_time(sec):
    """
    Return '2014-09-11_08-37-12'
    """
    return time.strftime( "%Y-%m-%d_%H-%M-%S", time.localtime(sec) )


if __name__ == "__main__":

    cmd_col = 0
    pm_col = 1
    output_path = raw_input("Please input the executor_output path: ")
        
    pm_processor = PmCommon.PmProcessor()
    
    #output_file_processor = FileProcessor.OutputFileProcessor(OUTPUT_FILE_DIR)
    output_file_processor = FileProcessor.OutputFileProcessor(output_path)
    if not output_file_processor.Init():
        sys.stderr.write("Error!!! No such as file or directory\n")
        a = raw_input("Press ENTER to exit: ")
        sys.exit(1)
        
    pm_excel_folder_name = format_time(current_second())
    try:
        os.mkdir(pm_excel_folder_name)
    except:
        logprint.warning("Can't create %s"%pm_excel_folder_name)
        sys.exit(1)
        
    for site_ip in output_file_processor.ne_info_and_pm_txt_dict.keys():
        output_excel_filename = ("%s.%s")%(re.sub(r"\.", '_', site_ip), "xlsx")
        output_excel_filename = os.path.join(pm_excel_folder_name, output_excel_filename)
        output_excel = PmExcel.PmExcel(output_excel_filename)
        if not output_excel.OpenWorkbook():
            logprint.warning("Can't open %s\n"%output_excel_filename)
            sys.exit(1)
        
        if not len(output_file_processor.ne_info_and_pm_txt_dict[site_ip]):
            continue
        for output_export_time in output_file_processor.ne_info_and_pm_txt_dict[site_ip].keys():
            if not len(output_file_processor.ne_info_and_pm_txt_dict[site_ip][output_export_time]):
                continue
            for output_pm_txt_list in output_file_processor.ne_info_and_pm_txt_dict[site_ip][output_export_time]:
                if not len(output_pm_txt_list):
                    continue
                cli_cmd = output_pm_txt_list[cmd_col]
                pm_txt  = output_pm_txt_list[pm_col]
                logprint.info( "Parse the PM data for [%s]"%(re.sub(r'\n', '', cli_cmd)) )

                if len(pm_txt):
                    pm_bin = copy.deepcopy(pm_processor.Parse(pm_txt))
                    #pm_bin.Dump()
                    if pm_bin is None: continue
                else:
                    continue
                
                if pm_bin.nodata_reason == "CLI Commd Error":
                    continue

                if not output_excel.OpenPmGrpSheet(pm_bin.group, pm_bin.interval):
                    logprint.warning("Open %s-%s Sheet[%s-%s] Fail."%(pm_bin.group, pm_bin.interval, \
                                                                      output_export_time, site_ip))
                    continue
                output_excel.AppendPmData(pm_bin, output_export_time)
            # End For <output_pm_txt_list>
        # End For <output_export_time>
        output_excel.CloseWithSave()
    # End For <site_ip>
        

    #----------------------------------------------------------------------------------------
    print "Done!!!"
    raw_input("Press ENTER to exit: ")
    sys.exit()


    
    