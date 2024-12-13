# Ip List Formatter

A small script that I wrote to scrape the Ip list for certain countries from lite.ip2location.com in a format that works with PeerBlock.

### Usage

#### Args:

| Required options (Choose one)            | Description                                                                      | Default Value  |
|------------------------------------------|----------------------------------------------------------------------------------|----------------|
| -i,                            --input   | input file (Do not use if specifying a country)                                  |                |
| -c,                            --country | Name of country to scrape IPs for (Do not use with input, this will override it) |                |
| **Optional options**                     |                                                                                  |                |
| -n,                            --name    | Name of the IP list. Will apear before every ip in the list                      | IP             |
| -o,                            --output  | Name of the output file (Include the file extention (I.E. outFile.txt))          | == to name.p2p |
| -v,                            --vervose | Prints what the program is doing                                                 |                |

Example:</br>
python3 ipListFormatter.py -c Canada -n "Canada IP List" -o CanadaList.txt

For file input usage, the file must already have some formatting. It must be organized so that the each line starts with an ip address, has a whitespace, then a second ip. Any other text must be sperated by a whitespace and be at the end of a line for it to work.

Example (inIPs.txt):</br>
100.100.0.0 100.100.0.255 random text</br>
101.100.3.6 105.100.0.0 <-anything after this whitespcae will be discarded

Output:</be>
(name):100.100.0.0-100.100.0.255</br>
(name):101.100.3.6 105.100.0.0
