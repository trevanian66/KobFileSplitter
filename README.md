File splitter and merge program.

Splits files into specified manageable chunks and merges them back into one file. Can be used when there is a limit on file size for example during data transfer (e.g. GitHub upload limit of 25Mb)
Consists of a harness named KobFileSplit which uses the class KobSplit.

General Usage:

Spltting:
KobFileSplit Split -f <<sourcefile> -s <<chunksize>> -d <<destination directory>> -rb <<read buffer size>>

  -f : soucce file to split including path
  -s : size of split files. Can be specified as a number of bytes or a number suffixed with "kb","mb" or "gb" for Kilo bytes, Mega bytes or Giga bytes respectively
  -d : directory into which to place file chunks.
  -rb: read buffer size. Determines how many bytes to read from file each time.

Merging
KobFileSplit Merge -d <<sourcedirectory> -f <<output file>> -rb <<read buffer size>>

  -d:  source directory of split files
  -f:  name of merged output file
  -rb: read buffer size. Determines how many bytes to read from split files each time.

Example of usage:

To split a file using harness:

>python kobfilesplit.py Split -f "D:\SourceFileName.Extension" -s "50mb" -d "D:\DestinationDirectory"

(This would split "D:\SourceFileName.Extension" into 50mb chunks and place the files in "D:\DestinationDirectory")

To merge a file using harness:

>python kobfilesplit.py Merge -d "D:\SourceDirectory" -f "D:\temp\MergedFile.Extension"  

(This would merge split files in "D:\SourceDirectory" into output file "D:\temp\MergedFile.Extension")
