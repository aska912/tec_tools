
import re, os.path
from Logger import (\
    dbgprint,       \
    logprint        \
)


class OutputFileProcessor(object):
    def __init__(self, output_file_folder):
        self.output_files_folder = output_file_folder
        self._output_files_list = []
        
        # Match: [s|Show interface ]
        self.__reg_siteip    = re.compile(r"(\d{1,3}\.){3}\d{1,3}")
        
        self.__reg_exportime = re.compile(r"\d{2}(\d{2}\-){2}\d{2}\_(\d{2}\-){2}\d{2}")
        self._reg_show_interface  = re.compile("(s|S)how\s+interface\s+")
        self._reg_show_otu = re.compile("(s|S)how\s+otu\s+")
        
        #output file name: output_135.252.213.151.txt
        self.__reg_output_filename = re.compile(r'^o\w+\_(\d{1,3}\.){4}txt$')
        
        # { siteip: {export_time: [pm_data_txt_list]} }
        self.ne_info_and_pm_txt_dict = {}
        
    
    def Init(self):
        self._output_files_list = self._get_output_files_in_dir(self.output_files_folder)
        if not len(self._output_files_list):
            return False
        
        for filename in self._output_files_list:
            #print filename
            # Get the export time 
            export_time = self._get_export_time_from_filename(filename)
            if export_time == "":
                logprint.warning("Can't get the exporting time from %s"%filename)
                continue
            
            # Get the site IP
            site_ip = self._get_site_ip_from_filename(filename)
            #print site_ip
            if site_ip == "":
                logprint.warning("Can't get the site ip from %s"%filename)
                continue
            
            pmdata_txt_list = self.ReadLines(filename)
            if not len(pmdata_txt_list):
                logprint.warning("")
                continue
            
            self._write_ne_info_and_pm_txt_dict(site_ip, export_time, pmdata_txt_list)
            
            #match_file = r"executor_output\2017-03-13_16-46-32\output_135.252.201.41.txt"
            #if filename == r"%s"%match_file:
            #    print filename
            #    print site_ip
            #    print export_time
            #    print pmdata_txt_list
            #    self._dump_ne_info_and_pm_txt_dict() 
        # End for
            
        if len(self.ne_info_and_pm_txt_dict):
            #self._dump_ne_info_and_pm_txt_dict()
            return True
        else:
            return False
            
        
        
    @property
    def outputfile(self):
        return self.__output_file_name
    
    @outputfile.setter
    def outputfile(self, filename):
        self.__output_file_name = filename
        
    def ReadLines(self, filename):
        """
        Return List:
        [ [cli_cmd_string, pm_data_string], [cli_cmd_sting, pm_data_string] ]
        """
        read_line_num = 0
        tmp_pm_data_string = ""
        cli_cmd = ""
        is_match_cli = False
        
        pmdata_txt_list = []
        raw_lines_list = self.ReadRawLines(filename)
        if not len(raw_lines_list): 
            return []
            
        #print "raw lines: ", raw_lines_list
        
        for ln in raw_lines_list:
            if not len(ln): continue
            if re.search(self._reg_show_interface, ln) or \
               re.search(self._reg_show_otu, ln):
                if read_line_num > 0:
                    pmdata_txt_list.append([cli_cmd, tmp_pm_data_string])
                    read_line_num = 0
                    tmp_pm_data_string = ""
                    cli_cmd = ln
                elif read_line_num == 0:
                    cli_cmd = ln
                    is_match_cli = True
                continue
            if is_match_cli is True:
                tmp_pm_data_string += ln
                read_line_num += 1
            else:
                continue
            
        if is_match_cli is True:
            pmdata_txt_list.append([cli_cmd, tmp_pm_data_string])
        
        #print "In File pmdata_txt_list: ", pmdata_txt_list
        return pmdata_txt_list

    
    def ReadRawLines(self, filename):
        raw_lines_list = []
        try:
            fn= open(filename, "r")
            raw_lines_list =  fn.readlines()
            fn.close()
        except:
            raw_lines_list = []
            
        return raw_lines_list
            
            
    def _get_export_time_from_filename(self, filename):
        #F:\cygwin\code\tec_prj\executor_output\executor_output\2017-03-13_16-46-32\output_135.252.210.32.txt
        exp_time = re.search(self.__reg_exportime, filename)
        if exp_time is not None:
            return exp_time.group(0)
        else:
            return ""
        
    def _get_site_ip_from_filename(self, filename):
        #F:\cygwin\code\tec_prj\executor_output\executor_output\2017-03-13_16-46-32\output_135.252.210.32.txt
        site_ip = re.search(self.__reg_siteip, filename)
        if site_ip is not None:
            return site_ip.group(0)
        else:
            return ""
            
    def __check_output_path_format(self):
        pass
    
    def _get_output_files_in_dir(self, dir_path):
        get_output_files = []
        fils_list = []
        dirname = os.path.normpath(dir_path)
        try:
            if os.path.isfile(dirname):
                ofile = dirname
                if self._is_output_file(ofile):
                    get_output_files.append(ofile)
                    return get_output_files
            elif os.path.isdir(dirname):
                fils_list = os.listdir(dirname)
        except OSError:
            fils_list = []
            
        if not len(fils_list):
            return []
    
        for filename in fils_list:
            ofile = os.path.join(dirname, filename)
            if os.path.isdir(ofile):
                dir_path = ofile
                tmp_files_list = self._get_output_files_in_dir(dir_path)
                if len(tmp_files_list):
                    for f in tmp_files_list:
                        get_output_files.append(f)
            elif os.path.isfile(ofile):
                if self._is_output_file(filename):
                    get_output_files.append(ofile)
            else:
                continue
        return get_output_files
    
    
    def _is_output_file(self, output_file):
        if re.search(self.__reg_output_filename, output_file):
            return True
        else:
            return False
        
    
    def _write_ne_info_and_pm_txt_dict(self, site_ip, export_time, pmdata_txt_list):
        if self.ne_info_and_pm_txt_dict.get(site_ip) is None:
            self.ne_info_and_pm_txt_dict.update( { site_ip: {export_time: pmdata_txt_list} } )
        else:
            if self.ne_info_and_pm_txt_dict[site_ip].get(export_time) is None:
                self.ne_info_and_pm_txt_dict[site_ip].update( {export_time: pmdata_txt_list} )
            else:
                self.ne_info_and_pm_txt_dict[site_ip][export_time].append(pmdata_txt_list)
        
    def _dump_ne_info_and_pm_txt_dict(self):
        if not len(self.ne_info_and_pm_txt_dict):
            print "ne_info_and_pm_txt_dict is Null."
            return
        for ip in self.ne_info_and_pm_txt_dict.keys():
            print "\n"
            print "Site IP: %s"%ip
            for time in self.ne_info_and_pm_txt_dict[ip].keys():
                print "    Export Time: %s"%time
                for txt in self.ne_info_and_pm_txt_dict[ip][time]:
                    print txt
        
        
    
    
    
    
        