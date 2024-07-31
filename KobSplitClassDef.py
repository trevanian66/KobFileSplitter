


from collections import namedtuple
from enum import Enum
from pathlib import Path
import os
import fnmatch
import math
from shlex import join
import string
from tkinter import CURRENT


#constants
MIN_CHUNK_SIZE = 1024 * 10;
SPLIT_FILE_SUFFIX = ".KOB";
DEFAULT_READ_BUFFER_SIZE = 1024 * 10;

class KobSplit:
    
    def __init__(self,buffer_size = DEFAULT_READ_BUFFER_SIZE  ):        
        self.read_buffer_size = self.__get_size_value(buffer_size)
        pass
    
    def split_file(self,input_file_name,destination,file_chunk_size = MIN_CHUNK_SIZE):
        
        chunk_size = self.__get_size_value(str(file_chunk_size))
        file_name = os.path.basename(input_file_name)
        input_file = Path(input_file_name)
        result = True
        chunk_count = 0
        current_chunk_file = ""
        chunk_file_prefix = ""
        bytes_read = 0
        bytes_to_read = 0
        bytes_left = 0
    
    
        if not input_file.is_file():
            raise ValueError(f'file {input_file_name} does not exist.')

    
        output_directory = Path(destination)
        if output_directory.is_dir():
            # check if we already have any split files in output directory
            extension = SPLIT_FILE_SUFFIX + "*"
            file_names = fnmatch.filter(os.listdir(output_directory),input_file_name +  SPLIT_FILE_SUFFIX + "*")
        
            if len(file_names) > 0:
                raise ValueError(f'there are already split files for {input_file_name} in folder {output_directory}')
    
        try:        
            # work out number of chunks and hence number of '0's to pad filename suffix with    
            file_size = os.path.getsize(input_file_name)
            chunk_number = (int) (file_size / chunk_size)
            if chunk_number * chunk_size < file_size:
                chunk_number+=1
    
            chunk_file_prefix = "0" *  (int(math.log10(chunk_number)) + 1)
            if len(chunk_file_prefix) < 2:
                chunk_file_prefix = "00"
                       
        
            bytes_read = 0  #initialize bytes read
        
            file = open(input_file_name, "rb")

            read_position = file.tell()
            while read_position != file_size:
            
                bytes_left = file_size - read_position
            
                if bytes_left < self.read_buffer_size:
                    bytes_to_read =  int(bytes_left)
                else:
                    bytes_to_read = int(self.read_buffer_size)           
       
                read_buffer = file.read(bytes_to_read)
            
                if (bytes_read + bytes_to_read > chunk_size) or bytes_read == 0:
                   chunk_count = chunk_count  + 1 
                   current_chunk_file = os.path.join(destination,file_name + SPLIT_FILE_SUFFIX + str(chunk_count).rjust(len(chunk_file_prefix),"0"))
                   bytes_read = 0
                   print (f'creating {current_chunk_file}...') 
               
                self.__write_chunk(read_buffer,current_chunk_file)            
                
                bytes_read = bytes_read + bytes_to_read
            
                read_position = file.tell()
            
            file.close()
        
        except:    
            result = False
            raise
        
    def merge_file(self,output_file_name,split_files_directory):        
   
        result = True
        bytes_to_read = 0
        bytes_left = 0
        output_file = Path(output_file_name)
        file_mask = "*" + SPLIT_FILE_SUFFIX + "*"
    
        if output_file.is_file():
           raise ValueError(f'file {output_file} already exists.')
   
        input_directory = Path(split_files_directory)
        if not input_directory.is_dir():
             raise ValueError(f'Directory {input_directory} does not exist.')
   
        #create output directory if needed
        directory =  os.path.dirname(output_file_name) 
        output_directory = Path(directory)
        if not output_directory.is_dir():
                 os.makedirs(directory)  
   
        file_names = fnmatch.filter(os.listdir(input_directory),file_mask)
        
        if len(file_names) == 0:
                raise ValueError(f'no files matching {file_mask} in directory {input_directory}')
        else:
             # check if we have more than one set of split files in merge folder 
             file_name = Path(file_names[0]).stem
             f = filter(lambda l: Path(l).stem != file_name, file_names )
             fl = list(f)
             if len(fl) > 0:
                 raise ValueError(f'there are more than one set of split files in directory {input_directory}')
         
             file_names.sort()
         
             try:
                 print(f'creating {output_file_name}...')
             
                 foutput = open(output_file_name,'wb') 

                 for current_file in file_names:
                
                    current_file = os.path.join(input_directory,current_file)
                
                    print(f'reading {current_file}...')    
                
                    file_size = os.path.getsize(current_file)
                    file = open(current_file,'rb') 
                    read_position = file.tell()
                
                    while read_position != file_size:
                    
                        bytes_left = file_size - read_position           
                
                        if bytes_left < self.read_buffer_size:
                           bytes_to_read =  int(bytes_left)
                        else:
                           bytes_to_read = int(self.read_buffer_size)

                        read_buffer = file.read(bytes_to_read)
                        foutput.write(read_buffer)
                    
                        read_position = file.tell()
                    
                    file.close()    
             
                 foutput.close()   

             except:
                 raise                       
    
   

    def __write_chunk(self,write_buffer,file_name):
        output_file = Path(file_name)
        if output_file.is_file():
             file = open(file_name,'ab') 
        else:
             directory =  os.path.dirname(file_name) 
             output_directory = Path(directory)
             if not output_directory.is_dir():
                 os.makedirs(directory)         
             file = open(file_name,'wb')
    
        file.write(write_buffer)
        file.close()
    
    

    def __get_size_value(self,size_string) -> int:
       
       kilo_bytes = 1024
       mega_bytes = kilo_bytes * 1024
       giga_bytes = mega_bytes * 1024
       
       result = -1

       try:           
           if str(size_string).isdigit():
               result = int(size_string)
           else:               
               size_string = size_string.lower()
               if "kb" in size_string:
                   result = int(size_string.replace("kb","").strip()) * kilo_bytes
               elif "mb" in size_string:
                   result = int(size_string.replace("mb","").strip()) * mega_bytes
               elif "gb" in size_string:
                   result = int(size_string.replace("gb","").strip()) * giga_bytes
               else:
                    raise ValueError(f'Invalid size parameter {size_string}')
       except:
           raise
       
       return result

        


    





    