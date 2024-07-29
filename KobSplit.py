




from collections import namedtuple
from enum import Enum
from pathlib import Path
import os
import fnmatch
import math
from shlex import join
import string
from tkinter import CURRENT


#helper objects
file_operation = Enum('file_operation',['Split','Merge'])
file_ops_data = namedtuple('file_ops_data','operation,file_name,source,destination,chunk_size')

#constants
MIN_CHUNK_SIZE = 1024 * 10;
SPLIT_FILE_SUFFIX = ".KOB";
READ_BUFFER_SIZE = 1024 * 10;


def split_file(file_data):
    
    file_name = os.path.basename(file_data.file_name)
    input_file = Path(file_data.file_name)
    result = True
    chunk_count = 0
    current_chunk_file = ""
    chunk_file_prefix = ""
    bytes_read = 0
    bytes_to_read = 0
    bytes_left = 0
    
    
    if not input_file.is_file():
        raise ValueError(f'file {file_name} does not exist.')

    
    output_directory = Path(file_data.destination)
    if output_directory.is_dir():
        # check if we already have any split files in output directory
        extension = SPLIT_FILE_SUFFIX + "*"
        file_names = fnmatch.filter(os.listdir(output_directory),file_name +  SPLIT_FILE_SUFFIX + "*")
        
        if len(file_names) > 0:
            raise ValueError(f'there are already split files for {file_name} in folder {output_directory}')
    
    try:        
        # work out number of chunks and hence number of '0's to pad filename suffix with    
        file_size = os.path.getsize(file_data.file_name)
        chunk_number = (int) (file_size / file_data.chunk_size)
        if chunk_number * file_data.chunk_size < file_size:
            chunk_number+=1
    
        chunk_file_prefix = "0" *  (int(math.log10(chunk_number)) + 1)
        if len(chunk_file_prefix) < 2:
            chunk_file_prefix = "00"
        
        print (f'we have {chunk_number} chunks babe. prefix is {chunk_file_prefix}')        
        
        bytes_read = 0  #initialize bytes read
        
        file = open(file_data.file_name, "rb")

        read_position = file.tell()
        while read_position != file_size:
            
            bytes_left = file_size - read_position
            
            if bytes_left < READ_BUFFER_SIZE:
                bytes_to_read =  int(bytes_left)
            else:
                bytes_to_read = int(READ_BUFFER_SIZE)           
       
            read_buffer = file.read(bytes_to_read)
            
            if (bytes_read + bytes_to_read > file_data.chunk_size) or bytes_read == 0:
               chunk_count = chunk_count  + 1 
               current_chunk_file = os.path.join(file_data.destination,file_name + SPLIT_FILE_SUFFIX + str(chunk_count).rjust(len(chunk_file_prefix),"0"))
               bytes_read = 0
               print (f'creating {current_chunk_file}...') 
               
            write_chunk(read_buffer,current_chunk_file)            
            bytes_read = bytes_read + bytes_to_read
            
            read_position = file.tell()
            
        file.close()
        
    except:    
        result = False
        raise
        
def merge_file(file_data):        
   
    result = True
    bytes_to_read = 0
    bytes_left = 0
    output_file = Path(file_data.file_name)
    file_mask = "*" + SPLIT_FILE_SUFFIX + "*"
    
    if output_file.is_file():
       raise ValueError(f'file {output_file} already exists.')
   
    input_directory = Path(file_data.source)
    if not input_directory.is_dir():
         raise ValueError(f'Directory {input_directory} does not exist.')
   
   
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
             print(f'creating {file_data.file_name}...')
             
             foutput = open(file_data.file_name,'wb') 

             for current_file in file_names:
                
                current_file = os.path.join(input_directory,current_file)
                
                print(f'reading {current_file}...')    
                
                file_size = os.path.getsize(current_file)
                file = open(current_file,'rb') 
                read_position = file.tell()
                
                while read_position != file_size:
                    
                    bytes_left = file_size - read_position           
                
                    if bytes_left < READ_BUFFER_SIZE:
                       bytes_to_read =  int(bytes_left)
                    else:
                       bytes_to_read = int(READ_BUFFER_SIZE)

                    read_buffer = file.read(bytes_to_read)
                    foutput.write(read_buffer)
                    
                    read_position = file.tell()
                    
                file.close()    
             
             foutput.close()   

         except:
             raise
         

   
    
   

def write_chunk(write_buffer,file_name):
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
    
    




file_op = file_operation.Split
file_data = file_ops_data(file_op,'d:\Angelique2.mp4','d:\ktest','d:\ktest',204800)
#split_file(file_data)
merge_file(file_data)


    