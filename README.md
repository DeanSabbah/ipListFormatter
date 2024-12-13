# Ip List Formatter

A small script that I wrote to scrape the Ip list for certain countries from lite.ip2location.com in a format that works with PeerBlock.

### Usage

#### Args:

| Required options (Choose one) |           | Description                                                                      | Default Value  |
|-------------------------------|-----------|----------------------------------------------------------------------------------|----------------|
| -i                            | --input   | input file (Do not use if specifying a country)                                  |                |
| -c                            | --country | Name of country to scrape IPs for (Do not use with input, this will override it) |                |
| Optional options              |           |                                                                                  |                |
| -n                            | --name    | Name of the IP list. Will apear before every ip in the list                      | IP             |
| -o                            | --output  | Name of the output file (Include the file extention (I.E. outFile.txt))          | == to name.p2p |
| -v                            | --vervose | Prints what the program is doing                                                 |                |

Example:</br>
python3 ipListFormatter.py -c Canada -n "Canada IP List" -o CanadaList.txt
