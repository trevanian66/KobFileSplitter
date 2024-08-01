
from KobSplitClassDef import KobSplit
import sys



def validate_arguments(argv) -> {}:
    
    result = {}
    arguments_valid = False
    
   
    try:
        if len(argv) == 1 and "-h,-help,?".find(argv[0]) > -1:
            arguments_valid = True
            write_usage()
        else:    #check if we are splitting or merging
            if len(argv) == 7 and argv[0].lower().strip() == "split":
                result["file_operation"] = "split"
                result["input_file_name"] = argv[2].strip()
                result["file_chunk_size"] = argv[4].strip()
                result["destination"] = argv[6].lower().strip()
                arguments_valid = True
        
            if len(argv) == 5 and argv[0].lower().strip() == "merge":
                if argv[1].lower().strip() == "-d" and argv[3].lower().strip() == "-f":
                  result["file_operation"] = "merge"
                  result["split_files_directory"] = argv[2].strip()
                  result["output_file_name"] = argv[4].strip()                  
                  arguments_valid = True
    except Exception as e:
        print(f'argument error: {e}')
        
    if not arguments_valid:
        print("Invalid arguments.",end=" ")
        write_usage()
    else:   # check if we have optional read buffer size specified
      if "-rb" in argv:
          rbindex = argv.index("-rb")
          if rbindex + 1 <= len(argv):
             result["read_buffer_size"] = argv[rbindex+1].strip()


        
    return result   

        
def write_usage():    
   print("USAGE:")
   print("KobSplit Split -f <<sourcefile> -s <<chunksize>> -d <<destination directory>> -rb <<read buffer size>>.")
   print("KobSplit Merge -d <<sourcedirectory> -f <<output file>> -rb <<read buffer size>>.")


def write_credits():
    print("-----------------------------------------------")
    print("Kobby's File Splitter v1.0 (c) KobbySoft 2024. ")
    print("-----------------------------------------------")
        


if __name__ == '__main__':
    arguments = validate_arguments(sys.argv[1::])
    
    if len(arguments) > 0:
        if "read_buffer_size" in arguments.keys():
            fsplit = KobSplit(arguments["read_buffer_size"])
        else:
           fsplit = KobSplit()    

        fsplit.log_to_screen = True
        
        if  arguments["file_operation"] == "split":                
            fsplit.split_file(arguments["input_file_name"],arguments["destination"],arguments["file_chunk_size"])
            
        elif  arguments["file_operation"] == "merge": 
            fsplit.merge_file(arguments["output_file_name"],arguments["split_files_directory"])
        


#split = KobSplit("5mb")
#split.split_file(r"d:\277486553_1920x1080_4000k.mp4",'d:\ktest',"50MB")
#split.merge_file(r"d:\lotto\zapata\zanzibar\zulu\fyeah.mp4",'d:\ktest')




    